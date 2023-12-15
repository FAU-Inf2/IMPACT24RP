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
    for (int c3 = 1; c3 < SIZE - 1; c3 += 1) {
      for (int c5 = 1; c5 < SIZE - 1; c5 += 1) {

        B[c5 + ((c3)*SIZE) + ((c1)*SIZE * SIZE)] =
            0.125 * (A[c5 + ((c3)*SIZE) + ((c1 + 1) * SIZE * SIZE)] -
                     2.0 * A[c5 + ((c3)*SIZE) + ((c1)*SIZE * SIZE)] +
                     A[c5 + ((c3)*SIZE) + ((c1 - 1) * SIZE * SIZE)]) +
            0.125 * (A[c5 + ((c3 + 1) * SIZE) + ((c1)*SIZE * SIZE)] -
                     2.0 * A[c5 + ((c3)*SIZE) + ((c1)*SIZE * SIZE)] +
                     A[c5 + ((c3 - 1) * SIZE) + ((c1)*SIZE * SIZE)]) +
            0.125 * (A[c5 + 1 + ((c3)*SIZE) + ((c1)*SIZE * SIZE)] -
                     2.0 * A[c5 + ((c3)*SIZE) + ((c1)*SIZE * SIZE)] +
                     A[c5 - 1 + ((c3)*SIZE) + ((c1)*SIZE * SIZE)]) +
            A[c5 + ((c3)*SIZE) + ((c1)*SIZE * SIZE)];
      }
    }
  }
}
