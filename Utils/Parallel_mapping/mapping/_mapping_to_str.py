
import typing as ty

from qiskit.circuit.quantumregister import Qubit


def mapping_to_str(partition: ty.List, mapping: ty.Dict[Qubit, int]) -> str:
    qubits_str = ["" for _ in range(len(mapping))]
    for k, v in mapping.items():
        qubits_str[partition.index(v)] = str(k)
    return ":".join(qubits_str)

def mapping_to_str_multiple(mapping: ty.Dict[Qubit, int]) -> str:
    qubits_str = ["" for _ in range(len(mapping))]
    for k, v in mapping.items():
        qubits_str[v] = str(k)
    return ":".join(qubits_str)
