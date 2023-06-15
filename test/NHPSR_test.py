from qiskit import QuantumCircuit

import Utils.Tools.qasm_to_list as qasm_to_list

def estimated_fidelity(gate_list):
    error_rate = {'0,1':0.02523,'1,2':0.00871,'1,3':0.01851,'3,4':0.01595}
    # print(error_rate.get('0,1'))
    fidelity = 1
    for i in range(len(gate_list)):
        gate_str = str(set(gate_list[i]))
        gate = gate_str[1] + ',' + gate_str[-2]
        # print(gate)
        fidelity = fidelity*(1-error_rate.get(gate))
        # print(fidelity)
    # print(fidelity)
    return fidelity

def print_result(filename):
    # 读取线路
    input_filename = 'E:/python/quantumctek/test/benchmark-5qubits/' + filename + '_eli.qasm'
    gate_list = qasm_to_list.converter_circ_from_qasm(input_filename)
    print(gate_list)
    gate_list = qasm_to_list.list_str_to_int(gate_list)
    # 量子位数
    circuit_qubit = max([max(row) for row in gate_list]) + 1
    print(gate_list)

    qc = QuantumCircuit(circuit_qubit, circuit_qubit)
    for i in range(len(gate_list)):
        qc.cx(gate_list[i][0], gate_list[i][1])
    qc.measure_all()
    # print(qc)

    fidelity = estimated_fidelity(gate_list)
    print(filename)
    print('CNOT数:' + str(len(gate_list)))
    print('深度:' + str(qc.depth()-1))
    print('保真度：' + str(fidelity))
    print(' ')

if __name__ == '__main__':
    filename_list = ['4gt5_75','4gt13_90','4gt13_91','4gt13_92','4mod5-v1_22','4mod5-v1_23','4mod5-v1_24','alu-v0_27','alu-v3_35','alu-v4_36','alu-v4_37','decod24-v2_43','hwb4_49','mod5mils_65','mod10_171']
    for i in range(len(filename_list)):
        print_result(filename_list[i])


