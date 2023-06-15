from qiskit import QuantumCircuit
from collections import defaultdict

import logging
import typing as ty
import numpy as np
import networkx as nx
import itertools

def largest_circuit_logical_degree(circuit: QuantumCircuit):
    """
    Iterate over all the gates of the circuit and obtain the largest logical
    node degree of the logical qubit.
    """
    logical_qubit_degree = defaultdict(list)
    qasm_file = circuit.qasm().split(';')
    for line in qasm_file:
        line = line.split()
        if not line:
            continue
        if line[0] == 'OPENQASM':
            continue
        if line[0] == 'include':
            continue
        if line[0] == 'creg':
            continue
        if line[0] == 'qreg':
            continue
        if line[0] == 'cx':
            qubits = line[1].split(',')
            qubit_1 = int(qubits[0][2:-1])
            qubit_2 = int(qubits[1][2:-1])
            if not logical_qubit_degree[qubit_1] or qubit_2 not in logical_qubit_degree[qubit_1]:
                logical_qubit_degree[qubit_1].append(qubit_2)
            if not logical_qubit_degree[qubit_2] or qubit_1 not in logical_qubit_degree[qubit_2]:
                logical_qubit_degree[qubit_2].append(qubit_1)

    return len(sorted(logical_qubit_degree.values(), key=lambda x: len(x))[-1])