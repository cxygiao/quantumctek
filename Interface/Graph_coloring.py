'''
功能：图着色问题接口
作者：陈新宇
版本: 1.0
完成时间：2023.4.20
'''

import Utils.Graph_coloring.two_colors as two_col
import Utils.Graph_coloring.three_colors as three_col
'''
二着色
输入：n:int 图的顶点数
输出：qc：circuit 生成的线路
'''
def two_color(n):
    qc = two_col.gen2(n)
    return qc


'''
三着色
输入：n:int 图的顶点数
输出：qc：circuit 生成的线路
'''
def three_color(n):
    qc = three_col.ciucuit_generate2(n)
    return qc


'''测试用例'''
if __name__ == '__main__':
    # 以三个顶点的三着色为例
    # 3表示三个顶点
    circuit = three_color(3)
    print(circuit)

    # print(circuit.qasm())