import pandas as pd
from Utils.Parallel_mapping.tools.read_color_qasm import converter_num_from_qasm
from Utils.Parallel_mapping.tools.read_color_qasm import converter_dataframe_from_qasm

def dataframe_to_list(dataFrame):
    df = dataFrame
    df_list = df.values.tolist()
    Gate_list = []
    Gate_list_new = []
    for i in df_list:
        # print(i)
        if i[0] == 'h ':
            Gate_list.append([i[0],i[2]])
        elif i[0] == 'CX':
            Gate_list.append([i[1], i[2]])
        elif i[0] == 'tdg ':
            Gate_list.append([i[0],i[2]])
        elif i[0] == 't ':
            Gate_list.append([i[0],i[2]])
        elif i[0] == 'x ':
            Gate_list.append([i[0],i[2]])
    for i in Gate_list:
        if isinstance(i[0],str):
            gatename = i[0].rstrip()
            gate=[gatename,i[1]]
            Gate_list_new.append(gate)
        else:
            Gate_list_new.append(i)
    return Gate_list_new

# input_filename = r'/Users/qyyy/研究生/科研/多程序并行/Multiprogramming-main/paralle_mapping/color_qasm/3z3fj_opt.qasm'
# qubit_num, gate_num, q_name_list, q_num_list = converter_num_from_qasm(input_filename)
# df_ori_qc = converter_dataframe_from_qasm(input_filename, qubit_num, gate_num, q_name_list, q_num_list)
#
# if __name__ == '__main__':
#     cir_list =dataframe_to_list(df_ori_qc)
#     print(cir_list)
#     print(len(cir_list))