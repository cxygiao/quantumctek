import networkx as nx

def qubit_in_circuit(D): # the set of logic qubits appeared in D, a subset of C 逻辑线路量子位集合
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

# each circuit C induces an undirected graph 连通图
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
