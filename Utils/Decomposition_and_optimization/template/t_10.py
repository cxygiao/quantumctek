from qiskit.circuit.quantumcircuit import QuantumCircuit


def template_10():
    """
    Returns:
        QuantumCircuit: template as a quantum circuit.
    """
    qc = QuantumCircuit(2)
    qc.s(0)
    qc.cx(0, 1)
    qc.sdg(0)
    qc.cx(0, 1)
    return qc