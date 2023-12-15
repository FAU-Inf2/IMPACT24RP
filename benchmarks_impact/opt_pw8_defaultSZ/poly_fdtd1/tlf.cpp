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

static void handleChunk0(int SIZEX, int SIZEY, hls::burst_maxi<AxiVec8> EX,
                         hls::burst_maxi<AxiVec8> HZ, int c1, int c2) {
  float EX_c[1][80];
#pragma HLS ARRAY_PARTITION variable = EX_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = EX_c type = complete dim = 2
  float HZ_c[1][80];
#pragma HLS ARRAY_PARTITION variable = HZ_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = HZ_c type = complete dim = 2

  int c3 = 0;

  // Cache load for EX at dim i
  {

  }

  // Cache load for HZ at dim i
  {}

  for (c3 = 0; c3 <= min(63, SIZEX - c1 - 1); c3 += 1) {
#pragma HLS PIPELINE

        int c5 = 0;

    // Cache load for EX at dim j
    if (SIZEX >= 1 && SIZEY >= 2 && c3 >= 0 && c3 <= 63 && c1 % 64 == 0 &&
        c2 % 64 == 0) {
      int len = 0;
      if ((c2 <= ((-66) + SIZEY))) {
        len = ((72 + (8 * (floor(c2 / 8)))) - (8 * (floor((7 + c2) / 8))));
      }
      if ((((-65) + SIZEY) <= c2 && c2 < SIZEY)) {
        len = ((8 * (floor((7 + SIZEY) / 8))) - (8 * (floor((7 + c2) / 8))));
      }

      int leftPad = 0;
      if ((((c2 % 8) == 0) &&
           (((-64) + SIZEY) <= c2 && c2 <= ((-2) + SIZEY)))) {
        leftPad = 1;
      }
      if ((((c2 % 8) == 0) && (c2 <= ((-65) + SIZEY)))) {
        leftPad = 1;
      }

      const int compLen = len - leftPad;

      EX.read_request((c2 + (-1) + 1 + ((c1 + c3) * SIZEY)) / 8, len / 8);

      for (int cc1 = -1; cc1 <= 63; cc1 += 8) {
        if (cc1 < compLen) {
          const AxiVec8 axiTmp = EX.read();
          EX_c[0][cc1 + 8] = axiTmp.e0;
          EX_c[0][cc1 + 9] = axiTmp.e1;
          EX_c[0][cc1 + 10] = axiTmp.e2;
          EX_c[0][cc1 + 11] = axiTmp.e3;
          EX_c[0][cc1 + 12] = axiTmp.e4;
          EX_c[0][cc1 + 13] = axiTmp.e5;
          EX_c[0][cc1 + 14] = axiTmp.e6;
          EX_c[0][cc1 + 15] = axiTmp.e7;
        }
      }
    }
    // Cache load for HZ at dim j
    if (SIZEX >= 1 && SIZEY >= 2 && c3 >= 0 && c3 <= 63 && c1 % 64 == 0 &&
        c2 % 64 == 0) {
      int len = 0;
      if ((c2 <= ((-66) + SIZEY))) {
        len = ((72 + (8 * (floor(c2 / 8)))) - (8 * (floor((7 + c2) / 8))));
      }
      if ((((-65) + SIZEY) <= c2 && c2 < SIZEY)) {
        len = ((8 * (floor((7 + SIZEY) / 8))) - (8 * (floor((7 + c2) / 8))));
      }

      const int leftPad = 0;

      const int compLen = len - leftPad;

      HZ.read_request((c2 + (0) + ((c1 + c3) * SIZEY)) / 8, len / 8);

      for (int cc1 = 0; cc1 <= 64; cc1 += 8) {
        if (cc1 < compLen) {
          const AxiVec8 axiTmp = HZ.read();
          HZ_c[0][cc1 + 8] = axiTmp.e0;
          HZ_c[0][cc1 + 9] = axiTmp.e1;
          HZ_c[0][cc1 + 10] = axiTmp.e2;
          HZ_c[0][cc1 + 11] = axiTmp.e3;
          HZ_c[0][cc1 + 12] = axiTmp.e4;
          HZ_c[0][cc1 + 13] = axiTmp.e5;
          HZ_c[0][cc1 + 14] = axiTmp.e6;
          HZ_c[0][cc1 + 15] = axiTmp.e7;
        }
      }
    }

    for (c5 = 0; c5 <= 63; c5 += 1) {
      EX_c[0][c5 + 8] =
          EX_c[0][c5 + 8] - 0.5 * (HZ_c[0][c5 + 1 + 8] - HZ_c[0][c5 + 8]);
    }

    // write back for arr EX
    if (SIZEX >= 1 && SIZEY >= 2 && c3 >= 0 && c3 <= 63 && c1 % 64 == 0 &&
        c2 % 64 == 0) {
      int len = 0;
      if ((c2 <= ((-66) + SIZEY))) {
        len = ((72 + (8 * (floor(c2 / 8)))) - (8 * (floor((7 + c2) / 8))));
      }
      if ((((-65) + SIZEY) <= c2 && c2 < SIZEY)) {
        len = ((8 * (floor((7 + SIZEY) / 8))) - (8 * (floor((7 + c2) / 8))));
      }
      int payLen = 0;
      if ((c2 <= ((-66) + SIZEY))) {
        payLen = 64;
      }
      if ((((-65) + SIZEY) <= c2 && c2 <= ((-2) + SIZEY))) {
        payLen = (((-1) + SIZEY) - c2);
      }
      int leftPad = 0;
      if ((((c2 % 8) == 0) &&
           (((-64) + SIZEY) <= c2 && c2 <= ((-2) + SIZEY)))) {
        leftPad = 1;
      }
      if ((((c2 % 8) == 0) && (c2 <= ((-65) + SIZEY)))) {
        leftPad = 1;
      }
      const int rightPad = (len - payLen) - leftPad;
      const int compLen = len - leftPad;

      EX.write_request((c2 + (-1) + 1 + ((c1 + c3) * SIZEY)) / 8, len / 8);

      for (int cc1 = -1; cc1 <= 63; cc1 += 8) {
        if (cc1 < compLen) {
          AxiVec8 t{EX_c[0][cc1 + 8],  EX_c[0][cc1 + 9],  EX_c[0][cc1 + 10],
                    EX_c[0][cc1 + 11], EX_c[0][cc1 + 12], EX_c[0][cc1 + 13],
                    EX_c[0][cc1 + 14], EX_c[0][cc1 + 15]};
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
          EX.write(t, writeStrobe);
        }
      }
      EX.write_response();
    }
    // shift
    {

    }

    // shift
    {}
  }
}

void tlf(int SIZEX, int SIZEY, hls::burst_maxi<AxiVec8> EX,
         hls::burst_maxi<AxiVec8> HZ) {
  // partition
  for (int c1 = 0; c1 < SIZEX; c1 += 64) {
    for (int c2 = 0; c2 < SIZEY - 1; c2 += 64) {
      handleChunk0(SIZEX, SIZEY, EX, HZ, c1, c2);
    }
  }
}
