from qiskit.circuit.quantumcircuit import QuantumCircuit


def template_16():
    """
    Returns:
        QuantumCircuit: template as a quantum circuit.
    """
    qc = QuantumCircuit(1)
    qc.t(0)
    qc.t(0)
    qc.sdg(0)
    return qc