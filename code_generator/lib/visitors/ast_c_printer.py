import isl

from util import *
from isl_util import *
from visitors.indentable import *
from visitors.precedence import *
from visitors.base_visitor import *

class AstCPrinter(AstVisitor, Indentable):
    def visitExprId(self, n):
        return str(n.get_id())

    def visitExprInt(self, n):
        return str(n.get_val())

    def visitExprOpAccess(self, n):
        return "* %s" % (self.dispatch(n.get_arg(0)))

    def visitExprBinop(self, n, op):
        if op == "floord":
            return self.visitExprBinopFdiv(n, op)

        return self.visitExprBinopDefault(n, op)

    def visitExprBinopFdiv(self, n, op):
        lhs = self.dispatch(n.get_arg(0))
        rhs = self.dispatch(n.get_arg(1))
        return "floord(%s, %s)" % (lhs, rhs)

    def visitExprBinopDefault(self, n, op):
        lhs = n.get_arg(0)
        rhs = n.get_arg(1)

        lhsTmpl = "(%s)" if isExp(lhs) and isLargerPrec(lhs, n) else "%s"
        rhsTmpl = "(%s)" if isExp(rhs) and isLargerPrec(rhs, n) else "%s"
        return (lhsTmpl + " %s " + rhsTmpl) % (
            self.dispatch(n.get_arg(0)), op, self.dispatch(n.get_arg(1)))

    def visitExprUnop(self, n, operator):
        return "%s %s" % (operator, self.dispatch(n.get_arg(0)))

    def visitExprOpCall(self, n):
        return ("%s(%s);" % (str(n.get_arg(0).get_id()),
                             ", ".join(self.dispatchOpList(n, 1))))

    def visitExprOpMin(self, n):
        return "min(%s)" % (", ".join(self.dispatchOpList(n)))

    def visitExprOpMax(self, n):
        return "max(%s)" % (", ".join(self.dispatchOpList(n)))

    def visitExprOpMember(self, n):
        raise Exception("Unimplemented")

    def visitExprOpSelect(self, n):
        raise Exception("Unimplemented")

    def visitIf(self, n):
        condStr = self.dispatch(n.get_cond())
        cond = "%sif (%s) {\n" % (self.indent(), condStr)
        self.inc()
        then = self.dispatch(n.get_then_node()) + "\n"
        self.dec()
        then_ = "%s}" % (self.indent())

        if n.has_else_node():
            els = "else {\n"
            self.inc()
            enode = self.dispatch(n.get_else_node()) + "\n"
            self.dec()
            end = "%s}\n" % (self.indent())
            return cond + then + then_ + els + enode + end
        return cond + then + then_

    def visitFor(self, n):
        iterator = self.dispatch(n.get_iterator())
        initStr = self.dispatch(n.get_init())
        condStr = self.dispatch(n.get_cond())
        incStr = self.dispatch(n.get_inc())
        head = "%sfor (int %s = %s; %s; %s += %s) {\n" % (
            self.indent(), iterator, initStr, condStr, iterator, incStr)
        self.inc()
        body = self.dispatch(n.get_body()) + "\n"
        self.dec()
        lst = "%s}" % (self.indent())
        return head + body + lst

    def visitBlock(self, n):
        fst = "%s{\n" % (self.indent())
        self.inc()
        mid = self.dispatch(n.get_children()) + "\n"
        self.dec()
        lst = "%s}\n" % (self.indent())
        return fst + mid + lst

    def visitMark(self, n):
        raise Expression("unimplemented")

    def visitList(self, n):
        return eJoin([ self.dispatch(n.at(i)) for i in range(0, n.size() )])

    def visitUser(self, n):
        return "%s%s" % (self.indent(), self.dispatch(n.get_expr()))
