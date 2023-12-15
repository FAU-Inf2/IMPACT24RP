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

static void handleChunk0(int SIZE, float fac, hls::burst_maxi<AxiVec8> A,
                         hls::burst_maxi<AxiVec8> X, int c1, int c2) {
  float A_c[3][80];
#pragma HLS ARRAY_PARTITION variable = A_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = A_c type = complete dim = 2
  float X_c[1][80];
#pragma HLS ARRAY_PARTITION variable = X_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = X_c type = complete dim = 2

  int c3 = 0;

  // Cache load for A at dim i
  if (SIZE >= 3 && c3 == 0 && c1 % 64 == 0 && c2 % 64 == 0) {
    for (int cc0 = 0; cc0 <= 1; cc0 += 1) {
      int len = 0;
      if ((((-64) + SIZE) <= c2 && c2 < SIZE)) {
        len = ((8 * (floor((7 + SIZE) / 8))) - (8 * (floor((7 + c2) / 8))));
      }
      if ((c2 <= ((-65) + SIZE))) {
        len = ((72 + (8 * (floor(c2 / 8)))) - (8 * (floor((7 + c2) / 8))));
      }

      const int leftPad = 0;

      const int compLen = len - leftPad;

      A.read_request((c2 + (0) + ((c1 + cc0) * SIZE)) / 8, len / 8);

      for (int cc1 = 0; cc1 <= 65; cc1 += 8) {
        if (cc1 < compLen) {
          const AxiVec8 axiTmp = A.read();
          A_c[cc0][cc1 + 8] = axiTmp.e0;
          A_c[cc0][cc1 + 9] = axiTmp.e1;
          A_c[cc0][cc1 + 10] = axiTmp.e2;
          A_c[cc0][cc1 + 11] = axiTmp.e3;
          A_c[cc0][cc1 + 12] = axiTmp.e4;
          A_c[cc0][cc1 + 13] = axiTmp.e5;
          A_c[cc0][cc1 + 14] = axiTmp.e6;
          A_c[cc0][cc1 + 15] = axiTmp.e7;
        }
      }
    }
  }

  for (c3 = 0; c3 <= min(63, SIZE - c1 - 3); c3 += 1) {
#pragma HLS PIPELINE

        int c5 = 0;

    // Cache load for A at dim j
    if (SIZE >= 3 && c3 >= 0 && c3 <= 63 && c1 % 64 == 0 && c2 % 64 == 0) {
      int len = 0;
      if ((c2 <= ((-66) + SIZE))) {
        len = ((72 + (8 * (floor(c2 / 8)))) - (8 * (floor((7 + c2) / 8))));
      }
      if ((((-65) + SIZE) <= c2 && c2 < SIZE)) {
        len = ((8 * (floor((7 + SIZE) / 8))) - (8 * (floor((7 + c2) / 8))));
      }

      const int leftPad = 0;

      const int compLen = len - leftPad;

      A.read_request((c2 + (0) + ((c1 + c3 + 2) * SIZE)) / 8, len / 8);

      for (int cc1 = 0; cc1 <= 65; cc1 += 8) {
        if (cc1 < compLen) {
          const AxiVec8 axiTmp = A.read();
          A_c[2][cc1 + 8] = axiTmp.e0;
          A_c[2][cc1 + 9] = axiTmp.e1;
          A_c[2][cc1 + 10] = axiTmp.e2;
          A_c[2][cc1 + 11] = axiTmp.e3;
          A_c[2][cc1 + 12] = axiTmp.e4;
          A_c[2][cc1 + 13] = axiTmp.e5;
          A_c[2][cc1 + 14] = axiTmp.e6;
          A_c[2][cc1 + 15] = axiTmp.e7;
        }
      }
    }

    for (c5 = 0; c5 <= min(63, SIZE - c1 - 1); c5 += 1) {
      X_c[0][c5 + 8] =
          (A_c[1][c5 + 2 + 8] + A_c[2][c5 + 2 + 8] + A_c[2][c5 + 1 + 8] +
           A_c[2][c5 + 8] + A_c[1][c5 + 8] + A_c[0][c5 + 8] +
           A_c[0][c5 + 1 + 8] + A_c[0][c5 + 2 + 8]) *
          fac;
    }

    // write back for arr X
    if (SIZE >= 3 && c3 >= 0 && c3 <= 63 && c1 % 64 == 0 && c2 % 64 == 0) {
      int len = 0;
      if ((c2 <= ((-67) + SIZE))) {
        len = ((72 + (8 * (floor(c2 / 8)))) - (8 * (floor((7 + c2) / 8))));
      }
      if ((((-66) + SIZE) <= c2 && c2 <= ((-2) + SIZE))) {
        len = ((8 * (floor((6 + SIZE) / 8))) - (8 * (floor((7 + c2) / 8))));
      }
      int payLen = 0;
      if ((c2 <= ((-67) + SIZE))) {
        payLen = 64;
      }
      if ((((-66) + SIZE) <= c2 && c2 <= ((-3) + SIZE))) {
        payLen = (((-2) + SIZE) - c2);
      }
      int leftPad = 0;
      if ((((c2 % 8) == 0) && (((-65) + SIZE) <= c2 && c2 <= ((-3) + SIZE)))) {
        leftPad = 1;
      }
      if ((((c2 % 8) == 0) && (c2 <= ((-66) + SIZE)))) {
        leftPad = 1;
      }
      const int rightPad = (len - payLen) - leftPad;
      const int compLen = len - leftPad;

      X.write_request((c2 + (-1) + 1 + ((c1 + c3 + 1) * SIZE)) / 8, len / 8);

      for (int cc1 = -1; cc1 <= 63; cc1 += 8) {
        if (cc1 < compLen) {
          AxiVec8 t{X_c[0][cc1 + 8],  X_c[0][cc1 + 9],  X_c[0][cc1 + 10],
                    X_c[0][cc1 + 11], X_c[0][cc1 + 12], X_c[0][cc1 + 13],
                    X_c[0][cc1 + 14], X_c[0][cc1 + 15]};
          ap_int<32> writeStrobe;
          const int s0 = (cc1 + 0 >= 0) - (cc1 + 0 >= payLen);
          const int s1 = (cc1 + 1 >= 0) - (cc1 + 1 >= payLen);
          const int s2 = (cc1 + 2 >= 0) - (cc1 + 2 >= payLen);
          const int s3 = (cc1 + 3 >= 0) - (cc1 + 3 >= payLen);
          const int s4 = (cc1 + 4 >= 0) - (cc1 + 4 >= payLen);
          const int s5 = (cc1 + 5 >= 0) - (cc1 + 5 >= payLen);
          const int s6 = (cc1 + 6 >= 0) - (cc1 + 6 >= payLen);
          const int s7 = (cc1 + 7 >= 0) - (cc1 + 7 >= payLen);
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
          X.write(t, writeStrobe);
        }
      }
      X.write_response();
    }
    // shift
    if (SIZE >= 3 && c3 >= 0 && c3 <= 63 && c1 % 64 == 0 && c2 % 64 == 0) {
      for (int cc0 = 0; cc0 <= 1; cc0 += 1) {
        for (int cc1 = 0; cc1 <= 65; cc1 += 1) {
          A_c[cc0][cc1 + 8] = A_c[cc0 + 1][cc1 + 8];
        }
      }
    }
  }
}

void tlf(int SIZE, float fac, hls::burst_maxi<AxiVec8> A,
         hls::burst_maxi<AxiVec8> X) {
  // partition
  for (int c1 = 0; c1 < SIZE - 2; c1 += 64) {
    for (int c2 = 0; c2 < SIZE - 2; c2 += 64) {
      handleChunk0(SIZE, fac, A, X, c1, c2);
    }
  }
}
