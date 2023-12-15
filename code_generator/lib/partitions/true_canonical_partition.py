from cache_decide import *
from partitions.canonical_partition import *

class TrueCanonicalPartition(CanonicalPartition):
    def __init__(self, stmts, scop):
        super().__init__(stmts, scop)

    def setTiling(self, tiling):
        self.tiling = tiling
        self.slabs = Slabs(tiling)
    def getTiling(self): return self.tiling
    def setOverlapGraph(self, og): self.og = og
    def getOverlapGraph(self): return self.og

    def getDepGraph(self):
        dom = self.getUnionDom()
        sch = self.getUnionSched()
        ord = Sch.lex_lt_union_map(Sch)
        stmts = self.getStmts()
        return calcDepGraph(dom, ord, "", stmts)

    # See exp13.py for explanation. This transforms sth. like
    # { O[ti, tj, tk, i, j, k] -> A[i, tj, tk] } (aka.
    # a map that always maps to the lex. smallest element
    # in the boxed read box of the ldSlab) into
    # { O[ti, tj, tk, ...] -> A[i, j - tj, k - tk] }
    # Which resembles the correct array indices.
    def transformAcc(self, fusedAccRel, accRel, slab, arrName):
        tiling = self.getTiling()
        schedNoDi = tiling.getTransformedScheduleNoDi()
        fusedAccInSched = accRelInSchedSpace(fusedAccRel, schedNoDi)
        accRelInSched = accRelInSchedSpace(accRel, schedNoDi)
        # TODO: This should be cached!!!
        cacheBox = getFilledBox(slab, fusedAccInSched)
        cBoxLmin = makeUnanon(getBoxedLexminPoint(cacheBox), arrName)
        fullSlab = tiling.getSlabs().getFullTileSlabNoDi()
        e = schedNoDi.range().intersect(fullSlab)
        Smin = arrow(e, cBoxLmin)

        #print("Smin: ", Smin)
        #print("cacheBox: ", cacheBox)
        #print("fusedAccInSched: ", fusedAccInSched)
        #print("fullSlab: ", fullSlab)
        #print("cBoxLmin: ", cBoxLmin)

        R0 = accRelInSched.intersect_domain(slab)
        res = (arrow(Smin.wrap(), R0.wrap())
               .deltas_map()
               .domain_factor_range()
               .domain_factor_domain()
               .range_factor_range())
        res = res.as_map().project_out_all_params()
        #exit(1)
        return res

    def transform(self, accs, acc):
        cacheStrat = cacheDecide(accs)
        if cacheStrat == "noCache":
            return self.transformOther(acc)
        slab = None
        if cacheStrat == "readSlab":
            slab = self.slabs.getReadCacheSlab()
        if cacheStrat == "fullSlab":
            slab = self.slabs.getFullTileSlabNoDi()
        if cacheStrat == "lineSlab":
            slab = self.slabs.getWriteCacheSlab()

        assert(slab != None)

        accsRel = accs.union()
        arrName = accs.getArrName()
        return self.transformAcc(accsRel, acc.get(), slab, arrName)

    def transformOther(self, acc):
        accRel = acc.get()
        tiling = self.getTiling()
        schedNoDi = tiling.getTransformedScheduleNoDi()
        oInSched = accRelInSchedSpace(accRel, schedNoDi)
        return oInSched

    def mkTiledAccTuple(self, readsInSched):
        chain = self.chainTogether(readsInSched)
        chain = self.addOriginalDiDims(chain)
        return chain

    def mkOrigAccTuple(self, readsInSched):
        chain = self.chainTogether(readsInSched)
        chain = chain.intersect_domain(self.getDomInScheduleSpace())
        return chain

    def chainTogether(self, readsInSched):
        def chainTwo(r0, r1): return r0.domain_map().apply_range(r1).curry()
        return functools.reduce(chainTwo, readsInSched)

    # Note that we pad the domain here
    def addOriginalDiDims(self, tpl):
        dis = self.getPaddedDomInTiledScheduleSpace()
        #print(dis)
        return self.getTiling().addDiDims(tpl).intersect_domain(dis)

    def getPaddedDomInTiledScheduleSpace(self):
        bs = getLsdBlockSize(self.getDimlist())
        dom = self.getPaddedUnionDom(bs)
        sched = self.getTiling().getTransformedSchedule(dom)
        #print(dom)
        dis = dom.apply(sched)
        return dis

    def getOffsetInAccessTuple(self, stmt, arrRef):
        acc = stmt.getAccessByArrRef(arrRef)
        accs = stmt.getAccs()
        assert(acc in accs)
        idx = accs.index(acc)
        accsLeftOfAcc = accs[0:idx]
        return sum([ a.getNumArrDim() for a in accsLeftOfAcc ])

    def generateTiledIndexTuple(self, stmt):
        og = self.getOverlapGraph()
        accessesOfS = stmt.getAccs()
        transformedAccs = []
        for acc in accessesOfS:
            node = og.findNodeThatContainsAcc(acc)
            accs = node["accesses"]
            transfAcc = self.transform(accs, acc)
            transformedAccs.append(transfAcc)
        tpl = self.mkTiledAccTuple(transformedAccs)
        tpl = self.setTupleName(tpl, stmt)
        return tpl

    def setTupleName(self, tpl, stmt):
        assert(tpl.isa_map())
        name = isl.id(stmt.getName())
        res = tpl.as_map().set_range_tuple(name)
        return res.to_union_map()

    def generateOrigIndexTuple(self, stmt):
        accs = stmt.getAccs()
        rels = [ accRelInSchedSpace(acc.get(), self.getUnionSched())
                 for acc in accs ]
        tpl = self.mkOrigAccTuple(rels)
        tpl = self.setTupleName(tpl, stmt)
        return tpl

    def buildAstFromChains(self, chains):
        unionChain = union(chains)
        #print("unionChain", unionChain)
        inp = unionChain.domain_map().domain_factor_range()
        #print("inp: ", inp)
        ab = isl.ast_build()
        ast = isl.ast_build.node_from_schedule_map(ab, inp)
        print(ast.to_C_str())
        return ast

    def genAst(self):
        print(self.getTiling().getTransformedSchedule())
        chains = [ self.generateTiledIndexTuple(s) for s in self.getStmts() ]
        return self.buildAstFromChains(chains)

    def genOrigAst(self):
        chains = [ self.generateOrigIndexTuple(s) for s in self.getStmts() ]
        return self.buildAstFromChains(chains)
