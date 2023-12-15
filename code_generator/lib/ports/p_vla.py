from util import *
from ports.port import *
from ports.common import *

class VarLengthArray(TlfPort):
    def __init__(self, ni, elemType, dims):
        self.elemType = elemType
        self.dims = dims

    def mkVarDecl(self, vn):
        arrDimStr = eJoin(brackWrap(self.dims))
        return "%s %s%s" % (self.elemType, vn, arrDimStr)

    def mkAccess(self, vn, indexExprs):
        return vn + eJoin(brackWrap(indexExprs))

    def mkLoad(self, vn, idx, offset):
        idx = addOffset(idx, offset)
        return self.mkAccess(vn, idx)

    def mkStore(self, vn, idx, offset):
        idx = addOffset(idx, offset)
        return self.mkAccess(vn, idx)

    def addArrayInfo(self, vn, dims):
        self.dims = dims

    def getAlign(self):
        return 1

    def getOffset(self):
        return 0

class VarLengthCacheArray(VarLengthArray):
    def __init__(self, ni, elemType, dims, alignOffset):
        super().__init__(ni, elemType, dims)
        self.alignOffset = alignOffset

    def mkLoad(self, vn, idx, offset):
        return super().mkLoad(vn, idx, offset + self.alignOffset)

    def mkStore(self, vn, idx, offset):
        return super().mkStore(vn, idx, offset + self.alignOffset)

    def getOffset(self):
        return self.alignOffset
