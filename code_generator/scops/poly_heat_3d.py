from scop import *
from scop_statement import *

S = (
    ScopStatement("S")
    .addDomain("[SIZE] -> { S[i, j, k] : 1 <= i < SIZE - 1 and 1 <= j < SIZE - 1 and 1 <= k < SIZE - 1}")
    .addSchedule("{ S[i, j, k] -> O[i, 0, j, 0, k, 0] }")
    .addDomAnonymizer("{ S[i, j, k] -> [i, j, k] }")
    .addRead("{ S[i, j, k] -> A[i + 1,j    ,k    ] }", "r0")
    .addRead("{ S[i, j, k] -> A[i    ,j + 1,k    ] }", "r1")
    .addRead("{ S[i, j, k] -> A[i    ,j    ,k + 1] }", "r2")

    .addRead("{ S[i, j, k] -> A[i    ,j    ,k    ] }", "r3")
    .addRead("{ S[i, j, k] -> A[i    ,j    ,k    ] }", "r4")
    .addRead("{ S[i, j, k] -> A[i    ,j    ,k    ] }", "r5")

    .addRead("{ S[i, j, k] -> A[i - 1,j    ,k    ] }", "r6")
    .addRead("{ S[i, j, k] -> A[i    ,j - 1,k    ] }", "r7")
    .addRead("{ S[i, j, k] -> A[i    ,j    ,k - 1] }", "r8")

    .addRead("{ S[i, j, k] -> A[i    ,j    ,k    ] }", "r9")
    .addWrite("{ S[i, j, k] -> B[i, j, k] }", "w0")
    .addDfg("""
    w0 =   0.125 * (r0 - 2.0 * r3 + r6)
         + 0.125 * (r1 - 2.0 * r4 + r7)
         + 0.125 * (r2 - 2.0 * r5 + r8)
         + r9;
     """)
)

TypeInfos = { "SIZE" : "int" }
ArrayInfos = { "A": ["SIZE", "SIZE", "SIZE"], "B": ["SIZE", "SIZE", "SIZE"] }

scop = (Scop()
        .addStmt(S)
        .addName("poly_heat_3d")
        .addTypeInfos(TypeInfos)
        .addArrayInfos(ArrayInfos))
