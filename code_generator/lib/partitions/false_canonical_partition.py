from partitions.canonical_partition import *

class FalseCanonicalPartition(CanonicalPartition):
    def __init__(self, stmts, scop):
        super().__init__(stmts, scop)

    def genAst(self):
        assert(False)
        sched = p.getUnionSched()
        AB = isl.ast_build()
        partDom = p.getUnionDom()
        inp = sched.intersect_domain(partDom)
        ast = isl.ast_build.node_from_schedule_map(AB, inp)
        return ast
