from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit.library import MCXGate
import time, os
from PIL import Image
from qiskit.providers.aer import QasmSimulator
from qiskit.providers.aer import AerSimulator
from qiskit import Aer, transpile
from qiskit.transpiler.passes import Unroller
from qiskit.transpiler import PassManager
from itertools import permutations
from itertools import combinations

def ciucuit_generate(vertex_num,selected_vertex,img_path,edges_list):
    # 边数
    edges_num = int(vertex_num * (vertex_num - 1) / 2)  # 4:6
    # 边寄存器
    edges = QuantumRegister(edges_num, 'e')
    # 顶点寄存器 三个颜色
    vertexes_1 = QuantumRegister(vertex_num, 'c1')
    vertexes_2 = QuantumRegister(vertex_num, 'c2')
    vertexes_3 = QuantumRegister(vertex_num, 'c3')
    # 第一部分辅助位
    # 顶点辅助位寄存器1 vertex_num=4
    vertex_auxiliary1 = QuantumRegister(vertex_num, 'va1')  #1
    # 顶点辅助位寄存器2 三个颜色
    vertex_auxiliary2 = QuantumRegister(vertex_num*3, 'va2') #1
    # 顶点辅助位寄存器3
    vertex_auxiliary3 = QuantumRegister(vertex_num, 'va3') #0
    # 顶点辅助位寄存器4
    vertex_auxiliary4 = QuantumRegister(vertex_num, 'va4') #0
    # 顶点辅助结果输出
    vertex_auxiliary_out = QuantumRegister(1, 'vout') #0
    # 第二部分辅助位
    # 边辅助位寄存器1
    edges_auxiliary1 = QuantumRegister(edges_num*3, 'ea1') #1
    # 边辅助位寄存器2
    edges_auxiliary2 = QuantumRegister(edges_num, 'ea2') #0
    # 边辅助输出位
    edges_auxiliary_out = QuantumRegister(1, 'eout') #0

    # 输出寄存器
    out = QuantumRegister(1, 'out')
    # 经典位
    c = ClassicalRegister(1, 'c')
    # 生成线路
    circuit = QuantumCircuit(edges, vertexes_1, vertexes_2, vertexes_3, vertex_auxiliary1,vertex_auxiliary2,vertex_auxiliary3,vertex_auxiliary4,vertex_auxiliary_out, edges_auxiliary1,edges_auxiliary2,edges_auxiliary_out,out, c)


    # 初始位添加not门
    # 边
    for i in selected_vertex:
        circuit.x(edges[i-1])
    circuit.x(vertex_auxiliary1)
    circuit.x(vertex_auxiliary2)
    circuit.x(edges_auxiliary1)
    # 前半部分
    for i in range(vertex_num):
        circuit.h(vertexes_1[i])
        circuit.h(vertexes_2[i])
        circuit.h(vertexes_3[i])
        circuit.mct([vertexes_1[i], vertexes_2[i], vertexes_3[i]], vertex_auxiliary1[i])
        circuit.x(vertexes_1[i])
        circuit.x(vertexes_2[i])
        circuit.x(vertexes_3[i])
        circuit.ccx(vertexes_1[i], vertexes_2[i], vertex_auxiliary2[i])
        circuit.ccx(vertexes_1[i], vertexes_3[i], vertex_auxiliary2[i + 1])
        circuit.ccx(vertexes_2[i], vertexes_3[i], vertex_auxiliary2[i + 2])
        circuit.mct([vertex_auxiliary2[i], vertex_auxiliary2[i + 1], vertex_auxiliary2[i + 2]], vertex_auxiliary3[i])
        circuit.ccx(vertex_auxiliary1[i], vertex_auxiliary3[i], vertex_auxiliary4[i])
    circuit.mct(vertex_auxiliary4,vertex_auxiliary_out)

    # 后半部分
    for j in range(edges_num):  #6
        circuit.mct([edges[j], vertexes_1[edges_list[j][0]-1], vertexes_1[edges_list[j][1]-1]], edges_auxiliary1[3*j])
        circuit.mct([edges[j], vertexes_2[edges_list[j][0]-1], vertexes_2[edges_list[j][1]-1]], edges_auxiliary1[3*j+1])
        circuit.mct([edges[j], vertexes_3[edges_list[j][0]-1], vertexes_3[edges_list[j][1]-1]], edges_auxiliary1[3*j+2])
        circuit.mct([edges_auxiliary1[3*j],edges_auxiliary1[3*j+1],edges_auxiliary1[3*j+2]],edges_auxiliary2[j])
    circuit.mct(edges_auxiliary2,edges_auxiliary_out)

    # toffoli输出最终结果
    circuit.ccx(vertex_auxiliary_out,edges_auxiliary_out,out)
    print(circuit)
    # 绘制线路
    circuit.draw('mpl', scale=1, filename=img_path, initial_state=True, plot_barriers=False, justify='left', fold=-1)
    return circuit

def ciucuit_generate2(vertex_num):
    # 边数
    edges_num = int(vertex_num * (vertex_num - 1) / 2)  # 4:6

    edges_list = []
    for i in range(vertex_num):
        for j in range(i + 1, vertex_num):
            edges_list.append([i + 1, j + 1])

    # 输入边
    selected_vertex = list(input("请输入边的编号(输入举例：123):"))
    # selected_vertex = '13'
    # str转int
    selected_vertex = list(map(int, selected_vertex))
    # 去重
    selected_vertex = list(set(selected_vertex))

    # 边寄存器
    edges = QuantumRegister(edges_num, 'e')
    # 顶点寄存器 三个颜色
    vertexes_1 = QuantumRegister(vertex_num, 'c1')
    vertexes_2 = QuantumRegister(vertex_num, 'c2')
    vertexes_3 = QuantumRegister(vertex_num, 'c3')
    # 第一部分辅助位
    # 顶点辅助位寄存器1 vertex_num=4
    vertex_auxiliary1 = QuantumRegister(vertex_num, 'va1')  #1
    # 顶点辅助位寄存器2 三个颜色
    vertex_auxiliary2 = QuantumRegister(vertex_num*3, 'va2') #1
    # 顶点辅助位寄存器3
    vertex_auxiliary3 = QuantumRegister(vertex_num, 'va3') #0
    # 顶点辅助位寄存器4
    vertex_auxiliary4 = QuantumRegister(vertex_num, 'va4') #0
    # 顶点辅助结果输出
    vertex_auxiliary_out = QuantumRegister(1, 'vout') #0
    # 第二部分辅助位
    # 边辅助位寄存器1
    edges_auxiliary1 = QuantumRegister(edges_num*3, 'ea1') #1
    # 边辅助位寄存器2
    edges_auxiliary2 = QuantumRegister(edges_num, 'ea2') #0
    # 边辅助输出位
    edges_auxiliary_out = QuantumRegister(1, 'eout') #0

    # 输出寄存器
    out = QuantumRegister(1, 'out')
    # 经典位
    c = ClassicalRegister(1, 'c')
    # 生成线路
    circuit = QuantumCircuit(edges, vertexes_1, vertexes_2, vertexes_3, vertex_auxiliary1,vertex_auxiliary2,vertex_auxiliary3,vertex_auxiliary4,vertex_auxiliary_out, edges_auxiliary1,edges_auxiliary2,edges_auxiliary_out,out, c)


    # 初始位添加not门
    # 边
    for i in selected_vertex:
        circuit.x(edges[i-1])
    circuit.x(vertex_auxiliary1)
    circuit.x(vertex_auxiliary2)
    circuit.x(edges_auxiliary1)
    # 前半部分
    for i in range(vertex_num):
        circuit.h(vertexes_1[i])
        circuit.h(vertexes_2[i])
        circuit.h(vertexes_3[i])
        circuit.mct([vertexes_1[i], vertexes_2[i], vertexes_3[i]], vertex_auxiliary1[i])
        circuit.x(vertexes_1[i])
        circuit.x(vertexes_2[i])
        circuit.x(vertexes_3[i])
        circuit.ccx(vertexes_1[i], vertexes_2[i], vertex_auxiliary2[i])
        circuit.ccx(vertexes_1[i], vertexes_3[i], vertex_auxiliary2[i + 1])
        circuit.ccx(vertexes_2[i], vertexes_3[i], vertex_auxiliary2[i + 2])
        circuit.mct([vertex_auxiliary2[i], vertex_auxiliary2[i + 1], vertex_auxiliary2[i + 2]], vertex_auxiliary3[i])
        circuit.ccx(vertex_auxiliary1[i], vertex_auxiliary3[i], vertex_auxiliary4[i])
    circuit.mct(vertex_auxiliary4,vertex_auxiliary_out)

    # 后半部分
    for j in range(edges_num):  #6
        circuit.mct([edges[j], vertexes_1[edges_list[j][0]-1], vertexes_1[edges_list[j][1]-1]], edges_auxiliary1[3*j])
        circuit.mct([edges[j], vertexes_2[edges_list[j][0]-1], vertexes_2[edges_list[j][1]-1]], edges_auxiliary1[3*j+1])
        circuit.mct([edges[j], vertexes_3[edges_list[j][0]-1], vertexes_3[edges_list[j][1]-1]], edges_auxiliary1[3*j+2])
        circuit.mct([edges_auxiliary1[3*j],edges_auxiliary1[3*j+1],edges_auxiliary1[3*j+2]],edges_auxiliary2[j])
    circuit.mct(edges_auxiliary2,edges_auxiliary_out)

    # toffoli输出最终结果
    circuit.ccx(vertex_auxiliary_out,edges_auxiliary_out,out)

    return circuit

# 排列组合
def permute(nums):
    num_list = []
    for i in range(1,nums+1):
        num_list.append(i)
    result = []
    comb = combinations(num_list, 2)
    for i in list(comb):
        result.append(''.join(map(str, i)))
    return result

if __name__ == '__main__':
    # 顶点数
    vertex_num = int(input('输入顶点数：'))
    # vertex_num = 10
    # 边的数量
    edges_num = int(vertex_num * (vertex_num - 1) / 2)
    print("边数为：" + str(edges_num))
    # print('边：' + str(permute(vertex_num)))
    edges_list = []
    for i in range(vertex_num):
        for j in range(i + 1, vertex_num):
            edges_list.append([i + 1, j + 1])
    print("边：",end='')
    print(edges_list)
    # 输入边
    selected_vertex = list(input("请输入边的编号(输入举例：123):"))
    # selected_vertex = '13'
    # str转int
    selected_vertex = list(map(int, selected_vertex))
    # 去重
    selected_vertex = list(set(selected_vertex))

    # 解决 pillow 加载超大图片报错问题
    Image.MAX_IMAGE_PIXELS = None
    Image.LOAD_TRUNCATED_IMAGES = True

    img_name = time.strftime("%Y-%m-%d %H.%M.%S", time.localtime()) + '.png'
    img_path = os.path.join(os.getcwd(), 'PNG', img_name)
    if not os.path.exists(os.path.join(os.getcwd(), 'PNG')):
        os.mkdir(os.path.join(os.getcwd(), 'PNG'))

    ciucuit_generate(vertex_num, selected_vertex, img_path,edges_list)

    img = Image.open(img_path)
    img.show()