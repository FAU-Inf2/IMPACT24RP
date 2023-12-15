import copy

from dataclasses import dataclass

from isl_util import *
from settings import *
from isl_parser import *
from visitors.ast_c_printer import *
from card_visitor.cond_assignment_gen import *

@dataclass
class CacheBoxes:
    codegenBox: ...
    payloadBox: ...
    burstBox: ...

class CacheReadPrinter(AstCPrinter):
    def __init__(self, arrName, destSuffix, srcSuffix,
                 boxes, itd, portMap, sl):
        super(CacheReadPrinter, self).__init__()
        self.arrName = arrName
        self.boxes = boxes
        self.destSuffix = destSuffix
        self.srcSuffix = srcSuffix
        self.idTransDict = itd
        self.shiftLoad = sl
        self.portMap = portMap
        self.forStack = []
        self.stashStack = []
        self.emitDebugCode = Settings.config("emitDebugCode")
        self.emitBurstVerify = Settings.config("emitBurstVerify")

    def pushStash(self, v):
        self.stashStack.append(v)

    def isShiftLoad(self):
        return self.shiftLoad

    def popStash(self):
        return self.stashStack.pop()

    def stashEmpty(self):
        return len(self.stashStack) == 0

    def topStash(self):
        return self.stashStack[-1]

    def pushFor(self, f):
        self.forStack.append(f)

    def popFor(self):
        return self.forStack.pop()

    def topFor(self):
        return self.forStack[-1]

    def topId(self):
        return self.topFor().get_iterator().get_id().get_name()

    def getDepth(self):
        return len(self.forStack)

    def isInUnrollLoop(self):
        return self.getDepth() > 2

    def splitUpCallArgs(self, n):
        args = self.dispatchOpList(n, 1)
        argsFst = args[0:len(args)//2]
        argsSnd = args[len(args)//2:]
        return (argsFst, argsSnd)

    def addLengthCheck(self, body):
        idx = "c" + self.topId()
        ifHead = "if (%s < compLen)" % (idx)
        res = nlJoin([ifHead, "{", body, "}"])
        return res

    def maybeGenBurstVerifyInc(self):
        return "burstVerify++;" if self.emitBurstVerify else ""

    def visitExprOpCall(self, n):
        (argsFst, argsSnd) = self.splitUpCallArgs(n)

        dest = self.arrName + self.destSuffix
        src = self.arrName + self.srcSuffix
        sn = self.portMap.genStructName()

        if self.portMap.isPortBurst(src):
            al = self.portMap.getAlign(src)
            self.stashAlignment(al)
            self.stashAlignment(al)
            self.stashLeftpadLength()
            self.stashReadReqStartAddr(n)
            self.stashBurstLen()
            self.stashReqTypeRead()
            axiVec = "const %s%s axiTmp = %s.read();" % (sn, al, src)
            res = nlJoin(
                [axiVec] +
                ["%s = axiTmp.e%s;" % (self.portMap.mkStore(dest, argsFst, i), i)
                 for i in range(0, al) ] +
                [ self.maybeGenBurstVerifyInc() ])
            return self.addLengthCheck(res)

        if self.portMap.isPortBurst(dest):
            al = self.portMap.getAlign(dest)
            self.stashAlignment(al)
            self.stashAlignment(al)
            self.stashPayloadLength()
            self.stashLeftpadLength()
            self.stashWriteReqStartAddr(n)
            self.stashBurstLen()
            self.stashReqTypeWrite()
            elems = cmJoin([ self.portMap.mkLoad(src, argsSnd, i)
                             for i in range(0, al) ])
            axiVec = "%s%s t{%s};" % (sn, al, elems)
            idx = "c" + self.topId()
            res = nlJoin([axiVec, self.portMap.mkStore(dest, [idx])] +
                         [self.maybeGenBurstVerifyInc()])
            return self.addLengthCheck(res)

        defRes = "%s = %s;" % (self.portMap.mkStore(dest, argsFst),
                               self.portMap.mkLoad(src, argsSnd))
        return defRes

    def stashAlignment(self, alignment):
        self.pushStash(alignment)

    def stashReqTypeRead(self):
        self.pushStash("read")

    def stashReqTypeWrite(self):
        self.pushStash("write")

    def stashReadReqStartAddr(self, n):
        self.stashReqStartAddr(n, read = True)

    def stashWriteReqStartAddr(self, n):
        self.stashReqStartAddr(n, read = False)

    def stashReqStartAddr(self, n, read = True):
        # print(self.topFor().get_init())
        initExpr = self.topFor().get_init().to_C_str()
        topId = self.topId()
        origMapping = self.idTransDict[topId]
        self.idTransDict[topId] = paren(initExpr)
        args = self.dispatchOpList(n, 1)
        # print("args: ", args)
        locus = len(args) // 2
        argsSnd = args[locus:] if read else args[0:locus]
        # print("argsSnd: ", argsSnd)
        off = self.portMap.mkOffset(self.arrName, argsSnd)
        self.idTransDict[topId] = origMapping
        self.pushStash(off)

    def stashLeftpadLength(self):
        pl1Dim = projectOutLast(self.boxes.payloadBox).coalesce()
        pl1Dim = trivGist(pl1Dim)
        bb1Dim = projectOutLast(self.boxes.burstBox).coalesce()
        bb1Dim = trivGist(bb1Dim)
        padParts = bb1Dim.subtract(pl1Dim)
        maxOrig = pl1Dim.lexmax()
        leftPad = maxOrig.apply(padParts.lex_lt_union_set(maxOrig).reverse())
        leftPadCard = leftPad.card()
        parsedLpCard = parseCard(leftPadCard)
        lpCode = CondAssignGen("leftPad", self.idTransDict).do(parsedLpCard)
        self.pushStash(lpCode)

    def stashPayloadLength(self):
        pl1Dim = projectOutLast(self.boxes.payloadBox).coalesce()
        pl1Dim = trivGist(pl1Dim)
        card = pl1Dim.card()
        parsedCard = parseCard(card)
        assign = CondAssignGen("payLen", self.idTransDict).do(parsedCard)
        self.pushStash(assign)

    def stashBurstLen(self):
        lastDimSet = projectOutLast(self.boxes.burstBox).coalesce()
        mi = isl.multi_id("{ [a] }")
        lastDimSet = lastDimSet.gist(lastDimSet.params().unbind_params(mi))
        lastDimSet = lastDimSet.drop_unused_params()
        card = lastDimSet.card()
        #print(cardStr)
        parsedCard = parseCard(card)
        res = CondAssignGen("len", self.idTransDict).do(parsedCard)
        #print(res)
        self.pushStash(res)

    def visitExprId(self, n):
        idstr = n.get_id().get_name()
        if idstr in self.idTransDict.keys():
            return self.idTransDict[idstr]
        else:
            return idstr

    def genDebugPrints(self, reqType, startAddr):
        res = """
        fprintf(stderr, "len = %%i\\n", len);
        fprintf(stderr, "compLen = %%i\\n", compLen);
        fprintf(stderr, "%s burst start addr = %%i\\n", %s);
        """ % (reqType, startAddr)
        return res

    def maybeGenDebugPrints(self, reqType, startAddr):
        if Settings.config("emitDebugCode"):
            return self.genDebugPrints(reqType, startAddr)
        return ""

    def decorateWithBurstVerify(self, loop, alignment):
        verifyCount = "int burstVerify = 0;"
        verify = "assert(burstVerify == (len / %s));" % (alignment)
        return nlJoin([verifyCount, loop, verify])

    def maybeDecorateWithBurstVerify(self, loop):
        alignment = self.popStash()
        if self.emitBurstVerify:
            return self.decorateWithBurstVerify(loop, alignment)
        return loop

    def decorateLoopWithBurst(self, loop):
        reqType = self.popStash()
        burstLen = self.popStash()
        startAddr = self.popStash()
        leftPadLen = self.popStash()
        payloadLen = self.popStash() if reqType == "write" else ""
        alignment = self.popStash()
        calcRightPad = "const int rightPad = (len - payLen) - leftPad;" \
            if reqType == "write" else ""
        compLen = "const int compLen = len - leftPad;"
        access = "%s.%s_request((%s) / %s, len / %s);" % (
            self.arrName, reqType, startAddr, alignment, alignment)
        response = "%s.write_response();" % (self.arrName) \
            if reqType == "write" else ""
        debug = self.maybeGenDebugPrints(reqType, startAddr)
        res = nlJoin([ burstLen, payloadLen, leftPadLen,
                       calcRightPad, compLen, debug,
                       access, NL, loop, response])
        return res

    def decorateLoopWithUnrollPragma(self, loop):
        pragma = "#pragma HLS UNROLL"
        return nlJoin([pragma, loop])

    def visitFor(self, n):
        self.pushFor(n)


        iterator = self.topId()
        iterator_ = "c" + iterator
        self.idTransDict[iterator] = iterator_
        loop = super().visitFor(n)

        if self.isInUnrollLoop() and self.isShiftLoad():
            loop = self.decorateLoopWithUnrollPragma(loop)

        if not self.stashEmpty():
            loop = self.decorateLoopWithBurst(loop)
            loop = self.maybeDecorateWithBurstVerify(loop)

        self.popFor()
        return loop
