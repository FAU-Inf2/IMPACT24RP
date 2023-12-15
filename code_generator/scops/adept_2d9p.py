from scop import *
from scop_statement import *

Stmt = (
    ScopStatement("S1")
    .addDomain("[SIZE] -> { S1[i, j] : 1 <= i < SIZE - 1 and 1 <= j < SIZE - 1 }")
    .addSchedule("{ S1[i, j] -> O[i, 0, j, 0] }")
    .addDomAnonymizer("{ S1[i, j] -> [i, j] }")
    .addRead("{ S1[i, j] -> A[i    , j + 1] }", "r0")
    .addRead("{ S1[i, j] -> A[i + 1, j + 1] }", "r1")
    .addRead("{ S1[i, j] -> A[i + 1,     j] }", "r2")
    .addRead("{ S1[i, j] -> A[i + 1, j - 1] }", "r3")
    .addRead("{ S1[i, j] -> A[i    , j - 1] }", "r4")
    .addRead("{ S1[i, j] -> A[i - 1, j - 1] }", "r5")
    .addRead("{ S1[i, j] -> A[i - 1, j    ] }", "r6")
    .addRead("{ S1[i, j] -> A[i - 1, j + 1] }", "r7")
    .addWrite("{ S1[i, j] -> X[i, j] }", "w0")
    .addDfg("w0 = (r0 + r1 + r2 + r3 + r4 + r5 + r6 + r7) * fac;")
)

TypeInfos = { "SIZE": "int", "fac": "float" }
ArrayInfos = { "A": ["SIZE", "SIZE"], "X": ["SIZE", "SIZE"] }

scop = (Scop()
        .addStmt(Stmt)
        .addName("adept2d9p")
        .addTypeInfos(TypeInfos)
        .addArrayInfos(ArrayInfos))
