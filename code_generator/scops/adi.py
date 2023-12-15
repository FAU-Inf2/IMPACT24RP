from scop import *
from scop_statement import *

S1 = (
    ScopStatement("S1")
    .addDomain("[SIZE] -> { S1[i] : 1 <= i < SIZE - 1 }")
    .addSchedule("{ S1[i] -> O[i, 0, 0, 0] }")
    .addDomAnonymizer("{ S1[i] -> [i] }")
    .addWrite("{ S1[i] -> V[0][i] }", "w0")
    .addDfg("w0 = 1.0")
)

S2 = (
    ScopStatement("S2")
    .addDomain("[SIZE] -> { S2[i] : 1 <= i < SIZE - 1 }")
    .addSchedule("{ S2[i] -> O[i, 1, 0, 0] }")
    .addDomAnonymizer("{ S2[i] -> [i] }")
    .addWrite("{ S2[i] -> P[i][0] }", "w0")
    .addDfg("w0 = 0.0")
)

S3 = (
    ScopStatement("S3")
    .addDomain("[SIZE] -> { S3[i] : 1 <= i < SIZE - 1 }")
    .addSchedule("{ S3[i] -> O[i, 2, 0, 0] }")
    .addDomAnonymizer("{ S3[i] -> [i] }")
    .addWrite("{ S3[i] -> Q[i][0] }", "w0")
    .addDfg("w0 = 1.0")
)

S4 = (
    ScopStatement("S4")
    .addDomain("[SIZE] -> { S4[i, j] : 1 <= i < SIZE - 1 and 1 <= j < SIZE - 1 }")
    .addSchedule("{ S4[i, j] -> O[i, 2, j, 0] }")
    .addDomAnonymizer("{ S4[i, j] -> [i, j] }")
    .addRead("{ S4[i, j] -> P[i, j-1] }", "r0")
    .addWrite("{ S4[i, j] -> P[i, j] }", "w0")
    .addDfg("w0 = -c / (a * r0 + b)")
)

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
    .addDfg("w0 = (-d * r0 + (1.0 + 2.0 * d) * r1 - f * r2 - a * r3) / (a * r4 + b)")
)

S6 = (
    ScopStatement("S6")
    .addDomain("[SIZE] -> { S6[i] : 1 <= i < SIZE - 1 }")
    .addSchedule("{ S6[i] -> O[i, 3, 0, 0] }")
    .addDomAnonymizer("{ S6[i] -> [i] }")
    .addWrite("[SIZE] -> { S6[i] -> V[SIZE - 1][i] }", "w0")
    .addDfg("w0 = 1.0")
)

S7 = (
    ScopStatement("S7")
    .addDomain("[SIZE] -> { S7[i, j] : 1 <= i < SIZE - 1 and 1 <= j <= SIZE - 2 }")
    .addSchedule("{ S7[i, j] -> O[i, 4, -j, 0] }")
    .addDomAnonymizer("{ S7[i, j] -> [i, j] }")
    .addRead("{ S7[i, j] -> P[i, j] }", "r0")
    .addRead("{ S7[i, j] -> Q[i, j] }", "r1")
    .addRead("{ S7[i, j] -> V[j + 1, i] }", "r2")
    .addWrite("{ S7[i, j] -> V[j][i] }", "w0")
    .addDfg("w0 = r0 * r2 + r1")
)

scop = (
    Scop()
    .addStmt(S1).addStmt(S2).addStmt(S3)
    .addStmt(S4).addStmt(S5).addStmt(S6).addStmt(S7)
    .addName("adi")
    .addTypeInfos({ "SIZE" : "int", "d": "float",
                    "c" : "float",
                    "b" : "float",
                    "e" : "float",
                    "f" : "float",
                    "a" : "float"})
    .addArrayInfos({}) # TODO
)
