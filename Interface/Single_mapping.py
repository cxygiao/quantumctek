from Utils.Single_mapping.single_mapping_fun import partition_fun
from Utils.Single_mapping.single_mapping_fun import single_fun
from Utils.Single_mapping.tools.list_to_result import quantum_cir
from Utils.Single_mapping.Q66 import q66
from Utils.Tools.qasm_to_dateframe import qc_to_qasm_list

'''测试用例'''
if __name__ == '__main__':
    hardware = q66()
    hardware_graph = q66()

    Root_path = r'C:\Users\13928\Desktop\quantumctek\Utils\Single_mapping\error_data\ClosedBetaQC_ 66bit.json'
    cir1 = "2z2fj_opt"
    cir2 = "empty"
    area, circ_list = partition_fun(Root_path, cir1, cir2, hardware_graph, hardware)

    if area:
        print('单线路初始映射为：', area[0][1])
        abpath = r'C:/Users/13928/Desktop/quantumctek/Utils/Single_mapping/color_qasm/'
        filname1 = circ_list[0].name + '.qasm'
        filname2 = circ_list[1].name + '.qasm'
        cout = single_fun(area, abpath, filname1, filname2, hardware_graph, 66)

        index = 0
        circuit = quantum_cir(cout[0], 66)
        print(circ_list[0].name+' circuit result:', circuit)
        qc_qasm = circuit.qasm()
        print(qc_qasm)


