from qiskit.circuit.quantumcircuit import QuantumCircuit


def template_17():
    """
    Returns:
        QuantumCircuit: template as a quantum circuit.
    """
    qc = QuantumCircuit(1)
    qc.tdg(0)
    qc.tdg(0)
    qc.s(0)
    return qc