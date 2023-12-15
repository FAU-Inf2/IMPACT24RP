from scop import *
from scop_statement import *

Stmt = (ScopStatement("S")
        .addDomain("[SIZEX, SIZEY] -> { S[i, j] : 0 <= i < SIZEX - 1 and 0 <= j < SIZEY - 1 }")
        .addDomAnonymizer("{ S[i, j] -> [i, j] }")
        .addSchedule("{ S[i, j] -> O[i, 0, j, 0] }")
        .addWrite("{ S[i, j] -> HZ[i, j] }",   "w0")
        .addRead("{ S[i, j] -> HZ[i, j] }", "r0")
        .addRead("{ S[i, j] -> EX[i, j+1] }", "r1")
        .addRead("{ S[i, j] -> EX[i, j] }", "r2")
        .addRead("{ S[i, j] -> EY[i+1, j] }", "r3")
        .addRead("{ S[i, j] -> EY[i, j] }", "r4")
        .addDfg("w0 = r0 - 0.7 * (r1 - r2 + r3 - r4);")
        )

scop = (
    Scop()
    .addStmt(Stmt)
    .addName("poly_fdtd2")
    .addArrayInfos({ "EX": ["SIZEX", "SIZEY"], "HZ": ["SIZEX", "SIZEY"], "EY": ["SIZEX", "SIZEY"] })
    .addTypeInfos({ "SIZEY": "int", "SIZEX": "int" })
)
