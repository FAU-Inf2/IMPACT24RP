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

void tlf_normal(int SIZEX, int SIZEY, float *EY, float *HZ) {
  for (int c1 = 1; c1 < SIZEX; c1 += 1) {
    for (int c3 = 0; c3 < SIZEY; c3 += 1) {
      EY[c3 + ((c1)*SIZEY)] =
          EY[c3 + ((c1)*SIZEY)] -
          0.5 * (HZ[c3 + ((c1)*SIZEY)] - HZ[c3 + ((c1 - 1) * SIZEY)]);
    }
  }
}
