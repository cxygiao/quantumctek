from qiskit.circuit.quantumcircuit import QuantumCircuit


def template_18():
    """
    Returns:
        QuantumCircuit: template as a quantum circuit.
    """
    qc = QuantumCircuit(2)
    qc.t(0)
    qc.cx(0,1)
    qc.tdg(0)
    qc.cx(0,1)
    return qc