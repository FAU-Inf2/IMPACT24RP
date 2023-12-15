#!/usr/bin/env python3

import glob
import json
import argparse
import statistics

benchmarks = [
    "adept_2d5p",
    "adept_2d9p",
    "adept_3d19p",
    "adept_3d27p",
    "poly_fdtd0",
    "poly_fdtd1",
    "poly_fdtd2",
    "poly_heat_3d",
    "poly_jacobi_1d",
    "poly_jacobi_2d"
]

benchSets = [
    "base",
    "opt_al4_defaultBS",
    "opt_al4_halfBS",
    "opt_al8_defaultBS",
    "opt_al8_halfBS",
]

def loadTiming(timingFile):
    f = open(timingFile)
    j = json.load(f)
    line = j[4]
    assert(line["type"] == "fpga")
    seconds = line["runtimeInSec"]
    microSecs = line["runtimeUsec"]
    return seconds + (microSecs / 10 ** 6)

def averageTimes(times):
    return sum(times) / len(times)

class DataPoint():
    def __init__(self, avgTime, stdev):
        self.avgTime = avgTime
        self.stdev = stdev

    def __str__(self):
        return "%s, %s" % (self.avgTime, self.stdev)

def calculateAvgRuntime(benchSet, benchmark):
    path = benchSet + "/" + benchmark
    timingFiles = glob.glob(path + "/timing*.json")

    if len(timingFiles) == 0:
        return DataPoint(-1, 0)

    assert(len(timingFiles) >= 5)
    times = list(map(loadTiming, timingFiles))
    stdev = statistics.stdev(times)
    avgTime = averageTimes(times)
    assert(avgTime > 0)
    return DataPoint(avgTime, stdev)

def main():
    parser = argparse.ArgumentParser(description = "aggregator")

    parser.add_argument(
        "-b", "--benchmarks", type = str,
        dest = "benchmarks", required = True,
        help = "Benchmarks"
    )

    parser.add_argument(
        "-T", "--only-avg-runtime", type = bool,
        dest = "onlyAvgRuntime", const = True,
        nargs = "?", default = False,
        help = "Benchmarks"
    )

    parser.add_argument(
        "-Bs", "--benchmark-set", type = str,
        dest = "benchmarkSet", required = True,
        help = "Benchmark set"
    )

    parser.add_argument(
        "-L", "--bench-labels", type = str,
        dest = "benchLabels", default = "fnord",
        help = "Benchmark labels"
    )

    args = parser.parse_args()

    benchs = args.benchmarks.split(",")
    benchSet = args.benchmarkSet
    benchLabels = args.benchLabels.split(",")
    onlyAvgRuntime = args.onlyAvgRuntime

    if onlyAvgRuntime:
        for bench in benchs:
            rt = calculateAvgRuntime(benchSet, bench)
            print(rt)
        exit(0)

    assert(len(benchs) == len(benchLabels))

    plotInfo = []

    for idx, bench in enumerate(benchs):
        rt = calculateAvgRuntime(benchSet, bench)
        rtBase = calculateAvgRuntime("base", bench)
        speedup = rtBase.avgTime / rt.avgTime
        plotInfo.append((benchLabels[idx], speedup))

    print("\\addplot coordinates {%s};" %
          (" ".join([ "(%s, %s)" % s for s in plotInfo ])))

main()
