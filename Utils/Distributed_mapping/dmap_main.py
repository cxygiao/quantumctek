import re

from Utils.Distributed_mapping import dmap6
from qiskit import QuantumCircuit
import random
import copy
from collections import deque
from Utils.Distributed_mapping import list_to_dataFrame as result


def get_counts_transportation(circ, tra_a, tra_b):
    counts = 0
    for i in circ:
        if i == 'swap[' + str(tra_a) + ',' + str(tra_b) + ']' or i == 'swap[' + str(tra_b) + ',' + str(tra_a) + ']':
            counts = counts + 1
    return counts


def get_counts_swaps(circ, tra_a, tra_b):
    counts = 0
    for i in circ:
        if i[0] == 's':
            counts = counts + 1
    a = get_counts_transportation(circ, tra_a, tra_b)
    return counts - a


def find_nearest_connected_points(graph, start, n):
    visited = {start}
    queue = deque([(start, 0)])
    result = []

    while queue and len(result) < n:
        curr, dist = queue.popleft()

        for neighbor in graph[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

                if len(result) < n and all(n in visited for n in result):
                    result.append(neighbor)

    return result


def quantum_cir(cir: list, n):
    circ = QuantumCircuit(n)
    for i in cir:
        if isinstance(i[0], str):
            if i[0] == 'h':
                circ.h(i[1])
            elif i[0] == 'tdg':
                circ.tdg(i[1])
            elif i[0] == 's':
                circ.s(i[1])
            elif i[0] == 't':
                circ.t(i[1])
            elif i[0] == 'x':
                circ.x(i[1])
        else:
            circ.h(i[1])
            circ.cz(i[1], i[0])
            circ.h(i[1])
    return circ


def change_circ(circ, num_qubits):
    # 通信逻辑量子比特为tra_a,tra_b
    if num_qubits % 2 == 0:
        middle = int(num_qubits / 2) - 1

    else:
        middle = int((num_qubits - 1) / 2) - 1
    tra_a = middle + 1
    tra_b = tra_a + 1
    for i in circ:
        if type(i[0]) == str:
            if i[1] > middle:
                i[1] = i[1] + 2
        else:
            if i[0] > middle:
                i[0] = i[0] + 2
            if i[1] > middle:
                i[1] = i[1] + 2
    return circ


def run_circ(time,circ, num_qubits,
             communication_Qubit, coupling_list,
             coupling_graph_A, coupling_graph_B,
             initial_mapping):
    if num_qubits % 2 == 0:
        middle = int(num_qubits / 2) - 1

    else:
        middle = int((num_qubits - 1) / 2) - 1
    tra_a = middle + 1
    tra_b = tra_a + 1
    global_num = 0
    for index in circ:
        # 存在全局门返回0，否则返回1
        # 若检测到swap中字符s则跳出该次循环
        if type(index[0]) == str:
            continue
        elif min(index[0], index[1]) <= middle + 1 and max(index[0], index[1]) >= middle + 2:
            global_num = global_num + 1
        else:
            continue
    print(f"全局门门数量为：{global_num}")

    ll = {}
    for x in range(time):
        transfer_direction = []
        for j in range(global_num):
            transfer_direction.append(random.randint(0, 1))
        tran = copy.deepcopy(transfer_direction)
        direction = 999
        i = 0
        circuit = copy.deepcopy(circ)
        print(f"第{x+1}次迭代")
        while True:
            if dmap6.is_gate_neighbour(circuit[i], initial_mapping, coupling_list):
                i = i + 1
            # 若该门不近邻，判断是全局门还是局部门
            else:
                # 若该门为全局门
                if dmap6.is_gate_global(circuit[i], middle):
                    # 若传态已经发生过，并且后一个门是全局门，则传回之前的信息
                    if direction == 0:
                        dmap6.swapgate(circuit, tra_b, tra_a, i)
                        i = i + 1
                        direction = 999
                        continue
                    elif direction == 1:
                        dmap6.swapgate(circuit, tra_a, tra_b, i)
                        i = i + 1
                        direction = 999
                        continue
                    # 如果传态列表为空，则跳出函数
                    if len(transfer_direction) == 0:
                        break
                    else:
                        # 先进行传态操作，并且记录传态所需的交换门，把指针更新，继续指向该门
                        swap_num, circuit, direction = dmap6.quantum_teleportation(circuit, middle,
                                                                                   communication_Qubit,
                                                                                   coupling_graph_A, coupling_graph_B,
                                                                                   initial_mapping, tran)
                        i = i + swap_num
                    # 若传态后已经为近邻门，则指针指向后面的门
                    if dmap6.is_gate_neighbour(circuit[i], initial_mapping, coupling_list):
                        i = i + 1
                    # 若传态后不为近邻门，则先路由
                    else:
                        swap_num, circuit = dmap6.gate_routine(circuit[i], middle, circuit, initial_mapping,
                                                               coupling_graph_A,
                                                               coupling_graph_B, i)
                        i = i + swap_num
                # 若该门为局部门
                else:
                    swap_num, circuit = dmap6.gate_routine(circuit[i], middle, circuit, initial_mapping,
                                                           coupling_graph_A,
                                                           coupling_graph_B,
                                                           i)
                    i = i + swap_num
            if dmap6.is_all_gate_neighbour(circuit, initial_mapping, coupling_list):
                break
        if len(transfer_direction) > 0:
            swap_num = get_counts_swaps(circuit, tra_a, tra_b)
            ST_num = get_counts_transportation(circuit, tra_a, tra_b)
            score = ST_num + 0.3 * swap_num
            ll[score] = circuit

    min_key = min(ll.keys())
    min_value = ll[min_key]
    print(f"ST门数量为：{get_counts_transportation(min_value,tra_a,tra_b)}")
    print(f"SWAP数量为：{get_counts_swaps(min_value,tra_a,tra_b)}")


    new_circ = []
    for i in min_value:
        if i[:4] == 'swap':
            if i == 'swap[' + str(tra_a) + ',' + str(tra_b) + ']' or i == 'swap[' + str(tra_b) + ',' + str(tra_a) + ']':
                new_circ.append(i)
                continue
            else:
                a = i[5:-1]
                r = r'[,]'
                swap_gate = re.split(r, a)
                aa = int(swap_gate[0])
                bb = int(swap_gate[1])
                new_circ.append(['h', aa])
                new_circ.append([aa, bb])
                new_circ.append(['h', aa])
                new_circ.append(['h', bb])
                new_circ.append([bb, aa])
                new_circ.append(['h', bb])
                new_circ.append(['h', aa])
                new_circ.append([aa, bb])
                new_circ.append(['h', aa])
        else:
            new_circ.append(i)
            continue


    aa = []
    m = 0
    while m < len(new_circ) - 1:
        n = m + 1
        while n < len(new_circ):
            if new_circ[m][0] == 'h' and new_circ[n][0] == 'h' and new_circ[m][1] == new_circ[n][1] and new_circ[m][1] not in aa:
                new_circ.pop(m)
                new_circ.pop(n - 1)  # 删除两个相同的子列表
                m -= 1  # 回退索引以继续检查上一个位置
                break
            if type(new_circ[n][0]) == str:
                aa.append(new_circ[n][1])
                n += 1
            else:
                aa.append(new_circ[n][0])
                aa.append(new_circ[n][1])
                n += 1
        m += 1
        aa.clear()

    a = result.list_to_dataframe(new_circ, tra_a, tra_b, initial_mapping)
    for index, row in a.iterrows():
        print(f"Row {index}: k={row['k']}, c={row['c']}, t={row['t']}")
    return a
