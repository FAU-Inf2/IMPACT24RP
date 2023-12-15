import isl
import igraph
import operator
import functools

from util import *
from access import *
from accesses import *
from isl_util import *
from isl_parser import *
from dependency import *
from igraph_util import *
from cache_decide import *
from read_box_analysis import *
from isl_parser_extract import *

def isFusedAccCacheAble(accs, tiling, dom):
    rba = ReadBoxAnalysis(tiling, dom)
    fused = functools.reduce(lambda x, y: x.add(y), accs)
    isCacheAble = rba.isCacheAble(fused.union())
    return isCacheAble

def prod(l):
    return functools.reduce(operator.mul, l, 1)

def reduceAccs(accs):
    print("reduceAccs: ")
    for acc in accs:
        print("acc: ", acc)
    return functools.reduce(lambda l, r: l.add(r), accs)

class OverlapGraph:
    def __str__(self):
        return str(self.graph)

    def __repr__(self):
        return repr(self.graph)

    def getAccs(self):
        res = [ v["accesses"] for v in self.graph.vs() ]
        return res

    def addDepEdge(self, vf, vt):
        self.graph.add_edge(vf, vt)["ty"] = "dep"

    def addOverlapEdge(self, vf, vt):
        self.graph.add_edge(vf, vt)["ty"] = "ovr"

    def getTyAccsWithVertices(self, ty):
        vs = self.graph.vs()
        res = []
        for v in vs:
            accs = v["accesses"]
            assert(not accs.isFused())
            acc = accs.getFirst()
            if ty == "r" and acc.isReadAcc():
                res.append((acc.get(), v))
            if ty == "w" and acc.isWriteAcc():
                res.append((acc.get(), v))
        return res

    def getWriteAccsWithVertices(self):
        return self.getTyAccsWithVertices(ty = "w")

    def getReadAccsWithVertices(self):
        return self.getTyAccsWithVertices(ty = "r")

    def doOverlap(self, v0, v1):
        es = self.graph.es.select(
            _source = v0, _target = v1, ty = "ovr")
        return len(es) > 0

    def detectDeps(self):
        ord = self.ord
        reads = self.getReadAccsWithVertices()
        writes = self.getWriteAccsWithVertices()

        for (r, vr) in reads:
            for (w, vw) in writes:
                rawSet = w.apply_range(r.reverse())
                rawSet = rawSet.intersect(ord)
                if (not rawSet.is_empty()):
                    self.addDepEdge(vr, vw)
                warSet = r.apply_range(w.reverse())
                warSet = warSet.intersect(ord)
                if (not warSet.is_empty()):
                    self.addDepEdge(vr, vw)
        for (w0, vw0) in writes:
            for (w1, vw1) in writes:
                if (vw0.index == vw1.index): continue
                wawSet = w0.apply_range(w1.reverse)
                wawSet = wawSet.intersect(ord)
                if (not wawSet.is_empty()):
                    self.addDepEdge(vw0, vw1)

    def fuseNodesStageOne(self, tiling, dom):
        vs = self.graph.vs()
        accs = self.getAccs()
        rba = ReadBoxAnalysis(tiling, dom)
        cc = self.graph.connected_components(mode = "weak")
        fuseMap = {}
        for vc in cc:
            accs = [ vs[v]["accesses"] for v in vc ]
            fusable = isFusedAccCacheAble(accs, tiling, dom)
            for v in vc:
                fuseMap[v] = vc[0]
            if not fusable:
                for v in vc:
                    vs[v]["accesses"].setCacheAble(False)
                    vs[v]["accesses"].setMustNotCache(True)

        combiner = { "accesses": reduceAccs }
        #print( [ v.index for v in vs ] )
        contractMap = [ fuseMap[ v.index ] for v in vs ]
        #print(contractMap)
        self.graph.contract_vertices(contractMap, combiner)

    def setAllUnsealed(self):
        vertices = self.graph.vs()
        for v in vertices: v["seal"] = False

    def getUnsealed(self):
        vs = self.graph.vs()
        return [ v for v in vs if v["seal"] == False ]

    def countUnsealed(self):
        return len(self.getUnsealed())

    def fuseNodesStageTwo(self, tiling, dom):
        self.setAllUnsealed()
        rba = ReadBoxAnalysis(tiling, dom)
        while self.countUnsealed() > 0:
            k = self.getUnsealed()[0]
            R = [ r for r in self.getUnsealed() if r != k ]
            toRemove = []
            for r in R:
                overlap = self.doOverlap(r, k)
                kAcc = k["accesses"]
                rAcc = r["accesses"]
                bothCacheAble = kAcc.isCacheAble() and rAcc.isCacheAble()
                sameArr = kAcc.getArrName() == rAcc.getArrName()
                testFuse = k["accesses"].add(r["accesses"])
                #print("testFuse: ", testFuse)
                ru = testFuse.union()
                fusedCacheAble = rba.isCacheAble(ru) if sameArr else False
                fuse = bothCacheAble and overlap and fusedCacheAble
                if fuse:
                    k["accesses"] = testFuse
                    toRemove.append(r)
            k["seal"] = True
            self.graph.delete_vertices(toRemove)

    def __init__(self, name, tiling, order):
        self.graph = igraph.Graph(directed = False)
        self.graph["name"] = name
        self.name = name
        self.tiling = tiling
        self.ord = order

    def findNodeThatContainsAcc(self, needle):
        nodes = self.getNodes()
        for node in nodes:
            for access in node["accesses"].unpack():
                if access.is_equal(needle.get()):
                    return node
        raise Exception("Not found: " + str(needle))

    def isAccessInFusedNode(self, access):
        node = self.findNodeThatContainsAcc(access)
        accs = node["accesses"]
        return accs.len() > 1

    def syncAttributes(self):
        for v in self.graph.vs():
            accs = v["accesses"]
            v["accType"] = accs.getAccType()
            v["label"] = accs.getName()
            v["arrayName"] = accs.getArrName()
            v["alignedToLoop"] = accs.isAlignedToLoop()
            v["isCacheAble"] = accs.isCacheAble()

    def addAcc(self, accesses):
        assert(isinstance(accesses, Accesses))
        #assert(access.get().isa_map())
        vertex = self.graph.add_vertex(accesses.getName())
        vertex["accesses"] = accesses
        return vertex

    def getVertexByName(self, vName):
        vsseq = self.graph.vs(name = vName)
        assert(len(vsseq) == 1)
        return vsseq[0]

    def writeToFs(self, name = None):
        self.graph["boxCardSum"] = self.getCardSum()
        self.graph["cacheCardSum"] = self.getCacheCardSum()
        name = self.graph["name"] if name == None else name
        writeToPng(self.graph, name)

    def writeToFsOnlyGraph(self, name = None):
        name = self.graph["name"] if name == None else name
        writeToPng(self.graph, name)

    def getNodes(self, pred = lambda v: True):
        return [ v for v in self.graph.vs() if pred(v) ]

    @staticmethod
    def getIsFusedPred(): return lambda v : v["accesses"].len() > 1

    @staticmethod
    def getOnlyOneAccPred(): return lambda v : v["accesses"].len() == 1

    @staticmethod
    def getIsReadPred():
        return lambda v : v["accesses"].getFirst().isReadAcc() \
            and v["accesses"].len() == 1

    @staticmethod
    def getIsWritePred():
        return lambda v : v["accesses"].getFirst().isWriteAcc() \
            and v["accesses"].len() == 1

    @staticmethod
    def getHasWritePred():
        return lambda v : v["accesses"].hasWrite()

    @staticmethod
    def getHasNoRarDepPred(ord):
        return lambda v : \
            v["accesses"].getFirst().hasNoReadAfterReadDependency(ord)

    def detectOverlaps(self):
        tileSched = self.tiling.getTransformedSchedule()
        fullTile = self.tiling.getTileChunk() # TODO: maybe duplicate?

        onlyOneAcc = OverlapGraph.getOnlyOneAccPred()
        vertices = self.getNodes(onlyOneAcc)
        for vi0 in range(0, len(vertices)):
            for vi1 in range(vi0 + 1, len(vertices)):
                v0 = vertices[vi0]
                v1 = vertices[vi1]
                accs0 = v0["accesses"]
                accs1 = v1["accesses"]
                assert(not accs0.isFused())
                assert(not accs1.isFused())
                r0 = accs0.getFirst().get()
                r1 = accs1.getFirst().get()

                ris0 = accRelInSchedSpace(r0, tileSched)
                ris1 = accRelInSchedSpace(r1, tileSched)
                rb0 = fullTile.apply(ris0)
                rb1 = fullTile.apply(ris1)

                inter = rb0.intersect(rb1)
                if not inter.is_empty():
                    self.addOverlapEdge(v0, v1)

    def getAlignedAccs(self):
        return sum([ (1 if v["alignedToLoop"] else 0) * v["boxCard"]
                     for v in self.graph.vs() ])

    def getAlignmentFactor(self):
        return self.getAlignedAccs() / self.getCardSum()

    def calculateCaches(self, dom):
        rba = ReadBoxAnalysis(self.tiling, dom)
        vs = self.graph.vs()
        for v in vs:
            accs = v["accesses"]
            accRel = accs.union()
            cache = cacheDecide(accs)
            if cache == "noCache":
                v["cacheCard"] = 0
                continue
            slab = slabDecide(self.tiling.getSlabs(), accs)
            bounds = rba.getCacheBounds(accRel, slab)
            print("accRel: ", accRel)
            print("bounds: ", bounds)
            print("slab: ", slab)
            v["cacheCard"] = prod(bounds)
            v["cacheShape"] = bounds
            v["cacheSlab"] = slab

    def getCacheCardSum(self):
        return sum([ v["cacheCard"] for v in self.graph.vs() ])

    def calculateCards(self):
        tileSched = self.tiling.getTransformedScheduleNoDi()
        chunk = self.tiling.getSlabs().getFullTileSlabNoDi()

        vertices = self.graph.vs()
        for v in vertices:
            #print("accesses of node: ", v["accesses"])
            rdsInSched = [ accRelInSchedSpace(r, tileSched)
                           for r in v["accesses"].unpack() ]
            fusedRead = union(rdsInSched)

            fullTileRbox = chunk.apply(fusedRead)
            #print("fullTileRbox: ", fullTileRbox)
            assert(not fullTileRbox.is_empty())
            fullTileBoxCard = fullTileRbox.card()
            #print(fullTileBoxCard)
            cardParsed = parseCard(fullTileBoxCard)
            fstEntry = islCardGetOnlyEntry(cardParsed)
            assert(fstEntry.isnumeric())
            v["boxCard"] = int(fstEntry)

    def getCardSum(self):
        return sum([ v["boxCard"] for v in self.graph.vs() ])
