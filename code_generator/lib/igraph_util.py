import igraph
import subprocess

def getAllSinks(g):
    return [ vs for vs in g.vs() if vs.outdegree() == 0 ]

def getNameFromVertex(v):
    # can probably be rewritten as v["name"]
    return v.attributes()["name"]

def hasVertexSelfCycle(v):
    succs = v.successors()
    for s in succs:
        if s == v:
            return True
    return False

def writeToPng(graph, basename):
    filename = "%s.dot" % (basename)
    igraph.write(graph, filename = filename, format = "dot")
    output = subprocess.run(["dot", "-Tpng", "-O", filename])
    if not output.returncode == 0:
        raise Exception("Error during runnint dot")

def printStronglyConComps(G):
    igraph.plot(
        G.connected_components(mode = "strong"),
        target = self.name + ".pdf"
    )
