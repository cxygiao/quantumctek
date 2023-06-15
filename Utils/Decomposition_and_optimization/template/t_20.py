from qiskit.circuit.quantumcircuit import QuantumCircuit


def template_20():
    """
    Returns:
        QuantumCircuit: template as a quantum circuit.
    """
    qc = QuantumCircuit(1)
    qc.sdg(0)
    qc.sdg(0)
    qc.sdg(0)
    qc.sdg(0)
    return qc