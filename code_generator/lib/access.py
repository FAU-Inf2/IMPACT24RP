import isl
import copy

from isl_util import *

class Access:
    def __init__(self, mstr, name):
        # print("Access ctor: ", mstr)
        self.islObj = isl.union_map(mstr)
        self.mustNotCache = False
        self.correspondingStmt = None
        self.alignedToLoop = None
        self.cacheAble = None
        self.name = name

    def setAlignedToLoop(self, b):
        self.alignedToLoop = b

    def isAlignedToLoop(self):
        assert(self.alignedToLoop != None)
        return self.alignedToLoop

    def setMustNotCache(self, b):
        self.mustNotCache = b

    def isMustNotCache(self):
        assert(self.mustNotCache != None)
        return self.mustNotCache

    def setCacheAble(self, b):
        self.cacheAble = b

    def isCacheAble(self):
        assert(self.cacheAble != None)
        return self.cacheAble

    def get(self):
        return self.islObj

    def getName(self):
        return self.name

    def setStmt(self, stmt, nthAccOfStmt):
        assert(stmt is not None)
        self.correspondingStmt = stmt
        self.nthAccOfStmt = nthAccOfStmt

    def getStmt(self):
        assert(self.correspondingStmt is not None)
        return self.correspondingStmt

    def getArrName(self):
        return getMapRangeTupleName(self.islObj)

    def getAccNumber(self):
        return self.nthAccOfStmt

    def getNumArrDim(self):
        ran = self.islObj.range()
        return assureSet(ran).n_dim()

    def getAccType(self):
        if self.isReadAcc():
            return "read"
        if self.isWriteAcc():
            return "write"
        raise Exception("Fail")

    def isReadAcc(self):
        return isinstance(self, ReadAccess)

    def isWriteAcc(self):
        return isinstance(self, WriteAccess)

    def hasReadAfterReadDependency(self, Ord):
        return False

    def hasNoReadAfterReadDependency(self, Ord):
        return not self.hasReadAfterReadDependency(Ord)

class ReadAccess(Access):
    def __repr__(self):
        return "ReadAccess(\"%s\")" % (str(self.islObj))

    def __deepcopy__(self, memo):
        return ReadAccess(str(self.islObj),
                          copy.deepcopy(self.name))

    def hasReadAfterReadDependency(self, Ord):
        dep = self.get().apply_range(self.get().reverse())
        dep = dep.intersect(Ord)
        return not dep.is_empty()

class WriteAccess(Access):
    def __repr__(self):
        return "WriteAccess(\"%s\")" % (str(self.islObj))

    def __deepcopy__(self, memo):
        return WriteAccess(str(self.islObj),
                           copy.deepcopy(self.name))

