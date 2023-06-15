#读取qasm文件，将线路转化为列表形式
from tools.read_circuit import read_benchmark_circuit
import os

# path = '/Users/qyyy/科研/多程序并行/multi-programming/TESTBechmark/Qasm/'
def cir_list(path):
    cir = []
    file = open(path)
    for line in file:
        line = line[:-2]
        line = line.split()
        if not line:
            continue
        elif line[0] == 'x':
            cir .append([line[0],int(line[1][2:-1])])
        elif line[0] == 's':
            cir .append([line[0],int(line[1][2:-1])])
        elif line[0] == 'h':
            cir .append([line[0],int(line[1][2:-1])])
        elif line[0] == 't':
            cir .append([line[0],int(line[1][2:-1])])
        elif line[0] == 'tdg':
            cir .append([line[0],int(line[1][2:-1])])
        elif line[0] == 'cx':
            qubits = line[1].split(',')
            qubit_1 = int(qubits[0][2:-1])
            qubit_2 = int(qubits[1][2:-1])
            cir.append([qubit_1, qubit_2])
    return cir