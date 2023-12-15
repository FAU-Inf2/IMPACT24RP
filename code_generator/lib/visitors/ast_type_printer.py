from visitors.indentable import *
from visitors.base_visitor import *

class AstTypePrinter(AstVisitor, Intendable):
    def prolog(self, n):
        self.inc()
        print("%s+%s" % (self.indent(), type(n)))

    def epilog(self, n):
        self.dec()
