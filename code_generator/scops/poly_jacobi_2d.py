from scop import *
from scop_statement import *

Stmt = (ScopStatement("S")
        .addDomain("[SIZE] -> { S[i, j] : 1 <= i < SIZE - 1 and 1 <= j < SIZE - 1 }")
        .addDomAnonymizer("{ S[i, j] -> [i, j] }")
        .addSchedule("{ S[i, j] -> O[i, 0, j, 0] }")
        .addRead("{ S[i, j] -> A[i, j] }",   "r0")
        .addRead("{ S[i, j] -> A[i, j-1] }", "r1")
        .addRead("{ S[i, j] -> A[i, 1+j] }", "r2")
        .addRead("{ S[i, j] -> A[1+i, j] }", "r3")
        .addRead("{ S[i, j] -> A[i-1, j] }", "r4")
        .addWrite("{ S[i, j] -> B[i, j] }", "w0")
        .addDfg("w0 = 0.2 * (r0 + r1 + r2 + r3 + r4);")
        )

scop = (
    Scop()
    .addStmt(Stmt)
    .addName("poly_jacobi_2d")
    .addArrayInfos({ "A": ["SIZE", "SIZE"], "B": ["SIZE", "SIZE"] })
    .addTypeInfos({ "SIZE": "int" })
)
