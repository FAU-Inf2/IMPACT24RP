from scop_statement import *
from scop import *

stmt = (
    ScopStatement("stmt")
    .addDomain("[S] -> { S[i, j, k, l] : 1 <= i < S - 1 and 1 <= j < S - 1 and 1 <= k < S - 1 and 1 <= l < S - 1 }")
    .addSchedule("{ S[i, j, k, l] -> O[i, 0, j, 0, k, 0, l, 0] }")
    .addDomAnonymizer("{ S[i, j, k, l] -> [i, j, k, l] }")
    .addRead("{ S[i, j, k, l] -> A[i, j, k, l] }", "r3")
    .addRead("{ S[i, j, k, l] -> A[i+1, j+1, k+1, l+1] }", "r4")
    .addRead("{ S[i, j, k, l] -> V[i, k, j, l] }", "r2")
    .addWrite("{ S[i, j, k, l] -> V[i, k, j, l] }", "w0")
    .addDfg("w0 = r2 + r3 + r4;")
)

scop = (
    Scop()
    .addStmt(stmt)
    .addName("runex4")
    .addArrayInfos({ "V": ["S", "S", "S", "S"], "A": ["S", "S", "S", "S"]})
    .addTypeInfos({ "S": "int" })
)
