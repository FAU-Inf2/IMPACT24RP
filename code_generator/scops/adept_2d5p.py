from scop import *
from scop_statement import *

S1 = (
    ScopStatement("S1")
    .addDomain("[SIZE] -> { S1[i, j] : 1 <= i < SIZE - 1 and 1 <= j < SIZE - 1 }")
    .addSchedule("{ S1[i, j] -> O[i, 0, j, 0] }")
    .addDomAnonymizer("{ S1[i, j] -> [i, j] }")
    .addRead("{ S1[i, j] -> A[i - 1, j] }", "r0")
    .addRead("{ S1[i, j] -> A[i + 1, j] }", "r1")
    .addRead("{ S1[i, j] -> A[i, j + 1] }", "r2")
    .addRead("{ S1[i, j] -> A[i, j - 1] }", "r3")
    .addWrite("{ S1[i, j] -> X[i, j] }", "w0")
    .addDfg("w0 = (r0 + r1 + r2 + r3) * fac;")
)

TypeInfos = { "SIZE" : "int", "fac": "float" }
ArrayInfos = { "A": ["SIZE", "SIZE"], "X": ["SIZE", "SIZE"] }

scop = (Scop()
        .addStmt(S1)
        .addName("adept2d5p")
        .addTypeInfos(TypeInfos)
        .addArrayInfos(ArrayInfos))
