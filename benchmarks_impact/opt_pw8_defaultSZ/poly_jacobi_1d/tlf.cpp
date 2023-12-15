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

static void handleChunk0(int SIZE, hls::burst_maxi<AxiVec8> A,
                         hls::burst_maxi<AxiVec8> B, int c1) {
#pragma HLS PIPELINE

      float A_c[528];
#pragma HLS ARRAY_PARTITION variable = A_c type = complete dim = 1
  float B_c[528];
#pragma HLS ARRAY_PARTITION variable = B_c type = complete dim = 1

  int c2 = 0;

  // Cache load for A at dim i
  if (SIZE >= 3 && c1 % 512 == 0) {
    int len = 0;
    if ((((-512) + SIZE) <= c1 && c1 < SIZE)) {
      len = ((8 * (floor((7 + SIZE) / 8))) - (8 * (floor((7 + c1) / 8))));
    }
    if ((c1 <= ((-513) + SIZE))) {
      len = ((520 + (8 * (floor(c1 / 8)))) - (8 * (floor((7 + c1) / 8))));
    }

    const int leftPad = 0;

    const int compLen = len - leftPad;

    A.read_request((c1 + (0)) / 8, len / 8);

    for (int cc0 = 0; cc0 <= 513; cc0 += 8) {
      if (cc0 < compLen) {
        const AxiVec8 axiTmp = A.read();
        A_c[cc0 + 8] = axiTmp.e0;
        A_c[cc0 + 9] = axiTmp.e1;
        A_c[cc0 + 10] = axiTmp.e2;
        A_c[cc0 + 11] = axiTmp.e3;
        A_c[cc0 + 12] = axiTmp.e4;
        A_c[cc0 + 13] = axiTmp.e5;
        A_c[cc0 + 14] = axiTmp.e6;
        A_c[cc0 + 15] = axiTmp.e7;
      }
    }
  }

  for (c2 = 0; c2 <= 511; c2 += 1) {
    B_c[c2 + 8] = 0.33333 * (A_c[c2 + 8] + A_c[c2 + 1 + 8] + A_c[c2 + 2 + 8]);
  }

  // write back for arr B
  if (SIZE >= 3 && c1 % 512 == 0) {
    int len = 0;
    if ((((-513) + SIZE) <= c1 && c1 <= ((-2) + SIZE))) {
      len = ((8 * (floor((6 + SIZE) / 8))) - (8 * (floor((7 + c1) / 8))));
    }
    if ((c1 <= ((-514) + SIZE))) {
      len = ((520 + (8 * (floor(c1 / 8)))) - (8 * (floor((7 + c1) / 8))));
    }
    int payLen = 0;
    if ((c1 <= ((-515) + SIZE))) {
      payLen = 512;
    }
    if ((((-514) + SIZE) <= c1 && c1 <= ((-3) + SIZE))) {
      payLen = (((-2) + SIZE) - c1);
    }
    int leftPad = 0;
    if ((((c1 % 8) == 0) && (((-513) + SIZE) <= c1 && c1 <= ((-3) + SIZE)))) {
      leftPad = 1;
    }
    if ((((c1 % 8) == 0) && (c1 <= ((-514) + SIZE)))) {
      leftPad = 1;
    }
    const int rightPad = (len - payLen) - leftPad;
    const int compLen = len - leftPad;

    B.write_request((c1 + (-1) + 1) / 8, len / 8);

    for (int cc0 = -1; cc0 <= 511; cc0 += 8) {
      if (cc0 < compLen) {
        AxiVec8 t{B_c[cc0 + 8],  B_c[cc0 + 9],  B_c[cc0 + 10], B_c[cc0 + 11],
                  B_c[cc0 + 12], B_c[cc0 + 13], B_c[cc0 + 14], B_c[cc0 + 15]};
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
        B.write(t, writeStrobe);
      }
    }
    B.write_response();
  }
}

void tlf(int SIZE, hls::burst_maxi<AxiVec8> A, hls::burst_maxi<AxiVec8> B) {
  // partition
  for (int c1 = 0; c1 < SIZE - 2; c1 += 512) {
    handleChunk0(SIZE, A, B, c1);
  }
}
