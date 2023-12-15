from scop import *
from scop_statement import *

D_S = "[N] -> { S[j, i] : 1 <= j < N and 1 <= i < N }"
D_Anon = "{ S[i, j] -> [i, j] }"
Sched_S = "{ S[j, i] -> O[j, i] }"

R1 = "{ S[j, i] -> total[i] }"
W = "{ S[j, i] -> total[i] }"
# R2 = ("{ S[j, i] -> A[i, j] }"

S1 = mkStatement("S1", D_S, Sched_S, [W], [R1], D_Anon)

RAR2 = Scop([S1], name = "RAR2")
