from partitions.canonical_partition import *
from partitions.true_canonical_partition import *
from scop_statement import *
from search_tile import *
from isl_util import *
from util import *

def testSearchTile():
    stmt = (ScopStatement("fnord")
            .addDomain("{ S1[i, j] : 0 <= i < 10 and 0 <= j < 10 }")
            .addSchedule("{ S1[i, j] -> O[0, i, 0, j, 0] }")
            .addDomAnonymizer("{ S1[i, j] -> [i, j] }"))
    stmts = [ stmt ]
    part = TrueCanonicalPartition(stmts)
    dimlist = ["i", "j"]
    bs = getUniformBlockSizes(dimlist, 32)
    st = SearchTile(part, "O", dimlist, dimlist, bs)

    print("part.getSchedRangeDims: ", part.getSchedRangeDims())

    print("Tiling Level: ", st.getTilingLevel())
    print("Full tile constr set: ", st.getFullTileConstrContextSet())
    print("Line constr set: ", st.getLineConstrContextSet())
    print("Tile union map: ", st.getFullTransform())
    print("Next map: ", st.getNextMap("i"))
    print("Full tile slab:", st.getSlabs().getFullTileSlab())
    print("Inner tile slab:", st.getSlabs().getInnerTileSlab(["i"]))
    print("Sched adjust transform:", st.getSchedAdjustTransform(stmt.getDom()))
    print("Var Slab: ", st.getSlabs().getVarSlab("i"))
    print("Var Slab No Di: ", st.getSlabs().getVarSlabNoDi("i"))
    print("lstLine: ", st.getLsdLine())
    print("Zero Shifter: ", st.getZeroShiftTransform())
    print("Schedule Range Dimlist: ", st.createScheduleRangeDimlist())
    print("Schedule Dom Dimlist: ", st.createScheduleDomDimlist())
    print("Tile Sched map: ", st.tileSchedMap)

SEARCH_TILE_TESTS = [testSearchTile]
