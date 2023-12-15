import isl

from util import *
from isl_util import *

def mkExpander(inpSet, num):
    if inpSet.is_empty():
        return isl.union_map("{}")
    tupId = getSetTupleId(inpSet)
    nDims = assureSet(inpSet).n_dim()
    pstrs = [ "i%s" % (n) for n in range(0, nDims) ]
    last = pstrs[-1]
    p0 = cmJoin(pstrs)
    p1 = cmJoin(pstrs[0:-1] + ["vv"])
    constr = "%s <= vv < %s + %s" % (last, last, num)
    mapStr = "{ %s[%s] -> %s[%s] : %s }" % (tupId, p0, tupId, p1, constr)
    # print(mapStr)
    return isl.map(mapStr)

# { A[i, j] -> A[i, (floor((j - off) / 4) * 4) + off] }
def mkAligner(inpSet, num, offset = 0):
    print(inpSet)
    print(inpSet.is_empty())
    if inpSet.is_empty():
        return isl.union_map("{}")
    # assert(not inpSet.is_empty())
    tupId = getSetTupleId(inpSet)
    nDims = assureSet(inpSet).n_dim()
    pStrs = [ "i%s" % (n) for n in range(0, nDims) ]
    last = pStrs[-1]
    p0 = cmJoin(pStrs)
    p1 = cmJoin(pStrs[0:-1]
                + ["(floor((%s - %s) / %s) * %s) + %s"
                   % (last, offset, num, num, offset)])
    mapStr = "{ %s[%s] -> %s[%s] }" % (tupId, p0, tupId, p1)
    m = isl.map(mapStr)
    return isl.map(mapStr)
