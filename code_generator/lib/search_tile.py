import isl

from scop_statement import *
from util import *

class Slabs():
    def __init__(self, tiling):
        self.tiling = tiling
        self.transform = tiling.getFullTransform()

    # e.g. [ti, tj, tk] -> { O[1, ti, tj, i, 1, j, 0] }
    # which represents all elements in one specific tile.
    def getInnerTileSlab(self, dims):
        tile = self.tiling.getTileDims()
        inDims = self.tiling.createScheduleRangeDimlist()
        setStr = "[%s] -> { %s[%s] }"
        inter = setStr % (cmJoin(tile + dims), self.tiling.tupleName,
                          cmJoin(inDims))
        res = isl.union_set(inter)
        return res

    def getInnerTileSlabNoDi(self, dims):
        return self.tiling.removeDiDims(self.getInnerTileSlab(dims))

    def getVarSlabNoDi(self, var):
        return self.getInnerTileSlabNoDi(wrapInListIfNotList(var))

    def getVarSlab(self, var):
        return self.getInnerTileSlab(wrapInListIfNotList(var))

    def getFullTileSlab(self):
        return self.getInnerTileSlab([])

    def getFullTileSlabNoDi(self):
        return self.tiling.removeDiDims(self.getFullTileSlab())

    def getLsdTileSlabNoDi(self):
        smallestDim = self.tiling.getSmallestElemDim()
        return self.getVarSlabNoDi(smallestDim)

    def getReadCacheSlab(self):
        oneElemDims = self.tiling.getNumElemDims() == 1
        largestDim = [] if oneElemDims else self.tiling.getLargestElemDim()
        return self.getVarSlabNoDi(largestDim)

    def getWriteCacheSlab(self):
        smallestDim = self.tiling.getSmallestElemDim()
        largerDims = self.tiling.getLargerElemDims(smallestDim)
        return self.getVarSlabNoDi(largerDims)

class SearchTile:
    @staticmethod
    def mkTileSchedMap(tileSched):
        return { "t" + t : t for t in tileSched }

    def __init__(self, partition, tupName,
                 tileSched, elemSched, blockSizes):
        self.partition = partition
        self.blockSizes = blockSizes
        self.tupleName = tupName
        # { "ti" : "i", "tj" : "j"... }
        self.tileSchedMap = SearchTile.mkTileSchedMap(tileSched)
        # { "i" : "ti", "j": "tj" }
        self.reverseTileSchedMap = mapReverse(self.tileSchedMap)
        # ["ti", "tj"]
        self.tileSched = list(self.tileSchedMap.keys())
        # ["i", "j"]
        self.elemSched = elemSched

    def getElemDims(self):
        return self.elemSched

    def getNumElemDims(self):
        return len(self.elemSched)

    def getTileDims(self):
        return self.tileSched

    def getSlabs(self):
        return Slabs(self)

    def getTilingLevel(self):
        return len(self.tileSched)

    def __str__(self):
        return sanitizeForPath(
            "TileSched: " + str(self.tileSched) +
            " ElemSched: " + str(self.elemSched))

    def __repr__(self):
        return sanitizeForPath(
            "SearchTile(%s, %s)" % (repr(self.tileSched),
                                    repr(self.elemSched)))

    def getFullTileConstrContextSet(self):
        return self.getSlabs().getFullTileSlab()

    def getLineConstrContextSet(self):
        smallest = self.getSmallestElemDim()
        largerDims = self.getLargerElemDims(smallest)
        return self.getSlabs().getVarSlab(largerDims)

    def getTilingTransform(self):
        constrs = []
        for k, v in self.tileSchedMap.items():
            bs = self.blockSizes[v]
            lb = self.partition.getLbOfDom(v)
            constr = "%s mod %s = 0 and %s <= %s < %s + %s" %\
                (k, bs, k, v, k, bs)
            constrs.append(constr)

        constrs = andJoin(constrs)
        mapStr = "{ %s[%s] -> %s[%s] : %s }"
        outDims = cmJoin(self.createScheduleRangeDimlist())
        inDims = cmJoin(self.createScheduleDomDimlist())
        tid = self.tupleName
        fillIns = (tid, inDims, tid, outDims, constrs)
        interpolated = mapStr % fillIns
        m = isl.union_map(interpolated)
        return m

    # e.g. { O[0, ti, tj, i, di, j, dj] -> O[0, ti, tj, ti - i, di, tj - j, dj] }
    def getZeroShiftTransform(self):
        tid = self.tupleName
        inDims = self.createScheduleRangeDimlist()
        outDims = [ (d + "-" + self.reverseTileSchedMap[d])
                    if d in self.reverseTileSchedMap.keys()
                    else d
                    if d in self.elemSched else d for d in inDims ]
        mStr = "{ %s[%s] -> %s[%s] }" % (tid, cmJoin(inDims), tid, cmJoin(outDims))
        return isl.union_map(mStr)

    # e.g. { O[0, ti, tj, i, di, j, dj] -> O[0, ti, tj, i - x, di, j - y, dj] }
    def getSchedAdjustTransform(self, dom):
        sch = self.partition.getUnionSched()
        tileTra = self.getTilingTransform()
        adjust = self.getAdjustTransform(dom)
        onlyTile = sch.apply_range(tileTra)
        combined = sch.apply_range(adjust).apply_range(tileTra)
        onlyAdjust = onlyTile.reverse().apply_range(combined)
        return onlyAdjust

    # e.g. { O[0, i, di, j, dj] -> O[0, i - x, di, j - y, dj] }
    # See scrapyard/schedule_adjust.py for why this is useful
    def getAdjustTransform(self, dom):
        sch = self.partition.getUnionSched()
        domList = unionSetToList(dom)
        #print(domList[0].apply(sch).lexmin().as_set())
        res = union([
            (d.apply(sch)
             .as_set().lexmin().translation()
             .reverse().deltas().translation())
            for d in domList ])
        return res

    def getTileTransform(self, dom = None):
        dom = dom if dom != None else self.partition.getUnionDom()
        shifter = self.getZeroShiftTransform()
        adjuster = self.getSchedAdjustTransform(dom)
        return adjuster.apply_range(shifter)

    def getFullTransform(self, dom = None):
        dom = dom if dom != None else self.partition.getUnionDom()
        shifter = self.getZeroShiftTransform()
        tiler = self.getTilingTransform()
        adjuster = self.getSchedAdjustTransform(dom)
        return tiler.apply_range(adjuster).apply_range(shifter)

    # e.g. { O[0, ti, tj, i, di, j, dj] -> O[0, ti, tj, i, j] }
    def getDiRemover(self):
        fr = self.createScheduleRangeDimlist()
        to = self.createScheduleRangeDimlistWithNoDi()
        mapStr = "{ %s[%s] -> %s[%s] }"
        inter = mapStr % (self.tupleName, cmJoin(fr),
                          self.tupleName, cmJoin(to))
        # print("inter:", inter)
        return isl.union_map(inter)

    def getDiAdder(self):
        return self.getDiRemover().reverse()

    def addDiDims(self, n):
        return self.modifyDiDims(n, self.getDiAdder())

    def removeDiDims(self, n):
        return self.modifyDiDims(n, self.getDiRemover())

    def modifyDiDimsOnMap(self, n, f):
        removeDis = f
        assert(n.isa_map())
        ranTupSpc = n.project_out_all_params().as_map().space().range()
        domTupSpc = n.project_out_all_params().as_map().space().domain()
        remDisSpc = removeDis.as_map().space().domain()

        applicableToDom = domTupSpc.is_equal(remDisSpc)
        applicableToRan = ranTupSpc.is_equal(remDisSpc)
        if applicableToDom and applicableToRan:
            return (n.apply_range(removeDis)
                    .reverse().apply_range(removeDis).reverse())
        if applicableToDom:
            return n.reverse().apply_range(removeDis).reverse()
        if applicableToRan:
            return n.apply_range(removeDis)
        raise Exception("Spaces do not match")

    def modifyDiDims(self, n, f):
        if isUnionSet(n) or isSet(n): return n.apply(f)
        if isMap(n): return self.modifyDiDimsOnMap(n, f)
        if isUnionMap(n):
            maps = unionMapToList(n)
            # n.foreach_map(lambda m: maps.append(m))
            res = union([ self.modifyDiDimsOnMap(m, f) for m in maps ])
            return res

        raise Exception("Not applicable to: " + type(n))

    # e.g. { O[1, ti, tj, i, 1, j, 0] -> O[1, ti, tj, i', 1, j', 0]
    #        : j' > j and i' > i }
    def getStepMap(self, dim, op):
        # elemSched = self.elemSched
        inDims = self.createScheduleRangeDimlist()
        outDims = self.createScheduleRangeDimlist()
        # for es in elemSched:
        outDims[outDims.index(dim)] = dim + "'"
        # print(outDims)
        constr = "%s' %s %s" % (dim, op, dim)
        mapStr = "{ %s[%s] -> %s[%s] : %s }"
        fillIns = (self.tupleName, cmJoin(inDims),
                   self.tupleName, cmJoin(outDims), constr)
        interpolated = mapStr % fillIns
        return isl.union_map(interpolated)

    def getNextMap(self, dim):
        return self.getStepMap(dim, ">")

    def getPrevMap(self, dim):
        return self.getStepMap(dim, "<")

    def getPrevEqMap(self, dim):
        return self.getStepMap(dim, "<=")

    def getLargerElemDims(self, dim):
        ed = self.getElemDims()
        return ed[0:ed.index(dim)]

    def getSmallerElemDims(self, dim):
        ed = self.getElemDims()
        return ed[ed.index(dim)+1:len(ed)]

    def getLargestElemDim(self):
        return self.getElemDims()[0]

    def getSmallestElemDim(self):
        return self.getElemDims()[-1]

    def getTransformedSchedule(self, dom = None):
        sched = self.partition.getUnionSched()
        tile = self.getFullTransform(dom)
        return sched.apply_range(tile)

    def getTransformedScheduleNoDi(self):
        return self.removeDiDims(self.getTransformedSchedule())

    def getLsdLine(self):
        tile = self.getFullTransform()
        #print("tile: ", tile)
        tileCnstr = self.getLineConstrContextSet()
        #print("tileCnstr: ", tileCnstr)
        lsdLine = tile.range().intersect(tileCnstr)
        assert(not lsdLine.is_empty())
        return lsdLine

    def getTileChunk(self):
        tile = self.getFullTransform()
        fullTileCnstr = self.getFullTileConstrContextSet()
        chunk = tile.range().intersect(fullTileCnstr)
        assert(not chunk.is_empty())
        return chunk

    def getLsdLineInD(self):
        sched = self.stmt.getSched()
        tile = self.getFullTransform()
        inverseSched = tile.reverse().apply_range(sched.reverse())
        line = self.getLsdLine().apply(inverseSched)
        assert(not line.is_empty())
        return line

    def getTiledScheduleRangeSignature(self):
        schedRanDims = self.partition.getSchedRangeDims()
        result = schedRanDims[0:1]
        result = result + self.tileSched
        for i in range(1, len(schedRanDims), 2):
            var = schedRanDims[i]
            var = var if not isinstance(var, list) else var[1]
            delim = schedRanDims[i + 1]
            result.append(var)
            result.append("d" + var if var in self.partition.getDimlist()
                          else delim)
        return result

    def createScheduleDomDimlist(self):
        sig = self.getTiledScheduleRangeSignature()
        return [ s for s in sig if s not in self.tileSched ]

    def createScheduleRangeDimlist(self):
        return self.getTiledScheduleRangeSignature()

    def createScheduleRangeDimlistWithNoDi(self):
        schedRanDims = self.partition.getSchedRangeDims()
        result = schedRanDims[0:1] + self.tileSched + self.elemSched
        return result
