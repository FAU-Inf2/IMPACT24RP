import copy
import igraph

from access import *
from settings import *
from isl_parser import *
from dependency import *
from igraph_util import *
from scop_statement import *
from isl_parser_extract import *
from partitions.canonical_partitions import *

class AlginmentInfos():
    def __init__(self):
        self.ai = {}
        self.defaultAlignment = Settings.config("defaultAxiWidth")

    def getAlignment(self, name):
        if name in self.ai.keys():
            return self.ai[name]
        else:
            return self.defaultAlignment

    def addAlignment(self, name, al):
        assert(al in [1, 2, 4, 8, 16, 32, 64])
        self.ai[name] = al

    def getPaddingAlignment(self):
        alignments = [ al for al in self.ai.values() ]
        if len(alignments) == 0:
            return self.defaultAlignment
        else:
            return max(alignments)

    def getPaddingElems(self):
        maxAlign = self.getPaddingAlignment()
        if maxAlign > 1:
            return maxAlign
        else:
            return 0

class Scop:
    def clone(self): return copy.deepcopy(self)
    def __init__(self, name = "_unknown_"):
        self.stmts = []
        self.name = name
        self.alignmentInfos = AlginmentInfos()

    def addStmt(self, stmt):
        self.stmts.append(stmt)
        stmt.setScop(self)
        return self

    def addName(self, name):
        self.name = name
        return self

    def __deepcopy__(self, memo):
        stmtsCpy = [ copy.deepcopy(s) for s in self.stmts ]
        nameCpy = copy.deepcopy(self.name)
        resScop = Scop(stmtsCpy, nameCpy)
        for s in stmtsCpy:
            s.setScop(resScop)
        return resScop

    def getArrayNames(self):
        return sorted(self.arrayInfos.keys())

    def getParams(self):
        return setUnion([ stmt.getParams() for stmt in self.stmts ])

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def __getitem__(self, key):
        return self.stmts[key]

    def checkConsistency(self):
        for s in self.stmts:
            s.checkConsistency()

    def doLoopSplitting(self, depGraph):
        stronglyConComps = depGraph.connected_components(mode = "strong")
        clusterGraph = stronglyConComps.cluster_graph()
        topSort = clusterGraph.topological_sorting()
        resultMap = {}
        count = 0
        for ts in topSort:
            curSubGraph = stronglyConComps.subgraph(ts)
            for v in curSubGraph.vs():
                stmtName = getNameFromVertex(v)
                resultMap[stmtName] = count
            count = count + 1


        for name, schedNum in resultMap.items():
            stmt = self.getByName(name)
            # print(stmt, schedNum)
            rangeDims = stmt.getSchedRangeDims()
            rangeName = stmt.getSchedRangeName()
            schNuStr = str(schedNum)
            convDimStr = [ "i%s" % (nu) for nu in range(0, len(rangeDims)) ]
            schedConverter = "{ %s[%s] -> %s[%s] }" \
                % (rangeName, ','.join(convDimStr),
                   rangeName, ','.join([schNuStr] + convDimStr))
            schedConvMap = isl.union_map(schedConverter)

            oldSched = stmt.getSched()
            newSched = oldSched.apply_range(schedConvMap)
            self.getByName(name).setSched(newSched)

    def altLoopSplitting(self):
        schedules = [ s.getSched() for s in self.stmts ]
        schedRanges = [ sched for sched in schedules ]

    def __str__(self):
        res = "scop name = " + self.name
        res = res + "\n"
        for s in self.stmts:
            res = res + str(s)
            res = res + "\n"
        return res

    from dependency import printStronglyConComps

    def printReadAfterRead(self):
        rarGraph = self.readAfterRead()
        igraph.plot(rarGraph, target = "rar_graph_%s.pdf" % (self.name))

    def writeReadAfterRead(self):
        rarGraph = self.readAfterRead()
        igraph.write(rarGraph,
                     filename = "rar_graph_%s.dot" % (self.name),
                     format = "dot")

    def readAfterRead(self):
        dom = self.getFullDom()
        ord = self.calcOrd()
        name = self.name
        stmts = self.stmts
        return calcRarGraph(ord, name, stmts)

    def depAnalysis(self):
        dom = self.getFullDom()
        ord = self.calcOrd()
        name = self.name
        stmts = self.stmts
        return calcDepGraph(ord, name, stmts)

    def codegen(self):
        astBuild = isl.ast_build()
        inp = self.getFullSched().intersect_domain(self.getFullDom())
        ast = isl.ast_build.node_from_schedule_map(astBuild, inp)
        return ast.to_C_str()

    def printCodegen(self):
        print(self.codegen())

    def getAllBeforeGraph(self):
        result = igraph.Graph(directed = True)
        for s in self.stmts:
            name = s.getName()
            result.add_vertex(name, label = name)

        for s0 in self.stmts:
            for s1 in self.stmts:
                if s0.allBefore(s1):
                    result.add_edge(s0.getName(), s1.getName())
        return result

    def partitionCanonicalStmts(self):
        allBeforeGraph = self.getAllBeforeGraph()
        res = CanonicalPartitions()
        sinks = getAllSinks(allBeforeGraph)
        while len(sinks) > 0:
            fstSink = sinks[0]
            fstStmt = self.getByName(getNameFromVertex(fstSink))
            if len(sinks) == 1:
                allBeforeGraph.delete_vertices(fstSink.index)
                res.addTrueCanonicalStatement(fstStmt, self)
            else:
                anonDomFst = fstStmt.getAnonDom()
                otherStmts = [self.getByName(getNameFromVertex(s))
                              for s in sinks[1:] ]
                allStmts = [ fstStmt ] + otherStmts
                otherAnonDoms = [ s.getAnonDom() for s in otherStmts ]
                allEq = all([ anonDomFst.is_equal(anonDomS)
                              for anonDomS in otherAnonDoms ])
                if not allEq:
                    res.addFalseCanonicalStatements(allStmts, self)
                else:
                    res.addTrueCanonicalStatements(allStmts, self)
                indices = [ s.index for s in sinks ]
                allBeforeGraph.delete_vertices(indices)
            sinks = getAllSinks(allBeforeGraph)
        return res

    def printIsPurelyCanonicalNest(self):
        res = self.partitionCanonicalStmts()
        # print(res.isFullyCanonical())

    def printAllBeforeGraph(self):
        g = self.getAllBeforeGraph()
        igraph.plot(g, "all_before_graph_%s.pdf" % (self.name))

    def getByName(self, name):
        for s in self.stmts:
            if s.getName() == name:
                return s
        assert(False)

    def getDependencyRelation(self):
        reads = self.getUnionReads()
        writes = self.getUnionWrites()
        order = self.calcOrd()
        RAW = writes.apply_range(reads.reverse()).intersect(order)
        WAR = reads.apply_range(writes.reverse()).intersect(order)
        WAW = writes.apply_range(writes.reverse()).intersect(order)
        res = RAW.union(WAR).union(WAW)
        return res

    def getDataFlowDeps(self):
        reads = self.getUnionReads()
        writes = self.getUnionWrites()

    def isValidSchedule(self, sched):
        sched = sched.project_out_all_params()
        deps = self.getDependencyRelation()
        return deps.is_subset(ordRel(sched))

    def calcOrd(self):
        Sch = self.getFullSched()
        Ord = ordRel(Sch)
        return Ord

    def addTypeInfos(self, typeInfos):
        self.typeInfos = typeInfos
        return self

    def addArrayInfos(self, arrayInfos):
        self.arrayInfos = arrayInfos
        return self

    def addAlignment(self, name, al):
        self.alignmentInfos.addAlignment(name, al)
        return self

    def getAlInfos(self):
        return self.alignmentInfos

    def getTypeInfos(self):
        return self.typeInfos

    def getFullDom(self):
        return union([ s.getDom() for s in self.stmts ])

    def getFullSched(self):
        return union([ s.getSched() for s in self.stmts ])

    def getUnionAccs(self):
        return union([ acc.get() for s in self.stmts for acc in s.getAccs() ])

    def getUnionReads(self):
        return union([ read.get() for s in self.stmts for read in s.getReads() ])

    def getUnionWrites(self):
        return union([ write.get() for s in self.stmts for write in s.getWrites() ])

    def getArrayInfos(self): return self.arrayInfos
