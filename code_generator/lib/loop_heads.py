import isl

class LoopHead():
    def __init__(self, ast, iterator, init, cond, inc):
        self.ast = ast
        self.iterator = iterator
        self.init = init
        self.cond = cond
        self.inc = inc

    def __repr__(self):
        return self.getAsC()

    def getAstNode(self):
        return self.ast

    def getIterAsStr(self):
        return self.iterator.to_C_str()

    def getNumIterId(self):
        return "numIter%s" % (self.getIterAsStr())

    def getUpperBoundId(self):
        return "upperBound%s" % (self.getIterAsStr())

    def isCondLe(self):
        return isinstance(self.cond, isl.ast_expr_op_le)

    def isCondLt(self):
        return isinstance(self.cond, isl.ast_expr_op_lt)

    def getCond(self):
        return self.cond

    def getUpperBound(self):
        if self.isCondLe() or self.isCondLt():
            return self.cond.get_arg(1)
        raise Exception("Invalid upper bound: " + self.cond.to_C_str())

    def getLowerBound(self):
        if self.isCondLe() or self.isCondLt():
            return self.cond.get_arg(0)
        raise Exception("Invalid upper bound: " + self.cond.to_C_str())

    def getNumIterStr(self):
        return "const int %s = %s - %s;" % (
            self.getNumIterId(), self.cond.get_arg(1).to_C_str(),
            self.init.to_C_str())

    def getNewUb(self, blockSize):
        return "const int %s = ( %s / %s ) * %s + %s;" % (
            self.getUpperBoundId(), self.getNumIterId(),
            str(blockSize), str(blockSize), self.init.to_C_str()
        )

    def getAsC(self, condStr = None, initStr = None, incStr = None):
        init = initStr if initStr else self.init.to_C_str()
        initStr = "int %s = %s" % (
            self.iterator.to_C_str(),
            init
        )
        cond = condStr if condStr else self.cond.to_C_str()
        incNum = incStr if incStr else self.inc.to_C_str()
        inc = "%s += %s" % (self.iterator.to_C_str(), incNum)
        return "for(%s; %s; %s)" % (initStr, cond, inc)

class LoopHeads:
    def __init__(self, partition):
        ast = partition.genAst()
        #print(ast.to_C_str())
        #exit(1)
        fstNode = ast.to_list().at(0)
        loopHeads = getLoopChain(fstNode)
        tilingLevel = partition.getTiling().getTilingLevel()
        self.tlfLoops = loopHeads[:-tilingLevel]
        self.chunkLoops = loopHeads[-tilingLevel:]

    def getTlfIters(self):
        return [ tl.getIterAsStr() for tl in self.getTlfLoops() ]

    def getChunkIters(self):
        return [ c.getIterAsStr() for c in self.getChunkLoops() ]

    def getTlfLoops(self):
        return self.tlfLoops

    def getChunkLoops(self):
        return self.chunkLoops


def getLoopChain(ast):
    if isinstance(ast, isl.ast_node_if):
        return getLoopChain(ast.get_then_node())

    if isinstance(ast, isl.ast_node_for):
        # print(type(ast))
        return [ LoopHead(ast, ast.get_iterator(), ast.get_init(),
                          ast.get_cond(), ast.get_inc())
                ] + getLoopChain(ast.get_body())
    else:
        # print(type(ast))
        return []
