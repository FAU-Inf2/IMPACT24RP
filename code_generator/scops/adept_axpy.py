from scop import *
from scop_statement import *

Stmt = (ScopStatement("S")
        .addDomain("[SIZE] -> { S[i] : 0 <= i < SIZE }")
        .addDomAnonymizer("{ S[i] -> [i] }")
        .addSchedule("{ S[i] -> O[i, 0] }")
        .addRead("{ S[i] -> Y[i] }", "r0")
        .addRead("{ S[i] -> X[i] }", "r1")
        .addWrite("{ S[i] -> Y[i] }", "w0")
        .addDfg("w0 = a * r1 + r0;")
        )

scop = (
    Scop()
    .addStmt(Stmt)
    .addName("axpy")
    .addArrayInfos({ "X": ["SIZE"], "Y": ["SIZE"] })
    .addTypeInfos({ "SIZE": "int", "a": "float" })
)
