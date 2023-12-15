import igraph
import graphviz
import subprocess

from igraph_util import *

def calcRarGraph(Ord, name, stmts):
    g = igraph.Graph(directed = True)

    for stmt in stmts:
        name = stmt.getName()
        g.add_vertex(name, label = name)

    for stmt1 in stmts:
        for stmt2 in stmts:
            n1 = stmt1.getName()
            n2 = stmt2.getName()
            rs1 = stmt1.getReads()
            rs2 = stmt2.getReads()
            for r1 in rs1:
                for r2 in rs2:
                    dep = r1.get().apply_range(r2.get().reverse())
                    dep = dep.intersect(Ord)
                    if (not dep.is_empty()):
                        g.add_edge(n2, n1)
    return g



def calcDepGraph(Ord, name, stmts):
    g = igraph.Graph(directed = True)

    for stmt in stmts:
        name = stmt.getName()
        g.add_vertex(name, label = name)

    def addEdge(g, f, t):
        g.add_edge(f, t)

    for stmt1 in stmts:
        for stmt2 in stmts:
            n1 = stmt1.getName()
            n2 = stmt2.getName()
            if (n1 == n2):
                continue
            rs1 = stmt1.getReads()
            ws1 = stmt1.getWrites()
            ws2 = stmt2.getWrites()
            # print("check for RAW between ", n1, n2)
            for r1 in rs1:
                for w2 in ws2:
                    resSet = w2.get().apply_range(r1.get().reverse())
                    # print ("resSet: ", resSet)
                    resSet = resSet.intersect(Ord)
                    # print("res set: ", resSet)
                    if (not resSet.is_empty()):
                        # print("Dependency between", n1, n2)
                        addEdge(g, n2, n1)

            #print ("check for WAR between", n1, n2)
            for r1 in rs1:
                for w2 in ws2:
                    resSet = r1.get().apply_range(w2.get().reverse())
                    resSet = resSet.intersect(Ord)
                    if (not resSet.is_empty()):
                        # print("WAR between", n1, n2)
                        addEdge(g, n2, n1)

            #print ("check for WAW between", n1, n2)
            #print ("ws1: ", ws1, " ws2: ", ws2)
            for w1 in ws1:
                for w2 in ws2:
                    resSet = w1.get().apply_range(w2.get().reverse())
                    resSet = resSet.intersect(Ord)
                    # resSet_r = w1.apply_range(w2.reverse())
                    # resSet_r = resSet_r.intersect(Ord)
                    if (not resSet.is_empty()):
                        #print("WAW between", n1, n2, " ResSet: ", resSet)
                        addEdge(g, n1, n2)
    return g

