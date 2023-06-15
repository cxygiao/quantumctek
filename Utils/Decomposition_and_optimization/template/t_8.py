from qiskit.circuit.quantumcircuit import QuantumCircuit


def template_8():
    """
    Returns:
        QuantumCircuit: template as a quantum circuit.
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.h(1)
    qc.cx(0, 1)
    qc.h(0)
    qc.h(1)
    qc.cx(1, 0)
    return qc