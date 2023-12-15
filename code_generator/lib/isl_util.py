import isl
import functools

def unionSetToList(us):
    us = assureUnionSet(us)
    res = []
    us.foreach_set(lambda x: res.append(x))
    return res

def unionMapToList(um):
    um = assureUnionMap(um)
    res = []
    um.foreach_map(lambda x: res.append(x))
    return res

def isSet(s):
    return isinstance(s, isl.set)

def isUnionSet(us):
    return isinstance(us, isl.union_set)

def isMap(m):
    return isinstance(m, isl.map)

def isUnionMap(m):
    return isinstance(m, isl.union_map)

def isExp(l):
    return isinstance(l, isl.ast_expr_op)

# this is a hack as isl does not seem to implement
# the __deepcopy__ methods correctly
def deepCopyUnionSet(us):
    return isl.union_set(str(us))

def deepCopySet(s):
    return isl.set(str(s))

def deepCopyUnionMap(um):
    return isl.union_map(str(um))

def arrow(dom, range):
    return isl.union_map.from_domain_and_range(dom, range)

def ordRel(sched):
    return sched.lex_lt_union_map(sched)

def accRelInSchedSpace(R, S):
    return (R.reverse().apply_range(S).reverse())

def universeRelation(R):
    return isl.union_map.from_domain_and_range(R, R)

def union(L):
    IslUnion = lambda a, b: a.union(b)
    return functools.reduce(IslUnion, L)

def dumpAst(m):
    ab = isl.ast_build()
    ast = isl.ast_build.node_from_schedule_map(ab, m)
    return ast.to_C_str()

def assureUnionSet(o):
    if isinstance(o, isl.set):
        return o.to_union_map()
    if isinstance(o, isl.union_set):
        return o
    raise Exception("s is neither a set nor an union_set")

def assureUnionMap(o):
    if isinstance(o, isl.map):
        return o.to_union_map()
    if isinstance(o, isl.union_map):
        return o
    raise Exception("s is neither a map nor an union_map")

def assureSet(o):
    if isinstance(o, isl.set):
        return o
    if isinstance(o, isl.union_set) and o.isa_set():
        return o.as_set()
    raise Exception("o is not a set: " + o)

def assureMap(o):
    if isinstance(o, isl.map):
        return o
    if isinstance(o, isl.union_map) and o.isa_map():
        return o.as_map()
    raise Exception("o is not a map: " + o)

def getSetTupleId(o):
    o = assureUnionSet(o)
    return o.identity().as_map().space().get_range_tuple_id().get_name()

def getMapRangeTupleName(o):
    o = assureMap(o)
    return o.space().get_range_tuple_id().get_name()

def getAst(box):
    ab = isl.ast_build()
    ast = isl.ast_build.node_from_schedule_map(ab, box)
    return ast

def projectOutLast(s):
    s = assureSet(s)
    toRemove = s.n_dim() - 1
    return s.project_out_set_dims(0, toRemove)

# [3, 2, 1, 0]
def projectOutNth(s, n):
    s = assureSet(s)
    numDims = s.n_dim()
    n = numDims -1 - n
    skipBefore = numDims - (numDims - n)
    s = s.project_out_set_dims(0, skipBefore)
    skipAfter = (numDims - skipBefore) - 1
    s = s.project_out_set_dims(1, skipAfter)
    return s

def projectToList(s):
    res = []
    s = assureSet(s)
    for i in range(0, s.n_dim()):
        res.append(projectOutNth(s, i))
    return res

def trivGist(s):
    mi = isl.multi_id("{ [a] }")
    s = s.gist(s.params().unbind_params(mi)).drop_unused_params()
    return s

ISL_ZERO = isl.set("{ [0] }")
