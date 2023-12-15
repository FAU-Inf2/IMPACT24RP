import isl

precedenceMap = {
    isl.ast_expr_op_add: 6,
    isl.ast_expr_op_address_of: 3,
    isl.ast_expr_op_and: 14,
    isl.ast_expr_op_and_then: 14,
    isl.ast_expr_op_call: 2,
    isl.ast_expr_op_cond: 16,
    isl.ast_expr_op_div: 5,
    isl.ast_expr_op_eq: 10,
    isl.ast_expr_op_fdiv_q: 5,
    isl.ast_expr_op_ge: 9,
    isl.ast_expr_op_gt: 9,
    isl.ast_expr_op_le: 9,
    isl.ast_expr_op_lt: 9,
    isl.ast_expr_op_max: 2,
    isl.ast_expr_op_min: 2,
    isl.ast_expr_op_member: 2,
    isl.ast_expr_op_minus: 6,
    isl.ast_expr_op_mul: 5,
    isl.ast_expr_op_or: 15,
    isl.ast_expr_op_or_else: 15,
    isl.ast_expr_op_pdiv_q: 5,
    isl.ast_expr_op_pdiv_r: 5,
    isl.ast_expr_op_select: 2,
    isl.ast_expr_op_sub: 6,
    isl.ast_expr_op_zdiv_r: 5
}

def isLowerPrec(l, r):
    return precedenceMap[type(l)] < precedenceMap[type(r)]

def isLargerPrec(l, r):
    return precedenceMap[type(l)] > precedenceMap[type(r)]
