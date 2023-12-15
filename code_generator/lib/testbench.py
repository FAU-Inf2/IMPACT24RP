from util import *
from scop import *
from ports.port_mapper import *

def genHostDriver(scop, portMap):
    arrayNames = list(scop.getArrayNames())
    numArrays = len(arrayNames)
    params = scop.getParams()
    tyInfos = scop.getTypeInfos()
    arrs = []
    arrVars = []
    ArrVars = []
    for idx, an in enumerate(arrayNames):
        arrInfos = scop.getArrayInfos()
        arrDims = len(arrInfos[an])
        align = portMap.getAlign(an)
        factoryFunction = "getAndInitNormalArray<float>"
        arrDims = arrInfos[an]
        sizeVecStr = cmJoin(arrDims)
        arr = []
        arr.append("std::vector<int> dims%s{%s};" % (idx, sizeVecStr))
        arr.append("auto A%s = %s(dims%s, \"a%s\");"
                   % (idx, factoryFunction, idx, idx))
        arr.append("float *a%s = A%s->getPtr();"
                   % (idx, idx))
        arr.append("const int a%s_size = A%s->getOmpMapSize();" % (idx, idx))
        arrVars.append("a%s" % (idx))
        ArrVars.append("A%s" % (idx))
        arrs.append(nlJoin(arr))
    arrsStr = nlJoin(arrs)
    ompMapParams = [ "a%s[:a%s_size]" % (i, i)
                     for i in range(0, len(arrayNames)) ]
    ompMapStr = cmJoin(ompMapParams)
    callArgs = [ s for (s, v) in tyInfos.items() ]
    callArgsStr = cmJoin(callArgs)
    paramArgs = [ "%s %s" % (tyInfos[p], p) for p in params ]
    paramArgsStr = cmJoin(paramArgs)
    innerParams = [ "%s %s = RandGen<%s>::getRand();" % (v, k, v)
                    for k, v in tyInfos.items() if k not in params ]
    innerParamVars = [ "%s" % (k) for (k, v) in tyInfos.items() ]
    innerParamsStr = nlJoin(innerParams)
    callArgsStr = cmJoin(innerParamVars + arrVars)

    code = """
Res<float, %s> driver_host(%s, unsigned int REPS) {
  %s
  %s
  struct timespec start, end;
  clock_gettime(CLOCK, &start);
#ifdef BASELINE
#pragma omp target map(tofrom : %s)
#endif
  { tlf_normal(%s); }
  clock_gettime(CLOCK, &end);
  elapsed_time_hr(start, end, "HOST code");
  return {%s};
}
    """ % (numArrays, paramArgsStr, arrsStr, innerParamsStr,
           ompMapStr, callArgsStr, cmJoin(ArrVars))
    return code


def genFpgaDriver(scop, portMap):
    arrayNames = list(scop.getArrayNames())
    numArrays = len(arrayNames)
    params = scop.getParams()
    tyInfos = scop.getTypeInfos()
    arrs = []
    arrVars = []
    ArrVars = []
    for idx, an in enumerate(arrayNames):
        arrInfos = scop.getArrayInfos()
        arrDims = len(arrInfos[an])
        align = portMap.getAlign(an)
        factoryFunction = "getAndInitAxiArray<AxiVec%s>" % (align)
        arrDims = arrInfos[an]
        sizeVecStr = cmJoin(arrDims)
        arr = []
        arr.append("std::vector<int> dims%s{%s};" % (idx, sizeVecStr))
        arr.append("auto A%s = %s(dims%s, 0, \"a%s\");"
                   % (idx, factoryFunction, idx, idx))
        arr.append("AxiVec%s *a%s = A%s->getCastedPtr<AxiVec%s>();"
                   % (align, idx, idx, align))
        arr.append("const int a%s_size = A%s->getOmpMapSize();" % (idx, idx))
        arrVars.append("a%s" % (idx))
        ArrVars.append("A%s" % (idx))
        arrs.append(nlJoin(arr))
    arrsStr = nlJoin(arrs)
    ompMapParams = [ "a%s[:a%s_size]" % (i, i)
                     for i in range(0, len(arrayNames)) ]
    ompMapStr = cmJoin(ompMapParams)
    callArgs = [ s for (s, v) in tyInfos.items() ]
    callArgsStr = cmJoin(callArgs)
    paramArgs = [ "%s %s" % (tyInfos[p], p) for p in params ]
    paramArgsStr = cmJoin(paramArgs)
    innerParams = [ "%s %s = RandGen<%s>::getRand();" % (v, k, v)
                    for k, v in tyInfos.items() if k not in params ]
    innerParamVars = [ "%s" % (k) for (k, v) in tyInfos.items() ]
    innerParamsStr = nlJoin(innerParams)
    callArgsStr = cmJoin(innerParamVars + arrVars)

    code = """
Res<float, %s> driver_fpga(%s, unsigned int REPS) {
  %s
  %s
  struct timespec start, end;
  clock_gettime(CLOCK, &start);
#ifdef POLYSAGE
#pragma omp target orkaTranslate(topLevelFunction : "tlf")   \\
    map(tofrom : %s)
#endif
  { tlf(%s); }
  clock_gettime(CLOCK, &end);
  elapsed_time_hr(start, end, "FPGA code");
  return {%s};
}
    """ % (numArrays, paramArgsStr, arrsStr, innerParamsStr,
           ompMapStr, callArgsStr, cmJoin(ArrVars))

    return code


def genTestbench(scop, portmap):
    incls = """
#include <stdbool.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>
#include <malloc.h>

#include <iostream>
#include <vector>
#include <array>
#include <array>

#include "orka_hls.h"
#include "orka_validate.h"
#include "orka_input_cli.h"
#include "orka_adept_rand.h"
#include "orka_adept_utils.h"
#include "orka_tiling_util.h"
#include "orka_adept_settings.h"
#include "orka_mem_alloc.hpp"
#include "tlf.hpp"
#include "tlf_normal.hpp"
    """

    numParams = len(scop.getParams())
    paramsStr = cmJoin(["size"] * numParams)

    main = """
int main(int argc, char **argv) {
  int buf[2];
  bool rc = orka_try_get_ints(argc, argv, 2, buf);
  int size = buf[0];
  int reps = buf[1];
  fprintf(stderr, "Run benchmark with size %%d and reps %%d\\n", size, reps);
  if (!rc) {
    fprintf(stderr, "Please pass two numbers. Size and REPS\\n");
    return 0;
  }

  {
    srand(42);
    auto devResult = driver_fpga(%s, reps);
    srand(43);
    auto hostResult = driver_host(%s, reps);
    bool res = validate<float, %s>(devResult, hostResult);
    assert(!res);
  }
  {
    srand(42);
    auto devResult = driver_fpga(%s, reps);
    srand(42);
    auto hostResult = driver_host(%s, reps);
    bool res = validate<float, %s>(devResult, hostResult);
    assert(res);
  }

  return 0;
}
    """ % (paramsStr, paramsStr, len(scop.getArrayInfos()) ,
           paramsStr, paramsStr, len(scop.getArrayInfos()))


    res = incls + NL + genFpgaDriver(scop, portmap) \
        + NL + genHostDriver(scop, portmap) + main + NL
    print(res)
    return res
