
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

Res<float, 2> driver_fpga(int SIZE, unsigned int REPS) {
  std::vector<int> dims0{SIZE, SIZE};
  auto A0 = getAndInitAxiArray<AxiVec4>(dims0, 0, "a0");
  AxiVec4 *a0 = A0->getCastedPtr<AxiVec4>();
  const int a0_size = A0->getOmpMapSize();
  std::vector<int> dims1{SIZE, SIZE};
  auto A1 = getAndInitAxiArray<AxiVec4>(dims1, 0, "a1");
  AxiVec4 *a1 = A1->getCastedPtr<AxiVec4>();
  const int a1_size = A1->getOmpMapSize();
  float fac = RandGen<float>::getRand();
  struct timespec start, end;
  clock_gettime(CLOCK, &start);
#ifdef POLYSAGE
#pragma omp target orkaTranslate(topLevelFunction                              \
                                 : "tlf") map(tofrom                           \
                                              : a0[:a0_size], a1               \
                                                  [:a1_size])
#endif
  { tlf(SIZE, fac, a0, a1); }
  clock_gettime(CLOCK, &end);
  elapsed_time_hr(start, end, "FPGA code");
  return {A0, A1};
}

Res<float, 2> driver_host(int SIZE, unsigned int REPS) {
  std::vector<int> dims0{SIZE, SIZE};
  auto A0 = getAndInitNormalArray<float>(dims0, "a0");
  float *a0 = A0->getPtr();
  const int a0_size = A0->getOmpMapSize();
  std::vector<int> dims1{SIZE, SIZE};
  auto A1 = getAndInitNormalArray<float>(dims1, "a1");
  float *a1 = A1->getPtr();
  const int a1_size = A1->getOmpMapSize();
  float fac = RandGen<float>::getRand();
  struct timespec start, end;
  clock_gettime(CLOCK, &start);
#ifdef BASELINE
#pragma omp target map(tofrom : a0[:a0_size], a1[:a1_size])
#endif
  { tlf_normal(SIZE, fac, a0, a1); }
  clock_gettime(CLOCK, &end);
  elapsed_time_hr(start, end, "HOST code");
  return {A0, A1};
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
    bool res = validate<float, 2>(devResult, hostResult);
    assert(!res);
  }
  {
    srand(42);
    auto devResult = driver_fpga(size, reps);
    srand(42);
    auto hostResult = driver_host(size, reps);
    bool res = validate<float, 2>(devResult, hostResult);
    assert(res);
  }

  return 0;
}
