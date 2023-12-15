from partitions.canonical_partition import *
from partitions.true_canonical_partition import *
from partitions.false_canonical_partition import *

class CanonicalPartitions:
    def __init__(self):
        self.partitions = []

    def getAllPartitions(self):
        return self.partitions

    def getTrueCanonStmts(self):
        return [ p for p in self.partitions
                 if isinstance(p, TrueCanonicalPartition) ]

    def isFullyCanonical(self):
        return len(self.getTrueCanonStmts()) == len(self.partitions)

    def addTrueCanonicalStatements(self, stmts, scop):
        ta = TrueCanonicalPartition(stmts, scop)
        self.partitions.insert(0, ta)

    def addTrueCanonicalStatement(self, stmt, scop):
        ta = TrueCanonicalPartition([stmt], scop)
        self.partitions.insert(0, ta)

    def addFalseCanonicalStatements(self, stmts, scop):
        ta = FalseCanonicalPartition(stmts, scop)
        self.partitions.insert(0, ta)

    def dump(self):
        for p in self.partitions:
            print("partition:", p)
            p.dump()
