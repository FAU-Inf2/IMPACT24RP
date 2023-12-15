import isl

from util import *
from isl_util import *
from alignment import *
from isl_parser import *
from isl_parser_extract import *

def getAnonStr(): return "Anon"

def makeAnon(box):
    translator = box.as_set().identity().set_range_tuple(isl.id(getAnonStr()))
    return box.apply(translator)

def makeUnanon(box, to):
    translator = box.as_set().identity().set_range_tuple(isl.id(to))
    return box.apply(translator)

def getProjMap(dims):
    tupIdStr = getAnonStr()
    dimStrs = [ "i%s" % (dn) for dn in range(0, dims) ]
    projMapStr = [ "%s[%s] -> %s[%s]" %
                   (tupIdStr, ",".join(dimStrs), tupIdStr + ds, ds)
                   for ds in dimStrs ]
    projMapStr = "{" + "; ".join(projMapStr) + "}"
    proj = isl.union_map(projMapStr)
    return proj

def projectShape(s):
    proj = getProjMap(assureSet(s).n_dim())
    indivDims = s.apply(proj)
    res = unionSetToList(indivDims)
    return res

def getReadBox(slab, r):
    return slab.apply(r).coalesce()

def projToIndivDims(rdBox):
    box = makeAnon(rdBox)
    numDims = assureSet(box).n_dim()
    proj = getProjMap(numDims)
    return box.apply(proj)

def setIntersect(ss):
    inters = lambda a, b: a.intersect(b)
    return functools.reduce(inters, ss)

def setUnion(ss):
    union = lambda a, b: a.union(b)
    return functools.reduce(union, ss)

def lift(indivDims):
    sets = unionSetToList(indivDims)
    numSets = len(sets)
    lifter = getProjMap(numSets).reverse()
    lifted = [ s.apply(lifter) for s in sets ]
    return lifted

def merge(indivDims):
    lifted = lift(indivDims)
    return setIntersect(lifted)

def fillInterval(lmin, lmax):
    lb = lmin.lex_le_union_set(lmin.universe())
    ub = lmax.lex_ge_union_set(lmax.universe())
    return lmin.apply(lb).intersect(lmax.apply(ub))

def getFilledBox(slab, r):
    readBox = getReadBox(slab, r)
    indivDims = projToIndivDims(readBox)
    indivDims = indivDims.coalesce()
    universes = unionSetToList(indivDims.universe())
    lexmins = indivDims.lexmin()
    lexmaxs = indivDims.lexmax()

    minMax = [ (lexmins.intersect(u), lexmaxs.intersect(u))
               for u in universes ]
    intervals = [ fillInterval(lmin, lmax) for lmin, lmax in minMax ]
    intervals = setUnion(intervals)
    res = merge(intervals)
    res = res.coalesce()

    return res

def getBoxed(slab, r):
    readBox = getReadBox(slab, r)
    indivDims = projToIndivDims(readBox)
    indivDims = indivDims.coalesce()
    res = merge(indivDims)
    res = res.coalesce()
    return res

def getBoxedLexminPoint(rb):
    indivDims = projToIndivDims(rb)
    indivDims = indivDims.coalesce()
    indivDims = indivDims.compute_divs()
    indivDims = indivDims.coalesce()

    indivDims = indivDims.lexmin()
    res = merge(indivDims)
    res = res.coalesce()
    return res

def getBoxedLexmaxPoint(rb):
    indivDims = projToIndivDims(rb)
    indivDims = indivDims.coalesce()
    lexmax = indivDims.lexmax()
    res = merge(lexmax)
    res = res.coalesce()
    return res

def getStep(slab, slabComp, r):
    rb = getReadBox(slab, r)
    rbNext = getReadBox(slabComp, r)
    basePoint = getBoxedLexminPoint(rb)
    compPoint = getBoxedLexminPoint(rbNext)
    deltas = arrow(basePoint, compPoint).deltas().as_set()
    deltas = deltas.coalesce()
    return deltas

def lexRoundUp(n):
    return n.lexmax().intersect(n)

def lexRoundDown(n):
    return n.lexmin().intersect(n)

def getTranslator(stepSet, box):
    return (arrow(stepSet, box)
            .deltas_map()
            .domain_factor_range())

def getProjStep(slab, slabComp, r):
    vStep = getStep(slab, slabComp, r)
    onlySteps = vStep.project_out_all_params()
    return onlySteps

def getShiftedSelfOverlap(ris, nextV):
    vBox = getFilledBox(nextV.domain(), ris)
    onlySteps = getProjStep(nextV.domain(), nextV.range(), ris)
    assert(onlySteps.is_singleton())
    shifter = getTranslator(onlySteps, vBox)
    return vBox.intersect(vBox.apply(shifter))

def getShapeFromReadBox(rb):
    (boxPointMin, boxPointMax) = (
        getBoxedLexminPoint(rb),
        getBoxedLexmaxPoint(rb)
    )
    shape = arrow(boxPointMin, boxPointMax).deltas().as_set()
    return shape

# A Shape is a isl.set with elements in Space "Anon[i0, ..., in]"
def isBoundedShape(shape):
    isBounded = all([ not shape.dim_max_val(i).is_infty()
                      for i in
                      range(0, assureSet(shape).n_dim()) ])
    return isBounded

def printShape(shape):
    print("Is singleton: ", shape.is_singleton())
    print("Shape: ", shape.compute_divs())
    print("Shape Eq: ", shape.compute_divs().detect_equalities())
    print("Shapes: ", shape.project_out_all_params().compute_divs())

class ReadBoxAnalysis():
    def __init__(self, tiling, dom):
        self.dom = dom
        self.tiling = tiling
        self.modSched = self.tiling.getTransformedScheduleNoDi()
        self.slabs = tiling.getSlabs()

    def isAccAlignedToTile(self, r):
        lsdLine = self.slabs.getLsdTileSlabNoDi()
        sched = self.modSched
        ris = self.liftAcc(r)
        rbox = lsdLine.apply(ris)
        deltas = arrow(rbox, rbox).deltas()
        dimAligned = sum([
            1 if pd.project_out_all_params().is_equal(ISL_ZERO)
            else 0 for pd in projectToList(deltas) ])
        rightMostDim = projectOutNth(deltas, 0)
        rightMostDim = rightMostDim.project_out_all_params()
        isAligned = dimAligned == 1 and rightMostDim.is_equal(ISL_ZERO)
        return isAligned

    def liftAcc(self, acc):
        return accRelInSchedSpace(acc, self.modSched)

    def alignToCache(self, r, box, cacheSlab):
        offset = self.getCacheOffset(r, cacheSlab)
        res = (arrow(offset, box)
               .deltas_map()
               .domain_factor_range()
               .reverse())
        return res

    def getCacheOffset(self, a, slab):
        ais = self.liftAcc(a)
        box = getFilledBox(slab, ais)
        lminPoint = getBoxedLexminPoint(box)
        return lminPoint

    def busAlignAndExpandBox(self, box, al):
        aligner = mkAligner(box, al)
        expander = mkExpander(box, al)
        box = box.apply(aligner).apply(expander)
        return box

    def busAlignBox(self, box, al):
        aligner = mkAligner(box, al)
        box = box.apply(aligner)
        return box

    def cacheShapePrepareBox(self, r, slab):
        ris = self.liftAcc(r)
        box = getFilledBox(slab, ris)
        return box

    def cacheShapeCalc(self, box):
        #print("Box: ", box)
        shape = getShapeFromReadBox(box)
        deparamShape = shape.project_out_all_params()
        #assert(deparamShape.is_singleton())
        return deparamShape

    def getUnpaddedCacheShape(self, r, slab):
        box = self.cacheShapePrepareBox(r, slab)
        shape = self.cacheShapeCalc(box)
        return shape

    def getPaddedCacheShape(self, r, slab, al):
        box = self.cacheShapePrepareBox(r, slab)
        box = self.busAlignAndExpandBox(box, al)
        shape = self.cacheShapeCalc(box)
        return shape

    def isCacheAble(self, r):
        fullSlab = self.slabs.getFullTileSlabNoDi()
        box = self.cacheShapePrepareBox(r, fullSlab)
        shape = self.cacheShapeCalc(box)
        isSing = shape.is_singleton()
        isBounded = isBoundedShape(shape)
        return isSing and isBounded

    def getCacheBounds(self, r, slab):
        box = self.cacheShapePrepareBox(r, slab)
        shape = self.cacheShapeCalc(box)
        isBounded = isBoundedShape(shape)
        bounds = [ shape.dim_max_val(i)
                   for i in range(0, assureSet(shape).n_dim()) ]
        ints = [ b.num_si() if b.is_int() else 42_000_000
                 for b in bounds ]
        return ints

    def getCacheDimensions(self, shape):
        point = shape.sample_point()
        parsedPoint = IslPointParser.grammar.parse(str(point)).unwrap()
        tupDims = islPointGetTupleDims(parsedPoint)
        tupDimsInt = [ int(td) for td in tupDims ]
        cacheDims = [ td + 1 for td in tupDimsInt ]
        return cacheDims

    def filterNonDomainElems(self, slab):
        domInSched = self.dom.apply(self.modSched)
        if isUnionMap(slab) or isMap(slab):
            return slab.intersect_domain(domInSched).intersect_range(domInSched)
        if isUnionSet(slab) or isSet(slab):
            return slab.intersect(domInSched)
        raise Exception("Invalid type: " + type(slab))

    def getGt(self, var):
        i = self.tiling.getNextMap(var)
        k = self.tiling.getSlabs().getInnerTileSlab([var])
        res = i.intersect_domain(k)
        return self.tiling.removeDiDims(res)

    def getLt(self, var):
        i = self.tiling.getPrevMap(var)
        k = self.tiling.getSlabs().getInnerTileSlab([var])
        res = i.intersect_domain(k)
        return self.tiling.removeDiDims(res)

    def getLe(self, var):
        i = self.tiling.getPrevEqMap(var)
        k = self.tiling.getSlabs().getInnerTileSlab([var])
        res = i.intersect_domain(k)
        return self.tiling.removeDiDims(res)

    def getFirst(self, var):
        next = self.getLe(var)
        sis = self.modSched.range()
        next = next.intersect_domain(sis).intersect_range(sis)
        next = lexRoundDown(next)
        return next.range()

    ###
    # Get Write Back group
    ###

    def getWriteBackFull(self, w, slab):
        box = self.calcWriteBack(w, slab)
        return box

    def getWriteBackNoDom(self, w, slab):
        slab = self.filterNonDomainElems(slab)
        box = self.calcWriteBack(w, slab)
        return box

    def calcWriteBack(self, w, slab):
        sis = self.modSched.range()
        slab = slab.intersect(sis)
        wis = self.liftAcc(w)
        box = getFilledBox(slab, wis)
        box = box.coalesce()
        return box

    ###
    # GetShift Group
    ###

    def getShiftFull(self, r, var):
        slab = self.slabs.getVarSlabNoDi(var)
        box = self.calcShiftBox(r, var, slab)
        return box

    def getShiftNoDom(self, r, var):
        slab = self.slabs.getVarSlabNoDi(var)
        slab = self.filterNonDomainElems(slab)
        box = self.calcShiftBox(r, var, slab)
        return box

    def calcShiftBox(self, r, var, kslab):
        ris = self.liftAcc(r)
        kbox = getFilledBox(kslab, ris)
        kbox = kbox.intersect(
            getShiftedSelfOverlap(ris, lexRoundDown(self.getGt(var)))
        ).coalesce()

        offset = self.getCacheOffset(r, self.slabs.getReadCacheSlab())
        aligner = getTranslator(offset, kbox)
        kboxAligned = kbox.apply(aligner)

        varPrev = lexRoundUp(self.getLt(var))
        onlyVStep = getProjStep(varPrev.domain(), varPrev.range(), ris)
        assert(onlyVStep.is_singleton())

        translator = getTranslator(onlyVStep, kboxAligned)
        shifter = kboxAligned.identity().apply_range(translator)

        return shifter

    ###
    # getInit Group
    ###

    def getInitFull(self, r, var):
        slab = self.prepareInitSlab(r, var)
        box = self.calcInitBox(slab, r, var)
        return box

    def getInitNoDom(self, r, var):
        slab = self.prepareInitSlab(r, var)
        slab = self.filterNonDomainElems(slab)
        box = self.calcInitBox(slab, r, var)
        return box

    def prepareInitSlab(self, r, var):
        fst = self.getFirst(var)
        nxt = lexRoundDown(self.getGt(var))
        slabRel = nxt.intersect_domain(fst)
        return slabRel

    def calcInitBox(self, slabRel, r, var):
        ris = self.liftAcc(r)
        varShift = getShiftedSelfOverlap(ris, slabRel)

        largerDims = self.tiling.getLargerElemDims(var)
        for ld in largerDims:
            ldNext = lexRoundDown(self.getGt(ld))
            fullBox = getFilledBox(ldNext.domain(), ris)
            ldShift = getShiftedSelfOverlap(ris, ldNext)
            ldBox = fullBox.subtract(ldShift)
            varShift = varShift.intersect(ldBox).coalesce()

        varShift = varShift.coalesce()
        return varShift

    ###
    # getFullInit
    ###

    def getFullSlabInitBoxFull(self, r):
        slab = self.prepareFullSlabInitSlab(r)
        box = self.calcFullSlabInitBox(r, slab)
        return box

    def getFullSlabInitBoxNoDom(self, r):
        slab = self.prepareFullSlabInitSlab(r)
        slab = self.filterNonDomainElems(slab)
        box = self.calcFullSlabInitBox(r, slab)
        return box

    def prepareFullSlabInitSlab(self, r):
        ris = self.liftAcc(r)
        slab = self.slabs.getFullTileSlabNoDi()
        return slab

    def calcFullSlabInitBox(self, r, slab):
        ris = self.liftAcc(r)
        slab = self.slabs.getFullTileSlabNoDi()
        slab = self.filterNonDomainElems(slab)
        box = getFilledBox(slab, ris)
        box = box.coalesce()
        return box

    ###
    # getNext Group
    ###

    def prepareNextSlab(self, var):
        largerDims = self.tiling.getLargerElemDims(var)
        kslab = self.tiling.getSlabs().getInnerTileSlabNoDi(largerDims)
        return kslab

    def cutNextBox(self, r, slab, var):
        largerDims = self.tiling.getLargerElemDims(var)
        ris = self.liftAcc(r)
        box = getFilledBox(slab, ris)
        for ld in largerDims:
            ldNext = lexRoundDown(self.getGt(ld))
            shiftedOlap = getShiftedSelfOverlap(ris, ldNext)
            box = box.subtract(shiftedOlap).coalesce().compute_divs()

        box = box.coalesce()
        return box

    def alignToReadCache(self, r, box):
        cacheSlab = self.slabs.getReadCacheSlab()
        aligned = self.alignToCache(r, box, cacheSlab)
        return aligned

    #def alignToWriteCache(self, r, box):
    #    cacheSlab = self.slabs.getWriteCacheSlab()
    #    aligned = self.alignToCache(r, box, cacheSlab)
    #    return aligned

    def getNextFull(self, r, var):
        slab = self.prepareNextSlab(var)
        box = self.cutNextBox(r, slab, var)
        return box

    # generates the next set without the non-domain elements
    def getNextNoDom(self, r, var):
        slab = self.prepareNextSlab(var)
        slab = self.filterNonDomainElems(slab)
        box = self.cutNextBox(r, slab, var)
        return box
