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

static void handleChunk0(int SIZEX, int SIZEY, hls::burst_maxi<AxiVec4> EY,
                         hls::burst_maxi<AxiVec4> HZ, int c1, int c2) {
  float EY_c[1][36];
#pragma HLS ARRAY_PARTITION variable = EY_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = EY_c type = complete dim = 2
  float HZ_c[2][36];
#pragma HLS ARRAY_PARTITION variable = HZ_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = HZ_c type = complete dim = 2

  int c3 = 0;

  // Cache load for EY at dim i
  {}

  // Cache load for HZ at dim i
  if (SIZEX >= 2 && SIZEY >= 1 && c3 == 0 && c1 % 32 == 0 && c2 % 32 == 0) {
    int len = 0;
    if ((((-28) + SIZEY) <= c2 && c2 < SIZEY)) {
      len = ((4 * (floor((3 + SIZEY) / 4))) - (4 * (floor((3 + c2) / 4))));
    }
    if ((c2 <= ((-29) + SIZEY))) {
      len = ((32 + (4 * (floor(c2 / 4)))) - (4 * (floor((3 + c2) / 4))));
    }

    const int leftPad = 0;

    const int compLen = len - leftPad;

    HZ.read_request((c2 + (0) + ((c1)*SIZEY)) / 4, len / 4);

    for (int cc1 = 0; cc1 <= 31; cc1 += 4) {
      if (cc1 < compLen) {
        const AxiVec4 axiTmp = HZ.read();
        HZ_c[0][cc1 + 4] = axiTmp.e0;
        HZ_c[0][cc1 + 5] = axiTmp.e1;
        HZ_c[0][cc1 + 6] = axiTmp.e2;
        HZ_c[0][cc1 + 7] = axiTmp.e3;
      }
    }
  }

  for (c3 = 0; c3 <= min(31, SIZEX - c1 - 2); c3 += 1) {
#pragma HLS PIPELINE

        int c5 = 0;

    // Cache load for EY at dim j
    if (SIZEX >= 2 && SIZEY >= 1 && c3 >= 0 && c3 <= 31 && c1 % 32 == 0 &&
        c2 % 32 == 0) {
      int len = 0;
      if ((c2 <= ((-30) + SIZEY))) {
        len = ((32 + (4 * (floor(c2 / 4)))) - (4 * (floor((3 + c2) / 4))));
      }
      if ((((-29) + SIZEY) <= c2 && c2 < SIZEY)) {
        len = ((4 * (floor((3 + SIZEY) / 4))) - (4 * (floor((3 + c2) / 4))));
      }

      const int leftPad = 0;

      const int compLen = len - leftPad;

      EY.read_request((c2 + (0) + ((c1 + c3 + 1) * SIZEY)) / 4, len / 4);

      for (int cc1 = 0; cc1 <= 31; cc1 += 4) {
        if (cc1 < compLen) {
          const AxiVec4 axiTmp = EY.read();
          EY_c[0][cc1 + 4] = axiTmp.e0;
          EY_c[0][cc1 + 5] = axiTmp.e1;
          EY_c[0][cc1 + 6] = axiTmp.e2;
          EY_c[0][cc1 + 7] = axiTmp.e3;
        }
      }
    }
    // Cache load for HZ at dim j
    if (SIZEX >= 2 && SIZEY >= 1 && c3 >= 0 && c3 <= 31 && c1 % 32 == 0 &&
        c2 % 32 == 0) {
      int len = 0;
      if ((c2 <= ((-30) + SIZEY))) {
        len = ((32 + (4 * (floor(c2 / 4)))) - (4 * (floor((3 + c2) / 4))));
      }
      if ((((-29) + SIZEY) <= c2 && c2 < SIZEY)) {
        len = ((4 * (floor((3 + SIZEY) / 4))) - (4 * (floor((3 + c2) / 4))));
      }

      const int leftPad = 0;

      const int compLen = len - leftPad;

      HZ.read_request((c2 + (0) + ((c1 + c3 + 1) * SIZEY)) / 4, len / 4);

      for (int cc1 = 0; cc1 <= 31; cc1 += 4) {
        if (cc1 < compLen) {
          const AxiVec4 axiTmp = HZ.read();
          HZ_c[1][cc1 + 4] = axiTmp.e0;
          HZ_c[1][cc1 + 5] = axiTmp.e1;
          HZ_c[1][cc1 + 6] = axiTmp.e2;
          HZ_c[1][cc1 + 7] = axiTmp.e3;
        }
      }
    }

    for (c5 = 0; c5 <= 31; c5 += 1) {
      EY_c[0][c5 + 4] =
          EY_c[0][c5 + 4] - 0.5 * (HZ_c[1][c5 + 4] - HZ_c[0][c5 + 4]);
    }

    // write back for arr EY
    if (SIZEX >= 2 && SIZEY >= 1 && c3 >= 0 && c3 <= 31 && c1 % 32 == 0 &&
        c2 % 32 == 0) {
      int len = 0;
      if ((c2 <= ((-30) + SIZEY))) {
        len = ((32 + (4 * (floor(c2 / 4)))) - (4 * (floor((3 + c2) / 4))));
      }
      if ((((-29) + SIZEY) <= c2 && c2 < SIZEY)) {
        len = ((4 * (floor((3 + SIZEY) / 4))) - (4 * (floor((3 + c2) / 4))));
      }
      int payLen = 0;
      if ((c2 <= ((-33) + SIZEY))) {
        payLen = 32;
      }
      if ((((-32) + SIZEY) <= c2 && c2 < SIZEY)) {
        payLen = (SIZEY - c2);
      }
      const int leftPad = 0;
      const int rightPad = (len - payLen) - leftPad;
      const int compLen = len - leftPad;

      EY.write_request((c2 + (0) + ((c1 + c3 + 1) * SIZEY)) / 4, len / 4);

      for (int cc1 = 0; cc1 <= 31; cc1 += 4) {
        if (cc1 < compLen) {
          AxiVec4 t{EY_c[0][cc1 + 4], EY_c[0][cc1 + 5], EY_c[0][cc1 + 6],
                    EY_c[0][cc1 + 7]};
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
          EY.write(t, writeStrobe);
        }
      }
      EY.write_response();
    }
    // shift
    {}

    // shift
    if (SIZEX >= 2 && SIZEY >= 1 && c3 >= 0 && c3 <= 31 && c1 % 32 == 0 &&
        c2 % 32 == 0) {
      for (int cc1 = 0; cc1 <= 31; cc1 += 1) {
        HZ_c[0][cc1 + 4] = HZ_c[1][cc1 + 4];
      }
    }
  }
}

void tlf(int SIZEX, int SIZEY, hls::burst_maxi<AxiVec4> EY,
         hls::burst_maxi<AxiVec4> HZ) {
  // partition
  for (int c1 = 0; c1 < SIZEX - 1; c1 += 32) {
    for (int c2 = 0; c2 < SIZEY; c2 += 32) {
      handleChunk0(SIZEX, SIZEY, EY, HZ, c1, c2);
    }
  }
}
