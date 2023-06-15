import heapq
from collections import defaultdict

# 获取线路中首个全局门，返回该全局门在列表里的索引
def get_exist_global_gate(circ, middle):
    i = 0  # 记录全局门所在索引位置
    for index in circ:
        # 存在全局门返回0，否则返回1
        # 若检测到swap中字符s则跳出该次循环
        if type(index[0]) == str:
            i = i + 1
            continue
        elif min(index[0], index[1]) <= middle + 1 and max(index[0], index[1]) >= middle + 2:
            return i
        else:
            i = i + 1
    return None  # 没有全局门了


# 获取当前全局门在物理拓扑图的映射,返回物理量子位
def get_globalgate_mapping(circ, initial_mapping_list, middle):
    index = get_exist_global_gate(circ, middle)
    qubit_A, qubit_B = circ[index][0], circ[index][1]
    Qubit_A, Qubit_B = initial_mapping_list[qubit_A], initial_mapping_list[qubit_B]
    return Qubit_A, Qubit_B


# 获取当前全局门需要传输的分区量子比特在物理拓扑图中的位置
def get_globalgate_with_transfer(circ, middle, initial_mapping_list, direction_list):
    Qubitt = get_globalgate_mapping(circ, initial_mapping_list, middle)
    # 获取传输方向列表上的首位元素，如果是0，则取全局门的低位量子比特，反之，取高位量子比特
    if len(direction_list) == 0:
        return "无全局门"  # 已经没有全局门
    else:
        if direction_list[0] == 0:
            Qubit_need_transfer = min(Qubitt)
        else:
            Qubit_need_transfer = max(Qubitt)
        return Qubit_need_transfer

# 判断通信物理量子比特与所需传输的物理量子比特是否重合
def is_coincide_communication(circ, middle, initial_mapping_list, direction_list, communication_Qubit_list):
    Qubit_need_transfer = get_globalgate_with_transfer(circ, middle, initial_mapping_list, direction_list)
    if Qubit_need_transfer in set(communication_Qubit_list):
        return 1
    else:
        return 0


# 插入交换门，返回插入后的电路
def swapgate(circ, swap_a, swap_b, insert_location):
    circ.insert(insert_location, f'swap[{swap_a},{swap_b}]')
    for index in range(insert_location, len(circ)):
        if type(circ[index][0]) == str:
            if circ[index][1] == swap_a:
                circ[index][1] = swap_b
            elif circ[index][1] == swap_b:
                circ[index][1] = swap_a
        else:
            for i in range(2):
                if circ[index][i] == swap_a:
                    circ[index][i] = swap_b
                elif circ[index][i] == swap_b:
                    circ[index][i] = swap_a
    return circ

# 判断即将用到的通信量子比特上是否有门占用
# （这里的if判断条件后期需要手动改，改成通信量子比特所在的逻辑量子线路中的位置）！！！
def is_occupied_communication(circ, middle,direction_list):
    index = get_exist_global_gate(circ, middle)
    transfer = direction_list[0]
    # 若此次传态方向为自上而下
    if transfer == 0:
        # 从当前全局门的后一个门判断是否有门占用通信逻辑量子比特
        for i in range(index + 1, len(circ)):
            # 若该全局门的后一个全局门相同，继续遍历
            if circ[i] == circ[index]:
                continue
            elif circ[i][0] == middle+2 or circ[i][1] == middle+2 :
                return 1  # 占用通信量子比特则返回1
            else:
                continue
        return 0
    # 若此次传态方向为自下而上
    if transfer == 0:
        # 从当前全局门的后一个门判断是否有门占用通信逻辑量子比特
        for i in range(index + 1, len(circ)):
            # 若该全局门的后一个全局门相同，继续遍历
            if circ[i] == circ[index]:
                continue
            elif circ[i][0] == middle + 1 or circ[i][1] == middle + 1 :
                return 1  # 占用通信量子比特则返回1
            else:
                continue
        return 0


# 判断该逻辑量子比特上是否空闲
def is_qubit_free(circ, now_qubit, middle):
    index = get_exist_global_gate(circ, middle)
    for i in range(index, len(circ)):
        if now_qubit == circ[i][0] or now_qubit == circ[i][1]:
            return 0  # 若该逻辑量子比特上不空闲则返回0
        else:
            continue
    return 1  # 若该逻辑量子比特上空闲则返回1


# 定义一个广度优先搜索算法便于找出最近的空闲逻辑量子比特
# 参数为物理架构图，开始位置,返回值列表首元素为开始的元素（即通信量子比特），返回的列表是物理量子比特
def bfs(graph, start):
    visited = []
    queue = [start]
    visited.append(start)
    while queue:
        node = queue.pop(0)
        for adjacent_node in graph[node]:
            if adjacent_node not in visited:
                visited.append(adjacent_node)
                queue.append(adjacent_node)
    return visited


# 使用迪杰斯特拉算法，计算图中两点最短路径，返回列表
def dijkstra(start, end, graph, points_list):
    # 用一个字典来保存节点的最短距离
    dist = {point: float('inf') for point in points_list}
    dist[start] = 0

    # 使用一个堆来保存当前可达的最小距离
    heap = []
    heapq.heappush(heap, (0, start))

    # 用一个字典来保存每个节点的前一个节点，以便后面回溯路径
    prev = defaultdict(lambda: None)

    # 使用一个集合来保存已经找到最短路径的节点，避免重复计算
    visited = set()

    adjacency_list = defaultdict(list)
    for node, neighbors in graph.items():
        adjacency_list[node] = [neighbor for neighbor in neighbors if neighbor in points_list]

    while heap:
        # 取出堆顶元素
        current_distance, current_node = heapq.heappop(heap)

        # 如果当前节点已经找到最短路径，直接跳过
        if current_node in visited:
            continue

        # 标记当前节点已经找到最短路径
        visited.add(current_node)

        # 如果找到了终点，回溯路径并返回
        if current_node == end:
            path = [end]
            while prev[path[-1]] is not None:
                path.append(prev[path[-1]])
            return list(reversed(path))

        # 否则，更新相邻节点的最短距离
        for neighbor in adjacency_list[current_node]:
            if neighbor in visited:
                continue
            new_distance = current_distance + 1
            if new_distance < dist[neighbor]:
                dist[neighbor] = new_distance
                prev[neighbor] = current_node
                heapq.heappush(heap, (new_distance, neighbor))

    # 如果无法从起点到达终点，返回空列表
    return []


# 根据传输方向和映射位置进行传态操作
# （ST交换门在不同的通信量子比特上需要更改）！！！
def quantum_teleportation(circ, middle, communication_Qubit_list, coupling_graph_a,
                          coupling_graph_b,
                          initial_mapping_list, direction_list):
    index = get_exist_global_gate(circ, middle)
    is_occupied = is_occupied_communication(circ, middle, direction_list)
    is_connect = is_coincide_communication(circ, middle, initial_mapping_list, direction_list,
                                           communication_Qubit_list)
    # 该全局门后没有门占用通信逻辑量子比特，并且传输物理量子比特与通信物理量子比特为同一物理比特
    if is_occupied == 0 and is_connect == 1:
        # 方向列表首位元素表示当前全局门的传输方向，如果为0，则从上向下传，并且将方向传输列表的首元素删除
        if direction_list[0] == 0:
            swapgate(circ, middle+1, middle+2, index)
            direction = direction_list.pop(0)
            return 1, circ, direction  # 插入了1个swap
        else:
            swapgate(circ, middle+2, middle+1, index)
            direction = direction_list.pop(0)
            return 1, circ, direction  # 插入了1个swap


    # 该全局门没有门占用通信逻辑量子比特，并且传输物理量子比特与通行物理量子比特不相邻
    elif is_occupied == 0 and is_connect == 0:
        if direction_list[0] == 0:
            # 获取该全局门上半区的物理量子比特
            Qubitt = initial_mapping_list[min(circ[index])]
            # 从该物理量子比特到通信量子比特的最短路径（这里要手动改）！！！！
            shortest_route_up_list = dijkstra(Qubitt, 6,coupling_graph_a, initial_mapping_list)
            for i in range(len(shortest_route_up_list) - 1):
                swapgate(circ, initial_mapping_list.index(shortest_route_up_list[i]),
                         initial_mapping_list.index(shortest_route_up_list[i + 1]), index + i)
            swapgate(circ, middle+1, middle+2, index + len(shortest_route_up_list) - 1)
            direction = direction_list.pop(0)
            return len(shortest_route_up_list), circ, direction
        else:
            # 获取该全局门下半区的物理量子比特
            Qubitt = initial_mapping_list[max(circ[index])]
            # 从该物理量子比特到通信量子比特的最短路径（这里要手动改）！！！！
            shortest_route_down_list = dijkstra(Qubitt, 67,coupling_graph_b,initial_mapping_list)
            for i in range(len(shortest_route_down_list) - 1):
                swapgate(circ, initial_mapping_list.index(shortest_route_down_list[i]),
                         initial_mapping_list.index(shortest_route_down_list[i + 1]), index + i)
            swapgate(circ, middle+2, middle+1, index + len(shortest_route_down_list) - 1)
            direction = direction_list.pop(0)
            return len(shortest_route_down_list), circ, direction

    # 若该全局门后通信逻辑量子比特被占用。
    # 依次清除通信量子比特所占用的门
    # 若传输物理量子比特与通行物理量子比特在同一个比特上
    elif is_occupied == 1 and is_connect == 1:
        # a和b记录上半区和下半区插入的swap数量
        a = 0
        b = 0
        # 若上方通信逻辑量子比特被占用
        if is_qubit_free(circ, middle+1, middle) == 0:
            # 获取到距离上方通信逻辑量子比特最近的空闲逻辑量子比特
            logic_qubit_up = get_near_logic_qubit_up(circ, coupling_graph_a, initial_mapping_list, middle)
            # 根据初始映射列表转化为物理量子比特
            physical_qubit_up = initial_mapping_list[logic_qubit_up]
            # 调用迪杰斯特拉算法获取该空闲物理量子比特到通信物理量子比特最短路径
            shortest_route_up_list = dijkstra(physical_qubit_up, 6,coupling_graph_a, initial_mapping_list)
            for i in range(len(shortest_route_up_list) - 1):
                swapgate(circ, initial_mapping_list.index(shortest_route_up_list[i]),
                         initial_mapping_list.index(shortest_route_up_list[i + 1]), index + i)
            a = a + len(shortest_route_up_list) - 1
        # 若下方逻辑量子比特被占用
        if is_qubit_free(circ, middle+2, middle) == 0:
            # 获取到距离下方通信逻辑量子比特最近的空闲逻辑量子比特
            logic_qubit_down = get_near_logic_qubit_down(circ, coupling_graph_b, initial_mapping_list, middle)
            # 根据初始映射列表转化为物理量子比特
            physical_qubit_down = initial_mapping_list[logic_qubit_down]
            # 调用迪杰斯特拉算法获取该空闲物理量子比特到通信物理量子比特最短路径
            shortest_route_down_list = dijkstra(physical_qubit_down, 67,coupling_graph_b, initial_mapping_list)
            for i in range(len(shortest_route_down_list) - 1):
                swapgate(circ, initial_mapping_list.index(shortest_route_down_list[i]),
                         initial_mapping_list.index(shortest_route_down_list[i + 1]), index + i)
            b = b + len(shortest_route_down_list) - 1
        # 方向列表首位元素表示当前全局门的传输方向，如果为0，则从上向下传
        if direction_list[0] == 0:
            swapgate(circ, middle+1, middle+2, index)
            direction = direction_list.pop(0)
            return a + b + 1, circ, direction
        else:
            swapgate(circ, middle+2, middle+1, index)
            direction = direction_list.pop(0)
            return a + b + 1, circ, direction
    # 若传输物理量子比特与通行物理量子比特不在同一个比特上
    else:
        # a和b记录上半区和下半区插入的swap数量
        a = 0
        b = 0
        # 若上方通信逻辑量子比特被占用
        if is_qubit_free(circ, middle+1, middle) == 0:
            # 获取到距离上方通信逻辑量子比特最近的空闲逻辑量子比特
            logic_qubit_up = get_near_logic_qubit_up(circ, coupling_graph_a, initial_mapping_list, middle)
            # 根据初始映射列表转化为物理量子比特
            physical_qubit_up = initial_mapping_list[logic_qubit_up]
            # 调用迪杰斯特拉算法获取该空闲物理量子比特到通信物理量子比特最短路径
            shortest_route_up_list = dijkstra(physical_qubit_up, 6,coupling_graph_a, initial_mapping_list)
            for i in range(len(shortest_route_up_list) - 1):
                swapgate(circ, initial_mapping_list.index(shortest_route_up_list[i]),
                         initial_mapping_list.index(shortest_route_up_list[i + 1]), index + i)
            a = a + len(shortest_route_up_list) - 1
        # 若下方逻辑量子比特被占用
        if is_qubit_free(circ, middle+2, middle) == 0:
            # 获取到距离下方通信逻辑量子比特最近的空闲逻辑量子比特
            logic_qubit_down = get_near_logic_qubit_down(circ, coupling_graph_b, initial_mapping_list, middle)
            # 根据初始映射列表转化为物理量子比特
            physical_qubit_down = initial_mapping_list[logic_qubit_down]
            # 调用迪杰斯特拉算法获取该空闲物理量子比特到通信物理量子比特最短路径
            shortest_route_down_list = dijkstra(physical_qubit_down, 67,coupling_graph_b, initial_mapping_list)
            for i in range(len(shortest_route_down_list) - 1):
                swapgate(circ, initial_mapping_list.index(shortest_route_down_list[i]),
                         initial_mapping_list.index(shortest_route_down_list[i + 1]), index + i)
            b = b + len(shortest_route_down_list) - 1
        # 上半区传态至下半区
        if direction_list[0] == 0:
            # 获取该全局门上半区的物理量子比特
            Qubitt = initial_mapping_list[min(circ[index + a + b])]
            # 从该物理量子比特到通信量子比特的最短路径（这里要手动改）！！！！
            shortest_route_up_list = dijkstra(Qubitt, 6,coupling_graph_a, initial_mapping_list)
            for i in range(len(shortest_route_up_list) - 1):
                swapgate(circ, initial_mapping_list.index(shortest_route_up_list[i]),
                         initial_mapping_list.index(shortest_route_up_list[i + 1]), index + i)
            swapgate(circ, middle+1, middle+2, index + len(shortest_route_up_list) - 1)
            direction = direction_list.pop(0)
            return len(shortest_route_up_list) + a + b, circ, direction
        # 下半区传态至上半区
        else:
            # 获取该全局门下半区的物理量子比特
            Qubitt = initial_mapping_list[max(circ[index + a + b])]
            # 从该物理量子比特到通信量子比特的最短路径（这里要手动改）！！！！
            shortest_route_down_list = dijkstra(Qubitt, 67,coupling_graph_b, initial_mapping_list)
            for i in range(len(shortest_route_down_list) - 1):
                swapgate(circ, initial_mapping_list.index(shortest_route_down_list[i]),
                         initial_mapping_list.index(shortest_route_down_list[i + 1]), index + i)
            swapgate(circ, middle+2, middle+1, index + len(shortest_route_down_list) - 1)
            direction = direction_list.pop(0)
            return len(shortest_route_down_list) + a + b, circ, direction


# 若上方通信逻辑量子比特被占用，找出距离最近的逻辑量子比特
def get_near_logic_qubit_up(circ, coupling_graph_a, initial_mapping_list, middle):
    # 通过广度优先算法得到距离上边的通信逻辑量子比特最近的物理量子比特列表
    near_free_qubit_list = bfs(coupling_graph_a, 6)
    # 遍历映射表，得到距离该通信量子比特最近的物理量子比特所对应的逻辑量子比特
    for index in range(1, len(near_free_qubit_list)):
        Qubitt = near_free_qubit_list[index]
        if Qubitt not in initial_mapping_list:
            continue
        logic_qubit_up = initial_mapping_list.index(Qubitt)
        if is_qubit_free(circ, logic_qubit_up, middle):
            return logic_qubit_up


# 若下方通信逻辑量子比特被占用，找出距离最近的逻辑量子比特
def get_near_logic_qubit_down(circ, coupling_graph_b, initial_mapping_list, num_qubits):
    # 通过广度优先算法得到距离下边通信逻辑量子比特最近的物理量子比特列表
    near_free_qubit_list = bfs(coupling_graph_b, 67)
    # 遍历映射表，得到距离该通信量子比特最近的物理量子比特所对应的逻辑量子比特
    for index in range(1, len(near_free_qubit_list)):
        Qubitt = near_free_qubit_list[index]
        if Qubitt not in initial_mapping_list:
            continue
        logic_qubit_down = initial_mapping_list.index(Qubitt)
        if is_qubit_free(circ, logic_qubit_down, num_qubits):
            return logic_qubit_down


# 判断该门是否近邻
def is_gate_neighbour(gate, initial_mapping_list, coupling_list):
    if type(gate[0]) == str:
        return 1
    else:
        qubit_A, qubit_B = gate[0], gate[1]
        Qubit_A, Qubit_B = initial_mapping_list[qubit_A], initial_mapping_list[qubit_B]
        for index in coupling_list:
            # 是近邻门则返回1
            if {Qubit_A, Qubit_B} == set(index):
                return 1
        return 0


# 判断该门是否全局门
def is_gate_global(gate, middle):
    if type(gate[0]) == str:
        return 0
    else:
        qubit_A, qubit_B = gate[0], gate[1]
        if (qubit_A <= middle + 1 and qubit_B >= middle + 2 ) or (qubit_A >=middle + 2  and qubit_B<=middle + 1):
            return 1
        return 0


# 对局部门进行路由操作
def gate_routine(gate, middle,circ, initial_mapping_list, coupling_graph_a, coupling_graph_b, index):
    qubit_A, qubit_B = gate[0], gate[1]
    Qubit_A, Qubit_B = initial_mapping_list[qubit_A], initial_mapping_list[qubit_B]
    # 若该局部门在上半区
    if qubit_A <= middle+1:
        # 若qubit_A在通信逻辑量子比特上
        if qubit_A == middle+1:
            shortest_route_up_list = dijkstra(Qubit_B, Qubit_A,coupling_graph_a, initial_mapping_list)
            for i in range(len(shortest_route_up_list) - 2):
                swapgate(circ, initial_mapping_list.index(shortest_route_up_list[i]),
                         initial_mapping_list.index(shortest_route_up_list[i + 1]), index + i)
            return len(shortest_route_up_list) - 2, circ
        # 若qubit_B在通信逻辑量子比特上
        elif qubit_B == middle+1:
            shortest_route_up_list = dijkstra(Qubit_A, Qubit_B,coupling_graph_a, initial_mapping_list)
            for i in range(len(shortest_route_up_list) - 2):
                swapgate(circ, initial_mapping_list.index(shortest_route_up_list[i]),
                         initial_mapping_list.index(shortest_route_up_list[i + 1]), index + i)
            return len(shortest_route_up_list) - 2, circ
        else:
            shortest_route_up_list = dijkstra(Qubit_A, Qubit_B,coupling_graph_a, initial_mapping_list)
            for i in range(len(shortest_route_up_list) - 2):
                swapgate(circ, initial_mapping_list.index(shortest_route_up_list[i]),
                         initial_mapping_list.index(shortest_route_up_list[i + 1]), index + i)
            return len(shortest_route_up_list) - 2, circ
    # 若该局部门在下半区
    else:
        # 若qubit_A在通信逻辑量子比特上
        if qubit_A == middle+2:
            shortest_route_up_list = dijkstra(Qubit_B, Qubit_A,coupling_graph_b, initial_mapping_list)
            for i in range(len(shortest_route_up_list) - 2):
                swapgate(circ, initial_mapping_list.index(shortest_route_up_list[i]),
                         initial_mapping_list.index(shortest_route_up_list[i + 1]), index + i)
            return len(shortest_route_up_list) - 2, circ
        # 若qubit_B在通信逻辑量子比特上
        elif qubit_B == middle+2:
            shortest_route_up_list = dijkstra(Qubit_A, Qubit_B,coupling_graph_b, initial_mapping_list)
            for i in range(len(shortest_route_up_list) - 2):
                swapgate(circ, initial_mapping_list.index(shortest_route_up_list[i]),
                         initial_mapping_list.index(shortest_route_up_list[i + 1]), index + i)
            return len(shortest_route_up_list) - 2, circ
        else:
            shortest_route_up_list = dijkstra(Qubit_A, Qubit_B,coupling_graph_b, initial_mapping_list)
            for i in range(len(shortest_route_up_list) - 2):
                swapgate(circ, initial_mapping_list.index(shortest_route_up_list[i]),
                         initial_mapping_list.index(shortest_route_up_list[i + 1]), index + i)
            return len(shortest_route_up_list) - 2, circ


# 判断线路中是否所有门均近邻
def is_all_gate_neighbour(circ, initial_mapping_list, coupling_list):
    for index in circ:
        if type(index[0]) == str:
            continue
        elif is_gate_neighbour(index, initial_mapping_list, coupling_list):
            continue
        else:
            return False
    return True

