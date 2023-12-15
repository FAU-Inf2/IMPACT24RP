from overlap_graph import *

class TileSearchResults:
    def __init__(self):
        self.data = {  }

    def add(self, partition, tsr):
        if partition in self.data.keys():
            self.data[partition].append(tsr)
        else:
            self.data[partition] = []
            self.add(partition, tsr)

    def getByPart(self, partition):
        return self.data[partition]

    def dump(self):
        for part in self.data.keys():
            print("partition: ", part)
            for idx, tsr in enumerate(self.data[part]):
                print("tsr %s " % (idx))
                tsr.dump()

def calculateReuseFactor(new, old):
    newCard = new["fullCard"]
    oldCard = old["fullCard"]
    return oldCard / newCard

def getDesignSpaceData(graph):
    return {
        "fullCard": graph.getCardSum(),
        "alignmentFactor": graph.getAlignmentFactor(),
        "tilingLevel": graph.tiling.getTilingLevel(),
        "cacheSize": graph.getCacheCardSum()
    }

class DesignSpacePoint:
    def __init__(self, tiling, origData, fusedData, graph):
        self.tiling = tiling
        self.origData = origData
        self.fusedData = fusedData
        self.graph = graph

    def getTiling(self):
        return self.tiling

    def getFusedOg(self):
        return self.graph

    def getReuseFactor(self):
        return calculateReuseFactor(self.fusedData, self.origData)

    def getAlignmentFactor(self):
        return self.fusedData["alignmentFactor"]

    def getTilingLevel(self):
        return self.origData["tilingLevel"]

    def dump(self):
        print("Reuse factor: ", self.getReuseFactor())
        print("Full Card: ", self.origGraph.getCardSum())
        print("Alignment factor rgfused", self.getAlignmentFactor())
        print("tiling level: ", self.getTilingLevel())
