from math import pi
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
import pandas as pd
import re

def get_data(str):
    # pattern = re.compile("\d")
    # result = re.findall(pattern, str)
    pattern = re.compile(r'\d+')  # 查找数字
    result = pattern.findall(str)
    return result


'''
读取qasm文件
'''
def converter_num_from_qasm(input_file_name):
    # df_ori_qc = pd.DataFrame(columns=['k', 'c', 't'])  # 近邻化 以dataframe形式存储的近邻化量子电路
    qasm_file = open(input_file_name, 'r')
    iter_f = iter(qasm_file)
    # 获取量子位
    q_name_list = []  # 量子位名寄存器
    q_num_list = []  # 量子位数寄存器
    line_num = 0 # 行数
    for line in iter_f:  # 一行行遍历
        line_num += 1
        if line[0:4] == 'qreg':
            # print(line)
            q_name_list.append(line[5:line.index('[')])
            q_num_list.append(line[line.index('[')+1:line.index(']')])
    print(q_name_list)
    for i in range(len(q_num_list)):
        q_num_list[i] = int(q_num_list[i])
    print(q_num_list)

    qubit_num = sum(q_num_list)
    gate_num = line_num - 3 - len(q_name_list)

    return qubit_num,gate_num,q_name_list,q_num_list


def converter_dataframe_from_qasm(input_file_name,qubit_num,gate_num,q_name_list,q_num_list):
    df_ori_qc = pd.DataFrame(columns=['k', 'c', 't'])  # 近邻化 以dataframe形式存储的近邻化量子电路
    qasm_file = open(input_file_name, 'r')
    iter_f = iter(qasm_file)
    count = 0
    base_line = 3+len(q_name_list)
    # 获取量子门
    for line in iter_f:  # 一行行遍历
        if count >= base_line:
            # CNOT门
            if line[0:2] == 'CZ' or line[0:2] == 'cz':
                cnot = get_two_qubit(line,q_name_list,q_num_list)
                cnot_control = cnot[0]
                cnot_target = cnot[1]
                df_ori_qc.loc[count-base_line] = ['CZ', cnot_control, cnot_target]
            else:
            #     # print(line.index(' '))
                df_ori_qc.loc[count-base_line] = [line[0:line.index(' ')+1], -1, get_single_qubit(line,q_name_list,q_num_list)]
            if 'measure' in line:
                df_ori_qc.loc[count - base_line] = ['measure','measure','measure']
        count += 1
    print(df_ori_qc)
    return df_ori_qc

'''h a1[0]; >>> 3'''
def get_single_qubit(line,q_name_list,q_num_list):
    q_order = q_order_list(q_num_list)
    qubit = line[line.index(' ')+1:line.index(';')]
    qubit_name = qubit[0:qubit.index('[')]
    qubit_num = int(get_data(qubit)[-1])
    new_qubit = q_order[q_name_list.index(qubit_name)]+qubit_num
    return new_qubit


'''cx v[1],a1[0]; >>> [v[1],a1[0]]   cnot门'''
def get_two_qubit(line,q_name_list,q_num_list):
    qubit_list = []
    q_order = q_order_list(q_num_list)
    qubit_list.append(line[line.index(' ')+1:line.index(',')])
    qubit_list.append(line[line.index(',')+1:line.index(';')])
    first_qubit_name = qubit_list[0][0:qubit_list[0].index('[')]
    second_qubit_name = qubit_list[1][0:qubit_list[1].index('[')]
    first_qubit_num = int(get_data(qubit_list[0])[-1])
    second_qubit_num = int(get_data(qubit_list[1])[-1])
    new_qubit_list = [q_order[q_name_list.index(first_qubit_name)]+first_qubit_num,q_order[q_name_list.index(second_qubit_name)]+second_qubit_num]
    # print(new_qubit_list)
    return new_qubit_list


'''[1, 2, 1, 1, 1] >>> [0, 1, 3, 4, 5]'''
def q_order_list(q_num_list):
    q_order = []
    for i in range(len(q_num_list)):
        q_order.append(sum(q_num_list[:i]))
    # print(q_order)
    return q_order


# if __name__ == '__main__':
#     input_filename = r'D:/PycharmProjects/pythonProject/qasm/2z2fj_opt.qasm'
#
#
#     qubit_num, gate_num,q_name_list,q_num_list = converter_num_from_qasm(input_filename)
#
#     # print(get_two_qubit('cx v[1],a1[0];',q_name_list,q_num_list))
#     #
#     # print(get_single_qubit('h a1[0];',q_name_list,q_num_list))
#
#     df_ori_qc = converter_dataframe_from_qasm(input_filename,qubit_num,gate_num,q_name_list,q_num_list)
