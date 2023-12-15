from codegen.common import *
from codegen.backend import *

from visitors.ast_c_printer import *

class NormalLoopGenerator(AstCPrinter):
    def __init__(self, partition, portMap):
        super(AstCPrinter, self).__init__()
        self.portMap = portMap
        self.partition = partition

    def do(self, ast):
        return self.dispatch(ast)

    def visitExprOpCall(self, n):
        arrayIndices = self.dispatchOpList(n, 1)
        og = self.partition.getOverlapGraph()
        name = n.get_arg(0).get_id().get_name()
        stmt = self.partition.getStmtByName(name)
        dfg = stmt.getDfg()
        # print(dfg)
        dfgArrRefs = stmt.getDfgArrRefs()
        for ar in dfgArrRefs:
            acc = stmt.getAccessByArrRef(ar)
            accDims = acc.getNumArrDim()
            arrName = acc.getArrName()
            offsetInAccTpl = self.partition.getOffsetInAccessTuple(stmt, ar)
            indexSlice = arrayIndices[offsetInAccTpl:offsetInAccTpl+accDims]
            load = self.portMap.mkLoad(arrName, indexSlice)
            dfg = dfg.replace(ar, load)

        res = dfg + "\n"
        return res

class NormalCodeGen(CodeGenBackend):
    def __init__(self, scop, portMap, partitions, name):
        super(NormalCodeGen, self).__init__(name)
        self.scop = scop
        self.portMap = portMap
        self.partitions = partitions.getAllPartitions()
        self.arrayNames = list(scop.getArrayNames())

    def getTlfParamsStr(self):
        arrayParams = [ self.portMap.mkVarDecl(an) for an in self.arrayNames ]
        otherVars = [ "%s %s" % (v, k) for k, v in self.scop.typeInfos.items() ]
        return cmJoin(otherVars + arrayParams)

    def do(self):
        self.mkCode()
        self.mkHeader()

    def mkHeader(self):
        return self.genHeader(self.genTlfSignature() + ";")

    def genTlfSignature(self):
        return "void tlf_normal(%s)" % (self.getTlfParamsStr())

    def mkCode(self):
        self.appendLn(genSysIncludes())
        self.appendLn(genLocalIncludes([self.getHeaderName()]))
        self.appendLn(genIslUtil())
        self.appendLn()
        self.appendLn(self.genTlfSignature() + "{")

        for partition in self.partitions:
            ast = partition.genOrigAst()
            self.appendLn(NormalLoopGenerator(partition, self.portMap).do(ast))

        self.appendLn("}")
