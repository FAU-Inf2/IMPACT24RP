from card_visitor.base_visitor import *

class PrettyPrintVisitor(CardVisitor):
    def visitTwRelOp(self, n):
        return "(%s %s %s %s %s)" % (
            self.dispatch(n[0]), n[1], self.dispatch(n[2]),
            n[3], self.dispatch(n[4])
        )

    def visitBinop(self, n):
        return "(%s %s %s)" % (self.dispatch(n[0]), n[1], self.dispatch(n[2]))

    def visitId(self, n):
        return n

    def visitInt(self, n):
        return str(n)

    def visitEntry(self, n):
        return self.dispatch(n[0]) + " : " + self.dispatch(n[1])

    def visitFunc(self, n):
        return "func"

    def do(self, n):
        return "; ".join(self.visitEntry(s) for s in n)
