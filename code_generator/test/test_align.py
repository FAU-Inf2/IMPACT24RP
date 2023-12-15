from scop_statement import *
from util import *
from scop import *

def testAlign():
    stmt = (ScopStatement("fnord")
            .addDomain("{ S1[i, j] : 1 <= i < 10 and 0 <= j <= 1 }")
            .addSchedule("{ S1[i, j] -> O[0, i, 0, j, 0] }")
            .addRead("{ S1[i, j] -> A[i, j] }", "r0")
            .addRead("{ S1[i, j] -> A[2i, 2j] }", "r1")
            .addDomAnonymizer("{ S1[i, j] -> [i, j] }"))
    scop = (Scop()
            .addName("myscop").
            addStmt(stmt))

    # newDom = stmt.padDomain(4)
    # oldDom = stmt.getDom()
    # print("oldDom.lexmin(): ", oldDom.lexmin())
    # print("newDom.lexmin(): ", newDom.lexmin())
    # print("oldDom.lexmax(): ", oldDom.lexmax())
    # print("newDom.lexmax(): ", newDom.lexmax())

ALIGN_TESTS = [testAlign]
