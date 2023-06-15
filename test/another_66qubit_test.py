from ezQpy import *
from qiskit import QuantumCircuit

def run():
    # login_key在 https://www.quantumcomputer.ac.cn/User  下的SDK密钥
    account = Account(login_key='b36e2a6064f128b0f18bb4e49720f9dc', machine_name='ClosedBetaQC')

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