from ports.port import *
from ports.common import *

class LinearizedPtrAcc(TlfPort):
    def __init__(self, ni, elemType, dims):
        self.elemType = elemType
        self.dims = dims

    def mkVarDecl(self, vn):
        return "%s *%s" % (self.elemType, vn)

    def mkAccess(self, vn, indexExprs):
        linExpr = multAll(self.dims, indexExprs)
        return "%s[%s]" % (vn, linExpr)

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
