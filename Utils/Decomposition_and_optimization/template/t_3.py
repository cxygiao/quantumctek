from qiskit.circuit.quantumcircuit import QuantumCircuit


def template_3():
    """
    Returns:
        QuantumCircuit: template as a quantum circuit.
    """
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.h(0)
    return qc