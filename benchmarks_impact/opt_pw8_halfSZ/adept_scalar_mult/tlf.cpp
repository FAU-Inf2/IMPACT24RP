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

static void handleChunk0(int SIZE, float a, hls::burst_maxi<AxiVec8> V,
                         int c1) {
#pragma HLS PIPELINE

      float V_c[264];
#pragma HLS ARRAY_PARTITION variable = V_c type = complete dim = 1

  int c2 = 0;

  // Cache load for V at dim i
  if (SIZE >= 1 && c1 % 256 == 0) {
    int len = 0;
    if ((((-248) + SIZE) <= c1 && c1 < SIZE)) {
      len = ((8 * (floor((7 + SIZE) / 8))) - (8 * (floor((7 + c1) / 8))));
    }
    if ((c1 <= ((-249) + SIZE))) {
      len = ((256 + (8 * (floor(c1 / 8)))) - (8 * (floor((7 + c1) / 8))));
    }

    const int leftPad = 0;

    const int compLen = len - leftPad;

    V.read_request((c1 + (0)) / 8, len / 8);

    for (int cc0 = 0; cc0 <= 255; cc0 += 8) {
      if (cc0 < compLen) {
        const AxiVec8 axiTmp = V.read();
        V_c[cc0 + 8] = axiTmp.e0;
        V_c[cc0 + 9] = axiTmp.e1;
        V_c[cc0 + 10] = axiTmp.e2;
        V_c[cc0 + 11] = axiTmp.e3;
        V_c[cc0 + 12] = axiTmp.e4;
        V_c[cc0 + 13] = axiTmp.e5;
        V_c[cc0 + 14] = axiTmp.e6;
        V_c[cc0 + 15] = axiTmp.e7;
      }
    }
  }

  for (c2 = 0; c2 <= 255; c2 += 1) {
    V_c[c2 + 8] = a * V_c[c2 + 8];
  }

  // write back for arr V
  if (SIZE >= 1 && c1 % 256 == 0) {
    int len = 0;
    if ((((-248) + SIZE) <= c1 && c1 < SIZE)) {
      len = ((8 * (floor((7 + SIZE) / 8))) - (8 * (floor((7 + c1) / 8))));
    }
    if ((c1 <= ((-249) + SIZE))) {
      len = ((256 + (8 * (floor(c1 / 8)))) - (8 * (floor((7 + c1) / 8))));
    }
    int payLen = 0;
    if ((c1 <= ((-257) + SIZE))) {
      payLen = 256;
    }
    if ((((-256) + SIZE) <= c1 && c1 < SIZE)) {
      payLen = (SIZE - c1);
    }
    const int leftPad = 0;
    const int rightPad = (len - payLen) - leftPad;
    const int compLen = len - leftPad;

    V.write_request((c1 + (0)) / 8, len / 8);

    for (int cc0 = 0; cc0 <= 255; cc0 += 8) {
      if (cc0 < compLen) {
        AxiVec8 t{V_c[cc0 + 8],  V_c[cc0 + 9],  V_c[cc0 + 10], V_c[cc0 + 11],
                  V_c[cc0 + 12], V_c[cc0 + 13], V_c[cc0 + 14], V_c[cc0 + 15]};
        ap_int<32> writeStrobe;
        const int s0 = (cc0 + 0 >= 0) - (cc0 + 0 >= payLen);
        const int s1 = (cc0 + 1 >= 0) - (cc0 + 1 >= payLen);
        const int s2 = (cc0 + 2 >= 0) - (cc0 + 2 >= payLen);
        const int s3 = (cc0 + 3 >= 0) - (cc0 + 3 >= payLen);
        const int s4 = (cc0 + 4 >= 0) - (cc0 + 4 >= payLen);
        const int s5 = (cc0 + 5 >= 0) - (cc0 + 5 >= payLen);
        const int s6 = (cc0 + 6 >= 0) - (cc0 + 6 >= payLen);
        const int s7 = (cc0 + 7 >= 0) - (cc0 + 7 >= payLen);
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
        writeStrobe.set_bit(16, s4);
        writeStrobe.set_bit(17, s4);
        writeStrobe.set_bit(18, s4);
        writeStrobe.set_bit(19, s4);
        writeStrobe.set_bit(20, s5);
        writeStrobe.set_bit(21, s5);
        writeStrobe.set_bit(22, s5);
        writeStrobe.set_bit(23, s5);
        writeStrobe.set_bit(24, s6);
        writeStrobe.set_bit(25, s6);
        writeStrobe.set_bit(26, s6);
        writeStrobe.set_bit(27, s6);
        writeStrobe.set_bit(28, s7);
        writeStrobe.set_bit(29, s7);
        writeStrobe.set_bit(30, s7);
        writeStrobe.set_bit(31, s7);
        V.write(t, writeStrobe);
      }
    }
    V.write_response();
  }
}

void tlf(int SIZE, float a, hls::burst_maxi<AxiVec8> V) {
  // partition
  for (int c1 = 0; c1 < SIZE; c1 += 256) {
    handleChunk0(SIZE, a, V, c1);
  }
}
