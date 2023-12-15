from util import *

def multOne(ad, ie):
    return paren(paren(ie[0]) + " * " + "*".join(ad[1:]))

def multAll(ad, ie):
    assert(len(ad) == len(ie))
    if ad == [] or len(ie) == 1:
        return ie[0]
    else:
        return multAll(ad[1:], ie[1:]) + "+" + multOne(ad, ie)

def addOffset(idx, offset):
    if offset == 0:
        return idx
    else:
        return idx[:-1] + [ idx[-1:][0] + " + " + str(offset) ]
