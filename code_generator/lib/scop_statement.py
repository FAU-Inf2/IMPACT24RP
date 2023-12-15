import functools
import igraph
import re

import copy

from util import *
from access import *
from isl_util import *
from alignment import *
from isl_parser import *
from igraph_util import *
from isl_parser_extract import *

class ScopStatement:
    def __init__(self, name):
        self.accCounter = 0
        self.writes = []
        self.reads = []
        self.name = name

    def nextAccCounter(self):
        res = self.accCounter
        self.accCounter += 1
        return res

    def __deepcopy__(self, memo):
        selfCpy = ScopStatement(copy.deepcopy(self.name))
        selfCpy.dom = deepCopyUnionSet(self.dom)
        selfCpy.sched = deepCopyUnionMap(self.sched)
        selfCpy.dfg = copy.deepcopy(self.dfg)
        selfCpy.domAnon = deepCopyUnionMap(self.domAnon)
        selfCpy.writes = [ copy.deepcopy(s) for s in self.writes ]
        for w in selfCpy.writes:
            w.setStmt(selfCpy)
        selfCpy.reads = [ copy.deepcopy(s) for s in self.reads ]
        for r in selfCpy.reads:
            r.setStmt(selfCpy)
        selfCpy.scop = None
        return selfCpy

    def getArrayNames(self):
        return { getRangeTupleName(s.get())
                 for s in self.writes + self.reads }

    def getParams(self):
        params = getParams(self.getDom().as_set())
        return params

    def __str__(self):
        res = "%s => { dom: %s, sched: %s, writes: %s, reads: %s }" % \
            (self.name, self.dom, self.sched, self.writes, self.reads)
        return res

    def checkConsistency(self):
        for w in self.writes:
            assert(w.getStmt() is self)
        for r in self.reads:
            assert(r.getStmt() is self)

    def getDom(self):
        return self.dom

    def setSched(self, sched):
        self.sched = sched

    def getSched(self):
        return self.sched

    def getWrites(self):
        return self.writes

    def getReads(self):
        return self.reads

    def getFstRead(self):
        assert(len(self.reads) > 0)
        return self.reads[0]

    def getName(self):
        return self.name

    def getDfg(self):
        return self.dfg

    def getDfgArrRefs(self):
        return self.dfgArrRefs

    def getAnonymizer(self):
        return self.domAnon

    def setScop(self, scop):
        assert(scop is not None);
        self.scop = scop

    def getScop(self):
        assert(self.scop is not None);
        return self.scop

    def getAnonDom(self):
        return self.getDom().apply(self.getAnonymizer())

    def getAccessByArrRef(self, ar):
        accs = self.getReads() + self.getWrites()
        filtered = [ a for a in accs if a.getName() == ar ]
        assert(len(filtered) == 1)
        return filtered[0]

    def getAccs(self):
        return self.getReads() + self.getWrites()

    def addDfg(self, dfg):
        self.dfg = dfg
        regexp = r'(r[0-9]+|w[0-9]+)'
        p = re.compile(regexp)
        dfgArrRefs = p.findall(dfg)
        assert(len(dfgArrRefs) >= 1)
        self.dfgArrRefs = dfgArrRefs
        return self

    def addDomain(self, usetStr):
        self.dom = isl.union_set(usetStr)
        return self

    def addSchedule(self, umap):
        self.sched = isl.union_map(umap)
        return self

    def addDomAnonymizer(self, umap):
        self.domAnon = isl.union_map(umap)
        return self

    def addRead(self, umapStr, name):
        acc = ReadAccess(umapStr, name)
        acc.setStmt(self, self.nextAccCounter())
        self.reads.append(acc)
        return self

    def addWrite(self, umapStr, name):
        acc = WriteAccess(umapStr, name)
        acc.setStmt(self, self.nextAccCounter())
        self.writes.append(acc)
        return self

    def getLbOfDom(self, dim):
        dimlist = self.getDimList()
        assert(dim in dimlist)
        dimIdx = dimlist.index(dim)
        # TODO: I can now express this via
        # isl.set.project_out_set_dims()...
        def getSetProjector(dimlist, numDim):
            template = "{ [%s] -> [%s] }"
            inDims = cmJoin(dimlist)
            outDims = dimlist[numDim]
            filledTmpl = template % (inDims, outDims)
            # print("filledTmpl: ", filledTmpl)
            islSet = isl.union_map(filledTmpl)
            return islSet

        numDims = len(dimlist)
        projected = self.getAnonDom().apply(getSetProjector(dimlist, dimIdx))
        lmin = projected.lexmin()
        return (int(getLexmin(assureSet(lmin))))

    def getPaddedDom(self, align):
        dom = self.dom
        dimList = self.getDimList()
        lastDim = dimList[-1]
        lastDimLb = self.getLbOfDom(lastDim)

        padder = mkAligner(dom, align, lastDimLb)
        print("padder: ", padder)
        expander = mkExpander(dom, align)
        print("expander: ", padder)
        newDom = self.dom.apply(padder)
        newDom = newDom.apply(expander)
        print("newDom: ", newDom)
        return newDom

    def getSchedRangeName(self):
        return getMapRangeTupleName(self.sched)

    def getSchedRangeDims(self):
        dims = getMapRangeTupleDims(self.sched)
        return dims

    def getDomInSched(self):
        return self.dom.apply(self.sched)

    def getDimList(self):
        return getDims(self.getDom().as_set())

    def getDomTupName(self):
        return getSetTupleId(self.getDom())

    def allBefore(self, other):
        assert(self.getScop() == other.getScop())
        elemsSelf = self.getDom()
        elemsOther = other.getDom()
        allInSelfBeforeOther = arrow(elemsSelf, elemsOther)
        ordRel = self.scop.calcOrd()
        res = allInSelfBeforeOther.is_subset(ordRel)
        return res

    def clone(self): return copy.deepcopy(self)

def mkStatement(name, dom, sched, writes, reads, domAnon = None):
    res = ScopStatement(name)
    res.addDomain(dom)
    res.addSchedule(sched)
    for r in reads:
        res.addRead(r)
    for w in writes:
        res.addWrite(w)
    res.addDomAnonymizer(domAnon)
    return res

