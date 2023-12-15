from scop_statement import *
from scop import *

stmt = (
    ScopStatement("stmt")
    .addDomain("[S] -> { S[i, j, k] : 1 <= i < S - 1 and 1 <= j < S - 1 and 1 <= k < S - 1 }")
    .addSchedule("{ S[i, j, k] -> O[i, 0, j, 0, k, 0] }")
    .addDomAnonymizer("{ S[i, j, k] -> [i, j, k] }")
    .addRead("{ S[i, j, k] -> P[i, j] }", "r0")
    .addRead("{ S[i, j, k] -> Q[i, j] }", "r1")
    .addRead("{ S[i, j, k] -> V[j+32, i] }", "r2")
    .addRead("{ S[i, j, k] -> A[i, j, k] }", "r3")
    .addRead("{ S[i, j, k] -> A[i, j+1, k] }", "r4")
    .addWrite("{ S[i, j, k] -> V[j, i] }", "w0")
    .addDfg("w0 = r0 + r1 + r2 + r3 + r4;")
)

scop = (
    Scop()
    .addStmt(stmt)
    .addName("runex2")
    .addArrayInfos({ "P": ["S", "S"], "Q": ["S", "S"],
                     "V": ["S", "S"], "A": ["S", "S", "S"]})
    .addTypeInfos({ "S": "int" })
)

#
# Hier ist noch einiges zu tun, irgendwie
# scheint mein Code-Generator die Reads und writes
# an die falsche Stelle zu packen. Zumindest sieht
# es so aus.
#
