from Utils.Parallel_mapping.hardware.IBMQHardwareArchitecture import IBMQHardwareArchitecture
from Utils.Parallel_mapping.partition_process.partition import Partition
from qiskit import QuantumCircuit
from collections import defaultdict

import logging
import typing as ty
import numpy as np
import networkx as nx
import itertools
import matplotlib.pyplot as plt

logger = logging.getLogger("qubit_partition")

#物理量子比特的保真度计算
#量子保真度=相邻位置连接错误率+读出错误率
def qubit_fidelity_degree(qubit_index: int,
                 hardware: IBMQHardwareArchitecture,
                 cnot_error_matrix: np.ndarray,
                 readout_error: ty.List,
                 weight_lambda: int,):
    """
    Return the fidelity degree of a qubit.物理量子比特保真度
    F_degree_Qi  = lambda * sum(1 - E[Qi][Qj]) + (1 - R_Qi), Qj are the neighbor qubits of Qi.
    """
    degree = 0.0
    cnot_error_matrix = np.array(cnot_error_matrix)
    for neighbour in hardware.neighbors(qubit_index):
        # print('neighbour', neighbour)
        # print(cnot_error_matrix.item(qubit_index, neighbour))
        degree += (1 - cnot_error_matrix.item(qubit_index, neighbour))
    degree *= weight_lambda
    degree += (1 - readout_error[qubit_index])
    return degree


def find_best_qubit(qubit_list: ty.List,
                    hardware: IBMQHardwareArchitecture,
                    cnot_error_matrix: np.ndarray,
                    readout_error: ty.List,
                    weight_lambda: int,):
    """
    For a given list of qubits, find the qubit with the highest fidelity degree.
    """
    best_qubit_fidelity_degree = -1
    best_qubit = -1
    for qubit in qubit_list:
        new_qubit_fidelity_degree = qubit_fidelity_degree(qubit, hardware, cnot_error_matrix, readout_error, weight_lambda)
        if new_qubit_fidelity_degree > best_qubit_fidelity_degree:
            best_qubit = qubit
            best_qubit_fidelity_degree = new_qubit_fidelity_degree
    return best_qubit


def find_qubit(partition: ty.List,
               hardware: IBMQHardwareArchitecture,
               cnot_error_matrix: np.ndarray,
               readout_error: ty.List,
               weight_lambda: int,):
    """
    Find the qubit to merge into the partition.
    First, we choose the best qubit(highest fidelity degree) of the current partition.
    Second, from the neighour qubits of the best qubit, we choose the one with highest
    fidelity degree to merge into the partition.
    """

    partition = sorted(partition, key=lambda x: qubit_fidelity_degree(x, hardware, cnot_error_matrix, readout_error,
                                                                      weight_lambda), reverse=True)
    for qubit_index in partition:
        neighbour_list = []
        for neighbour in hardware.neighbors(qubit_index):
            if neighbour not in partition:
                neighbour_list.append(neighbour)
        if not neighbour_list:
            continue
        else:
            best_qubit = find_best_qubit(neighbour_list, hardware, cnot_error_matrix, readout_error, weight_lambda)
            return best_qubit

    return None


def partition_hardware_heuristic(
        hardware: nx.DiGraph,
        hardware_graph: nx.DiGraph,
        circuit: QuantumCircuit,
        cnot_error_matrix: np.ndarray,
        readout_error: ty.List,
        qubits_used: ty.Set,
        starting_point: ty.List,
        weight_lambda: int,
        crosstalk_properties: ty.Dict=None):
    """
    Qubit fidelity degree-based heuristic subgraph partition algorithm.
    :param hardware: hardware target
    :param hardware_graph: the graph of the hardware target
    :param circuit: circuit for partition
    :param cnot_error_matrix: cnot error matrix of hardware
    :param readout_error: list of readout error of physical qubits
    :param qubits_used: qubits used by other circuits
    :param starting_point: starting points collected
    :param weight_lambda: weight parameter to weight the CNOT error rate
    :param crosstalk_properties: CNOT pairs with strong crosstalk effect
    :return: A list of partition candidates
    """

    # print('目前使用的是启发式分区方法！')
    circuit_qubit_num = circuit.cregs[0].size
    sub_partitions = []
    for i in starting_point:
        sub_graph = []
        num_qubit = 0
        while(num_qubit < circuit_qubit_num):
            if not sub_graph:
                sub_graph.append(i)
                num_qubit += 1
                continue
            new_qubit = find_qubit(sub_graph, hardware, cnot_error_matrix, readout_error, weight_lambda)
            if new_qubit!= None:
                sub_graph.append(new_qubit)
                num_qubit += 1
                continue
            else:
                break
        # print('候选子图', sub_graph)
        #物理量子位：逻辑量子位
        if len(sub_graph) == circuit_qubit_num:#已经找到足够大子图
            if not qubits_used:
                sub_graph = Partition(hardware_graph.subgraph(sub_graph))
                sub_graph.partition_connectivity_error_rate_heuristic(
                    hardware,
                    circuit,
                    cnot_error_matrix,
                    readout_error,
                    )
                sub_partitions.append(sub_graph)
                # for i in sub_partitions:
                #     print('候选子图列表：', i)
            else:
                flag = True
                for qubit in sub_graph:
                    if qubit in qubits_used:
                        flag = False
                        break
                if flag == True:
                    crosstalk_pairs = find_crosstalk_pair(sub_graph, crosstalk_properties, qubits_used)
                    sub_graph = Partition(hardware_graph.subgraph(sub_graph))
                    sub_graph.partition_connectivity_error_rate_heuristic(
                        hardware,
                        circuit,
                        cnot_error_matrix,
                        readout_error,
                        crosstalk_pairs,
                    )
                    sub_partitions.append(sub_graph)
                    # print('不够大候选子图', sub_partitions)
    # print('所有候选分区：', sub_partitions)
    return sub_partitions


def partition_hardware(hardware: IBMQHardwareArchitecture,
                       hardware_graph: nx.DiGraph,
                       circuit: QuantumCircuit,
                       cnot_error_matrix: np.ndarray,
                       readout_error: ty.List,
                       qubits_used: ty.Set,
                       starting_point: ty.List,
                       weight_lambda: int,
                       crosstalk_properties: ty.Dict=None):
    """
    Greedy sub-graph partition algorithm.
    """

    qubit_num = circuit.cregs[0].size
    sub_partition = []
    for sub_graph in itertools.combinations(hardware_graph.nodes, qubit_num):
        G_sub = hardware_graph.subgraph(sub_graph)
        if nx.is_weakly_connected(G_sub):
            if not qubits_used:
                sub_graph = Partition(G_sub)
                sub_graph.partition_connectivity_error_rate_greedy(
                    hardware,
                    circuit,
                    cnot_error_matrix,
                    readout_error,
                )
                sub_partition.append(sub_graph)
            else:
                flag = True
                for qubit in sub_graph:
                    if qubit in qubits_used:
                        flag = False
                        break
                if flag == True:
                    crosstalk_pairs = find_crosstalk_pair(sub_graph, crosstalk_properties, qubits_used)
                    sub_graph = Partition(G_sub)
                    sub_graph.partition_connectivity_error_rate_greedy(
                        hardware,
                        circuit,
                        cnot_error_matrix,
                        readout_error,
                        crosstalk_pairs,
                    )
                    sub_partition.append(sub_graph)

    return sub_partition


def find_crosstalk_pair(partition: ty.Tuple,
                        crosstalk_properties: ty.Dict,
                        qubits_used: ty.Set):
    """
    Check if there are crosstalk paris inside of the current partition that have
    strong crosstalk effect afftected by the partitions for other circuits
    :param partition: current partition
    :param crosstalk_properties: CNOT paris with high crosstalk effect
                                 E(g_i|g_j) > 3 * E(g_i) or E(g_j|g_i) > 3 * E(g_j)
    :param qubits_used: qubits that used in partitions for other circuits
    :return: the crosstalk pairs
    """
    crosstalk_pair = dict()
    if not qubits_used or not crosstalk_properties:
        return crosstalk_pair
    for q1 in partition:
        for q2 in partition:
            if (q1,q2) in crosstalk_properties.keys():
                for i in qubits_used:
                    for j in qubits_used:
                        if (i,j) in crosstalk_properties[(q1,q2)].keys():
                            crosstalk_pair[(q1,q2)] = crosstalk_properties[(q1,q2)][(i,j)]
    return crosstalk_pair


def hardware_qubit_physical_degree(hardware: IBMQHardwareArchitecture):
    """
    Return the physical node degree of the physical qubit and the largest physical node degree.
    """
    qubit_degree = defaultdict(list)
    largest_physical_degree = 0
    for num in range(hardware.qubit_number):
        degree = hardware.degree(num) / 2
        if degree > largest_physical_degree:
            largest_physical_degree = degree
        qubit_degree[degree].append(num)
    return qubit_degree, largest_physical_degree


def largest_circuit_logical_degree(circuit: QuantumCircuit):
    """
    Iterate over all the gates of the circuit and obtain the largest logical
    node degree of the logical qubit.
    """
    # print('逻辑量子线路的度')
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
            # print(qubits)
            qubit_1 = int(qubits[0][2:-1])
            # print(qubit_1)
            qubit_2 = int(qubits[1][2:-1])
            if not logical_qubit_degree[qubit_1] or qubit_2 not in logical_qubit_degree[qubit_1]:
                logical_qubit_degree[qubit_1].append(qubit_2)
            if not logical_qubit_degree[qubit_2] or qubit_1 not in logical_qubit_degree[qubit_2]:
                logical_qubit_degree[qubit_2].append(qubit_1)
    #logic_qubit_degree{逻辑量子位：[对应连接量子位]}  []的长度即为该逻辑量子位的度
    # print('logical circuit qubit mapping list:',logical_qubit_degree)
    #默认排序度从小到大
    # print('sorted circuit qubit mapping list:', sorted(logical_qubit_degree.items(), key = lambda x: len(x[1])))
    # print(list(logical_qubit_degree.keys())[::-1])
    mapping_list = []
    mapping_list = list(logical_qubit_degree.keys())[::-1]
    return len(sorted(logical_qubit_degree.values(), key=lambda x: len(x))[-1]), mapping_list


def starting_point_heuristic(hardware_qubit_physical_degree: ty.Dict,
                             largest_physical_degree: float,
                             largest_logical_degree: int):
    """
    If  largest_physical_degree < largest_logical_degree, the set of physical qubits with the
    largest physical node degree is collected as the list of starting points.
    Else, the physical qubits whose physical node degree is not less than the largst logical node
    degree are collected as starting points.
    """
    staring_points = []
    if largest_physical_degree < largest_logical_degree:
        return hardware_qubit_physical_degree[largest_physical_degree]
    else:
        for key, value in hardware_qubit_physical_degree.items():
            if key >= largest_logical_degree:
                staring_points.extend(value)
    return staring_points


def partition_circuits(circuits: ty.List[QuantumCircuit],
                       hardware_graph: nx.DiGraph,
                       hardware: IBMQHardwareArchitecture,
                       cnot_error_matrix: np.ndarray,
                       readout_error: ty.List,
                       qubit_physical_degree: ty.Dict,
                       largest_physical_degree: float,
                       largest_logical_degrees: ty.List,
                       logical_mapping_list: ty.List,
                       weight_lamda: int,
                       partition_method: ty.Callable[[
                           IBMQHardwareArchitecture,
                           nx.DiGraph,
                           QuantumCircuit,
                           np.ndarray,
                           ty.List,
                           ty.Set,
                           ty.List,
                           int,
                           ty.Dict,
                       ], ty.List] = partition_hardware_heuristic,
                       crosstalk_properties: ty.Dict=None):
    """
    Allocate partitions for multiple circuits.
    """
    partition_circuit_list = []
    mapping_list = []
    qubits_used = set()
    partition_circuit_tuple = []
#enumerate 给序列加上索引
#[(0,cir1),(1,cir2)]
    for index, circuit in enumerate(circuits):
        #starting_point 分区开始节点
        starting_point = starting_point_heuristic(qubit_physical_degree, largest_physical_degree, largest_logical_degrees[index])
        # print('starting points:', starting_point)
        partition_list = sorted(partition_method(hardware,
                                                 hardware_graph,
                                                 circuit,
                                                 cnot_error_matrix,
                                                 readout_error,
                                                 qubits_used,
                                                 starting_point,
                                                 weight_lamda,
                                                 crosstalk_properties),
                                key=lambda x: x.fidelity)

        # for i in range(0, 5):
        #     print('已排序保真度分区', partition_list[i].value.nodes, partition_list[i].fidelity)

        if not partition_list:
            logger.info(f"Too many simultaneous circuit. No suitable partitions'.")
            return []
        else:
            partition_circuit_list.append(partition_list[0])
            initial_mapping = dict(zip(logical_mapping_list[index], partition_list[0].value.nodes))
            partition_circuit_tuple.append([partition_list[0], initial_mapping])
        for qubit in partition_list[0].value.nodes:
            qubits_used.add(qubit)
        # print('分配到的物理位置：', partition_list[0].value.nodes)
        # print('剩余逻辑线路信息：',logical_mapping_list)
        # print('物理逻辑对应位：', initial_mapping)
    return partition_circuit_tuple