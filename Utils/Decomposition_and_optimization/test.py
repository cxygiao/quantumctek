from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import MCMT

# 将MCT电路转换为NCT电路
nct = QuantumCircuit(10)
nct.ccx(0, 1, 3)
nct.ccx(2, 1, 3)
nct.mct([0,1,2],3)


# clifford_t = nct.decompose()

# 将NCT电路转换为Clifford+T电路
# clifford_t = transpile(nct, basis_gates=['x','y','z','h','s','t','cx'], optimization_level=3)
basis_gates = ['x', 'y', 'z', 'h', 's','sdg', 't','tdg','rz','rx','ry', 'cz']
clifford_t = transpile(nct, basis_gates=basis_gates)

print(clifford_t)
