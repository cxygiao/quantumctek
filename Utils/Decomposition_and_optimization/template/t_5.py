from qiskit.circuit.quantumcircuit import QuantumCircuit


def template_5():
    """
    Returns:
        QuantumCircuit: template as a quantum circuit.
    """
    qc = QuantumCircuit(2)
    qc.cx(0, 1)
    qc.h(1)
    qc.cx(0, 1)
    qc.s(0)
    qc.sdg(1)
    qc.cx(0, 1)
    qc.s(1)
    qc.h(1)
    return qc