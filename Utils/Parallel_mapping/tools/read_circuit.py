#读取线路

import logging
from qiskit import QuantumCircuit
from pathlib import Path

logger = logging.getLogger("read_circuit")

def read_benchmark_circuit(name: str) -> QuantumCircuit:
    src_folder = Path(__file__).parent.parent
    benchmark_folder = src_folder/"benchmarks/multipleqasm/"
    return QuantumCircuit.from_qasm_file(
        benchmark_folder / f"{name}.qasm"
    )

def benchmark_circuit_path(name: str) -> str:
    src_folder = Path(__file__).parent.parent
    benchmark_folder = src_folder/f"benchmarks/multipleqasm/{name}.qasm"
    return benchmark_folder

# print(read_benchmark_circuit(3_17_13))