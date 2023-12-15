
from scop_statement import *
from scop import *


S5 = (
    ScopStatement("S5")
    .addDomain("[SIZE] -> { S5[i, j] : 1 <= i < SIZE - 1 and 1 <= j < SIZE - 1 }")
    .addSchedule("{ S5[i, j] -> O[i, 2, j, 1] }")
    .addDomAnonymizer("{ S5[i, j] -> [i, j] }")
    .addRead("{ S5[i, j] -> U[j, i - 1] }", "r0")
    .addRead("{ S5[i, j] -> U[j, i] }", "r1")
    .addRead("{ S5[i, j] -> U[j, i + 1] }", "r2")
    .addRead("{ S5[i, j] -> Q[i, j - 1] }", "r3")
    .addRead("{ S5[i, j] -> P[i, j - 1] }", "r4")
    .addWrite("{ S5[i, j] -> Q[i, j] }", "w0")
    .addDfg("w0 = (-d * r0 + (1.0 + 2.0 * d) * r1 - f * r2 - a * r3) / (a * r4 + b);")
)

scop = (
    Scop()
    .addStmt(S5)
    .addName("adi")
    .addTypeInfos({ "SIZE" : "int" })
    .addArrayInfos({ "V" : ["SIZE", "SIZE"],
                     "P": ["SIZE", "SIZE"],
                     "Q": ["SIZE", "SIZE"] })
)
