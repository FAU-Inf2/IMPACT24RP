from ports.port import *
from ports.common import *

typeToSizeMap = {
    "double": 8,
    "float": 4,
    "short": 2,
    "char": 1,
    "long": 8,
    "int": 4
}

class BurstMaxi(TlfPort):
    def __init__(self, numElems, elemType, dims):
        self.numElems = numElems
        self.elemType = elemType
        self.dims = dims

    def getSizeInBytesFromType(self):
        return typeToSizeMap[self.elemType]

    def mkVarDecl(self, vn):
        ty = "hls::burst_maxi<%s%s>" % ("AxiVec", self.numElems)
        return "%s %s" % (ty, vn)

    def mkLoad(self, vn, indexExprs, offset):
        return "%s.read" % (vn)

    def mkStore(self, vn, indexExprs, offset):
        strbDecl = "ap_int<%s> writeStrobe;" % (self.numElems * 4)
        iter = indexExprs[0]
        strobes = nlJoin([
            "const int s%s = (%s + %s >= 0) - (%s + %s >= payLen);"
            % (num, iter, num, iter, num)
            for num in range(0, self.numElems) ])
        bytesOfType = self.getSizeInBytesFromType()
        assigns = nlJoin([ "writeStrobe.set_bit(%s, s%s);"
                           % (num, num // bytesOfType)
                           for num in range(0, self.numElems * 4) ])

        write = "%s.write(t, writeStrobe);" % (vn)
        res = nlJoin([strbDecl, strobes, assigns, write])
        return res

    def mkOffset(self, vn, indexExprs):
        linExpr = multAll(self.dims, indexExprs)
        return linExpr

    def addArrayInfo(self, vn, dims):
        pass

    def getAlign(self):
        return self.numElems

    def getOffset(self):
        return 0
