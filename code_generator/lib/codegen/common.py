from util import *

def genSysIncludes(additional = []):
    incls = [  "stdlib.h", "stdio.h", "assert.h" ] + additional
    return nlJoin([ "#include <%s>" % (i) for i in incls ])

def genLocalIncludes(incls):
    return nlJoin([ "#include \"%s\"" % (i) for i in incls ])

def genIslUtil():
    return """
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
    """
