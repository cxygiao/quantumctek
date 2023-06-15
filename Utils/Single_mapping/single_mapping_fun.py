# from Utils.Parallel_mapping.Q66 import q66
import numpy as np
import networkx as nx
from Utils.Single_mapping.circuit_tran import Qubit_run
from Utils.Single_mapping.circuit_tran import shortway
from Utils.Single_mapping.circuit_tran import fun_qct
from Utils.Single_mapping.mapping.mapping_transition import circuits_partitions
from Utils.Single_mapping.tools.read_circuit import read_benchmark_circuit
from Utils.Single_mapping.tools.dataFrame_to_list import dataframe_to_list
from Utils.Single_mapping.tools.cz_error_list import read_error_cz
from Utils.Single_mapping.tools.readout_error_list import readout_error
from Utils.Single_mapping.partition_process.qubit_partition import partition_hardware_heuristic, partition_hardware
from Utils.Single_mapping.tools.read_color_qasm import converter_num_from_qasm
from Utils.Single_mapping.tools.read_color_qasm import converter_dataframe_from_qasm


def partition_fun(errorfilepath,circuit1name,circuit2name,hardware_graph,hardware):

    '''
    解析Jason文件，拿到门错误率和读出错误率
    '''
    cx_error_matrix = read_error_cz(errorfilepath)
    cx_error_matrix = np.array(cx_error_matrix)
    readout_error_matrix = readout_error(errorfilepath)

    # A list of circuit that are supposed to be executed simultaneously
    circuits = []
    circuit1 = read_benchmark_circuit(circuit1name)
    circuit1.name = circuit1name
    circuit2 = read_benchmark_circuit(circuit2name)
    circuit2.name = circuit2name
    circuits.append(circuit1)
    circuits.append(circuit2)
    # weight parameter lambda set by user to weight between the CNOT error rate and readout error rate
    # for fidelity degree of the qubit 权重参数，平衡连接错误率和读出错误率
    weight_lambda = 2

    Circ_List = sorted(circuits, key=lambda x: x.count_ops().get("cx", 0) / x.cregs[0].size, reverse=True)
    print('单线路名称：')

    print(Circ_List[0].name)

    partition = circuits_partitions(circuits,
                      hardware_graph,
                      hardware,
                      cx_error_matrix,
                      readout_error_matrix,
                      partition_hardware_heuristic,
                      weight_lambda,
                      )
    return partition,Circ_List

def single_fun(partition,path,circuit1_filename,circuit2_filename,hardware_graph,n):

    abpath = path
    filname1 = circuit1_filename
    input_filename1 = abpath + filname1
    qubit_num1, gate_num1, q_name_list1, q_num_list1 = converter_num_from_qasm(input_filename1)
    df_ori_qc1 = converter_dataframe_from_qasm(input_filename1, qubit_num1, gate_num1, q_name_list1, q_num_list1)
    Circ1 = dataframe_to_list(df_ori_qc1)

    filname2 = circuit2_filename
    input_filename2 = abpath + filname2
    qubit_num2, gate_num2, q_name_list2, q_num_list2 = converter_num_from_qasm(input_filename2)
    df_ori_qc2 = converter_dataframe_from_qasm(input_filename2, qubit_num2, gate_num2, q_name_list2, q_num_list2)
    Circ2 = dataframe_to_list(df_ori_qc2)


    Circ_List =[]
    Circ_List.append(Circ1)
    Circ_List.append(Circ2)


    G = nx.Graph.to_undirected(hardware_graph) #目标拓扑图
    EG = nx.edges(G)  #拓扑图边
    index = 0
    C_out = []

    for Circ in Circ_List:
        Len = len(Circ)
        for i in range(Len):
            Circ[i].insert(0, i)
        #找到所有双门
        C = list()
        for i in range(0, len(Circ)):
            if not isinstance(Circ[i][1], str):
                C.append(Circ[i])
        nl = len(Qubit_run.qubit_in_circuit(C))
        init_mapping = partition[index][1]
        index = index+1
        tau = [n] * (n+1)
        for key in init_mapping:  # map physical qubit BB[key] to logic qubit key
            tau[init_mapping[key]] = key

        count = 0
        sum_in = 0
        l = len(C)
        sum_in += l
        QFilter_type = '2x'
        wayindex = shortway.way(G)
        C_out.append(fun_qct.qct(Circ, G, EG, tau, QFilter_type, init_mapping, C))


       # result = submit(C_out)
       # print('线路',index,'转换后：', C_out)
    return C_out

