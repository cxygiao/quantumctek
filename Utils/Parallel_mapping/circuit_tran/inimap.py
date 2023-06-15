
import networkx as nx
from vfs import Vf
from Qubit_f import topgates


#####\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\

def qubit_in_circuit(D):  # the set of logic qubits appeared in D, a subset of C
    ''' Return the set of qubits in a circuit D

    Args:
        D (list): a sublist of CNOT gates of the input circuit C  逻辑线路cnot门的子集D
    Returns:
        Q (set): the set of qubits in D    子集D中所有量子位集合
    '''
    Q = set()
    for gate in D:
        Q.add(gate[0])
        Q.add(gate[1])
    return Q


#####\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
# Weighted SUBGRAPH
#####\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\


# each circuit C induces an undirected graph
def graph_of_circuit(C):
    ''' Return the graph induced by the circuit
            - node set: qubits in C
            - edge set: all pair (p,q) if CNOT [p,q] in C

    Args:
        C (list): the input circuit
    Returns:
        g (graph)
    '''

    g = nx.Graph()
    g.add_nodes_from(qubit_in_circuit(C))
    for gate in C:
        g.add_edge(gate[0], gate[1])
    return g


def best_g(C, G):
    ''' Return a graph g which is isomorphic to a subgraph of G
            while maximizing the number of CNOTs in C that correspond to edges in g
        Method: sort the edges according to their weights (the number of CNOTs in C corresponding to each edge);
                construct a graph by starting with the edge with the largest weight; then consider the edge with the second large weight, ...
                if in any step the graph is not isomorphic to a subgraph of G, skip this edge and consider the next till all edges are considered.

    Args:
        C (list): the input circuit
        G (graph): the architecture graph

    Returns:
        g (graph)
    '''
    #=============================
    #MUL使用函数
    # for i in range(0,len(C)):
    #     del(C[i][0])
    # print('删除索引后线路：', C)
    #=============================


    g_of_c = graph_of_circuit(C)  # c的连通图
    Eg = list(g_of_c.edges())
    Eg.sort()  # 边权重排序


    # #逻辑线路量子门附加门序  -----------------------------------------------------新门序权重
    C_list = []
    l = len(C)
    for i in range(l):
        C_list.append(list([l-i, tuple(C[i])]))
    #print('带权门列表C_list',C_list)
    #连通边附权重
    #print('连通图边Eg',Eg)
    #
    edge_wgt_list = list([0,e] for e in g_of_c.edges())
    # print('初始化连通图edge_wgt_list',edge_wgt_list)
    #
    for c in C_list:
        for e in edge_wgt_list:
            if c[1]==e[1] or c[1]==(e[1][1],e[1][0]):
                e[0]=c[0]+e[0]
    #print('权重连通图edge_wgt_list',edge_wgt_list)
    edge_wgt_list.sort(reverse=True)
    #print('权重降序排列edge_wgt_list',edge_wgt_list)

    edge_wgt_list1 = list(q[1] for q in edge_wgt_list)
    #提取连通边，已按权重优先降序排列完毕
    Egw = list(edge_wgt_list1)
    legw = len(Egw)
    #print('连通边列表Egw', Egw)



    # # 为连通图的边附上权重
    # edge_wgt_list = list([C.count([e[0], e[1]]) + C.count([e[1], e[0]]), e] for e in g_of_c.edges())
    # # 权重优先降序排列
    # edge_wgt_list.sort(key=lambda t: t[0], reverse=True)  # q[0] weight, q[1] edge
    # edge_wgt_list1 = list(q[1] for q in edge_wgt_list)
    #
    # Egw = list(edge_wgt_list1)
    # legw = len(Egw)

    # We use the vf2 algorithm to determine if a graph is embeddable in G and compute a mapping if it does
    vf2 = Vf()
    result = {}
    result = vf2.dfsMatch(g_of_c, G, result)
    lng = len(nx.nodes(g_of_c))
    if len(result) == lng:
        ##        print('The graph of the circuit is embeddable in G')
        return g_of_c

    ##    print('The graph of the circuit is NOT embeddable in G')

    # we search backward, remove the first edge that makes g not embeddable, and continue till we get a maximum graph
    Hard_Edge_index = 0  # the index of the first hard edge
    g = nx.Graph()
    # we don't include all nodes from QIC as sometimes my vf2 alg. is perhaps not good when g is disconnected

    # add the first edge into g
    q = Egw[0]
    g.add_edge(q[0], q[1])

    rp = 0
    for rp in range(legw):

        # h is the index of the last edge that can be added into g
        h = Hard_Edge_index
        if h == legw - 1:
            return g

        LW = Egw[h + 1:legw]

        for q in LW:
            g.add_edge(q[0], q[1])
            i = Egw.index(q)

            # find the largest i such that the first i-1 edges are embeddable
            vf2 = Vf()
            result = {}
            result = vf2.dfsMatch(g, G, result)
            if len(result) != len(nx.nodes(g)):
                Hard_Edge_index = i
                g.remove_edge(q[0], q[1])
                break

            if i == legw - 1 and len(result) == len(nx.nodes(g)):
                return g
    return g


###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
# compute the gate dependency graph of (a part of) the circuit
def gate_dependency_graph(C, nl, LX):  # LX is the index set of a subset of C
    ''' Return the gate dependency graph induced by the circuit

    Args:
        C (list): the input circuit
        nl (int): the number of qubits in C
        LX (list): the list of indices of a sublist X of C

    Returns:
        g (graph): its nodes are indices in LX and (i,j) is an edge in g if gate C[j] depends on C[i]
    '''
    g = nx.DiGraph()
    g.add_nodes_from(LX)
    L1 = LX[:]
    while L1:
        L0 = L1[:]
        TG = topgates(C, nl, L0)
        for i in TG:
            L0.remove(i)
        TGx = topgates(C, nl, L0)
        for i in TG:
            gate1 = C[i]
            for j in TGx:
                gate2 = C[j]
                if set(gate1) & set(gate2):
                    g.add_edge(i, j)

        L1 = L0[:]
    return g


# compute the top subgraph of C
def _topgraph_(C, G, nl, L1):
    ''' Return the topgraph g of the input circuit C
        Method: Consider all gates in the gate dependency graph one by one from the top.
                Let x=C[j] be the current edge. Add it to g and check if g is still embeddable into G.
                Otherwise, remove all gates that are dependent on x from the gate dependency graph and check if there are any gate left and continue.

    Args:
        C (list): the input circuit
        G (graph): the architecture graph
        nl (int): the number of qubits in C
        L1: the list of indices of unsolved gates in C

    Returns:
        g (graph): the topgraph
    '''

    # C is the input circuit
    # L1 is the index set of unsolved gates in C
    gdg = gate_dependency_graph(C, nl, L1)

    # construct the top subgraph g from the circuit
    g = nx.Graph()  # the subgraph of G induced by nodes with indices in GATES
    GATES = []  # the indices of topgates that can be executed (i.e., put in g) in this round

    # we consider unsolved gate in C one by one
    Dump = set()  # record all those gates that cannot be put in the solvable graph in this round
    for j in L1:
        a = L1.index(j)
        x = C[j]

        CHANGE = True
        while CHANGE and Dump:
            ldump = len(Dump)
            # for every s in Dump, add its descedents into s
            Dump_TG = topgates(C, nl, list(Dump))
            for s in Dump_TG:
                Dump = Dump | set(nx.descendants(gdg, s))

            if ldump == len(Dump):
                CHANGE = False

        if Dump >= set(L1[a:]):
            return g, GATES

        if j in Dump:
            continue

        if (x[0], x[1]) in g.edges():  # the same gate has been considered for some j<i with C[i]==C[j]
            GATES.append(j)  # C[i] is to be solved in this round
            continue

        # Temporalliy add x into g
        g.add_node(x[0])
        g.add_node(x[1])
        g.add_edge(x[0], x[1])

        vf2 = Vf()
        result = {}
        result = vf2.dfsMatch(g, G, result)

        if len(result) == len(g.nodes()):  # g is embeddable
            GATES.append(j)  # C[j] will be solved in this round

        # if g is not embeddable, then remove x from g
        else:
            # remove same gates from consideration
            Dump.add(j)

            g.remove_edge(x[0], x[1])
            if nx.degree(g, x[0]) == 0:
                g.remove_node(x[0])
            if nx.degree(g, x[1]) == 0:
                g.remove_node(x[1])

    return g, GATES


# \__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\#\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
# the weighted subgraph initial mapping
def _tau_bsg_(C, G):
    ''' Return the weighted subgraph initial mapping

    Args:
        C (list): the input circuit
        G (graph): the architecture graph
    Returns:
        tau (list): the weighted subgraph initial mapping
    '''
    bsg = best_g(C, G)  # 权重优先最大子图
    vf2 = Vf()
    result = {}
    print(result)
    result = vf2.dfsMatch(bsg, G, result)
    print(result)
    BB = result
    tau = [20] * 20
    for key in BB:  # map physical qubit BB[key] to logic qubit key
        tau[BB[key]] = key
    return tau


###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
# the topgraph initial mapping
def _tau_bstg_(C, G, nl):
    ''' Return the topgraph initial mapping

    Args:
        C (list): the input circuit
        G (graph): the architecture graph
        nl (int): the number of qubits in C
    Returns:
        tau (list): the topgraph initial mapping
    '''

    l = len(C)
    L = list(range(l))
    g_GATES = _topgraph_(C, G, nl, L)
    bstg = g_GATES[0]  # the topgraph of C
    vf2 = Vf()
    result = {}
    result = vf2.dfsMatch(bstg, G, result)

    BB = result
    tau = [20] * 20
    for key in BB:  # map physical qubit BB[key] to logic qubit key
        tau[BB[key]] = key
    return tau
###\__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
