from scop import *
from scop_statement import *

Stmt = (ScopStatement("S")
        .addDomain("[SIZEX, SIZEY] -> { S[i, j] : 1 <= i < SIZEX and 0 <= j < SIZEY  }")
        .addDomAnonymizer("{ S[i, j] -> [i, j] }")
        .addSchedule("{ S[i, j] -> O[i, 0, j, 0] }")
        .addWrite("{ S[i, j] -> EY[i, j] }",   "w0")
        .addRead("{ S[i, j] -> EY[i, j] }", "r0")
        .addRead("{ S[i, j] -> HZ[i, j] }", "r1")
        .addRead("{ S[i, j] -> HZ[i-1, j] }", "r2")
        .addDfg("w0 = r0 - 0.5 * (r1 - r2);")
        )

scop = (
    Scop()
    .addStmt(Stmt)
    .addName("poly_fdtd0")
    .addArrayInfos({ "EY": ["SIZEX", "SIZEY"], "HZ": ["SIZEX", "SIZEY"] })
    .addTypeInfos({ "SIZEX": "int", "SIZEY": "int" })
)
