from ports.p_vla import *
from ports.p_lin import *
from ports.p_burst import *

def isBurstMaxi(x):
    return isinstance(x, BurstMaxi)

class PortMapper:
    def __init__(self):
        self.portMap = {}

    def addCacheArray(self, arrName, dims, padding, ty = "float"):
        self.portMap[arrName] = VarLengthCacheArray(0, ty, dims, padding)

    def isPortBurst(self, vn):
        return isinstance(self.portMap[vn], BurstMaxi)

    def containsBurstMaxiPorts(self):
        return all(map(isBurstMaxi, self.portMap.values()))

    def getAllBurstPorts(self):
        return filter(isBurstMaxi, self.portMap.values())

    def getIncls(self):
        if self.containsBurstMaxiPorts():
            return ["orka_hls.h"]
        else:
            return []

    def genStruct(self):
        allBurstPorts = self.getAllBurstPorts()
        ga = lambda x: x.getAlign()
        alignments = set(map(ga, allBurstPorts))

        result = ""
        for al in alignments:
            members = [ "%s e%s;" % ("float", num) for num in range(0, al) ]
            membersStr = nlJoin(members)
            result += "struct %s%s " % ("AxiVec", al)
            result += "{"
            result += "%s" % (membersStr)
            result += "using value_type = float;"
            result += "};"
            result += NL * 2
        return result

    def genStructName(self):
        return "AxiVec"

    def mkVarDecl(self, vn):
        needle = self.portMap[vn]
        return needle.mkVarDecl(vn)

    def mkLoad(self, vn, idx, offset = 0):
        return self.portMap[vn].mkLoad(vn, idx, offset)

    def mkStore(self, vn, idx, offset = 0):
        return self.portMap[vn].mkStore(vn, idx, offset)

    def mkOffset(self, vn, idx):
        return self.portMap[vn].mkOffset(vn, idx)

    def getAlign(self, vn):
        return self.portMap[vn].getAlign()

    def getOffset(self, vn):
        return self.portMap[vn].getOffset()

class BurstMaxiDefaultPorts(PortMapper):
    def __init__(self, scop):
        super(BurstMaxiDefaultPorts, self).__init__()
        arrInfos = scop.getArrayInfos()
        align = scop.getAlInfos()
        for k, dims in arrInfos.items():
            al = align.getAlignment(k)
            self.portMap[k] = BurstMaxi(al, "float", dims)

class VarLengthDefaultPorts(PortMapper):
    def __init__(self, scop):
        super(VarLengthDefaultPorts, self).__init__()
        arrInfos = scop.getArrayInfos()
        align = scop.getAlInfos()
        for k, dims in arrInfos.items():
            al = align.getAlignment(k)
            self.portMap[k] = VarLengthArray(al, "float", dims)

class LinearizedDefaultPorts(PortMapper):
    def __init__(self, scop):
        super(LinearizedDefaultPorts, self).__init__()
        arrInfos = scop.getArrayInfos()
        align = scop.getAlInfos()
        for k, dims in arrInfos.items():
            al = align.getAlignment(k)
            self.portMap[k] = LinearizedPtrAcc(al, "float", dims)
