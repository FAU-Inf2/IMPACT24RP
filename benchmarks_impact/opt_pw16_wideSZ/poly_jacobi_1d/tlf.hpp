#ifndef C_HEADER_tlf
#define C_HEADER_tlf

#include "orka_hls.h"

struct AxiVec16 {
  float e0;
  float e1;
  float e2;
  float e3;
  float e4;
  float e5;
  float e6;
  float e7;
  float e8;
  float e9;
  float e10;
  float e11;
  float e12;
  float e13;
  float e14;
  float e15;
  using value_type = float;
};

void tlf(int SIZE, hls::burst_maxi<AxiVec16> A, hls::burst_maxi<AxiVec16> B);

#endif
