import isl

class AstVisitor():
    def dispatch(self, n):
        # print("Dispatch. type(n) = ", type(n))
        if isinstance(n, isl.ast_node_for):
            return self.visitFor(n)
        if isinstance(n, isl.ast_node_list):
            return self.visitList(n)
        if isinstance(n, isl.ast_node_user):
            return self.visitUser(n)
        if isinstance(n, isl.ast_node_mark):
            return self.visitMark(n)
        if isinstance(n, isl.ast_node_if):
            return self.visitIf(n)
        if isinstance(n, isl.ast_node_block):
            return self.visitBlock(n)
        if isinstance(n, isl.ast_expr_op_add):
            return self.visitExprBinop(n, "+")
        if isinstance(n, isl.ast_expr_op_address_of):
            return self.visitExprUnop(n, "&")
        if isinstance(n, isl.ast_expr_op_and):
            return self.visitExprBinop(n, "&&")
        if isinstance(n, isl.ast_expr_op_and_then):
            return self.visitExprBinop(n, "&->&")
        if isinstance(n, isl.ast_expr_op_call):
            return self.visitExprOpCall(n)
        if isinstance(n, isl.ast_expr_op_cond):
            return self.visitExprOpCond(n)
        if isinstance(n, isl.ast_expr_op_div):
            return self.visitExprBinop(n, "/")
        if isinstance(n, isl.ast_expr_op_eq):
            return self.visitExprBinop(n, "==")
        if isinstance(n, isl.ast_expr_op_or):
            return self.visitExprBinop(n, "||")
        if isinstance(n, isl.ast_expr_op_or_else):
            return self.visitExprBinop(n, "|->|")
        if isinstance(n, isl.ast_expr_op_ge):
            return self.visitExprBinop(n, ">=")
        if isinstance(n, isl.ast_expr_op_gt):
            return self.visitExprBinop(n, ">")
        if isinstance(n, isl.ast_expr_op_le):
            return self.visitExprBinop(n, "<=")
        if isinstance(n, isl.ast_expr_op_lt):
            return self.visitExprBinop(n, "<")
        if isinstance(n, isl.ast_expr_op_max):
            return self.visitExprOpMax(n)
        if isinstance(n, isl.ast_expr_op_min):
            return self.visitExprOpMin(n)
        if isinstance(n, isl.ast_expr_op_minus):
            return self.visitExprUnop(n, "-")
        if isinstance(n, isl.ast_expr_op_mul):
            return self.visitExprBinop(n, "*")
        if isinstance(n, isl.ast_expr_op_sub):
            return self.visitExprBinop(n, "-")
        if isinstance(n, isl.ast_expr_op_zdiv_r):
            return self.visitExprBinop(n, "%")
        if isinstance(n, isl.ast_expr_int):
            return self.visitExprInt(n)
        if isinstance(n, isl.ast_expr_id):
            return self.visitExprId(n)
        if isinstance(n, isl.ast_expr_op_pdiv_r):
            return self.visitExprBinop(n, "%")
        if isinstance(n, isl.ast_expr_op_fdiv_q):
            return self.visitExprBinop(n, "floord")

        raise Exception("Unimplemented Path: ", type(n))

    def dispatchOpList(self, n, off = 0):
        res = [ self.dispatch(n.get_arg(i)) for i in range(off, n.n_arg()) ]
        return res

    def beforeChild(self, n): return
    def afterChild(self, n): return
    def do(self, n): return self.dispatch(n)

    def visitOperandChilds(self, n):
        for i in range(0, n.n_arg()):
            arg = n.get_arg(i)
            self.beforeChild(arg)
            self.dispatch(arg)
            self.afterChild(arg)

    def visitChild(self, n):
        self.beforeChild(n)
        self.dispatch(n)
        self.afterChild(n)

    def prolog(self, n): return
    def epilog(self, n): return

    def visitExprId(self, n):
        self.prolog(n)
        self.epilog(n)

    def visitExprInt(self,n):
        self.prolog(n)
        self.epilog(n)

    def visitExprOpCall(self,n):
        self.prolog(n)
        self.visitOperandChilds(n)
        self.epilog(n)

    def visitExprOpAccess(self, n):
        self.prolog(n)
        self.visitOperandChilds(n)
        self.epilog(n)

    def visitExprBinop(self, n, operand):
        self.prolog(n)
        self.visitOperandChilds(n)
        self.epilog(n)

    def visitExprUnop(self, n, operator):
        self.prolog(n)
        self.visitOperandChilds(n)
        self.epilog(n)

    def visitExprOpMax(self, n):
        self.prolog(n)
        self.visitOperandChilds(n)
        self.epilog(n)

    def visitExprOpMember(self, n):
        self.prolog(n)
        self.visitOperandChilds(n)
        self.epilog(n)

    def visitExprOpMin(self, n):
        self.prolog(n)
        self.visitOperandChilds(n)
        self.epilog(n)

    def visitExprOpSelect(self, n):
        self.prolog(n)
        self.visitOperandChilds(n)
        self.epilog(n)

    def visitExprOpZdivr(self, n):
        self.prolog(n)
        self.visitOperandChilds(n)
        self.epilog(n)

    def visitFor(self, n):
        self.prolog(n)
        self.visitChild(n.get_iterator())
        self.visitChild(n.get_init())
        self.visitChild(n.get_cond())
        self.visitChild(n.get_inc())
        self.visitChild(n.get_body())
        self.epilog(n)

    def visitList(self, n):
        self.prolog(n)
        for i in range(0, n.size()):
            self.visitChild(n.at(i))
        self.epilog(n)

    def visitUser(self, n):
        self.prolog(n)
        # raise Exception("Unimplemented")
        self.visitChild(n.get_expr())
        self.epilog(n)

    def visitMark(self, n):
        self.prolog(n)
        raise Exception("Unimplemented")
        self.epilog(n)

    def visitIf(self, n):
        self.prolog(n)
        self.visitChild(n.get_cond())
        self.visitChild(n.get_then_node())
        if n.has_else_node():
            self.visitChild(n.get_else_node())
        self.epilog(n)

    def visitBlock(self, n):
        self.prolog(n)
        self.visitChild(n.get_children())
        self.epilog(n)
