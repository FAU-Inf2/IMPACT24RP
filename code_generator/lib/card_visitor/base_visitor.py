def abstractmethod(m):
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method' + repr(abstractmethod))
    default_abstract_method.__name__ = m.__name__
    return default_abstract_method

class CardVisitor():
    def dispatch(self, n):
        if isinstance(n, str):
            return self.visitId(n)
        if isinstance(n, int):
            return self.visitInt(n)
        if len(n) == 3:
            return self.visitBinop(n)
        if len(n) == 2:
            return self.visitUnop(n)
        if len(n) == 5:
            return self.visitTwRelOp(n)

    @abstractmethod
    def visitTwRelOp(self, n): pass
    @abstractmethod
    def visitBinop(self, n): pass
    @abstractmethod
    def visitId(self, n): pass
    @abstractmethod
    def visitInt(self, n): pass
    @abstractmethod
    def visitEntry(self, n): pass
    @abstractmethod
    def visitCard(self, n): pass
    @abstractmethod
    def visitUnop(self, n): pass

