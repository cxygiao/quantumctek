
import typing as ty

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.quantumregister import Qubit


from Utils.Parallel_mapping.mapping.initial_mapping_construct import get_best_mapping_sabre
from Utils.Parallel_mapping.hardware.IBMQHardwareArchitecture import (
    IBMQHardwareArchitecture,
)


def initial_mapping(
    circuit: QuantumCircuit,
    hardware: IBMQHardwareArchitecture,
    partition : ty.List,
    mapping_algorithm: ty.Callable[
        [QuantumCircuit, IBMQHardwareArchitecture, ty.Dict[Qubit, int]],
        ty.Tuple[QuantumCircuit, ty.Dict[Qubit, int]],
    ],
    cost_function: ty.Callable[
        [ty.Dict[Qubit, int], QuantumCircuit, IBMQHardwareArchitecture], float
    ],
    method: str,
    maximum_allowed_calls: int,
    circuit_initial_mapping: ty.Dict[Qubit, int],

) -> ty.Dict[Qubit, int]:

    if method == "sabre":
        mapping = get_best_mapping_sabre(
            circuit, partition, mapping_algorithm, cost_function, hardware, maximum_allowed_calls, circuit_initial_mapping,
        )

    return mapping
