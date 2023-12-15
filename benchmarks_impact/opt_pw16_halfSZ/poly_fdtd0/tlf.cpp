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

static void handleChunk0(int SIZEX, int SIZEY, hls::burst_maxi<AxiVec16> EY,
                         hls::burst_maxi<AxiVec16> HZ, int c1, int c2) {
  float EY_c[1][48];
#pragma HLS ARRAY_PARTITION variable = EY_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = EY_c type = complete dim = 2
  float HZ_c[2][48];
#pragma HLS ARRAY_PARTITION variable = HZ_c type = complete dim = 1
#pragma HLS ARRAY_PARTITION variable = HZ_c type = complete dim = 2

  int c3 = 0;

  // Cache load for EY at dim i
  {}

  // Cache load for HZ at dim i
  if (SIZEX >= 2 && SIZEY >= 1 && c3 == 0 && c1 % 32 == 0 && c2 % 32 == 0) {
    int len = 0;
    if ((((-16) + SIZEY) <= c2 && c2 < SIZEY)) {
      len =
          ((16 * (floor((15 + SIZEY) / 16))) - (16 * (floor((15 + c2) / 16))));
    }
    if ((c2 <= ((-17) + SIZEY))) {
      len = ((32 + (16 * (floor(c2 / 16)))) - (16 * (floor((15 + c2) / 16))));
    }

    const int leftPad = 0;

    const int compLen = len - leftPad;

    HZ.read_request((c2 + (0) + ((c1)*SIZEY)) / 16, len / 16);

    for (int cc1 = 0; cc1 <= 31; cc1 += 16) {
      if (cc1 < compLen) {
        const AxiVec16 axiTmp = HZ.read();
        HZ_c[0][cc1 + 16] = axiTmp.e0;
        HZ_c[0][cc1 + 17] = axiTmp.e1;
        HZ_c[0][cc1 + 18] = axiTmp.e2;
        HZ_c[0][cc1 + 19] = axiTmp.e3;
        HZ_c[0][cc1 + 20] = axiTmp.e4;
        HZ_c[0][cc1 + 21] = axiTmp.e5;
        HZ_c[0][cc1 + 22] = axiTmp.e6;
        HZ_c[0][cc1 + 23] = axiTmp.e7;
        HZ_c[0][cc1 + 24] = axiTmp.e8;
        HZ_c[0][cc1 + 25] = axiTmp.e9;
        HZ_c[0][cc1 + 26] = axiTmp.e10;
        HZ_c[0][cc1 + 27] = axiTmp.e11;
        HZ_c[0][cc1 + 28] = axiTmp.e12;
        HZ_c[0][cc1 + 29] = axiTmp.e13;
        HZ_c[0][cc1 + 30] = axiTmp.e14;
        HZ_c[0][cc1 + 31] = axiTmp.e15;
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
      if ((c2 <= ((-18) + SIZEY))) {
        len = ((32 + (16 * (floor(c2 / 16)))) - (16 * (floor((15 + c2) / 16))));
      }
      if ((((-17) + SIZEY) <= c2 && c2 < SIZEY)) {
        len = ((16 * (floor((15 + SIZEY) / 16))) -
               (16 * (floor((15 + c2) / 16))));
      }

      const int leftPad = 0;

      const int compLen = len - leftPad;

      EY.read_request((c2 + (0) + ((c1 + c3 + 1) * SIZEY)) / 16, len / 16);

      for (int cc1 = 0; cc1 <= 31; cc1 += 16) {
        if (cc1 < compLen) {
          const AxiVec16 axiTmp = EY.read();
          EY_c[0][cc1 + 16] = axiTmp.e0;
          EY_c[0][cc1 + 17] = axiTmp.e1;
          EY_c[0][cc1 + 18] = axiTmp.e2;
          EY_c[0][cc1 + 19] = axiTmp.e3;
          EY_c[0][cc1 + 20] = axiTmp.e4;
          EY_c[0][cc1 + 21] = axiTmp.e5;
          EY_c[0][cc1 + 22] = axiTmp.e6;
          EY_c[0][cc1 + 23] = axiTmp.e7;
          EY_c[0][cc1 + 24] = axiTmp.e8;
          EY_c[0][cc1 + 25] = axiTmp.e9;
          EY_c[0][cc1 + 26] = axiTmp.e10;
          EY_c[0][cc1 + 27] = axiTmp.e11;
          EY_c[0][cc1 + 28] = axiTmp.e12;
          EY_c[0][cc1 + 29] = axiTmp.e13;
          EY_c[0][cc1 + 30] = axiTmp.e14;
          EY_c[0][cc1 + 31] = axiTmp.e15;
        }
      }
    }
    // Cache load for HZ at dim j
    if (SIZEX >= 2 && SIZEY >= 1 && c3 >= 0 && c3 <= 31 && c1 % 32 == 0 &&
        c2 % 32 == 0) {
      int len = 0;
      if ((c2 <= ((-18) + SIZEY))) {
        len = ((32 + (16 * (floor(c2 / 16)))) - (16 * (floor((15 + c2) / 16))));
      }
      if ((((-17) + SIZEY) <= c2 && c2 < SIZEY)) {
        len = ((16 * (floor((15 + SIZEY) / 16))) -
               (16 * (floor((15 + c2) / 16))));
      }

      const int leftPad = 0;

      const int compLen = len - leftPad;

      HZ.read_request((c2 + (0) + ((c1 + c3 + 1) * SIZEY)) / 16, len / 16);

      for (int cc1 = 0; cc1 <= 31; cc1 += 16) {
        if (cc1 < compLen) {
          const AxiVec16 axiTmp = HZ.read();
          HZ_c[1][cc1 + 16] = axiTmp.e0;
          HZ_c[1][cc1 + 17] = axiTmp.e1;
          HZ_c[1][cc1 + 18] = axiTmp.e2;
          HZ_c[1][cc1 + 19] = axiTmp.e3;
          HZ_c[1][cc1 + 20] = axiTmp.e4;
          HZ_c[1][cc1 + 21] = axiTmp.e5;
          HZ_c[1][cc1 + 22] = axiTmp.e6;
          HZ_c[1][cc1 + 23] = axiTmp.e7;
          HZ_c[1][cc1 + 24] = axiTmp.e8;
          HZ_c[1][cc1 + 25] = axiTmp.e9;
          HZ_c[1][cc1 + 26] = axiTmp.e10;
          HZ_c[1][cc1 + 27] = axiTmp.e11;
          HZ_c[1][cc1 + 28] = axiTmp.e12;
          HZ_c[1][cc1 + 29] = axiTmp.e13;
          HZ_c[1][cc1 + 30] = axiTmp.e14;
          HZ_c[1][cc1 + 31] = axiTmp.e15;
        }
      }
    }

    for (c5 = 0; c5 <= 31; c5 += 1) {
      EY_c[0][c5 + 16] =
          EY_c[0][c5 + 16] - 0.5 * (HZ_c[1][c5 + 16] - HZ_c[0][c5 + 16]);
    }

    // write back for arr EY
    if (SIZEX >= 2 && SIZEY >= 1 && c3 >= 0 && c3 <= 31 && c1 % 32 == 0 &&
        c2 % 32 == 0) {
      int len = 0;
      if ((c2 <= ((-18) + SIZEY))) {
        len = ((32 + (16 * (floor(c2 / 16)))) - (16 * (floor((15 + c2) / 16))));
      }
      if ((((-17) + SIZEY) <= c2 && c2 < SIZEY)) {
        len = ((16 * (floor((15 + SIZEY) / 16))) -
               (16 * (floor((15 + c2) / 16))));
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

      EY.write_request((c2 + (0) + ((c1 + c3 + 1) * SIZEY)) / 16, len / 16);

      for (int cc1 = 0; cc1 <= 31; cc1 += 16) {
        if (cc1 < compLen) {
          AxiVec16 t{EY_c[0][cc1 + 16], EY_c[0][cc1 + 17], EY_c[0][cc1 + 18],
                     EY_c[0][cc1 + 19], EY_c[0][cc1 + 20], EY_c[0][cc1 + 21],
                     EY_c[0][cc1 + 22], EY_c[0][cc1 + 23], EY_c[0][cc1 + 24],
                     EY_c[0][cc1 + 25], EY_c[0][cc1 + 26], EY_c[0][cc1 + 27],
                     EY_c[0][cc1 + 28], EY_c[0][cc1 + 29], EY_c[0][cc1 + 30],
                     EY_c[0][cc1 + 31]};
          ap_int<64> writeStrobe;
          const int s0 = (cc1 + 0 >= 0) - (cc1 + 0 >= payLen);
          const int s1 = (cc1 + 1 >= 0) - (cc1 + 1 >= payLen);
          const int s2 = (cc1 + 2 >= 0) - (cc1 + 2 >= payLen);
          const int s3 = (cc1 + 3 >= 0) - (cc1 + 3 >= payLen);
          const int s4 = (cc1 + 4 >= 0) - (cc1 + 4 >= payLen);
          const int s5 = (cc1 + 5 >= 0) - (cc1 + 5 >= payLen);
          const int s6 = (cc1 + 6 >= 0) - (cc1 + 6 >= payLen);
          const int s7 = (cc1 + 7 >= 0) - (cc1 + 7 >= payLen);
          const int s8 = (cc1 + 8 >= 0) - (cc1 + 8 >= payLen);
          const int s9 = (cc1 + 9 >= 0) - (cc1 + 9 >= payLen);
          const int s10 = (cc1 + 10 >= 0) - (cc1 + 10 >= payLen);
          const int s11 = (cc1 + 11 >= 0) - (cc1 + 11 >= payLen);
          const int s12 = (cc1 + 12 >= 0) - (cc1 + 12 >= payLen);
          const int s13 = (cc1 + 13 >= 0) - (cc1 + 13 >= payLen);
          const int s14 = (cc1 + 14 >= 0) - (cc1 + 14 >= payLen);
          const int s15 = (cc1 + 15 >= 0) - (cc1 + 15 >= payLen);
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
        HZ_c[0][cc1 + 16] = HZ_c[1][cc1 + 16];
      }
    }
  }
}

void tlf(int SIZEX, int SIZEY, hls::burst_maxi<AxiVec16> EY,
         hls::burst_maxi<AxiVec16> HZ) {
  // partition
  for (int c1 = 0; c1 < SIZEX - 1; c1 += 32) {
    for (int c2 = 0; c2 < SIZEY; c2 += 32) {
      handleChunk0(SIZEX, SIZEY, EY, HZ, c1, c2);
    }
  }
}
