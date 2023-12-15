from access import *
from isl_util import *

class Accesses():
    def __init__(self, init = []):
        self.payload = init
        self.alignedToLoop = None
        self.cacheAble = None

    def union(self):
        return union(self.unpack())

    def isAlignedToLoop(self):
        return all([ acc.isAlignedToLoop() for acc in self.payload ])

    def setCacheAble(self, b):
        for acc in self.payload:
            acc.setCacheAble(b)

    def isCacheAble(self):
        return all([ acc.isCacheAble() for acc in self.payload ])

    def setMustNotCache(self, b):
        for acc in self.payload:
            acc.setMustNotCache(b)

    def isMustNotCache(self):
        return any([ acc.isMustNotCache() for acc in self.payload ])

    def add(self, otherAcc):
        return Accesses(self.payload + otherAcc.payload)

    def len(self):
        return len(self.payload)

    def getArrName(self):
        print(self.payload)
        #assert(len(self.payload) == 1)
        res = set([ acc.getArrName() for acc in self.payload ])
        assert(len(res) == 1)
        return res.pop()

    def getAccType(self):
        containsWrites = any([ acc.isWriteAcc() for acc in self.payload ])
        containsReads = any([ acc.isReadAcc() for acc in self.payload ])
        if containsWrites and (not containsReads):
            return "W"
        if (not containsWrites) and containsReads:
            return "R"
        if containsWrites and containsReads:
            return "M"
        return "ERR"

    def getName(self):
        return "_".join([ acc.getName() for acc in self.payload ])

    def isFused(self):
        return self.len() > 1

    def getFirst(self):
        assert(self.len() > 0)
        return self.get()[0]

    # TODO is this used?
    def get(self):
        return self.payload

    def unpack(self):
        return map(lambda x: x.get(), self.payload)

    def hasWrite(self):
        return any(map(lambda x: x.isWriteAcc(), self.payload))

    def __str__(self):
        return str(self.union())
