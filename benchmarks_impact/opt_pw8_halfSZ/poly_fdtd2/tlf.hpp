#ifndef C_HEADER_tlf
#define C_HEADER_tlf

#include "orka_hls.h"

struct AxiVec8 {
  float e0;
  float e1;
  float e2;
  float e3;
  float e4;
  float e5;
  float e6;
  float e7;
  using value_type = float;
};

void tlf(int SIZEY, int SIZEX, hls::burst_maxi<AxiVec8> EX,
         hls::burst_maxi<AxiVec8> EY, hls::burst_maxi<AxiVec8> HZ);

#endif