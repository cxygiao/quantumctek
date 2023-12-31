import networkx as nx
import numpy
from Utils.Parallel_mapping.hardware.IBMQHardwareArchitecture import IBMQHardwareArchitecture
import logging
import typing as ty
from functools import partial

logger = logging.getLogger("hardware.distance_matrix")

#返回值类型建议符 float
#swap数量
def _get_swap_number(*_) -> float:
    return 1.0

#numpy.ndarrary对象
#a = np.array([[1,  2],  [3,  4]])
#[[1  2]
#[3  4]]
#
def get_partition_distance_matrix_swap_number(
        hardware: IBMQHardwareArchitecture,
        partition: ty.List,
) -> numpy.ndarray:
    pass


def get_qubit_readout_error(hardware: IBMQHardwareArchitecture):
    readout_error = []
    for i in range(hardware.qubit_number):
        readout_error.append(hardware.get_qubit_readout_error(i))
    return readout_error

def get_single_qubit_error_rate(hardware: IBMQHardwareArchitecture):
    single_qubit_error = []
    for i in range(hardware.qubit_number):
        single_qubit_error.append(hardware.get_single_qubit_error(i))
    return single_qubit_error

def _get_cnot_error_cost(node, hardware: IBMQHardwareArchitecture):
    source, sink = node
    return hardware.get_link_error_rate(source, sink)


def _get_swap_execution_time_cost(node, hardware: IBMQHardwareArchitecture) -> float:
    source, sink = node
    cnot_cost = hardware.get_link_execution_time(source, sink)
    reversed_cnot_cost = hardware.get_link_execution_time(sink, source)
    return cnot_cost + reversed_cnot_cost + min(cnot_cost, reversed_cnot_cost)

def _get_swap_error_cost(node, hardware: IBMQHardwareArchitecture,) -> float:
    source, sink = node
    cnot_fidelity = 1 - hardware.get_link_error_rate(source, sink)
    reversed_cnot_fidelity = 1 - hardware.get_link_error_rate(sink, source)
    return 1 - cnot_fidelity * reversed_cnot_fidelity * max(
        cnot_fidelity, reversed_cnot_fidelity
    )

def get_distance_matrix_swap_error_cost(hardware: IBMQHardwareArchitecture):
    hardware.weight_function = _get_swap_error_cost
    return nx.floyd_warshall_numpy(hardware)

def get_distance_matrix_cnot_error_cost(hardware: IBMQHardwareArchitecture):
    hardware.weight_function = _get_cnot_error_cost
    return nx.floyd_warshall_numpy(hardware)

def get_distance_matrix_execution_time_cost(hardware: IBMQHardwareArchitecture):
    hardware.weight_function = _get_swap_execution_time_cost
    return nx.floyd_warshall_numpy(hardware)

def get_distance_matrix_swap_number(
    hardware: IBMQHardwareArchitecture,
) -> numpy.ndarray:
    hardware.weight_function = _get_swap_number
    return nx.floyd_warshall_numpy(hardware)

def _get_mixed_cost(
    node,
    hardware: IBMQHardwareArchitecture,
    swap_weight: float,
    execution_time_weight: float,
    error_weight: float,
) -> float:

    swap_cost = swap_weight * _get_swap_number(node, hardware)
    execution_time_cost = execution_time_weight * _get_swap_execution_time_cost(
        node, hardware
    )
    error_cost = error_weight * _get_swap_error_cost(node, hardware)
    return (swap_cost + execution_time_cost + error_cost) / (
            swap_weight + execution_time_weight + error_weight
    )


def get_distance_matrix_mixed(
    hardware: IBMQHardwareArchitecture,
    swap_weight: float,
    execution_time_weight: float,
    error_weight: float,
) -> numpy.ndarray:
    if swap_weight < 0 or execution_time_weight < 0 or error_weight < 0:
        raise RuntimeError("All the weight should be positive.")
    coefficient_sum = swap_weight + execution_time_weight + error_weight
    if coefficient_sum < 1e-10:
        raise RuntimeError("The coefficients you provided are too small.")

    distance_matrix_swap_number = get_distance_matrix_swap_number(hardware)
    norm_swap_number = numpy.linalg.norm(distance_matrix_swap_number)
    swap_cost = swap_weight * distance_matrix_swap_number / norm_swap_number

    distance_matrix_execution_time = get_distance_matrix_execution_time_cost(hardware)
    norm_execution_time = numpy.linalg.norm(distance_matrix_execution_time)
    execution_time_cost = execution_time_weight * distance_matrix_execution_time / norm_execution_time

    distance_matrix_cnot_error_cost = get_distance_matrix_cnot_error_cost(hardware)
    norm_cnot_error_cost = numpy.linalg.norm(distance_matrix_cnot_error_cost)
    error_cost = error_weight * distance_matrix_cnot_error_cost / norm_cnot_error_cost

    return (swap_cost + execution_time_cost + error_cost) / (
            swap_weight + execution_time_weight + error_weight
    )


def get_distance_matrix_swap_number_and_error(
    hardware: IBMQHardwareArchitecture,
) -> numpy.ndarray:
    return get_distance_matrix_mixed(hardware, 0.5, 0, 0.5)

