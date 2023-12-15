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

static void handleChunk0(int SIZE, float fac, hls::burst_maxi<AxiVec4> A,
                         hls::burst_maxi<AxiVec4> X, int c1, int c2) {
  float A_c[3][136];
#pragma HLS ARRAY_PARTITION variable = A_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = A_c type = complete dim = 2
  float X_c[1][136];
#pragma HLS ARRAY_PARTITION variable = X_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = X_c type = complete dim = 2

  int c3 = 0;

  // Cache load for A at dim i
  if (SIZE >= 3 && c3 == 0 && c1 % 128 == 0 && c2 % 128 == 0) {
    for (int cc0 = 0; cc0 <= 1; cc0 += 1) {
      int len = 0;
      if ((((-128) + SIZE) <= c2 && c2 < SIZE)) {
        len = ((4 * (floor((3 + SIZE) / 4))) - (4 * (floor((3 + c2) / 4))));
      }
      if ((c2 <= ((-129) + SIZE))) {
        len = ((132 + (4 * (floor(c2 / 4)))) - (4 * (floor((3 + c2) / 4))));
      }

      const int leftPad = 0;

      const int compLen = len - leftPad;

      A.read_request((c2 + (0) + ((c1 + cc0) * SIZE)) / 4, len / 4);

      for (int cc1 = 0; cc1 <= 129; cc1 += 4) {
        if (cc1 < compLen) {
          const AxiVec4 axiTmp = A.read();
          A_c[cc0][cc1 + 4] = axiTmp.e0;
          A_c[cc0][cc1 + 5] = axiTmp.e1;
          A_c[cc0][cc1 + 6] = axiTmp.e2;
          A_c[cc0][cc1 + 7] = axiTmp.e3;
        }
      }
    }
  }

  for (c3 = 0; c3 <= min(127, SIZE - c1 - 3); c3 += 1) {
#pragma HLS PIPELINE

        int c5 = 0;

    // Cache load for A at dim j
    if (SIZE >= 3 && c3 >= 0 && c3 <= 127 && c1 % 128 == 0 && c2 % 128 == 0) {
      int len = 0;
      if ((c2 <= ((-130) + SIZE))) {
        len = ((132 + (4 * (floor(c2 / 4)))) - (4 * (floor((3 + c2) / 4))));
      }
      if ((((-129) + SIZE) <= c2 && c2 < SIZE)) {
        len = ((4 * (floor((3 + SIZE) / 4))) - (4 * (floor((3 + c2) / 4))));
      }

      const int leftPad = 0;

      const int compLen = len - leftPad;

      A.read_request((c2 + (0) + ((c1 + c3 + 2) * SIZE)) / 4, len / 4);

      for (int cc1 = 0; cc1 <= 129; cc1 += 4) {
        if (cc1 < compLen) {
          const AxiVec4 axiTmp = A.read();
          A_c[2][cc1 + 4] = axiTmp.e0;
          A_c[2][cc1 + 5] = axiTmp.e1;
          A_c[2][cc1 + 6] = axiTmp.e2;
          A_c[2][cc1 + 7] = axiTmp.e3;
        }
      }
    }

    for (c5 = 0; c5 <= 127; c5 += 1) {
      X_c[0][c5 + 4] =
          (A_c[1][c5 + 2 + 4] + A_c[2][c5 + 2 + 4] + A_c[2][c5 + 1 + 4] +
           A_c[2][c5 + 4] + A_c[1][c5 + 4] + A_c[0][c5 + 4] +
           A_c[0][c5 + 1 + 4] + A_c[0][c5 + 2 + 4]) *
          fac;
    }

    // write back for arr X
    if (SIZE >= 3 && c3 >= 0 && c3 <= 127 && c1 % 128 == 0 && c2 % 128 == 0) {
      int len = 0;
      if ((c2 <= ((-131) + SIZE))) {
        len = ((132 + (4 * (floor(c2 / 4)))) - (4 * (floor((3 + c2) / 4))));
      }
      if ((((-130) + SIZE) <= c2 && c2 <= ((-2) + SIZE))) {
        len = ((4 * (floor((2 + SIZE) / 4))) - (4 * (floor((3 + c2) / 4))));
      }
      int payLen = 0;
      if ((c2 <= ((-131) + SIZE))) {
        payLen = 128;
      }
      if ((((-130) + SIZE) <= c2 && c2 <= ((-3) + SIZE))) {
        payLen = (((-2) + SIZE) - c2);
      }
      int leftPad = 0;
      if ((((c2 % 4) == 0) && (((-129) + SIZE) <= c2 && c2 <= ((-3) + SIZE)))) {
        leftPad = 1;
      }
      if ((((c2 % 4) == 0) && (c2 <= ((-130) + SIZE)))) {
        leftPad = 1;
      }
      const int rightPad = (len - payLen) - leftPad;
      const int compLen = len - leftPad;

      X.write_request((c2 + (-1) + 1 + ((c1 + c3 + 1) * SIZE)) / 4, len / 4);

      for (int cc1 = -1; cc1 <= 127; cc1 += 4) {
        if (cc1 < compLen) {
          AxiVec4 t{X_c[0][cc1 + 4], X_c[0][cc1 + 5], X_c[0][cc1 + 6],
                    X_c[0][cc1 + 7]};
          ap_int<16> writeStrobe;
          const int s0 = (cc1 + 0 >= 0) - (cc1 + 0 >= payLen);
          const int s1 = (cc1 + 1 >= 0) - (cc1 + 1 >= payLen);
          const int s2 = (cc1 + 2 >= 0) - (cc1 + 2 >= payLen);
          const int s3 = (cc1 + 3 >= 0) - (cc1 + 3 >= payLen);
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
          X.write(t, writeStrobe);
        }
      }
      X.write_response();
    }
    // shift
    if (SIZE >= 3 && c3 >= 0 && c3 <= 127 && c1 % 128 == 0 && c2 % 128 == 0) {
      for (int cc0 = 0; cc0 <= 1; cc0 += 1) {
        for (int cc1 = 0; cc1 <= 129; cc1 += 1) {
          A_c[cc0][cc1 + 4] = A_c[cc0 + 1][cc1 + 4];
        }
      }
    }
  }
}

void tlf(int SIZE, float fac, hls::burst_maxi<AxiVec4> A,
         hls::burst_maxi<AxiVec4> X) {
  // partition
  for (int c1 = 0; c1 < SIZE - 2; c1 += 128) {
    for (int c2 = 0; c2 < SIZE - 2; c2 += 128) {
      handleChunk0(SIZE, fac, A, X, c1, c2);
    }
  }
}
