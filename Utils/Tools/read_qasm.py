# -*- coding: utf-8 -*-
from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
import pandas as pd
import re
from qiskit import BasicAer
from qiskit.quantum_info import Operator
backend = BasicAer.get_backend('unitary_simulator')

"""
字符串表达式 获取门的位置
"""
'''
dataframe格式的电路转为设备的基础门库
'''


def df_to_cirrz(quantum_circuit):
    quantum_bit = 5
    circuit = QuantumCircuit(quantum_bit, quantum_bit)

    for i in range(quantum_circuit.shape[0]):
        k = quantum_circuit.iloc[i, 0]  # 种类

      #  if quantum_circuit.iloc[i, 1] is not None:
        c = int(quantum_circuit.iloc[i, 1]) #

        t = int(quantum_circuit.iloc[i, 2])  #

        if k == 'cnot':
            circuit.cx(c, t)
        elif k == 'swap':
            circuit.cx(c, t)
            circuit.cx(t, c)
            circuit.cx(c, t)
        elif k == 'tdg':
            circuit.rz(pi/4*7, t)
        elif k == 't':
            circuit.rz(pi / 4, t)
        elif k == 'x':
            circuit.x(t)

        elif k == 'h':
            circuit.rz(pi / 2, t)
            circuit.sx(t)
            circuit.rz(pi / 2, t)

    circuit.measure(range(quantum_bit), range(quantum_bit))
    return circuit


def get_data(str):
    # pattern = re.compile("\d")
    # result = re.findall(pattern, str)
    pattern = re.compile(r'\d+')  # 查找数字
    result = pattern.findall(str)
    return result


'''
读取qasm文件
'''
def converter_dataframe_from_qasm(input_file_name):
    df_ori_qc = pd.DataFrame(columns=['k', 'c', 't'])  # 近邻化 以dataframe形式存储的近邻化量子电路
    qasm_file = open(input_file_name, 'r')
    iter_f = iter(qasm_file)
    reserve_line = 5
    num_line = 0
    for line in iter_f:  # 遍历文件，一行行遍历，读取文本
        num_line += 1
        if num_line <= reserve_line:
            continue
        else:
            if line[0:2] == 'CX' or line[0:2] == 'cx':
                '''获取CNOT'''
                cnot = get_data(line)
                cnot_control = cnot[0]
                cnot_target = cnot[1]
                df_ori_qc = df_ori_qc.append([{'k': 'cnot', 'c': cnot_control, 't': cnot_target}], ignore_index=True)
            else:
                ''''获取单量子比特门'''
                single_qubit_gate = get_data(line)[0]

                if line[0:1] == "h":
                    df_ori_qc = df_ori_qc.append([{'k': 'h', 'c': -1, 't': single_qubit_gate}], ignore_index=True)
                if line[0:1] == "x":
                    df_ori_qc = df_ori_qc.append([{'k': 'x', 'c': -1, 't': single_qubit_gate}], ignore_index=True)
                if line[0:2] == "t ":
                    df_ori_qc = df_ori_qc.append([{'k': 't', 'c': -1, 't': single_qubit_gate}], ignore_index=True)
                if line[0:2] == "rz":
                    df_ori_qc = df_ori_qc.append([{'k': 'z', 'c': -1, 't': single_qubit_gate}], ignore_index=True)
                if line[0:3] == "tdg":
                    df_ori_qc = df_ori_qc.append([{'k': 'tdg', 'c': -1, 't': single_qubit_gate}], ignore_index=True)
    print(df_ori_qc)
    # df_ori_qc.reindex(index=df_ori_qc.index[::-1])
    # df_ori_qc = df_ori_qc.iloc[::-1]
    # print(df_ori_qc)
    print('circuit length:', end='')
    print(len(df_ori_qc))
    return df_ori_qc


def converter_dataframe_from_qasm2(input_file_name):
    df_ori_qc = pd.DataFrame(columns=['k', 'c', 't'])  # 近邻化 以dataframe形式存储的近邻化量子电路
    qasm_file = open(input_file_name, 'r')
    iter_f = iter(qasm_file)
    reserve_line = 5
    num_line = 0
    for line in iter_f:  # 遍历文件，一行行遍历，读取文本

        num_line += 1
        if num_line <= reserve_line:
            continue
        else:
            if line[0:2] == 'CX' or line[0:2] == 'cx':
                '''获取CNOT'''
                cnot = get_data(line)
                cnot_control = cnot[0]
                cnot_target = cnot[1]
                df_ori_qc = df_ori_qc.append([{'k': 'cnot', 'c': cnot_control, 't': cnot_target}], ignore_index=True)
            else:
                ''''获取单量子比特门'''
                single_qubit_gate = get_data(line)[0]

                if line[0:1] == "h":
                    df_ori_qc = df_ori_qc.append([{'k': 'h', 'c': -1, 't': single_qubit_gate}], ignore_index=True)
                if line[0:1] == "x":
                    df_ori_qc = df_ori_qc.append([{'k': 'x', 'c': -1, 't': single_qubit_gate}], ignore_index=True)
                if line[0:2] == "t ":
                    df_ori_qc = df_ori_qc.append([{'k': 't', 'c': -1, 't': single_qubit_gate}], ignore_index=True)
                if line[0:2] == "rz":
                    df_ori_qc = df_ori_qc.append([{'k': 'z', 'c': -1, 't': single_qubit_gate}], ignore_index=True)
                if line[0:3] == "tdg":
                    df_ori_qc = df_ori_qc.append([{'k': 'tdg', 'c': -1, 't': single_qubit_gate}], ignore_index=True)
    print(df_ori_qc)
    # df_ori_qc.reindex(index=df_ori_qc.index[::-1])
    df_ori_qc = df_ori_qc.iloc[::-1]
    # print(df_ori_qc)
    print('circuit length:', end='')
    print(len(df_ori_qc))
    return df_ori_qc


if __name__ == '__main__':
    input_filename = r'E:\python\quantumctek\qasm\mini_alu_305.qasm'
    df_ori_qc = converter_dataframe_from_qasm(input_filename)
    circuit = df_to_cirrz(df_ori_qc)
    print(circuit)


