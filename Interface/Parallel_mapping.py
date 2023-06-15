'''
功能：线路并行映射接口
作者：钱炀
版本: 1.0
完成时间：2023.5.10
'''

from Utils.Parallel_mapping.paralle_mapping_fun import partition_fun
from Utils.Parallel_mapping.paralle_mapping_fun import paralle_fun
from Utils.Parallel_mapping.tools.list_to_result import quantum_cir
from Utils.Parallel_mapping.Q66 import q66
from Utils.Tools.qasm_to_dateframe import qc_to_qasm_list


'''测试用例'''
if __name__ == '__main__':
    hardware = q66()
    hardware_graph = q66()

    '''
    Root_path ：错误率数据json格式文件路径
    cir1/cir2 : 优化好的线路文件名
    abpath : 优化好的线路文件路径
    
    example:
        Root_path = '/Users/quantumctek/Utils/Parallel_mapping/error_data/ClosedBetaQC_ 66bit.json'
        abpath = r'/Users/quantumctek/Utils/Parallel_mapping/color_qasm/'
        cir1 = "2z2fj_opt"
        cir2 = "2z3fj_opt"
    '''

    Root_path = 'E:/python/quantumctek/Utils/Parallel_mapping/error_data/ClosedBetaQC_ 66bit.json'
    cir1 = "2z2fj_opt"
    cir2 = "2z3fj_opt"
    area, circ_list = partition_fun(Root_path, cir1, cir2, hardware_graph, hardware)

    if area:
        print('并行初始映射为：',area)
        abpath = r'E:/python/quantumctek/Utils/Parallel_mapping/color_qasm/'
        filname1 = circ_list[0].name+'.qasm'
        filname2 = circ_list[1].name+'.qasm'
        cout = paralle_fun(area,abpath,filname1,filname2,hardware_graph,66)
        index = 0
        for i in cout:
            circuit = quantum_cir(i,66)
            # print(circ_list[index].name+' circuit result:', circuit)
            qc_qasm = circuit.qasm()
            print(qc_qasm)
            index = index+1
