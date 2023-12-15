#ifndef C_HEADER_tlf
#define C_HEADER_tlf

#include "orka_hls.h"

struct AxiVec4 {
  float e0;
  float e1;
  float e2;
  float e3;
  using value_type = float;
};

void tlf(int SIZE, float a, hls::burst_maxi<AxiVec4> X,
         hls::burst_maxi<AxiVec4> Y);

#endif
