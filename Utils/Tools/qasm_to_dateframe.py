'''
功能：将生成的电路转化为 qasm 文件，再转化为 datefrom 格式
作者：陈新宇
版本: 1.0
完成时间：2023.4.20
'''

from qiskit import QuantumCircuit
import pandas as pd
import re

''' 将circuit转化为qasm的list格式 
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];
转化为：
['OPENQASM 2.0;', 'include "qelib1.inc";', 'qreg q[2];', 'creg c[2];', 'h q[0];', 'cx q[0],q[1];', 'measure q[0] -> c[0];', 'measure q[1] -> c[1];']
'''
def qc_to_qasm_list(qc):
    # qc 转化为 qsam
    qc_qasm = qc.qasm()  # str类型
    print(qc_qasm)
    # print(qc_qasm.count(';'))
    # print(qc_qasm.find(';'))
    lst = []
    # ；的索引号，用于换行
    for pos, char in enumerate(qc_qasm):
        if (char == ';'):
            lst.append(pos)
    # print(lst)
    qc_qasm_list = []
    qc_qasm_list.append(qc_qasm[0:lst[0] + 1])
    # print(qc_qasm_list)

    for i in range(len(lst) - 1):
        qc_qasm_list.append(qc_qasm[lst[i] + 2:lst[i + 1] + 1])
    # print(qc_qasm_list)
    return qc_qasm_list

''' 获取数字 '''
def get_data(str):
    pattern = re.compile(r'\d+')  # 查找数字
    result = pattern.findall(str)
    return result

''' 将list格式的qasm转化为datefrome格式 '''
def qasm_list_to_df(qc_qasm_list):
    df_ori_qc = pd.DataFrame(columns=['k', 'c', 't'])  # 以dataframe形式存储的量子电路
    for i in range(4, len(qc_qasm_list)):  # 一行行遍历
        line = qc_qasm_list[i]
        if line[0:2] == 'CX' or line[0:2] == 'cx':
            '''获取CNOT'''
            cnot = get_data(line)
            cnot_control = cnot[0]
            cnot_target = cnot[1]
            df_ori_qc.loc[i - 4] = ['CX', cnot_control, cnot_target]
        if line[0:2] == 'CZ' or line[0:2] == 'cz':
            '''获取Cz'''
            cz = get_data(line)
            cz_control = cz[0]
            cz_target = cz[1]
            df_ori_qc.loc[i - 4] = ['CZ', cz_control, cz_target]
        else:
            ''''获取单量子比特门'''
            single_qubit_gate = get_data(line)[0]
            if line[0:1] == "h" or line[0:1] == "H":
                df_ori_qc.loc[i - 4] = ['H', -1, single_qubit_gate]
            if line[0:1] == "t" or line[0:1] == "T":
                df_ori_qc.loc[i - 4] = ['T', -1, single_qubit_gate]
            if line[0:1] == "x" or line[0:1] == "X":
                df_ori_qc.loc[i - 4] = ['X', -1, single_qubit_gate]
            if line[0:1] == "y" or line[0:1] == "Y":
                df_ori_qc.loc[i - 4] = ['Y', -1, single_qubit_gate]
            if line[0:1] == "z" or line[0:1] == "Z":
                df_ori_qc.loc[i - 4] = ['Z', -1, single_qubit_gate]
            if line[0:1] == "s" or line[0:1] == "S":
                df_ori_qc.loc[i - 4] = ['S', -1, single_qubit_gate]
            if line[0:1] == "RZ" or line[0:1] == "rz":
                df_ori_qc.loc[i - 4] = ['RZ', -1, single_qubit_gate]
            if line[0:1] == "RX" or line[0:1] == "rx":
                df_ori_qc.loc[i - 4] = ['RX', -1, single_qubit_gate]
            if line[0:1] == "RY" or line[0:1] == "ry":
                df_ori_qc.loc[i - 4] = ['RY', -1, single_qubit_gate]
    print(df_ori_qc)
    return df_ori_qc

if __name__ == '__main__':
    # 创建一个量子电路
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    # 将 circuit 转化为 qasm 的 list 格式
    qc_qasm_list = qc_to_qasm_list(qc)
    # 将 list 格式的 qasm 转化为 datefrome 格式
    qasm_list_to_df(qc_qasm_list)




