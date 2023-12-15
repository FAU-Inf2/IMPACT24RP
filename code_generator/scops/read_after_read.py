from scop import *
from scop_statement import *

Dom = isl.union_set("[SIZE] -> { S1[i, j] : 0<=i<SIZE and 0<=j<SIZE }")
Sch = isl.union_map("{ S1[i, j] -> O[i, j] }")
SchTilIJ = isl.union_map("""
{ S1[s0, s1] -> O[t0, t1, s0, s1] :
  t0 mod 4 = 0 and t0 <= s0 < t0 + 4 and
  t1 mod 4 = 0 and t1 <= s1 < t1 + 4 }
""")
Write = isl.union_map("{ S1[i, j] -> W[i, j] }")

Read1 = isl.union_map("{ S1[i, j] -> A[0, j] }")
Read2 = isl.union_map("{ S1[i, j] -> A[i mod 2, j/4] }")
Read3 = isl.union_map("{ S1[i, j] -> A[i + 1, i] }")
Read4 = isl.union_map("{ S1[i, j] -> A[0, 4] }")

S1 = mkStatement("S1", Dom, Sch, [Write], [Read2])

RAR = Scop([S1], name = "RAR")
