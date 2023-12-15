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

static void handleChunk0(int SIZE, float fac, hls::burst_maxi<AxiVec16> A0,
                         hls::burst_maxi<AxiVec16> A1, int c1, int c2, int c3) {
  float A0_c[3][34][64];
#pragma HLS ARRAY_PARTITION variable = A0_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = A0_c type = complete dim = 2
#pragma HLS ARRAY_PARTITION variable = A0_c type = complete dim = 3
  float A1_c[1][1][64];
#pragma HLS ARRAY_PARTITION variable = A1_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = A1_c type = complete dim = 2
#pragma HLS ARRAY_PARTITION variable = A1_c type = complete dim = 3

  int c4 = 0;

  // Cache load for A0 at dim i
  if (SIZE >= 3 && c4 == 0 && c1 % 32 == 0 && c2 % 32 == 0 && c3 % 32 == 0) {
    for (int cc0 = 0; cc0 <= 1; cc0 += 1) {
      for (int cc1 = 0; cc1 <= 33; cc1 += 1) {
        int len = 0;
        if ((c3 <= ((-34) + SIZE))) {
          len =
              ((48 + (16 * (floor(c3 / 16)))) - (16 * (floor((15 + c3) / 16))));
        }
        if ((((-33) + SIZE) <= c3 && c3 < SIZE)) {
          len = ((16 * (floor((15 + SIZE) / 16))) -
                 (16 * (floor((15 + c3) / 16))));
        }

        const int leftPad = 0;

        const int compLen = len - leftPad;

        A0.read_request(
            (c3 + (0) + ((c2 + cc1) * SIZE) + ((c1 + cc0) * SIZE * SIZE)) / 16,
            len / 16);

        for (int cc2 = 0; cc2 <= 33; cc2 += 16) {
          if (cc2 < compLen) {
            const AxiVec16 axiTmp = A0.read();
            A0_c[cc0][cc1][cc2 + 16] = axiTmp.e0;
            A0_c[cc0][cc1][cc2 + 17] = axiTmp.e1;
            A0_c[cc0][cc1][cc2 + 18] = axiTmp.e2;
            A0_c[cc0][cc1][cc2 + 19] = axiTmp.e3;
            A0_c[cc0][cc1][cc2 + 20] = axiTmp.e4;
            A0_c[cc0][cc1][cc2 + 21] = axiTmp.e5;
            A0_c[cc0][cc1][cc2 + 22] = axiTmp.e6;
            A0_c[cc0][cc1][cc2 + 23] = axiTmp.e7;
            A0_c[cc0][cc1][cc2 + 24] = axiTmp.e8;
            A0_c[cc0][cc1][cc2 + 25] = axiTmp.e9;
            A0_c[cc0][cc1][cc2 + 26] = axiTmp.e10;
            A0_c[cc0][cc1][cc2 + 27] = axiTmp.e11;
            A0_c[cc0][cc1][cc2 + 28] = axiTmp.e12;
            A0_c[cc0][cc1][cc2 + 29] = axiTmp.e13;
            A0_c[cc0][cc1][cc2 + 30] = axiTmp.e14;
            A0_c[cc0][cc1][cc2 + 31] = axiTmp.e15;
          }
        }
      }
    }
  }

  for (c4 = 0; c4 <= min(31, SIZE - c1 - 3); c4 += 1) {

    int c6 = 0;

    // Cache load for A0 at dim j
    if (SIZE >= 3 && c4 >= 0 && c4 <= 31 && c6 == 0 && c1 % 32 == 0 &&
        c2 % 32 == 0 && c3 % 32 == 0) {
      for (int cc1 = 0; cc1 <= 1; cc1 += 1) {
        int len = 0;
        if ((((-32) + SIZE) <= c3 && c3 < SIZE)) {
          len = ((16 * (floor((15 + SIZE) / 16))) -
                 (16 * (floor((15 + c3) / 16))));
        }
        if ((c3 <= ((-33) + SIZE))) {
          len =
              ((48 + (16 * (floor(c3 / 16)))) - (16 * (floor((15 + c3) / 16))));
        }

        const int leftPad = 0;

        const int compLen = len - leftPad;

        A0.read_request(
            (c3 + (0) + ((c2 + cc1) * SIZE) + ((c1 + c4 + 2) * SIZE * SIZE)) /
                16,
            len / 16);

        for (int cc2 = 0; cc2 <= 33; cc2 += 16) {
          if (cc2 < compLen) {
            const AxiVec16 axiTmp = A0.read();
            A0_c[2][cc1][cc2 + 16] = axiTmp.e0;
            A0_c[2][cc1][cc2 + 17] = axiTmp.e1;
            A0_c[2][cc1][cc2 + 18] = axiTmp.e2;
            A0_c[2][cc1][cc2 + 19] = axiTmp.e3;
            A0_c[2][cc1][cc2 + 20] = axiTmp.e4;
            A0_c[2][cc1][cc2 + 21] = axiTmp.e5;
            A0_c[2][cc1][cc2 + 22] = axiTmp.e6;
            A0_c[2][cc1][cc2 + 23] = axiTmp.e7;
            A0_c[2][cc1][cc2 + 24] = axiTmp.e8;
            A0_c[2][cc1][cc2 + 25] = axiTmp.e9;
            A0_c[2][cc1][cc2 + 26] = axiTmp.e10;
            A0_c[2][cc1][cc2 + 27] = axiTmp.e11;
            A0_c[2][cc1][cc2 + 28] = axiTmp.e12;
            A0_c[2][cc1][cc2 + 29] = axiTmp.e13;
            A0_c[2][cc1][cc2 + 30] = axiTmp.e14;
            A0_c[2][cc1][cc2 + 31] = axiTmp.e15;
          }
        }
      }
    }

    for (c6 = 0; c6 <= min(31, SIZE - c2 - 3); c6 += 1) {
#pragma HLS PIPELINE

          int c8 = 0;

      // Cache load for A0 at dim k
      if (SIZE >= 3 && c6 >= 0 && c6 <= 31 && c4 >= 0 && c4 <= 31 &&
          c1 % 32 == 0 && c2 % 32 == 0 && c3 % 32 == 0) {
        int len = 0;
        if ((((c3 % 32) == 0) && (0 <= c3 && c3 <= ((-35) + SIZE)))) {
          len = 48;
        }
        if ((((c3 % 32) == 0) && (((-33) + SIZE) <= c3 && c3 < SIZE))) {
          len = ((-c3) + (16 * (floor((480 + (32 * SIZE)) / 512))));
        }
        if (((c3 == ((-34) + SIZE)) && ((((-2) + SIZE) % 32) == 0))) {
          len = 48;
        }

        const int leftPad = 0;

        const int compLen = len - leftPad;

        A0.read_request((c3 + (0) + ((c2 + c6 + 2) * SIZE) +
                         ((c1 + c4 + 2) * SIZE * SIZE)) /
                            16,
                        len / 16);

        for (int cc2 = 0; cc2 <= 33; cc2 += 16) {
          if (cc2 < compLen) {
            const AxiVec16 axiTmp = A0.read();
            A0_c[2][c6 + 2][cc2 + 16] = axiTmp.e0;
            A0_c[2][c6 + 2][cc2 + 17] = axiTmp.e1;
            A0_c[2][c6 + 2][cc2 + 18] = axiTmp.e2;
            A0_c[2][c6 + 2][cc2 + 19] = axiTmp.e3;
            A0_c[2][c6 + 2][cc2 + 20] = axiTmp.e4;
            A0_c[2][c6 + 2][cc2 + 21] = axiTmp.e5;
            A0_c[2][c6 + 2][cc2 + 22] = axiTmp.e6;
            A0_c[2][c6 + 2][cc2 + 23] = axiTmp.e7;
            A0_c[2][c6 + 2][cc2 + 24] = axiTmp.e8;
            A0_c[2][c6 + 2][cc2 + 25] = axiTmp.e9;
            A0_c[2][c6 + 2][cc2 + 26] = axiTmp.e10;
            A0_c[2][c6 + 2][cc2 + 27] = axiTmp.e11;
            A0_c[2][c6 + 2][cc2 + 28] = axiTmp.e12;
            A0_c[2][c6 + 2][cc2 + 29] = axiTmp.e13;
            A0_c[2][c6 + 2][cc2 + 30] = axiTmp.e14;
            A0_c[2][c6 + 2][cc2 + 31] = axiTmp.e15;
          }
        }
      }

      for (c8 = 0; c8 <= 31; c8 += 1) {
        A1_c[0][0][c8 + 16] =
            (A0_c[1][c6][c8 + 1 + 16] + A0_c[1][c6 + 2][c8 + 1 + 16] +
             A0_c[0][c6 + 1][c8 + 1 + 16] + A0_c[2][c6 + 1][c8 + 1 + 16] +
             A0_c[0][c6][c8 + 1 + 16] + A0_c[0][c6 + 2][c8 + 1 + 16] +
             A0_c[2][c6][c8 + 1 + 16] + A0_c[2][c6 + 2][c8 + 1 + 16] +
             A0_c[1][c6][c8 + 16] + A0_c[1][c6 + 2][c8 + 16] +
             A0_c[0][c6 + 1][c8 + 16] + A0_c[2][c6 + 1][c8 + 16] +
             A0_c[1][c6][c8 + 2 + 16] + A0_c[1][c6 + 2][c8 + 2 + 16] +
             A0_c[0][c6 + 1][c8 + 2 + 16] + A0_c[2][c6 + 1][c8 + 2 + 16] +
             A0_c[1][c6 + 1][c8 + 16] + A0_c[1][c6 + 1][c8 + 2 + 16]) *
            fac;
      }

      // write back for arr A1
      if (SIZE >= 3 && c4 >= 0 && c4 <= 31 && c6 >= 0 && c6 <= 31 &&
          c1 % 32 == 0 && c2 % 32 == 0 && c3 % 32 == 0) {
        int len = 0;
        if ((((-33) + SIZE) <= c3 && c3 <= ((-2) + SIZE))) {
          len = ((16 * (floor((14 + SIZE) / 16))) -
                 (16 * (floor((15 + c3) / 16))));
        }
        if ((c3 <= ((-34) + SIZE))) {
          len =
              ((48 + (16 * (floor(c3 / 16)))) - (16 * (floor((15 + c3) / 16))));
        }
        int payLen = 0;
        if ((c3 <= ((-35) + SIZE))) {
          payLen = 32;
        }
        if ((((-34) + SIZE) <= c3 && c3 <= ((-3) + SIZE))) {
          payLen = (((-2) + SIZE) - c3);
        }
        int leftPad = 0;
        if ((((c3 % 16) == 0) &&
             (((-33) + SIZE) <= c3 && c3 <= ((-3) + SIZE)))) {
          leftPad = 1;
        }
        if ((((c3 % 16) == 0) && (c3 <= ((-34) + SIZE)))) {
          leftPad = 1;
        }
        const int rightPad = (len - payLen) - leftPad;
        const int compLen = len - leftPad;

        A1.write_request((c3 + (-1) + 1 + ((c2 + c6 + 1) * SIZE) +
                          ((c1 + c4 + 1) * SIZE * SIZE)) /
                             16,
                         len / 16);

        for (int cc2 = -1; cc2 <= 31; cc2 += 16) {
          if (cc2 < compLen) {
            AxiVec16 t{A1_c[0][0][cc2 + 16], A1_c[0][0][cc2 + 17],
                       A1_c[0][0][cc2 + 18], A1_c[0][0][cc2 + 19],
                       A1_c[0][0][cc2 + 20], A1_c[0][0][cc2 + 21],
                       A1_c[0][0][cc2 + 22], A1_c[0][0][cc2 + 23],
                       A1_c[0][0][cc2 + 24], A1_c[0][0][cc2 + 25],
                       A1_c[0][0][cc2 + 26], A1_c[0][0][cc2 + 27],
                       A1_c[0][0][cc2 + 28], A1_c[0][0][cc2 + 29],
                       A1_c[0][0][cc2 + 30], A1_c[0][0][cc2 + 31]};
            ap_int<64> writeStrobe;
            const int s0 = (cc2 + 0 >= 0) - (cc2 + 0 >= payLen);
            const int s1 = (cc2 + 1 >= 0) - (cc2 + 1 >= payLen);
            const int s2 = (cc2 + 2 >= 0) - (cc2 + 2 >= payLen);
            const int s3 = (cc2 + 3 >= 0) - (cc2 + 3 >= payLen);
            const int s4 = (cc2 + 4 >= 0) - (cc2 + 4 >= payLen);
            const int s5 = (cc2 + 5 >= 0) - (cc2 + 5 >= payLen);
            const int s6 = (cc2 + 6 >= 0) - (cc2 + 6 >= payLen);
            const int s7 = (cc2 + 7 >= 0) - (cc2 + 7 >= payLen);
            const int s8 = (cc2 + 8 >= 0) - (cc2 + 8 >= payLen);
            const int s9 = (cc2 + 9 >= 0) - (cc2 + 9 >= payLen);
            const int s10 = (cc2 + 10 >= 0) - (cc2 + 10 >= payLen);
            const int s11 = (cc2 + 11 >= 0) - (cc2 + 11 >= payLen);
            const int s12 = (cc2 + 12 >= 0) - (cc2 + 12 >= payLen);
            const int s13 = (cc2 + 13 >= 0) - (cc2 + 13 >= payLen);
            const int s14 = (cc2 + 14 >= 0) - (cc2 + 14 >= payLen);
            const int s15 = (cc2 + 15 >= 0) - (cc2 + 15 >= payLen);
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
            writeStrobe.set_bit(32, s8);
            writeStrobe.set_bit(33, s8);
            writeStrobe.set_bit(34, s8);
            writeStrobe.set_bit(35, s8);
            writeStrobe.set_bit(36, s9);
            writeStrobe.set_bit(37, s9);
            writeStrobe.set_bit(38, s9);
            writeStrobe.set_bit(39, s9);
            writeStrobe.set_bit(40, s10);
            writeStrobe.set_bit(41, s10);
            writeStrobe.set_bit(42, s10);
            writeStrobe.set_bit(43, s10);
            writeStrobe.set_bit(44, s11);
            writeStrobe.set_bit(45, s11);
            writeStrobe.set_bit(46, s11);
            writeStrobe.set_bit(47, s11);
            writeStrobe.set_bit(48, s12);
            writeStrobe.set_bit(49, s12);
            writeStrobe.set_bit(50, s12);
            writeStrobe.set_bit(51, s12);
            writeStrobe.set_bit(52, s13);
            writeStrobe.set_bit(53, s13);
            writeStrobe.set_bit(54, s13);
            writeStrobe.set_bit(55, s13);
            writeStrobe.set_bit(56, s14);
            writeStrobe.set_bit(57, s14);
            writeStrobe.set_bit(58, s14);
            writeStrobe.set_bit(59, s14);
            writeStrobe.set_bit(60, s15);
            writeStrobe.set_bit(61, s15);
            writeStrobe.set_bit(62, s15);
            writeStrobe.set_bit(63, s15);
            A1.write(t, writeStrobe);
          }
        }
        A1.write_response();
      }
    }

    // shift
    if (SIZE >= 3 && c4 >= 0 && c4 <= 31 && c1 % 32 == 0 && c2 % 32 == 0 &&
        c3 % 32 == 0) {
      for (int cc0 = 0; cc0 <= 1; cc0 += 1) {
        for (int cc1 = 0; cc1 <= 33; cc1 += 1) {
#pragma HLS UNROLL
          for (int cc2 = 0; cc2 <= 33; cc2 += 1) {
            A0_c[cc0][cc1][cc2 + 16] = A0_c[cc0 + 1][cc1][cc2 + 16];
          }
        }
      }
    }
  }
}

void tlf(int SIZE, float fac, hls::burst_maxi<AxiVec16> A0,
         hls::burst_maxi<AxiVec16> A1) {
  // partition
  for (int c1 = 0; c1 < SIZE - 2; c1 += 32) {
    for (int c2 = 0; c2 < SIZE - 2; c2 += 32) {
      for (int c3 = 0; c3 < SIZE - 2; c3 += 32) {
        handleChunk0(SIZE, fac, A0, A1, c1, c2, c3);
      }
    }
  }
}
