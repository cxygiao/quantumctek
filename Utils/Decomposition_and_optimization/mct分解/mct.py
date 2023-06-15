from qiskit import QuantumCircuit,AncillaRegister,QuantumRegister
from qiskit.circuit.library import CCXGate
import matplotlib.pyplot as plt
import math
import random

#定义一个区间数组
def create_interval_list(low, high, n):
    if n > (high - low + 1):  # 允许的最大长度是[low, high]之间整数的个数
        raise ValueError("n不能大于[low, high]之间整数的个数")

    result = []
    # 从[low, high]之间选择一个随机起点
    start = random.randint(low, high - n + 1)
    for i in range(start, start + n):  # 将n个连续整数添加到结果列表中
        result.append(i)
    return result

# 当n_controls小于等于math.ceil(n_qubits / 2)
def mct_fj1(qc,controls, target):
    n_controls = len(controls)
    n_qubits = qc.num_qubits
    target = target
    toff_registers = [QuantumRegister(n_qubits)]
    toff_circuit = QuantumCircuit(*toff_registers, name='toffoli_circuit')

    for i in range(1,n_controls-1):
        toff_circuit.append(CCXGate(), [controls[n_controls-i], target-i, target-(i-1)])

    toff_circuit.append(CCXGate(), [controls[0], controls[1], controls[n_controls - 1] + 1])

    for x,j in zip(range(0, n_controls - 3),range(n_controls-2,1,-1)):
        toff_circuit.append(CCXGate(), [controls[2]+x, target-j, target-(j-1)])

    for i in range(1,n_controls-1):
        toff_circuit.append(CCXGate(), [controls[n_controls-i], target-i, target-(i-1)])

    toff_circuit.append(CCXGate(), [controls[0], controls[1], controls[n_controls - 1] + 1])

    for x,j in zip(range(0, n_controls - 3),range(n_controls-2,1,-1)):
        toff_circuit.append(CCXGate(), [controls[2]+x, target-j, target-(j-1)])

    return toff_circuit

#当n_controls大于math.ceil(n_qubits / 2)且小于(n_qubits-1)
def mct_fj2(qc,controls, target):

    n_qubits = len(qc.qubits)
    circ_registers = [QuantumRegister(n_qubits)]
    circ_circuit = QuantumCircuit(*circ_registers, name='toffoli_circuit')

    circ_circuit.mcx(controls[:math.ceil(n_qubits/2)],target-1)


    c = create_interval_list(target-(n_qubits-math.ceil(n_qubits/2)-1), target-1,n_qubits-math.ceil(n_qubits/2)-1)
    circ_circuit.mcx(c,target)
    circ_circuit.mcx(controls[:math.ceil(n_qubits / 2)], target - 1)
    circ_circuit.mcx(c, target)
    return circ_circuit

#当n_controls==(n_qubits-1)
def mct_fj3(qc,controls, target):

    n_qubits = qc.num_qubits
    ancillas = QuantumRegister(1, 'anc')
    circ_registers = [QuantumRegister(n_qubits)]
    circ_circuit = QuantumCircuit(*(circ_registers + [ancillas]), name='toffoli_circuit')
    if n_controls > 3:
        circ_circuit.mcx(controls[:math.ceil(n_qubits / 2)], target)

        c = create_interval_list( target- (n_qubits - math.ceil(n_qubits / 2)-1), target,
                             n_qubits - math.ceil(n_qubits / 2))
        circ_circuit.mcx(c, ancillas[0])
        circ_circuit.mcx(controls[:math.ceil(n_qubits / 2)], target)
        circ_circuit.mcx(c, ancillas[0])

    elif n_controls == 3:
        circ_circuit.ccx(controls[2], target, ancillas[0])
        circ_circuit.ccx(controls[0], controls[1], target)
        circ_circuit.ccx(controls[2], target, ancillas[0])
        circ_circuit.ccx(controls[0], controls[1], target)
    return circ_circuit


if __name__ == '__main__':
    qubits = int(input('输入量子位个数：'))
    qc = QuantumCircuit(qubits)
    control_input = input("请输入一个从0开始连续的控制位数组，元素之间用空格分隔：")
    controls = control_input.split()
    controls = [int(x) for x in controls]
    target = int(input('输入目标位的序号(量子位个数减一)：'))
    qc.mct(controls, target)

    n_controls = len(controls)
    n_qubits = qc.num_qubits
    if n_controls <= math.ceil(n_qubits / 2):
        fj = mct_fj1(qc, controls, target)
        # print(fj)
        fj.draw()
        plt.show()
    elif math.ceil(n_qubits / 2) < n_controls < (n_qubits-1):
        fj = mct_fj2(qc, controls, target)
        # print(fj)
        fj.draw()
        plt.show()
    elif n_controls == (n_qubits-1):
        fj = mct_fj3(qc, controls, target)
        # print(fj)
        fj.draw()
        plt.show()