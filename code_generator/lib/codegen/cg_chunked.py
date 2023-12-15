from loop_heads import *
from overlap_graph import *
from read_box_analysis import *
from partitions.canonical_partition import *
from partitions.true_canonical_partition import *

from codegen.common import *
from codegen.backend import *
from codegen.cacheReadPrinter import *

class ChunkFuncGenerator(AstCPrinter):
    def __init__(self, partition, portMap, alInfo):
        super(AstCPrinter, self).__init__()
        self.partition = partition
        self.loopDepthCnt = 0
        self.portMap = portMap
        self.alInfo = alInfo

        self.loopHeads = LoopHeads(partition)
        self.tlfLoopIds = self.loopHeads.getTlfIters()
        self.chunkLoopIds = self.loopHeads.getChunkIters()

        self.tiling = self.partition.getTiling()
        self.slabs = self.tiling.getSlabs()
        self.dom = self.partition.getUnionDom()
        self.rba = ReadBoxAnalysis(self.tiling, self.dom)

    def do(self):
        fstChunkLoopNode = self.loopHeads.getChunkLoops()[0].getAstNode()
        return self.dispatch(fstChunkLoopNode)

    def incLoopDepth(self):
        self.loopDepthCnt += 1

    def decLoopDepth(self):
        self.loopDepthCnt -= 1

    def inPipelineLoop(self):
        return self.loopDepthCnt == len(self.chunkLoopIds) - 1

    def getCurrentDim(self):
        elemDims = self.tiling.getElemDims()
        currentDim = elemDims[self.loopDepthCnt - 1]
        return currentDim

    def isAtSmallestDim(self):
        smallestDim = self.tiling.getSmallestElemDim()
        currentDim = self.getCurrentDim()
        return currentDim == smallestDim

    def isAtLargestDim(self):
        largestDim = self.tiling.getLargestElemDim()
        currentDim = self.getCurrentDim()
        return currentDim == largestDim

    def getIdTranslationDict(self):
        orig = self.tlfLoopIds + self.chunkLoopIds
        trans = self.partition.getTiling().getTileDims() + \
            self.partition.getTiling().getElemDims()
        print("(orig): ", orig)
        print("(trans): ", trans)
        assert(len(orig) == len(trans))
        return { a : b for a, b in zip(trans, orig) }

    def maybeGenCaches(self, og):
        if (self.loopDepthCnt == 1):
            return self.genCaches(og)
        else:
            return ""

    def genCaches(self, og):
        def getArraySpec(name, cacheDims):
            return (arrayName, eJoin(brackWrap([ str(cd) for cd in cacheDims ])))
        def getArrPartPragma(name, cacheDims):
            pragmas = [ "#pragma HLS ARRAY_PARTITION variable = %s type = complete dim = %s"
                        % (arrayName, dim) for dim in range(1, len(cacheDims) + 1) ]
            return nlJoin(pragmas)
        res = ""
        for rn in og.getNodes():
            cacheStrat = cacheDecide(rn["accesses"])
            if cacheStrat == "noCache":
                return res
            cacheSlab = slabDecide(self.slabs, rn["accesses"])
            assert(cacheSlab != None)
            read = rn["accesses"].union()
            origName = rn["arrayName"]
            arrayName = origName + "_c"
            al = self.alInfo.getAlignment(origName)
            mustPad = self.portMap.isPortBurst(origName)
            shape = self.rba.getPaddedCacheShape(read, cacheSlab, al) \
                if mustPad else self.rba.getUnpaddedCacheShape(read, cacheSlab)
            cacheDims = self.rba.getCacheDimensions(shape)
            cacheDims[-1] = cacheDims[-1] + self.alInfo.getPaddingElems()
            res += "float %s%s;\n" % getArraySpec(arrayName, cacheDims)
            res += getArrPartPragma(arrayName, cacheDims)
            res += NL
            padAlignment = self.alInfo.getPaddingElems()
            self.portMap.addCacheArray(arrayName, cacheDims, padAlignment)
        return res

    def emitLoadCode(self, arrayName, curDim, boxes):
        res = ""
        res += "// Cache load for %s at dim %s \n" % (
            arrayName, curDim)
        res += self.buildLoadToCache(arrayName, boxes, "_c", "")
        res += NL
        return res

    def genCacheInit(self, arrayName, read):
        cd = self.getCurrentDim()
        alignment = self.alInfo.getAlignment(arrayName)
        initFull = self.rba.getInitFull(read, cd)
        initFullAl = self.alignIfBurst(initFull, arrayName)
        initFullAr = self.rba.alignToReadCache(read, initFullAl)
        initNoDom = self.rba.getInitNoDom(read, cd)
        initNoDomAl = self.rba.busAlignAndExpandBox(initNoDom, alignment)
        boxes = CacheBoxes(codegenBox = initFullAr,
                           payloadBox = initNoDom,
                           burstBox = initNoDomAl)
        return self.emitLoadCode(arrayName, cd, boxes)

    def genFullCacheInit(self, arrayName, read):
        cd = self.getCurrentDim()
        al = self.alInfo.getAlignment(arrayName)
        initFull = self.rba.getFullSlabInitBoxFull(read)
        initFullAl = self.alignIfBurst(initFull, arrayName)
        fullSlab = self.slabs.getFullTileSlabNoDi()
        initFullAr = self.rba.alignToCache(read, initFullAl, fullSlab)
        initNoDom = self.rba.getFullSlabInitBoxNoDom(read)
        initNoDomAl = self.rba.busAlignAndExpandBox(initNoDom, al)
        boxes = CacheBoxes(codegenBox = initFullAr,
                           payloadBox = initNoDom,
                           burstBox = initNoDomAl)
        return self.emitLoadCode(arrayName, cd, boxes)

    def alignIfBurst(self, box, arrayName):
        alignment = self.alInfo.getAlignment(arrayName)
        mustAlign = self.portMap.isPortBurst(arrayName)
        if mustAlign:
            return self.rba.busAlignBox(box, alignment)
        else:
            return box

    def genNext(self, arrayName, read):
        cd = self.getCurrentDim()
        alignment = self.alInfo.getAlignment(arrayName)
        nxt = self.rba.getNextFull(read, cd)
        nxtAl = self.alignIfBurst(nxt, arrayName)
        nxtAr = self.rba.alignToReadCache(read, nxtAl)
        nextNoDom = self.rba.getNextNoDom(read, cd)
        nextNoDomAl = self.rba.busAlignAndExpandBox(nextNoDom, alignment)
        boxes = CacheBoxes(codegenBox = nxtAr,
                           payloadBox = nextNoDom,
                           burstBox = nextNoDomAl)
        return self.emitLoadCode(arrayName, cd, boxes)

    def genCacheInitOrNext(self, og):
        res = ""
        for rn in og.getNodes():
            accs = rn["accesses"]
            arrayName = rn["arrayName"]
            accType = rn["accType"]
            read = accs.union()
            cacheStrat = cacheDecide(accs)
            if accType == "W":
                continue
            if cacheStrat == "noCache":
                continue
            if cacheStrat == "readSlab" and not self.isAtSmallestDim():
                res += self.genCacheInit(arrayName, read)
            if cacheStrat == "readSlab" and self.isAtSmallestDim():
                res += self.genNext(arrayName, read)
            if cacheStrat == "lineSlab" and self.isAtSmallestDim():
                res += self.genNext(arrayName, read)
            if cacheStrat == "fullSlab" and self.isAtLargestDim():
                res += self.genFullCacheInit(arrayName, read)
        return res

    def emitWriteBackLoadCode(self, arrayName, write, slab):
        assert(slab != None)
        al = self.alInfo.getAlignment(arrayName)
        wb = None
        if self.isAtSmallestDim():
            wb = self.rba.getWriteBackFull(write, slab)
        else:
            wb = self.rba.getWriteBackNoDom(write, slab)
        wbAl = self.alignIfBurst(wb, arrayName)
        wbAr = self.rba.alignToCache(write, wbAl, slab)

        wbNd = self.rba.getWriteBackNoDom(write, slab)
        wbNdAl = self.rba.busAlignAndExpandBox(wbNd, al)
        boxes = CacheBoxes(codegenBox = wbAr.reverse(),
                           payloadBox = wbNd,
                           burstBox = wbNdAl)
        res = "// write back for arr %s" % (arrayName)
        res += NL + self.buildLoadToPort(arrayName, boxes, "", "_c")
        return res

    def maybeGenWriteBack(self, og):
        res = ""
        for writeNode in og.getNodes(OverlapGraph.getHasWritePred()):
            accs = writeNode["accesses"]
            write = accs.union()
            cacheStrat = cacheDecide(accs)
            arrayName = writeNode["arrayName"]
            if cacheStrat == "noCache":
                continue
            slab = writeSlabDecide(self.slabs, accs)
            if cacheStrat == "lineSlab" and self.isAtSmallestDim():
                res += self.emitWriteBackLoadCode(arrayName, write, slab)
            if cacheStrat == "readSlab" and self.isAtSmallestDim():
                res += self.emitWriteBackLoadCode(arrayName, write, slab)
            if cacheStrat == "fullSlab" and self.isAtLargestDim():
                res += self.emitWriteBackLoadCode(arrayName, write, slab)
        return res

    def genShift(self, og):
        res = ""
        largestDim = self.tiling.getLargestElemDim()
        moreThanOneDims = self.tiling.getTilingLevel() > 1
        if self.isAtLargestDim() and moreThanOneDims:
            for readNode in og.getNodes(OverlapGraph.getIsFusedPred()):
                read = readNode["accesses"].union()
                arrayName = readNode["arrayName"]
                shift = self.rba.getShiftFull(read, largestDim)
                boxes = CacheBoxes(shift, None, None)
                res += "// shift \n"
                res += self.buildShift(arrayName, boxes, "_c", "_c")
                res += "\n"
        return res

    def genLoopHead(self, n):
        iterator = self.dispatch(n.get_iterator())
        initStr = self.dispatch(n.get_init())
        condStr = self.dispatch(n.get_cond())
        incStr = self.dispatch(n.get_inc())
        head = "for (%s = %s; %s; %s += %s)" % (
            iterator, initStr, condStr, iterator, incStr)
        return head

    def genConstraintHack(self, n):
        iterator = self.dispatch(n.get_iterator())
        initStr = self.dispatch(n.get_init())
        constraintHack = ("int %s = %s; \n" % (iterator, initStr))
        return constraintHack

    def visitFor(self, n):
        self.incLoopDepth()

        pragma = "#pragma HLS PIPELINE\n" if self.isAtSmallestDim() else ""
        og = self.partition.getOverlapGraph()
        cacheInits = self.maybeGenCaches(og)
        head = self.genLoopHead(n)
        nextOrInit = self.genCacheInitOrNext(og)
        body = self.dispatch(n.get_body())
        shift = self.genShift(og)
        body = brace(nlJoin([body, shift]))
        writeBacks = self.maybeGenWriteBack(og)
        constraintHack = self.genConstraintHack(n)
        res = nlJoin([pragma, cacheInits, constraintHack,
                      nextOrInit, NL, head,
                      body, NL, writeBacks])
        self.decLoopDepth()
        return res

    def visitExprOpCall(self, n):
        arrayIndices = self.dispatchOpList(n, 1)
        og = self.partition.getOverlapGraph()
        stmts = self.partition.getStmts()
        name = n.get_arg(0).get_id().get_name()
        s = self.partition.getStmtByName(name)
        dfg = s.getDfg()
        dfgArrRefs = s.getDfgArrRefs()
        for ar in dfgArrRefs:
            acc = s.getAccessByArrRef(ar)
            accDims = acc.getNumArrDim()
            arrName = acc.getArrName() + "_c"
            offsetInAccTpl = self.partition.getOffsetInAccessTuple(s, ar)
            indexSlice = arrayIndices[offsetInAccTpl:offsetInAccTpl+accDims]
            indexSlice[-1] += "+ " + str(self.portMap.getOffset(arrName))
            dfg = dfg.replace(ar, arrName + eJoin(brackWrap(indexSlice)))

        res = dfg + "\n"
        return res

    def buildLoadToCache(self, name, boxes, destSuffix, srcSuffix):
        return self.buildLoadToX(name, boxes, destSuffix, srcSuffix, False,
                                 scheduleGen = isl.union_map.domain_map)

    def buildShift(self, name, boxes, destSuffix, srcSuffix):
        return self.buildLoadToX(name, boxes, destSuffix, srcSuffix, True,
                                 scheduleGen = isl.union_map.domain_map)

    def buildLoadToPort(self, name, boxes, destSuffix, srcSuffix):
        return self.buildLoadToX(name, boxes, destSuffix, srcSuffix, False,
                                 scheduleGen = isl.union_map.range_map)

    def buildLoadToX(self, name, boxes, destSuffix,
                     srcSuffix, isShift, scheduleGen):
        # introduce a default schedule
        boxes.codegenBox = scheduleGen(boxes.codegenBox)
        ast = getAst(boxes.codegenBox)
        idTransDict = self.getIdTranslationDict()
        cPrinter = CacheReadPrinter(
            name, destSuffix, srcSuffix, boxes,
            idTransDict, self.portMap, isShift)
        res = cPrinter.do(ast)
        return res

class OrkaCodeGen(CodeGenBackend):
    def __init__(self, scop, portMap, partitions, name):
        super(OrkaCodeGen, self).__init__(name)
        self.scop = scop
        self.portMap = portMap
        self.arrayNames = list(scop.getArrayNames())
        self.partitions = partitions.getAllPartitions()
        self.loopHeadsByPartition = { p : LoopHeads(p) for p in
                                      partitions.getTrueCanonStmts() }

    def genTlfLoopsMoreD(self, partition):
        loopHeads = self.loopHeadsByPartition[partition]
        tlfLoops = loopHeads.tlfLoops
        for tlfLoop in tlfLoops:
            self.appendLn(tlfLoop.getAsC())
            self.append("{")

        self.append(self.getChunkFuncCall(partition))
        self.append("}" * len(tlfLoops))

    def genTlfLoops(self, partition):
        self.appendLn("// partition")
        if isinstance(partition, TrueCanonicalPartition):
            tilingLevel = partition.getTiling().getTilingLevel()
            self.genTlfLoopsMoreD(partition)
        else:
            raise Exception("Unimplemented")
        self.appendLn()

    def getTlfLoopIdents(self, partition):
        tlfLoops = self.loopHeadsByPartition[partition].getTlfLoops()
        iterIds = [ t.getIterAsStr() for t in tlfLoops ]
        return iterIds

    def getChunkFuncName(self, partition):
        return "handleChunk%s" % (partition.getId())

    def getChunkFuncCall(self, partition):
        paramsStr = cmJoin(list(self.scop.typeInfos.keys()) +
                           self.arrayNames +
                           self.getTlfLoopIdents(partition))
        call = "%s(%s);" % (self.getChunkFuncName(partition), paramsStr)
        return call

    def getChunkFuncParams(self, partition):
        params = self.getTlfParamsStr()
        iterIds = self.getTlfLoopIdents(partition)
        iterParams = [ "int " + t for t in iterIds ]
        return params + iterParams

    def genChunkFunc(self, partition):
        paramsStr = cmJoin(self.getChunkFuncParams(partition))
        funcSig = "static void %s(%s)" % (
            self.getChunkFuncName(partition), paramsStr
        )
        self.appendLn(funcSig)
        self.append("{ %s }" % (ChunkFuncGenerator(
            partition, self.portMap, self.scop.getAlInfos()
        ).do()))
        self.appendLn()
        self.appendLn()

    def getTlfParamsStr(self):
        arrayParams = [ self.portMap.mkVarDecl(an)
                        for an in self.arrayNames ]
        otherVars = [ "%s %s" % (v, k)
                      for k, v in self.scop.typeInfos.items() ]
        return otherVars + arrayParams

    def genTlfSignature(self):
        paramsStr = cmJoin(self.getTlfParamsStr())
        return "void tlf(%s)" % (paramsStr)

    def mkCode(self):
        self.appendLn(genSysIncludes(self.portMap.getIncls()))
        self.appendLn(genLocalIncludes([self.getHeaderName()]))
        self.appendLn(genIslUtil())
        self.appendLn()
        self.appendLn()

        for partition in self.partitions:
            self.genChunkFunc(partition)

        self.appendLn(self.genTlfSignature())
        self.appendLn("{")

        for partition in self.partitions:
            self.genTlfLoops(partition)

        self.appendLn("}")

    def mkHeader(self):
        headerBody = nlJoin([self.portMap.genStruct(),
                             self.genTlfSignature() + ";"])
        self.genHeader(headerBody)

    def do(self):
        self.mkCode()
        self.mkHeader()
