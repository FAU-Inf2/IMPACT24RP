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

void tlf_normal(int SIZE, float fac, float *A, float *X) {
  for (int c1 = 1; c1 < SIZE - 1; c1 += 1) {
    for (int c3 = 1; c3 < SIZE - 1; c3 += 1) {
      X[c3 + ((c1)*SIZE)] =
          (A[c3 + ((c1 - 1) * SIZE)] + A[c3 + ((c1 + 1) * SIZE)] +
           A[c3 + 1 + ((c1)*SIZE)] + A[c3 - 1 + ((c1)*SIZE)]) *
          fac;
    }
  }
}
