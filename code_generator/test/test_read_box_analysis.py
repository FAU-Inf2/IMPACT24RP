from read_box_analysis import *
from isl_util import *
from scop_statement import *
from partitions.true_canonical_partition import *
from search_tile import *

domain = "[SZ] -> { S[i, j] : 1 <= i < SZ and 1 <= j < SZ }"
schedule = "{ S[i, j] -> O[0, i, 0, j, 0] }"
read = "{ S[i, j] -> A[i, j] }"

stmt = (
    ScopStatement("S")
    .addDomain(domain)
    .addSchedule(schedule)
    .addRead(read, "r0")
    .addDomAnonymizer("{ S[i, j] -> [i, j] }")
)
part = TrueCanonicalPartition([ stmt ])
dimlist = ["i", "j"]
bs = getUniformBlockSizes(dimlist, 32)
tiling = SearchTile(part, "O", dimlist, dimlist, bs)

def testCalcCacheShape():
    read = stmt.getReads()[0]
    rba = ReadBoxAnalysis(tiling, domain)
    slab = rba.slabs.getReadCacheSlab()
    print("slab: ", slab)
    cache = rba.getUnpaddedCacheShape(read.get(), slab)
    print("cache: ", cache)
    print("cache ast: ", getAst(cache.identity()).to_C_str())
    pass

def testSelfOverlap():
    domain = "[SZ] -> { S[i, j] : 1 <= i < SZ and 1 <= j < SZ }"
    schedule = "{ S[i, j] -> O[0, i, 0, j, 0] }"
    read0 = "{ S[i, j] -> A[i, j] }"
    read1 = "{ S[i, j] -> A[j, i] }"

    stmt = (
        ScopStatement("S")
        .addDomain(domain)
        .addSchedule(schedule)
        .addRead(read0, "r0")
        .addRead(read1, "r1")
        .addDomAnonymizer("{ S[i, j] -> [i, j] }")
    )


    part = TrueCanonicalPartition([ stmt ])
    dimlist = ["i", "j"]
    bs = getUniformBlockSizes(dimlist, 32)
    tiling = SearchTile(part, "O", dimlist, dimlist, bs)
    print(tiling)

    rba = ReadBoxAnalysis(tiling, domain)
    fst = rba.getFirst("i")
    nxt = lexRoundDown(rba.getGt("i"))
    nextV = nxt.intersect_domain(fst)
    r = isl.union_map(read0).union(isl.union_map(read1))
    ris = rba.liftAcc(r)

    b = rba.getUnpaddedCacheShape(r, rba.slabs.getReadCacheSlab())
    print(b)

def testIsCacheable():
    stmt = (
        ScopStatement("S")
        .addDomain("[SZ] -> { S[i, j, k] : 1 <= i < SZ and 1 <= j < SZ and 1 <= k < SZ }")
        .addSchedule("{ S[i, j, k] -> O[0, i, 0, j, 0, k, 0] }")
        .addRead("{ S[i, j, k] -> A[i, j, k] }", "r0")
        .addRead("{ S[i, j, k] -> A[i, j, k]; S[i, j, k] -> A[i, j, k+1] }", "r1")
        .addRead("{ S[i, j, k] -> A[i, j, k]; S[i, j, k] -> A[i, j, k+1]; S[i, j, k] -> A[i, j+1, k] }", "r2")
        .addRead("{ S[i, j, k] -> A[i, j, k]; S[i, j, k] -> A[j, i, k] }", "r3")
        .addRead("{ S[i, j, k] -> A[2i, j, k] }", "r4")
        .addRead("{ S[i, j, k] -> A[i, i, k] }", "r5")
        .addRead("{ S[i, j, k] -> A[2i, j, k]; S[i, j, k] -> A[i, j, k] }", "r6")
        .addDomAnonymizer("{ S[i, j, k] -> [i, j, k] }")
    )

    resDict = { "r0": True, "r1": True, "r2": True, "r3":
                False, "r4": True, "r5": True, "r6": False }
    dimlist = ["i", "j", "k"]
    bs = getUniformBlockSizes(dimlist, 32)
    tiling = SearchTile(TrueCanonicalPartition([stmt]), "O", dimlist, dimlist, bs)

    for arrRef, expected in resDict.items():
        read = stmt.getAccessByArrRef(arrRef)
        rba = ReadBoxAnalysis(tiling, stmt.getDom())
        print("arrRef: ", arrRef)
        cacheable = rba.isCacheAble(read.get())
        assert(cacheable == expected)

def testIsAligned():
    stmt = (
        ScopStatement("S")
        .addDomain("[SZ] -> { S[i, j, k] : 1 <= i < SZ and 1 <= j < SZ and 1 <= k < SZ }")
        .addSchedule("{ S[i, j, k] -> O[0, i, 0, j, 0, k, 0] }")
        .addRead("{ S[i, j, k] -> A[i, j, k] }", "r0")
        .addRead("{ S[i, j, k] -> A[j, i, k] }", "r1")
        .addRead("{ S[i, j, k] -> A[j, j, k] }", "r2")
        .addRead("{ S[i, j, k] -> A[k, i, k] }", "r3")
        .addRead("{ S[i, j, k] -> A[j, i, (2k+42) %10] }", "r4")
        .addRead("{ S[i, j, k] -> A[i, k, j] }", "r5")
        .addRead("{ S[i, j, k] -> A[i, j, k]; S[i, j, k] -> A[i, j, k+1] }", "r6")
        .addDomAnonymizer("{ S[i, j, k] -> [i, j, k] }")
    )

    resDict = { "r0": True, "r1": True, "r2": True, "r3": False,
                "r4": True, "r5": False, "r6": False}

    part = TrueCanonicalPartition([ stmt ])
    dimlist = ["i", "j", "k"]
    bs = getUniformBlockSizes(dimlist, 32)
    tiling = SearchTile(part, "O", dimlist, dimlist, bs)

    for arrRef, expected in resDict.items():
        read = stmt.getAccessByArrRef(arrRef)
        rba = ReadBoxAnalysis(tiling, stmt.getDom())
        isAligned = rba.isAccAlignedToTile(read.get())
        print("addRef: ", isAligned)
        assert(isAligned == expected)


TESTS = [testCalcCacheShape, testSelfOverlap,
         testIsAligned, testIsCacheable]
