from qiskit.circuit.quantumcircuit import QuantumCircuit


def template_12():
    """
    Returns:
        QuantumCircuit: template as a quantum circuit.
    """
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    qc.x(1)
    qc.cx(1, 0)
    qc.x(1)
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.x(1)
    qc.cx(0, 1)
    qc.cx(1, 0)
    return qc