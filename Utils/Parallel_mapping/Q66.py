import networkx as nx
import matplotlib.pyplot as plt

# define the architecture graph  定义结构图
def q66():
    g = nx.DiGraph()
    g.add_nodes_from([0, 66])
    g.add_edge(0,1)
    for i in range(1, 6):
        g.add_edge(i, i + 6)
        g.add_edge(i + 6, i)
        g.add_edge(i, i + 7)
        g.add_edge(i + 7, i)
    for i in range(8, 13):
        g.add_edge(i, i + 5)
        g.add_edge(i + 5, i)
        g.add_edge(i, i + 6)
        g.add_edge(i + 6, i)
    for i in range(13, 18):
        g.add_edge(i, i + 6)
        g.add_edge(i + 6, i)
        g.add_edge(i, i + 7)
        g.add_edge(i + 7, i)
    for i in range(20, 25):
        g.add_edge(i, i + 5)
        g.add_edge(i + 5, i)
        g.add_edge(i, i + 6)
        g.add_edge(i + 6, i)
    for i in range(25, 30):
        g.add_edge(i, i + 6)
        g.add_edge(i + 6, i)
        g.add_edge(i, i + 7)
        g.add_edge(i + 7, i)
    for i in range(32, 37):
        g.add_edge(i, i + 5)
        g.add_edge(i + 5, i)
        g.add_edge(i, i + 6)
        g.add_edge(i + 6, i)
    for i in range(37, 42):
        g.add_edge(i, i + 6)
        g.add_edge(i + 6, i)
        g.add_edge(i, i + 7)
        g.add_edge(i + 7, i)
    for i in range(44, 49):
        g.add_edge(i, i + 5)
        g.add_edge(i + 5, i)
        g.add_edge(i, i + 6)
        g.add_edge(i + 6, i)
    for i in range(49, 54):
        g.add_edge(i, i + 6)
        g.add_edge(i + 6, i)
        g.add_edge(i, i + 7)
        g.add_edge(i + 7, i)
    for i in range(56, 61):
        g.add_edge(i, i + 5)
        g.add_edge(i + 5, i)
        g.add_edge(i, i + 6)
        g.add_edge(i + 6, i)
    single = [6,66]
    g.add_edge(6, 12)
    g.add_edge(12, 6)
    g.add_edge(66,60)
    g.add_edge(60,66)
    node1 = [7,18,19,30,31,42,43,54,55]
    for i in node1:
        g.add_edge(i,i-6)
        g.add_edge(i-6,i)
        g.add_edge(i, i + 6)
        g.add_edge(i + 6, i)
    node2 = [61,62,63,64,65]
    for i in node2:
        g.add_edge(i, i - 6)
        g.add_edge(i - 6, i)
        g.add_edge(i, i - 5)
        g.add_edge(i - 5, i)
    return g

