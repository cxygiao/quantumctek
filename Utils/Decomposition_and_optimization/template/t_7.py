from qiskit.circuit import QuantumCircuit


def template_7():
    """
    Returns:
        QuantumCircuit: template as a quantum circuit.
    """
    qc = QuantumCircuit(2)
    qc.cx(0,1)
    qc.t(0)
    qc.t(0)
    qc.cx(0,1)
    qc.tdg(0)
    qc.tdg(0)
    return qc