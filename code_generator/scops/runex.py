from scop_statement import *
from scop import *

stmt = (
    ScopStatement("S")
    .addDomain("[SZ] -> { S[i, j, k] : 1 <= i < SZ and 1 <= j < SZ and 1 <= k < SZ }")
    .addSchedule("{ S[i, j, k] -> O[i, 0, j, 0, k, 0] }")
    .addDomAnonymizer("{ S[i, j, k] -> [i, j, k] }")
    .addRead("{ S[i, j, k] -> A[i, j, k] }", "r0")
    .addRead("{ S[i, j, k] -> A[i+1, j, k+1] }", "r1")
    .addRead("{ S[i, j, k] -> A[j, i, k] }", "r2")
    .addRead("{ S[i, j, k] -> A[2i, j, k] }", "r3")
    .addRead("{ S[i, j, k] -> U[k, j] }", "r4")
    .addRead("{ S[i, j, k] -> U[k+1, j] }", "r5")
    .addRead("{ S[i, j, k] -> B[i, j, k+1] }", "r6")
    .addRead("{ S[i, j, k] -> B[2i, j, k] }", "r7")
    .addWrite("{ S[i, j, k] -> B[i, j, k] }", "w0")
    .addDfg("w0 = r0+r1+r2+r3+r4+r5+r6+r7")
)

scop = (
    Scop()
    .addName("runex")
    .addStmt(stmt)
    .addArrayInfos({ "A": ["SZ", "SZ", "SZ"], "U": ["SZ", "SZ"], "B": ["SZ", "SZ", "SZ"]})
    .addTypeInfos({ "SZ": "int" })
)
