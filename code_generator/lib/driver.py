from dse import *
from scop import *
from settings import *
from isl_util import *
from testbench import *
from ports.port_mapper import *
from codegen.cg_normal import *
from codegen.cg_chunked import *

from dependency import *

def runCodegen(cg):
    cg.do()
    if Settings.config("noReformat") == False:
        cg.reformat()
    cg.writeCodeToFile()
    cg.writeHeaderToFile()

def doTilingDse(partitions, scop):
    truePartitions = partitions.getTrueCanonStmts()
    tileSearchResultsPerPart = getTileSearchResultsPerPartition(truePartitions, scop)
    winners = findWinningTiles(truePartitions, tileSearchResultsPerPart)
    setWinningTiles(truePartitions, winners)

def transform(scop, codegenFac, portMap):
    depGraph = scop.depAnalysis()
    scop.doLoopSplitting(depGraph)
    # scop.writeReadAfterRead()

    partitions = scop.partitionCanonicalStmts()
    doTilingDse(partitions, scop)
    codegen = codegenFac(scop, portMap, partitions)
    runCodegen(codegen)

def getCodegen():
    codegenSpec = Settings.config("codegen")
    fn = Settings.config("outFile")
    if codegenSpec == "normal":
        return lambda s, pm, pa: NormalCodeGen(s, pm, pa, fn)
    if codegenSpec == "orka":
        return lambda s, pm, pa: OrkaCodeGen(s, pm, pa, fn)

    raise Exception("Unimplemented Path")

def findTilingScheme():
    scop = readScop()
    depGraph = scop.depAnalysis()
    scop.doLoopSplitting(depGraph)
    partitions = scop.partitionCanonicalStmts()
    truePartitions = partitions.getTrueCanonStmts()
    tileSearchResultsPerPart = getTileSearchResultsPerPartition(truePartitions, scop)
    winners = findWinningTiles(truePartitions, tileSearchResultsPerPart)
    setWinningTiles(truePartitions, winners)
    for tp in truePartitions:
        print("Winning tile: ", tp.getTiling())
        dsp = winners[tp]
        dsp.dump()

def calculateFusedOverlapGraph():
    scop = readScop()
    depGraph = scop.depAnalysis()
    scop.doLoopSplitting(depGraph)
    partitions = scop.partitionCanonicalStmts()
    doTilingDse(partitions, scop)
    truePartitions = partitions.getTrueCanonStmts()
    for tp in truePartitions:
        fusedOg = tp.getOverlapGraph()
        fusedOg.writeToFs("FINAL_FUSED_OVERLAP_GRAPH")

def testTilingScheme():
    scop = readScop()
    depGraph = scop.depAnalysis()
    scop.doLoopSplitting(depGraph)
    partitions = scop.partitionCanonicalStmts()
    part = partitions.getTrueCanonStmts()[0]
    bs = getBlockSizes(part.getDimlist())

    tileDims = Settings.config("tileDims")
    elemDims = Settings.config("elemDims")

    stile = SearchTile(part, "O", tileDims, elemDims, bs)

    tra = stile.getTransformedSchedule()

    isValid = scop.isValidSchedule(tra)
    print("%s \nis %s a valid schedule" % (tra, "" if isValid else "NOT"))

def getPortMap(scop):
    portSpec = Settings.config("portMap")
    if portSpec == "axi":
        return BurstMaxiDefaultPorts(scop)
    if portSpec == "vla":
        return VarLengthDefaultPorts(scop)
    if portSpec == "lin":
        return LinearizedDefaultPorts(scop)

    raise Exception("Unimplemented Path")

def readScop():
    scopFile = Settings.config("scopFile")
    globs = {}
    locs = {}
    exec(open(scopFile).read(), globs, locs)
    return locs["scop"]

def runLoopSplitting():
    scop = readScop()
    depGraph = scop.depAnalysis()
    print("Full Original Dom: ", scop.getFullDom())
    print("Full Original Sched: ", scop.getFullSched())

    writeToPng(depGraph, "dependency_graph")

    scop.doLoopSplitting(depGraph)
    print("Full Original Dom after splitting: ", scop.getFullDom())
    print("Full Original Sched after splitting: ", scop.getFullSched())

def main():
    if Settings.config("onlyLoopSplitting"):
        runLoopSplitting()
        exit(0)

    if Settings.config("onlyCalcFusedOverlapGraph"):
        calculateFusedOverlapGraph()
        exit(0)

    if Settings.config("generateCode"):
        scop = readScop()
        portmap = getPortMap(scop)
        codegen = getCodegen()
        transform(scop, codegen, portmap)
        exit(0)

    if Settings.config("generateTestBench"):
        scop = readScop()
        portmap = getPortMap(scop)
        tb = genTestbench(scop, portmap)
        tb = clangFormat(tb)
        f = open("input.cpp", "w")
        f.write(tb)
        f.close()
        exit(0)

    if Settings.config("testTilingScheme"):
        testTilingScheme()
        exit(0)

    if Settings.config("findTilingScheme"):
        findTilingScheme()
        exit(0)
