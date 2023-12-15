from scop_statement import *
from scop import *

S7 = (
    ScopStatement("S7")
    .addDomain("[SIZE] -> { S7[i, j] : 1 <= i < SIZE - 1 and 1 <= j <= SIZE - 2 }")
    .addSchedule("{ S7[i, j] -> O[i, 0, -j, 0] }")
    .addDomAnonymizer("{ S7[i, j] -> [i, j] }")
    .addRead("{ S7[i, j] -> P[i, j] }", "r0")
    .addRead("{ S7[i, j] -> Q[i, j] }", "r1")
    .addRead("{ S7[i, j] -> V[j + 1, i] }", "r2")
    .addWrite("{ S7[i, j] -> V[j][i] }", "w0")
    .addDfg("w0 = r0 * r2 + r1;")
)

scop = (
    Scop()
    .addStmt(S7)
    .addName("adi")
    .addTypeInfos({ "SIZE" : "int" })
    .addArrayInfos({ "V" : ["SIZE", "SIZE"],
                     "P": ["SIZE", "SIZE"],
                     "Q": ["SIZE", "SIZE"] })
)
