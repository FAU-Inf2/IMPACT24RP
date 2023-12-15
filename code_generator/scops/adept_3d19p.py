from scop import *
from scop_statement import *

Dom_S1 = """
  [SIZE] -> {
    S1[i, j, k] :
      1 <= i < SIZE - 1 and
      1 <= j < SIZE - 1 and
      1 <= k < SIZE - 1
  }
"""
Dom_Anon_S1 = "{ S1[i, j, k] -> [i, j, k] }"
Sch_S1 = "{ S1[i, j, k] -> O[i, 0, j, 0, k, 0] }"
Write = "{ S1[i, j, k] -> A1[i, j, k] }"

Read1  = "{ S1[i, j, k] -> A0[i    ,j - 1, k    ] }"
Read2  = "{ S1[i, j, k] -> A0[i    ,j + 1, k    ] }"
Read3  = "{ S1[i, j, k] -> A0[i - 1,j    , k    ] }"
Read4  = "{ S1[i, j, k] -> A0[i + 1,j    , k    ] }"
Read5  = "{ S1[i, j, k] -> A0[i - 1,j - 1, k    ] }"
Read6  = "{ S1[i, j, k] -> A0[i - 1,j + 1, k    ] }"
Read7  = "{ S1[i, j, k] -> A0[i + 1,j - 1, k    ] }"
Read8  = "{ S1[i, j, k] -> A0[i + 1,j + 1, k    ] }"

Read9  = "{ S1[i, j, k] -> A0[i    , j - 1, k - 1] }"
Read10 = "{ S1[i, j, k] -> A0[i    , j + 1, k - 1] }"
Read11 = "{ S1[i, j, k] -> A0[i - 1, j    , k - 1] }"
Read12 = "{ S1[i, j, k] -> A0[i + 1, j    , k - 1] }"

Read13 = "{ S1[i, j, k] -> A0[i    , j - 1, k + 1] }"
Read14 = "{ S1[i, j, k] -> A0[i    , j + 1, k + 1] }"
Read15 = "{ S1[i, j, k] -> A0[i - 1, j    , k + 1] }"
Read16 = "{ S1[i, j, k] -> A0[i + 1, j    , k + 1] }"

Read17 = "{ S1[i, j, k] -> A0[i    , j    , k - 1] }"
Read18 = "{ S1[i, j, k] -> A0[i    , j    , k + 1] }"

S1 = (
    ScopStatement("S1")
    .addDomain(Dom_S1)
    .addSchedule(Sch_S1)
    .addDomAnonymizer(Dom_Anon_S1)
    .addRead(Read1, "r00")
    .addRead(Read2, "r01")
    .addRead(Read3, "r02")
    .addRead(Read4, "r03")
    .addRead(Read5, "r04")
    .addRead(Read6, "r05")
    .addRead(Read7, "r06")
    .addRead(Read8, "r07")
    .addRead(Read9, "r08")
    .addRead(Read10, "r09")
    .addRead(Read11, "r10")
    .addRead(Read12, "r11")
    .addRead(Read13, "r12")
    .addRead(Read14, "r13")
    .addRead(Read15, "r14")
    .addRead(Read16, "r15")
    .addRead(Read17, "r16")
    .addRead(Read18, "r17")
    .addWrite(Write, "w0")
    .addDfg("w0 = (r00+r01+r02+r03+r04+r05+r06+r07+r08+r09+r10+r11+r12+r13+r14+r15+r16+r17) * fac;")
)

scop = (
    Scop()
    .addStmt(S1)
    .addName("adept3d19p")
    .addTypeInfos({ "SIZE" : "int", "fac" : "float" })
    .addArrayInfos({ "A1": ["SIZE", "SIZE", "SIZE"], "A0": ["SIZE", "SIZE", "SIZE"] })
)
