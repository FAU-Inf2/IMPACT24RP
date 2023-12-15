#include "tlf_normal.hpp"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

static int min(int a, int b) { return a <= b ? a : b; }
static int max(int a, int b) { return a <= b ? b : a; }
static int floord(int a, int b) { return a / b; }
static int exp(int a, int b) {
#pragma HLS INLINE
  int res = 1;
  for (int i = 0; i < b; i++) {
    res *= a;
  }
  return res;
}
#define floor(x) (x)

void tlf_normal(int SIZE, float *A, float *B) {
  for (int c1 = 1; c1 < SIZE - 1; c1 += 1) {
    B[c1] = 0.33333 * (A[c1 + 1] + A[c1] + A[c1 + 1]);
  }
}
