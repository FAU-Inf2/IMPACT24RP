import argparse

from settings import *

def parseArguments():
    parser = argparse.ArgumentParser(
        description = "Polysage"
    )

    parser.add_argument(
        "-T", "--find-tiling-scheme", type = bool,
        dest = "findTilingScheme", const = True,
        default = False, nargs = '?',
        help = "Run DSE to find tiling scheme"
    )

    parser.add_argument(
        "-I", "--generate-testbench", type = bool,
        dest = "generateTestBench", const = True,
        default = False, nargs = '?',
        help = "Generate testbench"
    )

    parser.add_argument(
        "-W", "--test-schedule", type = bool,
        dest = "testTilingScheme",
        const = True,
        default = False, nargs = '?',
        help = "..."
    )

    parser.add_argument(
        "-Wt", "--tile-dims", type = str,
        dest = "tileDims", default = None,
        help = "..."
    )

    parser.add_argument(
        "-We", "--elem-dims", type = str,
        dest = "elemDims", default = None,
        help = "..."
    )

    parser.add_argument(
        "-R", "--no-reformat", type = bool,
        dest = "noReformat", const = True,
        default = False, nargs = '?',
        help = "Do not automatically reformat"
    )

    parser.add_argument(
        "-O", "--output", type = str,
        default = "tlf",
        dest = "outFile", help = "Output file"
    )

    parser.add_argument(
        "-S", "--scop-file", type = str,
        dest = "scopFile", help = "Scop file",
        required = True
    )

    parser.add_argument(
        "-D", "--use-default-sched", type = bool,
        dest = "useDefaultSched", const = True,
        default = False, nargs="?",
        help = "Use default schedule instead of DSE"
    )

    parser.add_argument(
        "-Bu", "--uniform-block-size", type = int,
        dest = "uniformBlockSize",
        default = None,
        help = "Use uniform block size"
    )

    parser.add_argument(
        "-Bs", "--block-sizes", type = str,
        dest = "blockSizes", default = None,
        help = "Block sizes for tiling"
    )

    parser.add_argument(
        "-L", "--only-loop-splitting", type = bool,
        nargs = '?', const = True, dest = "onlyLoopSplitting"
    )

    parser.add_argument(
        "-C", "--code-gen", type = str, choices = ["orka", "normal"],
        dest = "codegen", default = "normal"
    )

    parser.add_argument(
        "-G", "--generate-code", type = bool,
        const = True, dest = "generateCode",
        nargs = '?', default = False
    )

    parser.add_argument(
        "-P", "--port-map", type = str,
        choices = ["axi", "lin", "vla"],
        dest = "portMap", default = "lin"
    )

    parser.add_argument(
        "-A", "--default-axi-width", type = int,
        choices = [1, 2, 4, 8, 16, 32],
        dest = "defaultAxiWidth", default = 1
    )

    parser.add_argument(
        "-V", "--emit-debug-code", type = bool,
        default = False,
        nargs = '?', const = True, dest = "emitDebugCode"
    )

    parser.add_argument(
        "-X", "--emit-burst-verify", type = bool,
        default = False,
        nargs = '?', const = True, dest = "emitBurstVerify"
    )

    parser.add_argument(
        "-F", "-only-calculate-fused-overlap-graph",
        type = bool, default = False, nargs = '?', const = True,
        dest = "onlyCalcFusedOverlapGraph"
    )

    parsedArgs = parser.parse_args()

    Settings.set("useDefaultSched", parsedArgs.useDefaultSched)
    Settings.set("uniformBlockSize", parsedArgs.uniformBlockSize)
    Settings.set("scopFile", parsedArgs.scopFile)
    Settings.set("noReformat", parsedArgs.noReformat)
    Settings.set("generateCode", parsedArgs.generateCode)
    Settings.set("portMap", parsedArgs.portMap)
    Settings.set("codegen", parsedArgs.codegen)
    Settings.set("onlyLoopSplitting", parsedArgs.onlyLoopSplitting)
    Settings.set("outFile", parsedArgs.outFile)
    Settings.set("defaultAxiWidth", parsedArgs.defaultAxiWidth)
    Settings.set("emitDebugCode", parsedArgs.emitDebugCode)
    Settings.set("emitBurstVerify", parsedArgs.emitBurstVerify)
    Settings.set("onlyCalcFusedOverlapGraph",
                 parsedArgs.onlyCalcFusedOverlapGraph)
    Settings.set("findTilingScheme", parsedArgs.findTilingScheme)
    Settings.set("testTilingScheme", parsedArgs.testTilingScheme)
    Settings.set("generateTestBench", parsedArgs.generateTestBench)

    edims = parsedArgs.elemDims
    edims = edims.replace(" ", "").split(",") if edims != None else edims
    Settings.set("elemDims", edims)

    tdims = parsedArgs.tileDims
    tdims = tdims.replace(" ", "").split(",") if tdims != None else tdims
    Settings.set("tileDims", tdims)

    if parsedArgs.blockSizes != None:
        Settings.set("useUniformBlockSize", False)
        bs = parsedArgs.blockSizes
        bs = list(map(int, bs.replace(" ", "").split(","))) if bs != None else bs
        Settings.set("blockSizes", bs)

    if parsedArgs.uniformBlockSize != None:
        Settings.set("useUniformBlockSize", True)
        Settings.set("uniformBlockSize", parser.uniformBlockSize)

    if parsedArgs.uniformBlockSize == None and parsedArgs.blockSizes == None:
        Settings.set("useUniformBlockSize", True)
        Settings.set("uniformBlockSize", 32)

    return parsedArgs
