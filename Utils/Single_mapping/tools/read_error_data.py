
import pandas as pd

'''读取错误率数据Excel文件并转换为错误率list列表
list[m][n]=a
m 双门控制位
n 双门目标位
a 双门执行错误率
'''
def converter_list_from_excel(input_file_name, NumA, NumB):
    '''
    input_file_name文件位置
    NumA 行数
    NumB 列数
    '''
    f = open(input_file_name,'rb')
    df = pd.read_excel(f, sheet_name='Sheet1')
    column = df.columns.values
    data = df.values[0]
    newlist = [[0]*NumA for _ in range(NumB)]
    l = len(column)
    for i in range(1,l):
        value = data[i]
        table = column[i]
        index = table.split(',')
        a = index[0][1:]
        b = index[1][1:]
        newlist[int(a)][int(b)] = value
        newlist[int(b)][int(a)] = value
    return newlist