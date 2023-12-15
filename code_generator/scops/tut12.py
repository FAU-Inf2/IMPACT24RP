from scop import *
from scop_statement import *

S1 = (ScopStatement("S1")
      .addDomain("[N] -> { S1[i] : 1 <= i < N }")
      .addSchedule("{ S1[i] -> O[i, 0, 0, 0] }")
      .addDomAnonymizer("{ S1[i] -> [i] }")
      .addRead("{ S1[i] -> A[i+1] }", "r1")
      .addRead("{ S1[i] -> D[i] }", "r2")
      .addDfg("w1 = r1 * 2 + r2")
      .addWrite("{ S1[i] -> A[i] }", "w1"))

S2 = (ScopStatement("S2")
      .addDomain("[N] -> { S2[i, j] : 1 <= i < N and 1 <= j <= N }")
      .addSchedule("{ S2[i, j] -> O[i, 1, j, 0] }")
      .addDomAnonymizer("{ S2[i, j] -> [i, j] }")
      .addRead("{ S2[i, j] -> B[i, j-1] }", "r1")
      .addRead("{ S2[i, j] -> A[i] }", "r2")
      .addDfg("w1 = 2 / r1 + r2")
      .addWrite("{ S2[i, j] -> B[i, j] }", "w1"))

S3 = (ScopStatement("S3")
      .addDomain("[N] -> { S3[i] : 1 <= i < N }")
      .addSchedule("{ S3[i] -> O[i, 2 ,0, 0] }")
      .addDomAnonymizer("{ S3[i] -> [i] }")
      .addRead("{ S3[i] -> A[i-1] }", "r1")
      .addRead("[N] -> { S3[i] -> B[i, N] }", "r2")
      .addDfg("w1 = r1 * r2")
      .addWrite("{ S3[i] -> C[i] }", "w1")
      )

S4 = (ScopStatement("S4")
      .addDomain("[N] -> { S4[i] : 1 <= i < N }")
      .addSchedule("{ S4[i] -> O[i, 3, 0, 0] }")
      .addDomAnonymizer("{ S4[i] -> [i] }")
      .addRead("{ S4[i] -> A[i+1] }", "r1")
      .addDfg("w1 = 2 * r1 + fac")
      .addWrite("{ S4[i] -> D[i] }", "w1"))

TypeInfos = {
    "N" : "int",
    "fac": "int"
}

Tut12 = Scop([S1, S2, S3, S4],
             name = "Tut12").addTypeInfos(TypeInfos)
