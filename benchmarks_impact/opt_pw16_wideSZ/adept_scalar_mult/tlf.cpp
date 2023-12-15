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

static void handleChunk0(int SIZE, float a, hls::burst_maxi<AxiVec16> V,
                         int c1) {
#pragma HLS PIPELINE

      float V_c[1040];
#pragma HLS ARRAY_PARTITION variable = V_c type = complete dim = 1

  int c2 = 0;

  // Cache load for V at dim i
  if (SIZE >= 1 && c1 % 1024 == 0) {
    int len = 0;
    if ((((-1008) + SIZE) <= c1 && c1 < SIZE)) {
      len = ((16 * (floor((15 + SIZE) / 16))) - (16 * (floor((15 + c1) / 16))));
    }
    if ((c1 <= ((-1009) + SIZE))) {
      len = ((1024 + (16 * (floor(c1 / 16)))) - (16 * (floor((15 + c1) / 16))));
    }

    const int leftPad = 0;

    const int compLen = len - leftPad;

    V.read_request((c1 + (0)) / 16, len / 16);

    for (int cc0 = 0; cc0 <= 1023; cc0 += 16) {
      if (cc0 < compLen) {
        const AxiVec16 axiTmp = V.read();
        V_c[cc0 + 16] = axiTmp.e0;
        V_c[cc0 + 17] = axiTmp.e1;
        V_c[cc0 + 18] = axiTmp.e2;
        V_c[cc0 + 19] = axiTmp.e3;
        V_c[cc0 + 20] = axiTmp.e4;
        V_c[cc0 + 21] = axiTmp.e5;
        V_c[cc0 + 22] = axiTmp.e6;
        V_c[cc0 + 23] = axiTmp.e7;
        V_c[cc0 + 24] = axiTmp.e8;
        V_c[cc0 + 25] = axiTmp.e9;
        V_c[cc0 + 26] = axiTmp.e10;
        V_c[cc0 + 27] = axiTmp.e11;
        V_c[cc0 + 28] = axiTmp.e12;
        V_c[cc0 + 29] = axiTmp.e13;
        V_c[cc0 + 30] = axiTmp.e14;
        V_c[cc0 + 31] = axiTmp.e15;
      }
    }
  }

  for (c2 = 0; c2 <= 1023; c2 += 1) {
    V_c[c2 + 16] = a * V_c[c2 + 16];
  }

  // write back for arr V
  if (SIZE >= 1 && c1 % 1024 == 0) {
    int len = 0;
    if ((((-1008) + SIZE) <= c1 && c1 < SIZE)) {
      len = ((16 * (floor((15 + SIZE) / 16))) - (16 * (floor((15 + c1) / 16))));
    }
    if ((c1 <= ((-1009) + SIZE))) {
      len = ((1024 + (16 * (floor(c1 / 16)))) - (16 * (floor((15 + c1) / 16))));
    }
    int payLen = 0;
    if ((c1 <= ((-1025) + SIZE))) {
      payLen = 1024;
    }
    if ((((-1024) + SIZE) <= c1 && c1 < SIZE)) {
      payLen = (SIZE - c1);
    }
    const int leftPad = 0;
    const int rightPad = (len - payLen) - leftPad;
    const int compLen = len - leftPad;

    V.write_request((c1 + (0)) / 16, len / 16);

    for (int cc0 = 0; cc0 <= 1023; cc0 += 16) {
      if (cc0 < compLen) {
        AxiVec16 t{V_c[cc0 + 16], V_c[cc0 + 17], V_c[cc0 + 18], V_c[cc0 + 19],
                   V_c[cc0 + 20], V_c[cc0 + 21], V_c[cc0 + 22], V_c[cc0 + 23],
                   V_c[cc0 + 24], V_c[cc0 + 25], V_c[cc0 + 26], V_c[cc0 + 27],
                   V_c[cc0 + 28], V_c[cc0 + 29], V_c[cc0 + 30], V_c[cc0 + 31]};
        ap_int<64> writeStrobe;
        const int s0 = (cc0 + 0 >= 0) - (cc0 + 0 >= payLen);
        const int s1 = (cc0 + 1 >= 0) - (cc0 + 1 >= payLen);
        const int s2 = (cc0 + 2 >= 0) - (cc0 + 2 >= payLen);
        const int s3 = (cc0 + 3 >= 0) - (cc0 + 3 >= payLen);
        const int s4 = (cc0 + 4 >= 0) - (cc0 + 4 >= payLen);
        const int s5 = (cc0 + 5 >= 0) - (cc0 + 5 >= payLen);
        const int s6 = (cc0 + 6 >= 0) - (cc0 + 6 >= payLen);
        const int s7 = (cc0 + 7 >= 0) - (cc0 + 7 >= payLen);
        const int s8 = (cc0 + 8 >= 0) - (cc0 + 8 >= payLen);
        const int s9 = (cc0 + 9 >= 0) - (cc0 + 9 >= payLen);
        const int s10 = (cc0 + 10 >= 0) - (cc0 + 10 >= payLen);
        const int s11 = (cc0 + 11 >= 0) - (cc0 + 11 >= payLen);
        const int s12 = (cc0 + 12 >= 0) - (cc0 + 12 >= payLen);
        const int s13 = (cc0 + 13 >= 0) - (cc0 + 13 >= payLen);
        const int s14 = (cc0 + 14 >= 0) - (cc0 + 14 >= payLen);
        const int s15 = (cc0 + 15 >= 0) - (cc0 + 15 >= payLen);
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
        V.write(t, writeStrobe);
      }
    }
    V.write_response();
  }
}

void tlf(int SIZE, float a, hls::burst_maxi<AxiVec16> V) {
  // partition
  for (int c1 = 0; c1 < SIZE; c1 += 1024) {
    handleChunk0(SIZE, a, V, c1);
  }
}
