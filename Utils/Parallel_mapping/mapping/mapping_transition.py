from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.circuit.classicalregister import Clbit
from qiskit.dagcircuit.dagcircuit import DAGCircuit
from qiskit.circuit.quantumregister import Qubit
from Utils.Parallel_mapping.mapping.iterative_mapping import iterative_mapping_algorithm
from Utils.Parallel_mapping.mapping.initial_mapping_wrapper import initial_mapping
from Utils.Parallel_mapping.mapping.initial_mapping_construct import cost
from Utils.Parallel_mapping.partition_process.qubit_partition import (
    partition_circuits,
    largest_circuit_logical_degree,
)
import networkx as nx
import logging
import typing as ty
import numpy as np
import time

logger = logging.getLogger("mapping_transisiton")

def _modify_dag_circuit(circuit: QuantumCircuit, previous_qubits_used: int):
    """
    Modify the dag circuit in order to merge several dag circuits into one dag circuit
    """
    origin_dag = circuit_to_dag(circuit)
    new_dag = DAGCircuit()
    for qreg in origin_dag.qregs.values():
        new_dag.add_qreg(qreg)
    for creg in origin_dag.cregs.values():
        new_dag.add_creg(creg)
    for node in origin_dag.topological_op_nodes():
        new_dag.apply_operation_back(node.op,
                                       qargs=[Qubit(new_dag.qregs['q'], qarg.index + previous_qubits_used) for qarg in
                                              node.qargs],
                                       cargs=[Clbit(new_dag.cregs['c'], carg.index) for carg in
                                              node.cargs])
    new_circuit = dag_to_circuit(new_dag)
    return new_circuit

def multiprogram_initial_mapping(
        circuits: ty.List[QuantumCircuit],
        mappings: ty.List[ty.Dict[Qubit, int]]
) -> ty.Dict[Qubit, int]:
    """
    Contruct a complete initial mapping for multiprogramming process
    """

    multi_initial_mapping = dict()
    partition_qubit_number_diff = len(circuits[0].qubits)
    for index, circuit in enumerate(circuits):
        dag = circuit_to_dag(circuit)
        qubits_non_idle = [qubit for qubit in circuit.qubits if qubit not in dag.idle_wires()]
        partition_qubit_number_diff -= len(qubits_non_idle)
        for qubit in qubits_non_idle:
            multi_initial_mapping[qubit] = mappings[index][qubit]

    left_physical_qubit_list = []

    for i in range(len(circuits[0].qubits)):
        if i not in multi_initial_mapping.values():
            left_physical_qubit_list.append(i)

    j = 0
    for i, qubit in enumerate(circuits[0].qubits):
        if qubit in multi_initial_mapping.keys():
            continue
        else:
            multi_initial_mapping[qubit] = left_physical_qubit_list[j]
            j += 1

    return multi_initial_mapping

def cost_gate_num(quantum_circuit: QuantumCircuit):
    cx_num = quantum_circuit.count_ops().get("cx", 0)
    swap_num = quantum_circuit.count_ops().get("swap", 0) * 3
    ops_num = (
        cx_num + swap_num
    )
    return ops_num

def multiprogram_mapping(circuits: ty.List[QuantumCircuit],
                         hardware,
                         circuit_partitions: ty.List,
                         ):
    """
    Perform the qubit mapping algorithm for the multiprogramming mechanism.
    Include initial mapping generation and mapping transition.
    """
    circuit_partitions = [list(part.value) for part in circuit_partitions]
    print(circuit_partitions)

    # obtain the complete initial mapping of the merged circuit
    circuit_initial_mapping = dict()
    computed_initial_mappings = []
    update_circuits = []
    previous_qubit_used = 0

    num_cnots_circuits = sum([cost_gate_num(circuit) for circuit in circuits])

    for index, circuit in enumerate(circuits):
        circuit = _modify_dag_circuit(circuit, previous_qubit_used)
        update_circuits.append(circuit)
        computed_initial_mapping = initial_mapping(
            circuit, hardware, circuit_partitions[index], iterative_mapping_algorithm, cost, "sabre", 10,
            circuit_initial_mapping,
        )
        computed_initial_mappings.append(computed_initial_mapping)
        previous_qubit_used += len(circuit_partitions[index])
    merge_final_mapping = multiprogram_initial_mapping(update_circuits, computed_initial_mappings)

    # the result circuit of the merged circuit
    merge_circuit, merged_final_mapping = iterative_mapping_algorithm(
        update_circuits,
        hardware,
        merge_final_mapping,
        circuit_partitions,
        )
    num_cnots_merge_circuit = cost_gate_num(merge_circuit)
    num_additional_cnots = num_cnots_merge_circuit - num_cnots_circuits

    print(f"additional cnots is {num_additional_cnots}")

    initial_layout = merge_final_mapping.values()

    return initial_layout, merge_circuit


def circuits_partitions(circuits: ty.List[QuantumCircuit],#逻辑线路
                      hardware_graph,#目标架构
                      hardware,
                      cnot_error_matrix: np.ndarray,#链接错误率
                      readout_error: ty.List,#读出错误率
                      partition_method: ty.Callable[[
                           nx.DiGraph,
                           nx.DiGraph,
                           QuantumCircuit,
                           np.ndarray,
                           ty.List,
                           ty.Set,
                           ty.List,
                           int,
                           ty.Dict,
                       ], ty.List],
                      weight_lambda,
                      ansatz_parameter:ty.List=None,
                      crosstalk_properties: ty.Dict=None):

    initial_layouts = []
    final_circuits = []
    partitions = []

    # Sort circuit according to ascending order of CNOT density
    if not ansatz_parameter:
        circuits = sorted(circuits, key=lambda x: x.count_ops().get("cx", 0) / x.cregs[0].size, reverse=True)
        # print('排序后线路顺序')
        # for i in circuits:
        #     print(i.name)

    # Pick up K circuits that are able to be executed on hardware at the same time
    # sum(n_i) <= N (qubit number of hardware), 1 <= i <= K
    circuit_list = []
    qubit_circuit_sum = 0
    for circuit in circuits:
        qubit_circuit_sum += circuit.cregs[0].size #逻辑线路量子位数
        circuit.cregs
        if qubit_circuit_sum <= 66:
            circuit_list.append(circuit)
        else:
            print('The number of quantum qubits exceeds the limit:',qubit_circuit_sum,'>66')
            break

#目标物理架构的度
#Q66
    qubit_physical_degree = {
        4.0: [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 23, 24, 25, 26, 28, 29, 32, 33, 34, 35, 36, 38, 39, 40, 41,
              44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 56, 57, 58, 59],
        2.0: [43, 1, 3, 4, 5, 7, 19, 31, 55, 63, 64, 65], 1.0: [6]}
    largest_physical_degree = 4.0


#逻辑线路的度
    largest_logical_degrees = []
    logical_mapping_list = []
    for circuit in circuit_list:
        largest_logical_degrees.append(largest_circuit_logical_degree(circuit)[0])
        logical_mapping_list.append(largest_circuit_logical_degree(circuit)[1])

    # print('逻辑线路的最大度',largest_logical_degrees)

    # Partition independently (PHA algorithm)
    partition_fidelity_independent_list = []
    independent_partitions = []
    multiple_partition = []

    # If K > 1, circuits are executed on the hardware simultaneously (Parallelism metric), K = length of circuit list
    while len(circuit_list) > 1:
        # Partition simultaneously (multiprogramming)
        start = time.time()
        # print('并行执行状态：')
        multiple_partition = partition_circuits(circuit_list,
                                                hardware_graph,
                                                hardware,
                                                cnot_error_matrix,
                                                readout_error,
                                                qubit_physical_degree,
                                                largest_physical_degree,
                                                largest_logical_degrees,
                                                logical_mapping_list,
                                                weight_lambda,
                                                partition_method,
                                                crosstalk_properties,
                                                )
        #print(f"time is {time.time() - start}")
        # for i in multiple_partition:
        #     print('并行分区：', i.value.nodes)
        # print('并行状态分区：', multiple_partition)

        if not multiple_partition:
            print('The quantum circuit qubits number exceed limit!')
            break

        partition_fidelity_multiple = 0.0
        partition_fidelity_independent = sum(partition_fidelity_independent_list)
        for partition in multiple_partition:
            partition_fidelity_multiple += partition[0].fidelity

        # Post qubit partition process
        partition_fidelity_difference = abs(partition_fidelity_independent - partition_fidelity_multiple)
        # print("paritition fidelity difference is", partition_fidelity_difference)
        break
    if len(circuit_list) > 1:
        return multiple_partition
    else:
        return independent_partitions