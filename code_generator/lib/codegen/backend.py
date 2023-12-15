from util import *

class CodeGenBackend():
    ID = 0
    @staticmethod
    def getNextId():
        res = CodeGenBackend.ID
        CodeGenBackend.ID = CodeGenBackend.ID + 1
        return res

    def __init__(self, name):
        self.outStr = ""
        self.outStrHeader = ""
        self.name = name
        self.id = CodeGenBackend.getNextId()

    def getId(self): return self.id

    def appendLn(self, s = ""): self.outStr = self.outStr + s + "\n"

    def append(self, s): self.outStr = self.outStr + s

    def appendHdrLn(self, s = ""):
        self.outStrHeader = self.outStrHeader + s + "\n"

    def appendHdr(self, s): self.outStrHeader = self.outStrHeader + s

    def reformat(self):
        self.outStr = clangFormat(self.outStr)
        self.outStrHeader = clangFormat(self.outStrHeader)

    def writeCodeToFile(self):
        path = self.name + ".cpp"
        f = open(path, "w")
        f.write(self.getOut())
        f.close()

    def getHeaderName(self):
        return self.name + ".hpp"

    def writeHeaderToFile(self):
        path = self.getHeaderName()
        f = open(path, "w")
        f.write(self.getOutHdr())
        f.close()

    def dump(self): print(self.getOut())

    def getOut(self): return self.outStr

    def getOutHdr(self): return self.outStrHeader

    def genHeader(self, body):
        headerName = "C_HEADER_" + str(self.name)
        self.appendHdrLn("#ifndef " + headerName)
        self.appendHdrLn("#define " + headerName)
        self.appendHdrLn()
        self.appendHdrLn("#include \"orka_hls.h\"")
        self.appendHdrLn()
        self.appendHdrLn(body)
        self.appendHdrLn()
        self.appendHdrLn("#endif")
