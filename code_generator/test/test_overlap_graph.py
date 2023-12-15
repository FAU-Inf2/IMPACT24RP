from overlap_graph import *
from isl_util import *
from scop_statement import *
from scop import *
from accesses import *
from partitions.true_canonical_partition import *
from search_tile import *


def testFirstStage():
    stmt = (
        ScopStatement("S")
        .addDomain("[SZ] -> { S[i, j, k] : 1 <= i < SZ and 1 <= j < SZ and 1 <= k < SZ }")
        .addSchedule("{ S[i, j, k] -> O[0, i, 0, j, 0, k, 0] }")
        .addDomAnonymizer("{ S[i, j, k] -> [i, j, k] }")
        .addRead("{ S[i, j, k] -> A[i, j, k] }", "r0")
        .addRead("{ S[i, j, k] -> A[i+1, j, k+1] }", "r1")
        .addRead("{ S[i, j, k] -> A[j, i, k] }", "r2")
        .addRead("{ S[i, j, k] -> A[2i, j, k] }", "r3")
        .addRead("{ S[i, j, k] -> U[k, j] }", "r4")
        .addRead("{ S[i, j, k] -> A[i+1, j, k+4] }", "r8")
        .addRead("{ S[i, j, k] -> U[k+1, j] }", "r5")
        .addRead("{ S[i, j, k] -> B[i, j, k+1] }", "r6")
        .addRead("{ S[i, j, k] -> B[2i, j, k+4] }", "r7")
        .addWrite("{ S[i, j, k] -> B[i, j, k] }", "w0")
        .addDfg("w0 = r0+r1+r2+r3+r4+r5+r6+r7")
       )
    scop = (
        Scop()
        .addName("runex")
        .addStmt(stmt)
        .addArrayInfos({ "A": ["SZ", "SZ", "SZ"], "U": ["SZ", "SZ"], "B": ["SZ", "SZ", "SZ"]})
        .addTypeInfos({ "SZ": "int" })
    )

    dom = stmt.getDom()
    dimlist = ["i", "j", "k"]
    bs = getUniformBlockSizes(dimlist, 32)
    part = TrueCanonicalPartition([stmt])
    tiling = SearchTile(part, "O", dimlist, dimlist, bs)
    rba = ReadBoxAnalysis(tiling, dom)

    og = OverlapGraph(str(tiling), tiling, scop.calcOrd())
    for r in part.getAllAccs():
        r.setCacheAble(rba.isCacheAble(r.get()))
        r.setAlignedToLoop(rba.isAccAlignedToTile(r.get()))
        newAccs = Accesses([r])
        og.addAcc(newAccs)

    og.detectDeps()
    og.writeToFs("AfterDepDetect")
    og.fuseNodesStageOne(tiling, dom)
    og.writeToFs("AfterFirstNodeFusion")
    og.syncAttributes()
    og.detectOverlaps()
    og.writeToFs("AfterOverlapDetection")
    og.fuseNodesStageTwo(tiling, dom)
    og.syncAttributes()
    og.writeToFs("AfterSecondNodeFusion")
    og.calculateCards()


TESTS = [testFirstStage]
