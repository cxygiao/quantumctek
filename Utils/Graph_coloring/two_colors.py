from qiskit import QuantumRegister, ClassicalRegister, AncillaRegister, QuantumCircuit
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

def gen2(n, img_path, bdh, vi):

    # 顶点的数量
    v_num = n
    # 边的数量
    e_num = int(n * (n - 1) / 2)

    # 边寄存器
    edges = QuantumRegister(e_num, 'e')
    # 顶点寄存器
    vertexes = QuantumRegister(v_num, 'v')
    # 辅助位1寄存器
    aids1 = AncillaRegister(e_num, 'a1')
    # 辅助位2寄存器
    aids2 = AncillaRegister(e_num, 'a2')
    # 输出寄存器
    out = QuantumRegister(1, 'o')
    # 经典位
    c = ClassicalRegister(1, 'c')
    print('量子位数：'+str(e_num*3+v_num+2))
    # 生成线路
    circuit = QuantumCircuit(edges, vertexes, aids1, aids2, out, c)

    # 添加门
    # 初始位
    for i in range(len(vi)):
        circuit.x(edges[i])
    circuit.x(aids2)
    if bdh:
        circuit.h(vertexes)
    circuit.barrier()  # 画分界线
    # 计算顶点和边是否满足着色条件
    k = 0
    for i in range(v_num):
        for j in range(i + 1, v_num):
            # 判断i,j两顶点是否相同
            circuit.ccx(vertexes[i], vertexes[j], aids1[k])
            circuit.x(vertexes[i])
            circuit.x(vertexes[j])
            circuit.ccx(vertexes[i], vertexes[j], aids1[k])
            circuit.x(vertexes[i])
            circuit.x(vertexes[j])
            # 判断边是否存在
            circuit.ccx(edges[k], aids1[k], aids2[k])

            circuit.barrier()
            k += 1

    if bdh:
        circuit.h(vertexes)

    # 合并结果
    gate = MCXGate(e_num)
    ct = list(range(e_num * 2 + v_num, e_num * 3 + v_num + 1))
    circuit.append(gate, ct)

    # 测量量子比特
    circuit.measure(out, c)

    # # 输出结果
    # # simulator = Aer.get_backend('qasm_simulator')
    # simulator = QasmSimulator()
    # # Execute the circuit on the qasm simulator
    # job = simulator.run(circuit, shots=1000)
    # # Grab results from the job
    # result = job.result()
    # counts = result.get_counts(circuit)
    print(circuit)
    # print(counts)

    simulator = AerSimulator(method='matrix_product_state')
    tcirc = transpile(circuit, simulator)
    result = simulator.run(tcirc).result()
    print("Time taken: {} sec".format(result.time_taken))
    print(result.get_counts())

    # 化简线路

    # 绘制线路
    circuit.draw('mpl', scale=1, filename=img_path, initial_state=True, plot_barriers=False, justify='left', fold=-1)

    return img_path

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
    # 输入参数-顶点数
    n = int(input("请输入顶点数："))
    # 边的数量
    e_num = int(n * (n - 1) / 2)
    print("边数为："+str(e_num))
    print('边：'+ str(permute(n)))
    # 输入边
    v = list(input("请输入边的编号(输入举例：123):"))
    # str转int
    v = list(map(int,v))
    # 去重
    v = list(set(v))
    # 是否在前后添加H门
    bdh = False
    if str(input("是否在顶点线路前后添加H门(输入Y表示添加，默认不添加)：")).upper() == 'Y':
        bdh = True

    # 解决 pillow 加载超大图片报错问题
    Image.MAX_IMAGE_PIXELS = None
    Image.LOAD_TRUNCATED_IMAGES = True

    img_name = time.strftime("%Y-%m-%d %H.%M.%S", time.localtime()) + '.png'
    img_path = os.path.join(os.getcwd(), 'PNG', img_name)
    if not os.path.exists(os.path.join(os.getcwd(), 'PNG')):
        os.mkdir(os.path.join(os.getcwd(), 'PNG'))

    gen2(n, img_path, bdh, v)

    print('生成线路图在：%s' % img_path)

    img = Image.open(img_path)
    img.show()