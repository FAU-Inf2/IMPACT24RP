from util import *

from card_visitor.base_visitor import *

class CondAssignGen(CardVisitor):
    def visitTwRelOp(self, n):
        lhs = self.dispatch(n[0])
        lop = n[1]
        mhs = self.dispatch(n[2])
        rop = n[3]
        rhs = self.dispatch(n[4])
        return "(%s %s %s && %s %s %s)" % (lhs, lop, mhs, mhs, rop, rhs)

    def __init__(self, dest, transMap):
        self.dest = dest
        self.transMap = transMap

    def visitBinop(self, n):
        op = n[1]
        if op == "and":
            op = "&&"
        if op == "mod":
            op = "%"
        if op == "=":
            op = "=="
        if op == "^":
            return "(exp(%s, %s))" % (self.dispatch(n[0]), self.dispatch(n[2]))
        return "(%s %s %s)" % (self.dispatch(n[0]), op, self.dispatch(n[2]))

    def visitUnop(self, n):
        op = n[0]
        return "(%s %s)" % (op, self.dispatch(n[1]))

    def visitId(self, n):
        if n in self.transMap.keys():
            return self.transMap[n]
        else:
            return n

    def visitInt(self, n):
        return str(n)

    def visitEntry(self, n):
        bdy = self.dispatch(n[0])
        cond = self.dispatch(n[1][0]) if n[1] != [] else "1"
        res = "if (%s) { %s = %s; }" % (cond, self.dest, bdy)
        return res

    # [X, Y] -> { 32 }
    def visitOneEntryNoCond(self, n):
        res = "const int %s = %s;" % (self.dest, self.dispatch(n[0]))
        return res

    # [X, Y] -> {  }
    def visitNoEntryNoCond(self):
        res = "const int %s = 0;" % (self.dest)
        return res

    def oneEntryNoCond(self, n):
        # there is only one entry
        if len(n) == 1:
            # ... and the entry has no condition
            # (which then implies true)
            if n[0][1] == []:
                return True
        return False

    def noEntryNoCond(self, n):
        # print("noEntryNocond:", n)
        # there is no entry (which implies the value 0)
        if len(n) == 0:
            return True
        return False

    def do(self, n):
        if self.oneEntryNoCond(n):
            return self.visitOneEntryNoCond(n[0])
        if self.noEntryNoCond(n):
            return self.visitNoEntryNoCond()

        res = "int %s = 0;" % (self.dest)
        res = nlJoin([res] + [self.visitEntry(s) for s in n])
        return res
