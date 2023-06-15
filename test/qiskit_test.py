from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

# 创建一个量子电路，包含2个量子比特和1个经典比特
circ = QuantumCircuit(2, 1)

# 对第一个量子比特进行Hadamard变换
circ.h(0)

# 对第一个量子比特作为控制位，第二个量子比特作为目标位，实现CNOT门操作
circ.cx(0, 1)

# 对第一个量子比特再次进行Hadamard变换
circ.h(0)

# 测量第一个量子比特
circ.measure(0, 0)

# 使用模拟器进行模拟
simulator = Aer.get_backend('qasm_simulator')
job = execute(circ, simulator, shots=1000)
result = job.result()
counts = result.get_counts()
print(counts)
# 输出测量结果的概率分布
plot_histogram(counts)
