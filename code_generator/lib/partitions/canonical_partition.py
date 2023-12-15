from settings import *
from block_sizes import *
from combinatorics import *
from read_box_analysis import *

# A canonical partition models a set
# of statements inside the same canonical
# loop nest
class CanonicalPartition:
    def __init__(self, stmts, scop):
        self.stmts = stmts
        self.scop = scop
        self.id = CanonicalPartition.getNextId()

    ID = 0

    @staticmethod
    def getNextId():
        res = CanonicalPartition.ID
        CanonicalPartition.ID = CanonicalPartition.ID + 1
        return res

    def getScop(self):
        return self.scop

    def getId(self):
        return self.id

    def dump(self):
        for stmt in self.stmts:
            print("stmt: ", stmt)

    def getAllReads(self):
        res = []
        for stmt in self.stmts:
            for read in stmt.getReads():
                res.append(read)
        return res

    def getAllAccs(self):
        return flatten([ stmt.getAccs() for stmt in self.stmts ])

    def getRarSelfDeps(self, Ord):
        return [ ar for ar in self.getAllReads()
                 if ar.hasReadAfterReadDependency(Ord) ]

    def getNonRarSelfDeps(self, Ord):
        withCy = self.getRarSelfDeps(Ord)
        allReads = self.getAllReads()
        return [ i for i in allReads if i not in withCy ]

    def getPaddedUnionDom(self, al = 4):
        return union([ s.getPaddedDom(al) for s in self.stmts ])

    def getUnionDom(self):
        return union([ s.getDom() for s in self.stmts ])

    def getUnionSched(self):
        return union([ s.getSched() for s in self.stmts ])

    def getDomInScheduleSpace(self):
        return self.getUnionDom().apply(self.getUnionSched())

    def getStmts(self): return self.stmts

    def getStmtByName(self, name):
        for stmt in self.getStmts():
            if stmt.getName() == name:
                return stmt

        raise Exception("Not found: " + name)

    # Needs schedules to be in 2k + 1 abstraction.
    def checkSchedRangeDimsMergable(self):
        schedRangeDims = [ stmt.getSchedRangeDims() for stmt in self.stmts ]
        lengths = [ len(s) for s in schedRangeDims ]
        lengthsEq = allEq(lengths)
        if not lengthsEq:
            return False
        dimVarLists = [ srd[1::2] for srd in schedRangeDims ]
        delimsLists = [ srd[0::2] for srd in schedRangeDims ]
        dimVarListsOk = allEq(dimVarLists)
        delimsListsOk = allIntConvertible(flatten(delimsLists))
        return dimVarListsOk and delimsListsOk

    def getDimlist(self):
        dims = [ s.getDimList() for s in self.stmts ]
        assert(allEq(dims))
        assert(len(dims) > 0)
        return dims[0]

    def getSchedRangeDims(self):
        assert(self.checkSchedRangeDimsMergable())
        someStmt = self.stmts[0]
        return someStmt.getSchedRangeDims()

    def getDefaultTilingSchedule(self):
        tupName = "O"
        dimlist = self.getDimlist()
        bs = getBlockSizes(dimlist)
        return SearchTile(self, tupName, dimlist, dimlist, bs)

    def getPossibleTilingSchedules(self):
        dimlist = self.getDimlist()
        tupName = "O"
        dimLen = len(dimlist)
        res = []

        bs = getBlockSizes(dimlist)
        viTile = sortedVar(dimlist, dimLen)
        viElems = variations(dimlist, dimLen)
        for vit in viTile:
            for vie in viElems:
                st = SearchTile(self, tupName, vit, vie, bs)
                res.append(st)

        return res

    def getLbOfDom(self, v):
        lbs = [ s.getLbOfDom(v) for s in self.stmts ]
        assert(allEq(lbs))
        assert(len(lbs) > 0)
        return lbs[0]

    def isTruePart(self):
        return isinstance(self, TrueCanonicalPartition)

    def isFalsePart(self):
        return isinstance(self, FalseCanonicalPartition)
