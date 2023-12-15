from abc import ABC, abstractmethod

from ports.common import *
from util import *

def isBurstPort(n): pass
def isPtrPort(n): pass
def isVlaPort(n): pass

class TlfPort:
    @abstractmethod
    def mkVarDecl(self, vn): pass

    @abstractmethod
    def mkLoad(self, vn, indexExprs): pass

    @abstractmethod
    def mkStore(self, vn, indexExprs): pass

    @abstractmethod
    def addArrayInfo(self, vn, dims): pass

    @abstractmethod
    def isTlfArray(self, vn): pass

    @abstractmethod
    def getAlign(self): pass

    @abstractmethod
    def getOffset(self): pass
