from scop import *
from scop_statement import *

Stmt = (ScopStatement("S")
        .addDomain("[SIZE] -> { S[i] : 1 <= i < SIZE - 1 }")
        .addDomAnonymizer("{ S[i] -> [i] }")
        .addSchedule("{ S[i] -> O[i, 0] }")
        .addRead("{ S[i] -> A[i - 1] }", "r0")
        .addRead("{ S[i] -> A[i] }", "r1")
        .addRead("{ S[i] -> A[i + 1] }", "r2")
        .addWrite("{ S[i] -> B[i] }", "w0")
        .addDfg("w0 = 0.33333 * (r0 + r1 + r2);")
        )

scop = (
    Scop()
    .addStmt(Stmt)
    .addName("poly_jacobi_1d")
    .addArrayInfos({ "A": ["SIZE"], "B": ["SIZE"] })
    .addTypeInfos({ "SIZE": "int" })
)
