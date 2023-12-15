from search_tile import *

def variations(L, n):
    if (n == 0):
        return [[]]
    tp = variations(L, n - 1)
    res = [ t + [y] for y in L for t in tp if y not in t ]
    return res

def sortedVar(L, n):
    stage = []
    vars = sorted(variations(L, n))
    for var in vars:
        stage.append(sorted(var))

    res = []
    for s in stage:
        if s not in res:
            res.append(s)

    return sorted(res)

