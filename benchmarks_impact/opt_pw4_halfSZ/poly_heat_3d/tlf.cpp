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

static void handleChunk0(int SIZE, hls::burst_maxi<AxiVec4> A,
                         hls::burst_maxi<AxiVec4> B, int c1, int c2, int c3) {
  float A_c[3][18][24];
#pragma HLS ARRAY_PARTITION variable = A_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = A_c type = complete dim = 2
#pragma HLS ARRAY_PARTITION variable = A_c type = complete dim = 3
  float B_c[1][1][24];
#pragma HLS ARRAY_PARTITION variable = B_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = B_c type = complete dim = 2
#pragma HLS ARRAY_PARTITION variable = B_c type = complete dim = 3

  int c4 = 0;

  // Cache load for A at dim i
  if (SIZE >= 3 && c4 == 0 && c1 % 16 == 0 && c2 % 16 == 0 && c3 % 16 == 0) {
    for (int cc0 = 0; cc0 <= 1; cc0 += 1) {
      for (int cc1 = 0; cc1 <= 17; cc1 += 1) {
        int len = 0;
        if ((c3 <= ((-18) + SIZE))) {
          len = ((20 + (4 * (floor(c3 / 4)))) - (4 * (floor((3 + c3) / 4))));
        }
        if ((((-17) + SIZE) <= c3 && c3 < SIZE)) {
          len = ((4 * (floor((3 + SIZE) / 4))) - (4 * (floor((3 + c3) / 4))));
        }

        const int leftPad = 0;

        const int compLen = len - leftPad;

        A.read_request(
            (c3 + (0) + ((c2 + cc1) * SIZE) + ((c1 + cc0) * SIZE * SIZE)) / 4,
            len / 4);

        for (int cc2 = 0; cc2 <= 17; cc2 += 4) {
          if (cc2 < compLen) {
            const AxiVec4 axiTmp = A.read();
            A_c[cc0][cc1][cc2 + 4] = axiTmp.e0;
            A_c[cc0][cc1][cc2 + 5] = axiTmp.e1;
            A_c[cc0][cc1][cc2 + 6] = axiTmp.e2;
            A_c[cc0][cc1][cc2 + 7] = axiTmp.e3;
          }
        }
      }
    }
  }

  for (c4 = 0; c4 <= min(15, SIZE - c1 - 3); c4 += 1) {

    int c6 = 0;

    // Cache load for A at dim j
    if (SIZE >= 3 && c4 >= 0 && c4 <= 15 && c6 == 0 && c1 % 16 == 0 &&
        c2 % 16 == 0 && c3 % 16 == 0) {
      for (int cc1 = 0; cc1 <= 1; cc1 += 1) {
        int len = 0;
        if ((((-16) + SIZE) <= c3 && c3 < SIZE)) {
          len = ((4 * (floor((3 + SIZE) / 4))) - (4 * (floor((3 + c3) / 4))));
        }
        if ((c3 <= ((-17) + SIZE))) {
          len = ((20 + (4 * (floor(c3 / 4)))) - (4 * (floor((3 + c3) / 4))));
        }

        const int leftPad = 0;

        const int compLen = len - leftPad;

        A.read_request(
            (c3 + (0) + ((c2 + cc1) * SIZE) + ((c1 + c4 + 2) * SIZE * SIZE)) /
                4,
            len / 4);

        for (int cc2 = 0; cc2 <= 17; cc2 += 4) {
          if (cc2 < compLen) {
            const AxiVec4 axiTmp = A.read();
            A_c[2][cc1][cc2 + 4] = axiTmp.e0;
            A_c[2][cc1][cc2 + 5] = axiTmp.e1;
            A_c[2][cc1][cc2 + 6] = axiTmp.e2;
            A_c[2][cc1][cc2 + 7] = axiTmp.e3;
          }
        }
      }
    }

    for (c6 = 0; c6 <= min(15, SIZE - c2 - 3); c6 += 1) {
#pragma HLS PIPELINE

          int c8 = 0;

      // Cache load for A at dim k
      if (SIZE >= 3 && c6 >= 0 && c6 <= 15 && c4 >= 0 && c4 <= 15 &&
          c1 % 16 == 0 && c2 % 16 == 0 && c3 % 16 == 0) {
        int len = 0;
        if ((((-16) + SIZE) <= c3 && c3 < SIZE)) {
          len = ((4 * (floor((3 + SIZE) / 4))) - (4 * (floor((3 + c3) / 4))));
        }
        if ((c3 <= ((-17) + SIZE))) {
          len = ((20 + (4 * (floor(c3 / 4)))) - (4 * (floor((3 + c3) / 4))));
        }

        const int leftPad = 0;

        const int compLen = len - leftPad;

        A.read_request((c3 + (0) + ((c2 + c6 + 2) * SIZE) +
                        ((c1 + c4 + 2) * SIZE * SIZE)) /
                           4,
                       len / 4);

        for (int cc2 = 0; cc2 <= 17; cc2 += 4) {
          if (cc2 < compLen) {
            const AxiVec4 axiTmp = A.read();
            A_c[2][c6 + 2][cc2 + 4] = axiTmp.e0;
            A_c[2][c6 + 2][cc2 + 5] = axiTmp.e1;
            A_c[2][c6 + 2][cc2 + 6] = axiTmp.e2;
            A_c[2][c6 + 2][cc2 + 7] = axiTmp.e3;
          }
        }
      }

      for (c8 = 0; c8 <= 15; c8 += 1) {
        B_c[0][0][c8 + 4] = 0.125 * (A_c[2][c6 + 1][c8 + 1 + 4] -
                                     2.0 * A_c[1][c6 + 1][c8 + 1 + 4] +
                                     A_c[0][c6 + 1][c8 + 1 + 4]) +
                            0.125 * (A_c[1][c6 + 2][c8 + 1 + 4] -
                                     2.0 * A_c[1][c6 + 1][c8 + 1 + 4] +
                                     A_c[1][c6][c8 + 1 + 4]) +
                            0.125 * (A_c[1][c6 + 1][c8 + 2 + 4] -
                                     2.0 * A_c[1][c6 + 1][c8 + 1 + 4] +
                                     A_c[1][c6 + 1][c8 + 4]) +
                            A_c[1][c6 + 1][c8 + 1 + 4];
      }

      // write back for arr B
      if (SIZE >= 3 && c4 >= 0 && c4 <= 15 && c6 >= 0 && c6 <= 15 &&
          c1 % 16 == 0 && c2 % 16 == 0 && c3 % 16 == 0) {
        int len = 0;
        if ((((-17) + SIZE) <= c3 && c3 <= ((-2) + SIZE))) {
          len = ((4 * (floor((2 + SIZE) / 4))) - (4 * (floor((3 + c3) / 4))));
        }
        if ((c3 <= ((-18) + SIZE))) {
          len = ((20 + (4 * (floor(c3 / 4)))) - (4 * (floor((3 + c3) / 4))));
        }
        int payLen = 0;
        if ((c3 <= ((-19) + SIZE))) {
          payLen = 16;
        }
        if ((((-18) + SIZE) <= c3 && c3 <= ((-3) + SIZE))) {
          payLen = (((-2) + SIZE) - c3);
        }
        int leftPad = 0;
        if ((((c3 % 4) == 0) &&
             (((-17) + SIZE) <= c3 && c3 <= ((-3) + SIZE)))) {
          leftPad = 1;
        }
        if ((((c3 % 4) == 0) && (c3 <= ((-18) + SIZE)))) {
          leftPad = 1;
        }
        const int rightPad = (len - payLen) - leftPad;
        const int compLen = len - leftPad;

        B.write_request((c3 + (-1) + 1 + ((c2 + c6 + 1) * SIZE) +
                         ((c1 + c4 + 1) * SIZE * SIZE)) /
                            4,
                        len / 4);

        for (int cc2 = -1; cc2 <= 15; cc2 += 4) {
          if (cc2 < compLen) {
            AxiVec4 t{B_c[0][0][cc2 + 4], B_c[0][0][cc2 + 5],
                      B_c[0][0][cc2 + 6], B_c[0][0][cc2 + 7]};
            ap_int<16> writeStrobe;
            const int s0 = (cc2 + 0 >= 0) - (cc2 + 0 >= payLen);
            const int s1 = (cc2 + 1 >= 0) - (cc2 + 1 >= payLen);
            const int s2 = (cc2 + 2 >= 0) - (cc2 + 2 >= payLen);
            const int s3 = (cc2 + 3 >= 0) - (cc2 + 3 >= payLen);
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
            B.write(t, writeStrobe);
          }
        }
        B.write_response();
      }
    }

    // shift
    if (SIZE >= 3 && c4 >= 0 && c4 <= 15 && c1 % 16 == 0 && c2 % 16 == 0 &&
        c3 % 16 == 0) {
      for (int cc0 = 0; cc0 <= 1; cc0 += 1) {
        for (int cc1 = 0; cc1 <= 17; cc1 += 1) {
#pragma HLS UNROLL
          for (int cc2 = 0; cc2 <= 17; cc2 += 1) {
            A_c[cc0][cc1][cc2 + 4] = A_c[cc0 + 1][cc1][cc2 + 4];
          }
        }
      }
    }
  }
}

void tlf(int SIZE, hls::burst_maxi<AxiVec4> A, hls::burst_maxi<AxiVec4> B) {
  // partition
  for (int c1 = 0; c1 < SIZE - 2; c1 += 16) {
    for (int c2 = 0; c2 < SIZE - 2; c2 += 16) {
      for (int c3 = 0; c3 < SIZE - 2; c3 += 16) {
        handleChunk0(SIZE, A, B, c1, c2, c3);
      }
    }
  }
}
