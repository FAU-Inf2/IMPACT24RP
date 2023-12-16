#ifndef MEM_ALLOC_H
#define MEM_ALLOC_H

#include <vector>
#include <memory>

#include <cstdlib>
#include "orka_validate.h"

template <typename T> struct RandGen {
  static T getRand();
};

template <> struct RandGen<int> {
  static int getRand() { return rand(); }
};

template <> struct RandGen<float> {
  static float getRand() { return (float)rand() / (float)(1.0 + RAND_MAX); }
};

// rounds v up to the next multiple of Elems.
// As seen in Hackers Delight
int roundUp(int v, int m) { return v + (m - 1) & (-m); }

int getNumPayElems(std::vector<int> dims) {
  int len = 1;
  for (int i = 0; i < dims.size(); i++) {
    len *= dims[i];
  }
  return len;
}

// Elems = The number of elements over the bus
// LsdBlockSize = The tiling block size of the innermost dimension
template <typename T> class PaddedArray {
private:
  std::vector<int> dims;
  T *ptr = nullptr;
  const char *name = nullptr;

  int numPayElems = 0;
  int numPadElems = 0;
  int portWidth = 0;

public:
  PaddedArray(std::vector<int> d, int pw, int npe, const char *n) {
    assert(d.size() > 0);
    int rightmost = d.size() - 1;
    int lsd = d[rightmost];
    int newLsd = roundUp(lsd, pw);
    fprintf(stderr, "newLsdSize: %i\n", newLsd);
    d[rightmost] = newLsd;

    dims = d;
    portWidth = pw;
    numPadElems = npe;
    numPayElems = getNumPayElems(d);
    name = n;

    const int len = numPadElems + numPayElems;
    fprintf(stderr, "Elems to alloc: %i\n", len);
    ptr = (T *)new int[len];
  }

  int getNumPayloadElems() const { return numPayElems; }
  int getNumPaddingElements() const { return numPadElems; }
  int getNumElemsToTransfer() const {
    return getNumPayloadElems() + getNumPaddingElements();
  }

  int getOmpMapSize() const { return getNumElemsToTransfer() / portWidth; }

  // depends on whether this is used for AXI or not
  T *getPtr() const { return ptr + numPadElems; }

  template <typename G>
  G *getCastedPtr() const { return reinterpret_cast<G*>(getPtr()); }

  ~PaddedArray() {
    delete[] ptr;
    fprintf(stderr, "Array %s deletes\n", name);
  }

  bool isValid() const { return ptr != nullptr; }

  void randInit() {
    //fprintf(stderr, "Rand init\n");
    for (int i = 0; i < getNumPayloadElems(); i++) {
      float val = RandGen<T>::getRand();
      //fprintf(stderr, "Init with: %f\n", val);
      //exit(1);
      getPtr()[i] = val;
    }
  }

  const char *getName() const { return name; }
};

template <typename T>
std::shared_ptr<PaddedArray<T>> getAndInitNormalArray(std::vector<int> dims,
                                                      const char *n) {
  auto res = std::make_shared<PaddedArray<T>>(dims, 1, 0, n);
  res->randInit();
  return res;
}

template <typename T>
std::shared_ptr<PaddedArray<typename T::value_type>>
getAndInitAxiArray(std::vector<int> dims, int padding, const char *n) {
  using AxiValT = typename T::value_type;
  const int align = sizeof(T) / sizeof(AxiValT);
  auto res = std::make_shared<PaddedArray<AxiValT>>(dims, align, padding, n);
  res->randInit();
  return res;
}

template <typename T>
bool validate(std::shared_ptr<PaddedArray<T>> l,
              std::shared_ptr<PaddedArray<T>> r) {
  assert(l->getNumPayloadElems() == r->getNumPayloadElems());
  fprintf(stderr, "Len(l): %i, len(r): %i \n", l->getNumPayloadElems(),
          r->getNumPayloadElems());
  fprintf(stderr, "Validate arrays %s and %s\n", l->getName(), r->getName());
  bool res = validate_float_arr(l->getPtr(), r->getPtr(), l->getNumPayloadElems());
  fprintf(stderr, "Validation: %s\n", res ? "OK" : "FAIL");
  return res;
}

template <typename T>
using PaddedArrayPtr = std::shared_ptr<PaddedArray<T>>;

template <typename T, int NE>
using Res = std::array<PaddedArrayPtr<T>, NE>;

template <typename T, int NE>
bool validate(Res<T, NE> l, Res<T, NE> r) {
  bool result = true;
  for (int i = 0; i < NE; i++) {
    result = result && (validate(l[i], r[i]));
  }
  return result;
}

#endif
