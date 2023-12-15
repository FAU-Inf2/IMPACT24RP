
#include <assert.h>
#include <malloc.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <array>
#include <iostream>
#include <vector>

#include "orka_adept_rand.h"
#include "orka_adept_settings.h"
#include "orka_adept_utils.h"
#include "orka_hls.h"
#include "orka_input_cli.h"
#include "orka_mem_alloc.hpp"
#include "orka_tiling_util.h"
#include "orka_validate.h"
#include "tlf.hpp"
#include "tlf_normal.hpp"

Res<float, 1> driver_fpga(int SIZE, unsigned int REPS) {
  std::vector<int> dims0{SIZE};
  auto A0 = getAndInitAxiArray<AxiVec8>(dims0, 0, "a0");
  AxiVec8 *a0 = A0->getCastedPtr<AxiVec8>();
  const int a0_size = A0->getOmpMapSize();
  float a = RandGen<float>::getRand();
  struct timespec start, end;
  clock_gettime(CLOCK, &start);
#ifdef POLYSAGE
#pragma omp target orkaTranslate(topLevelFunction                              \
                                 : "tlf") map(tofrom                           \
                                              : a0[:a0_size])
#endif
  { tlf(SIZE, a, a0); }
  clock_gettime(CLOCK, &end);
  elapsed_time_hr(start, end, "FPGA code");
  return {A0};
}

Res<float, 1> driver_host(int SIZE, unsigned int REPS) {
  std::vector<int> dims0{SIZE};
  auto A0 = getAndInitNormalArray<float>(dims0, "a0");
  float *a0 = A0->getPtr();
  const int a0_size = A0->getOmpMapSize();
  float a = RandGen<float>::getRand();
  struct timespec start, end;
  clock_gettime(CLOCK, &start);
#ifdef BASELINE
#pragma omp target map(tofrom : a0[:a0_size])
#endif
  { tlf_normal(SIZE, a, a0); }
  clock_gettime(CLOCK, &end);
  elapsed_time_hr(start, end, "HOST code");
  return {A0};
}

int main(int argc, char **argv) {
  int buf[2];
  bool rc = orka_try_get_ints(argc, argv, 2, buf);
  int size = buf[0];
  int reps = buf[1];
  fprintf(stderr, "Run benchmark with size %d and reps %d\n", size, reps);
  if (!rc) {
    fprintf(stderr, "Please pass two numbers. Size and REPS\n");
    return 0;
  }

  {
    srand(42);
    auto devResult = driver_fpga(size, reps);
    srand(43);
    auto hostResult = driver_host(size, reps);
    bool res = validate<float, 1>(devResult, hostResult);
    assert(!res);
  }
  {
    srand(42);
    auto devResult = driver_fpga(size, reps);
    srand(42);
    auto hostResult = driver_host(size, reps);
    bool res = validate<float, 1>(devResult, hostResult);
    assert(res);
  }

  return 0;
}
