# 先安装依赖包 pip install ezQpy==0.2.0.2 和 pip install isqmap==0.2
from ezQpy import *
from qiskit import QuantumCircuit

# # login_key在 https://www.quantumcomputer.ac.cn/User  下的SDK密钥
# account = Account(login_key='b14d3912329ca67b607a59412eeb4f9d', machine_name='ClosedBetaQC')
#
# fileqasm = r'E:\python\quantumctek\qasm\test_qasm\cnt3-5_179.qasm'
# circuit = QuantumCircuit.from_qasm_file(fileqasm)
# #print(circuit)
# cost = circuit.count_ops()['cx']
# print(cost)
# print(circuit.depth())
#
# # qcis_circuit = '''
# # H Q7
# # X Q1
# # H Q1
# # CZ Q7 Q1
# # H Q1
# # M Q7
# # M Q1
# # '''
#
# qcis_circuit = account.convert_qasm_to_qcis_from_file(fileqasm)
# # print(qcis_circuit)
#
# count_list = []
# depth_list = []
# qasm_list = []
#
# for i in range(0, 20):
#     qcis_circuit = account.qcis_mapping_isq(qcis_circuit)
#     # print(qcis_circuit)
#     qasm = account.convert_qcis_to_qasm(qcis_circuit)
#     # print(qasm)
#     qasm_list.append(qasm)
#     mapped_circuit = QuantumCircuit.from_qasm_str(qasm)
#     count_list.append(mapped_circuit.count_ops()['cz'])
#     depth_list.append(mapped_circuit.depth())
#     # print(mapped_circuit.count_ops()['cz'])
#     # print(mapped_circuit.depth())
# min_count = count_list[0]
# mini = 0
# for ii in range(len(count_list)):
#     if min_count > count_list[ii]:
#         min_count = count_list[ii]
#         mini = ii
# print(mini)
# print(count_list)
# print(depth_list)
# print(min_count)
# # print(qasm_list[mini])

def run():
    # login_key在 https://www.quantumcomputer.ac.cn/User  下的SDK密钥
    account = Account(login_key='', machine_name='ClosedBetaQC')

    fileqasm = r'E:\python\quantumctek\qasm\test_qasm\ham15_298.qasm'

    qcis_circuit = account.convert_qasm_to_qcis_from_file(fileqasm)

    qcis_circuit = account.qcis_mapping_isq(qcis_circuit)
    qasm = account.convert_qcis_to_qasm(qcis_circuit)
    mapped_circuit = QuantumCircuit.from_qasm_str(qasm)
    cz_num = mapped_circuit.count_ops()['cz']
    depth = mapped_circuit.depth()

    return qcis_circuit,cz_num,depth


if __name__ == '__main__':
    cz_num_list = []
    depth_list = []
    for i in range(100):
        print(i)
        qcis_circuit, cz_num, depth = run()
        print(cz_num)
        print(depth)
        cz_num_list.append(cz_num)
        depth_list.append(depth)
    print(cz_num_list)
    print(depth_list)
    print(min(cz_num_list))
    print(depth_list[cz_num_list.index(min(cz_num_list))])

