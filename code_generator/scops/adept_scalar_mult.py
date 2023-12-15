from scop import *
from scop_statement import *

S = (
    ScopStatement("S")
    .addDomain("[SIZE] -> { S[i] : 0 <= i < SIZE }")
    .addSchedule("{ S[i] -> O[i, 0] }")
    .addDomAnonymizer("{ S[i] -> [i] }")
    .addRead("{ S[i] -> V[i] }", "r0")
    .addWrite("{ S[i] -> V[i] }", "w0")
    .addDfg("w0 = a * r0;")
)

TypeInfos = { "SIZE" : "int", "a": "float" }
ArrayInfos = { "V": ["SIZE"] }

scop = (Scop()
        .addStmt(S)
        .addName("scalar_mult")
        .addTypeInfos(TypeInfos)
        .addArrayInfos(ArrayInfos))
