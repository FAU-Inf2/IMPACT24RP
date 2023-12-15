#include "tlf.hpp"
#include <assert.h>
#include <orka_hls.h>
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

static void handleChunk0(int SIZE, float a, hls::burst_maxi<AxiVec4> V,
                         int c1) {
#pragma HLS PIPELINE

      float V_c[516];
#pragma HLS ARRAY_PARTITION variable = V_c type = complete dim = 1

  int c2 = 0;

  // Cache load for V at dim i
  if (SIZE >= 1 && c1 % 512 == 0) {
    int len = 0;
    if ((((-508) + SIZE) <= c1 && c1 < SIZE)) {
      len = ((4 * (floor((3 + SIZE) / 4))) - (4 * (floor((3 + c1) / 4))));
    }
    if ((c1 <= ((-509) + SIZE))) {
      len = ((512 + (4 * (floor(c1 / 4)))) - (4 * (floor((3 + c1) / 4))));
    }

    const int leftPad = 0;

    const int compLen = len - leftPad;

    V.read_request((c1 + (0)) / 4, len / 4);

    for (int cc0 = 0; cc0 <= 511; cc0 += 4) {
      if (cc0 < compLen) {
        const AxiVec4 axiTmp = V.read();
        V_c[cc0 + 4] = axiTmp.e0;
        V_c[cc0 + 5] = axiTmp.e1;
        V_c[cc0 + 6] = axiTmp.e2;
        V_c[cc0 + 7] = axiTmp.e3;
      }
    }
  }

  for (c2 = 0; c2 <= 511; c2 += 1) {
    V_c[c2 + 4] = a * V_c[c2 + 4];
  }

  // write back for arr V
  if (SIZE >= 1 && c1 % 512 == 0) {
    int len = 0;
    if ((((-508) + SIZE) <= c1 && c1 < SIZE)) {
      len = ((4 * (floor((3 + SIZE) / 4))) - (4 * (floor((3 + c1) / 4))));
    }
    if ((c1 <= ((-509) + SIZE))) {
      len = ((512 + (4 * (floor(c1 / 4)))) - (4 * (floor((3 + c1) / 4))));
    }
    int payLen = 0;
    if ((c1 <= ((-513) + SIZE))) {
      payLen = 512;
    }
    if ((((-512) + SIZE) <= c1 && c1 < SIZE)) {
      payLen = (SIZE - c1);
    }
    const int leftPad = 0;
    const int rightPad = (len - payLen) - leftPad;
    const int compLen = len - leftPad;

    V.write_request((c1 + (0)) / 4, len / 4);

    for (int cc0 = 0; cc0 <= 511; cc0 += 4) {
      if (cc0 < compLen) {
        AxiVec4 t{V_c[cc0 + 4], V_c[cc0 + 5], V_c[cc0 + 6], V_c[cc0 + 7]};
        ap_int<16> writeStrobe;
        const int s0 = (cc0 + 0 >= 0) - (cc0 + 0 >= payLen);
        const int s1 = (cc0 + 1 >= 0) - (cc0 + 1 >= payLen);
        const int s2 = (cc0 + 2 >= 0) - (cc0 + 2 >= payLen);
        const int s3 = (cc0 + 3 >= 0) - (cc0 + 3 >= payLen);
        writeStrobe.set_bit(0, s0);
        writeStrobe.set_bit(1, s0);
        writeStrobe.set_bit(2, s0);
        writeStrobe.set_bit(3, s0);
        writeStrobe.set_bit(4, s1);
        writeStrobe.set_bit(5, s1);
        writeStrobe.set_bit(6, s1);
        writeStrobe.set_bit(7, s1);
        writeStrobe.set_bit(8, s2);
        writeStrobe.set_bit(9, s2);
        writeStrobe.set_bit(10, s2);
        writeStrobe.set_bit(11, s2);
        writeStrobe.set_bit(12, s3);
        writeStrobe.set_bit(13, s3);
        writeStrobe.set_bit(14, s3);
        writeStrobe.set_bit(15, s3);
        V.write(t, writeStrobe);
      }
    }
    V.write_response();
  }
}

void tlf(int SIZE, float a, hls::burst_maxi<AxiVec4> V) {
  // partition
  for (int c1 = 0; c1 < SIZE; c1 += 512) {
    handleChunk0(SIZE, a, V, c1);
  }
}
