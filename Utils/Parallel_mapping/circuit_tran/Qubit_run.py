import json
import os
import time


# \__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\
def save_result(name, content):
    name = str(name)
    content = str(content)
    file = open("testRecord/circuit_tran-" + "2022-01-03-" + name + ".txt", mode='a')
    file.write(content)
    file.write('\n')
    file.close()


# \__/#\#/\#\__/#\#/\__/--\__/#\__/#\#/~\

def qubit_in_circuit(D):  # the set of logic qubits appeared in D, a subset of C
    ''' Return the set of qubits in a circuit D
        Args:
            D (list): a sublist of CNOT gates of the input circuit C
        Returns:
            Q (set): the set of qubits in D
    '''
    Q = set() #创建无序不重复元素集
    for gate in D:
        Q.add(gate[1])
        Q.add(gate[2])
    return Q

    #======MUL使用=========
    # Q.add(gate[0])
    # Q.add(gate[1])

        # Q.add(gate[1])
        # Q.add(gate[2])
    #=====================




