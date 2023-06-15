from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
import pandas as pd

def dateframe_to_qasm_fun(dateframe):

    # circuit = QuantumCircuit(quantum_bit, quantum_bit)

    # for row in dateframe.iterrows():
    #     if row['k'] == 'CX':
    #         circuit.cx(int(row['c']),int(row['t']))
    #     else:
    #         circuit.append(row['k'],row['c'],row['t'])
    # print(circuit)
    # return circuit

    # 将DataFrame中的字符串型数字转换为为数值类型
    dateframe[['c', 't']] = dateframe[['c', 't']].astype(int)
    # 计算DataFrame中所有元素的最大值
    max_value = dateframe[['c', 't']].values.max()
    print('所有元素最大值：', max_value)

    # 转换为QASM格式
    qasm = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[{}];\ncreg c[{}];\n'.format(max_value+1,max_value+1)
    for index, row in dateframe.iterrows():
        if row['k'] == 'CX':
            qasm += 'cx q[%d],q[%d];\n' % (row['c'], row['t'])
        else:
           qasm += '{} q[{}];\n'.format(row['k'],row['t'])
    print(qasm)