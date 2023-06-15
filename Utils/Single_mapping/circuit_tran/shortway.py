import networkx as nx

def way(G):
    # shortest_path = []
    # shortest_way = []
    n = G.number_of_nodes()
    way_index=[]
    for i in range(n):
        for j in range(i+1, n):
            # shortest_path.append(nx.shortest_path(G, i, j))
            # shortest_way.append(len(nx.shortest_path(G, i, j))-1)
            way_index.append([[i, j],len(nx.shortest_path(G, i, j))-1])

    #print(way_index)
    return way_index
