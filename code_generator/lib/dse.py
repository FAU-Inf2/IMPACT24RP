from search_tile import *
from block_sizes import *
from overlap_graph import *
from read_box_analysis import *
from tile_search_result import *

from settings import *

def getReadStepsVectors(r, dim, t):
    ## Read box movement
    tiledSched = t.getTransformedSchedule()
    dom = r.getStmt().getDom()
    ris = accRelInSchedSpace(r.get(), tiledSched)
    domInSched = dom.apply(tiledSched)

    DShift = (t.getNextMap(dim)
              .intersect_domain(domInSched)
              .intersect_range(domInSched))

    DShiftDeltasMap = DShift.deltas_map().reverse()
    DShiftDeltaLexmin = DShiftDeltasMap.domain().lexmin()
    DShift = DShiftDeltaLexmin.apply(DShiftDeltasMap).unwrap()

    # print("Final DShift: ", DShift)
    R1 = ris.intersect_domain(domInSched)
    R2 = DShift.apply_range(ris).intersect_domain(domInSched)
    res = (arrow(R1.wrap(), R2.wrap())
           .zip()
           .intersect_domain(domInSched.identity().wrap())
           .zip()
           .deltas().unwrap().compute_divs())
    return res

def getSearchTiles(partition):
    if Settings.config("useDefaultSched"):
        return [ partition.getDefaultTilingSchedule() ]
    if Settings.config("testTilingScheme"):
        tileDims = Settings.config("tileDims")
        elemDims = Settings.config("elemDims")
        bs = getBlockSizes(partition.getDimlist())
        return [ SearchTile(partition, "O", tileDims, elemDims, bs) ]

    return partition.getPossibleTilingSchedules()

def onlyValidSearchTiles(searchTiles, part, scop):
    res = []
    for t in searchTiles:
        tra = t.getTilingTransform()
        print(tra)
        sched = part.getUnionSched()
        newSched = sched.apply_range(tra)
        isValid = scop.isValidSchedule(newSched)
        if isValid:
            res.append(t)
    return res

def getTileSearchResultsPerPartition(truePartitions, scop):
    results = TileSearchResults()
    for partition in truePartitions:
        dom = partition.getUnionDom()
        searchTiles = getSearchTiles(partition)
        searchTiles = onlyValidSearchTiles(searchTiles, partition, scop)

        if len(searchTiles) == 0:
            raise Exception("Could not tile input program due to data dependencies")

        for t in searchTiles:
            rba = ReadBoxAnalysis(t, dom)
            print("current search tile: ", t)
            accGraph = OverlapGraph(str(t), t, scop.calcOrd())
            for r in partition.getAllAccs():
                r.setCacheAble(rba.isCacheAble(r.get()))
                r.setAlignedToLoop(rba.isAccAlignedToTile(r.get()))
                newAccs = Accesses([r])
                node = accGraph.addAcc(newAccs)

            accGraph.syncAttributes()
            accGraph.calculateCards()
            accGraph.calculateCaches(dom)
            #accGraph.writeToFs("%s_unfused" % (str(t)))
            origData = getDesignSpaceData(accGraph)

            accGraph.detectDeps()
            #accGraph.writeToFsOnlyGraph("%s_deps" % (str(t)))
            accGraph.fuseNodesStageOne(t, dom)
            accGraph.syncAttributes()
            accGraph.detectOverlaps()
            accGraph.fuseNodesStageTwo(t, dom)
            accGraph.syncAttributes()
            accGraph.calculateCards()
            accGraph.calculateCaches(dom)
            accGraph.writeToFs("%s_fused" % (str(t)))
            #exit(1)

            fusedData = getDesignSpaceData(accGraph)
            tsr = DesignSpacePoint(t, origData, fusedData, accGraph)
            results.add(partition, tsr)

    return results

def findWinningTile(designSpacePoints):
    #print("Start with: ", designSpacePoints)
    #for partition, candidates in results.items:
    c1min = max(designSpacePoints, key = lambda x: x.getAlignmentFactor())
    c1 = [ c for c in designSpacePoints
           if c1min.getAlignmentFactor() == c.getAlignmentFactor() ]
    #print("c1: ", c1)
    c2min = max(c1, key = lambda x: x.getReuseFactor())
    c2 = [ c for c in c1 if c2min.getReuseFactor() == c.getReuseFactor() ]
    # print("c2: ", c2)
    c3min = max(c2, key = lambda x: x.getTilingLevel())
    c3 = [ c for c in c2 if c3min.getTilingLevel() == c.getTilingLevel() ]
    # print("c3: ", c3)
    # c2 = sorted(c2, )
    firstCand = c3[0]
    return firstCand

def findWinningTiles(partitions, tileSearchResultsPerPart):
    winningTilePerPart = dict()
    for partition in partitions:
        tileSearchResults = tileSearchResultsPerPart.getByPart(partition)
        win = findWinningTile(tileSearchResults)
        winningTilePerPart[partition] = win
    return winningTilePerPart

def setWinningTiles(truePartitions, winsPerPart):
    for partition in truePartitions:
        win = winsPerPart[partition]
        partition.setTiling(win.getTiling())
        partition.setOverlapGraph(win.getFusedOg())
