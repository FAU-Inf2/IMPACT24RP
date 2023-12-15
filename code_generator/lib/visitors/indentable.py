
class Indentable():
    def __init__(self):
        self.incCnt = 0

    def inc(self):
        self.incCnt += 2

    def dec(self):
        self.incCnt -= 2

    def indent(self):
        return " " * self.incCnt
