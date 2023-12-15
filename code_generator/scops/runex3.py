from scop_statement import *
from scop import *

stmt = (
    ScopStatement("stmt")
    .addDomain("[S] -> { S[i, j, k] : 1 <= i < S - 1 and 1 <= j < S - 1 and 1 <= k < S - 1 }")
    .addSchedule("{ S[i, j, k] -> O[i, 0, j, 0, k, 0] }")
    .addDomAnonymizer("{ S[i, j, k] -> [i, j, k] }")
    .addRead("{ S[i, j, k] -> P[i, j, k] }", "r0")
    .addRead("{ S[i, j, k] -> V[i, k, j] }", "r2")
    .addRead("{ S[i, j, k] -> A[i, j, k] }", "r3")
    .addRead("{ S[i, j, k] -> A[i+1, j+1, k+1] }", "r4")
    .addWrite("{ S[i, j, k] -> V[i, k, j] }", "w0")
    .addDfg("w0 = r0 + r2 + r3 + r4;")
)

scop = (
    Scop()
    .addStmt(stmt)
    .addName("runex2")
    .addArrayInfos({ "P": ["S", "S", "S"], "V": ["S", "S", "S"], "A": ["S", "S", "S"]})
    .addTypeInfos({ "S": "int" })
)
