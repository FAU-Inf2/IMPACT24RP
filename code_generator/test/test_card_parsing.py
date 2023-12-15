from partitions.canonical_partition import *
from scop_statement import *
from card_visitor.pretty_printer import *
from card_visitor.cond_assignment_gen import *
from accesses import *
from util import *
from scop import *

def testCardParsing():
    stmt = (ScopStatement("fnord")
            .addDomain("[N, K] -> { S1[i, j] : 1 <= i < N and 0 <= j <= K }")
            .addSchedule("{ S1[i, j] -> O[0, i, 0, j, 0] }")
            .addRead("{ S1[i, j] -> A[i, j] }", "r0")
            .addRead("{ S1[i, j] -> A[i + 1, j + 1] }", "r1")
            .addDomAnonymizer("{ S1[i, j] -> [i, j] }"))
    # scop = Scop([ stmt ], name = "myscop")
    part = TrueCanonicalPartition([ stmt ])
    dimlist = ["i", "j"]
    bs = getUniformBlockSizes(dimlist, 32)
    tiling = SearchTile(part, "O", dimlist, dimlist, bs)
    rba = ReadBoxAnalysis(tiling, stmt.getDom())

    accs = Accesses()
    r0 = stmt.getAccessByArrRef("r0")
    accs.add(r0)
    r1 = stmt.getAccessByArrRef("r1")
    accs.add(r1)
    #print("read: ", read)

    initSet = rba.getInitNoDom(accs.union(), "i")
    print("initSet:", initSet)

    lastDim = projectOutLast(initSet)
    print("projected: ", lastDim)

    print("card: ", lastDim.card())

    mi = isl.multi_id("{ [a] }")
    l = lastDim.gist(lastDim.params().unbind_params(mi))
    print(l)
    print(l.card())

    p = IslCardParser.grammar.parse(str(l.card())).unwrap()
    print(p)

    # ppv = PrettyPrintVisitor()
    # print(ppv.do(p))

    # cg = CondAssignGen("len")
    # print(cg.do(p))


CARD_TESTS = [testCardParsing]
