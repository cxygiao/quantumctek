
"""
正向模板匹配，它采用初始匹配、量子比特配置以及电路和模板作为输入。 结果是模板和电路之间的匹配列表。

"""

from qiskit.circuit.controlledgate import ControlledGate


class ForwardMatch:
    """
    Object to apply template matching in the forward direction.
    """

    def __init__(
        self, circuit_dag_dep, template_dag_dep, node_id_c, node_id_t, qubits, clbits=None
    ):
        """
        创建一个带有必要参数的ForwardMatch类。Args：
        circuit _ dag _ dep ( DAGDependency )：dag依赖形式的电路.
        template _ dag _ dep ( DAGDependency )：dag依赖形式的模板.
        node _ id _ c ( int )：电路中匹配的第一个门的索引.
        node _ id _ t ( int )：模板中匹配的第一个门的索引.
        qubits (列表)：电路中考虑的qubits列表.
        clbits (列表)：电路中考虑的clbits列表.
        """

        # 电路的dag依赖项表示
        self.circuit_dag_dep = circuit_dag_dep.copy()

        # The dag dependency representation of the template
        self.template_dag_dep = template_dag_dep.copy()

        # 电路的节点作用在其上的量子比特的列表
        self.qubits = qubits

        # List of qubit on which the node of the circuit is acting on
        self.clbits = clbits if clbits is not None else []

        # Id of the node in the circuit
        self.node_id_c = node_id_c

        # Id of the node in the template
        self.node_id_t = node_id_t

        # List of match
        self.match = []

        # 前锋匹配的候选名单
        self.candidates = []

        # List of nodes in circuit which are matched
        self.matched_nodes_list = []

        # 对电路的qarg指标进行变换，使其与模板指标相适应
        self.qarg_indices = []

        # Transformation of the carg indices of the circuit to be adapted to the template indices
        self.carg_indices = []

    def _init_successors_to_visit(self):
        """
        初始化属性列表' SuccessorsToVisit '
        """
        for i in range(0, self.circuit_dag_dep.size()):
            if i == self.node_id_c:
                self.circuit_dag_dep.get_node(
                    i
                ).successorstovisit = self.circuit_dag_dep.direct_successors(i)

    def _init_matched_with_circuit(self):
        """
        在模板DAG依赖项中初始化属性' MatchedWith '。
        """
        for i in range(0, self.circuit_dag_dep.size()):
            if i == self.node_id_c:
                self.circuit_dag_dep.get_node(i).matchedwith = [self.node_id_t]
            else:
                self.circuit_dag_dep.get_node(i).matchedwith = []

    def _init_matched_with_template(self):
        """
        在电路DAG依赖项中初始化属性' MatchedWith '。
        """
        for i in range(0, self.template_dag_dep.size()):
            if i == self.node_id_t:
                self.template_dag_dep.get_node(i).matchedwith = [self.node_id_c]
            else:
                self.template_dag_dep.get_node(i).matchedwith = []

    def _init_is_blocked_circuit(self):
        """
        在电路DAG依赖项中初始化属性' IsBlock '
        """
        for i in range(0, self.circuit_dag_dep.size()):
            self.circuit_dag_dep.get_node(i).isblocked = False

    def _init_is_blocked_template(self):
        """
        Initialize the attribute 'IsBlocked' in the template DAG dependency.
        """
        for i in range(0, self.template_dag_dep.size()):
            self.template_dag_dep.get_node(i).isblocked = False

    def _init_list_match(self):
        """
        用找到的第一个匹配初始化电路和模板之间的匹配节点列表。
        """
        self.match.append([self.node_id_t, self.node_id_c])

    def _find_forward_candidates(self, node_id_t):
        """
        为给定的节点在模板中找到待匹配的候选节点。Args：node _ id _ t ( int )：考虑节点id。
        """
        matches = []

        for i in range(0, len(self.match)):
            matches.append(self.match[i][0])

        pred = matches.copy()
        if len(pred) > 1:
            pred.sort()
        pred.remove(node_id_t)

        if self.template_dag_dep.direct_successors(node_id_t):
            maximal_index = self.template_dag_dep.direct_successors(node_id_t)[-1]
            for elem in pred:
                if elem > maximal_index:
                    pred.remove(elem)

        block = []
        for node_id in pred:
            for dir_succ in self.template_dag_dep.direct_successors(node_id):
                if dir_succ not in matches:
                    succ = self.template_dag_dep.successors(dir_succ)
                    block = block + succ
        self.candidates = list(
            set(self.template_dag_dep.direct_successors(node_id_t)) - set(matches) - set(block)
        )

    def _init_matched_nodes(self):
        """
        初始化当前匹配节点的列表。
        """
        self.matched_nodes_list.append(
            [self.node_id_c, self.circuit_dag_dep.get_node(self.node_id_c)]
        )

    def _get_node_forward(self, list_id):
        """
        对于给定的列表id，从匹配的_ node _ list中返回一个节点。
        Args：
        list _ id ( int )：考虑的期望节点列表id。
        返回：DAGDepNode：匹配后的_ node _ list的第i个节点对应的DAGDepNode对象。
        """
        node = self.matched_nodes_list[list_id][1]
        return node
    def _remove_node_forward(self, list_id):
        """
        对于给定的列表id，删除当前匹配列表的一个节点。Args：list _ id ( int )：考虑的期望节点列表id。
        """
        self.matched_nodes_list.pop(list_id)

    def _update_successor(self, node, successor_id):
        """
        返回一个具有更新属性' SuccessorToVisit '的节点
        Args:
            node (DAGDepNode): current node.
            successor_id (int): successor id to remove.
        Returns:
            DAGOpNode or DAGOutNode: Node with updated attribute 'SuccessorToVisit'.
        """
        node_update = node
        node_update.successorstovisit.pop(successor_id)
        return node_update

    def _get_successors_to_visit(self, node, list_id):
        """
        返回给定节点和id的后继节点。
        Args:
            node (DAGOpNode or DAGOutNode): current node.
            list_id (int): id in the list for the successor to get.
        Returns:
            int: id of the successor to get.
        """
        successor_id = node.successorstovisit[list_id]
        return successor_id

    def _update_qarg_indices(self, qarg):
        """
        改变当前电路节点的量子比特索引，以便与模板量子比特列表的索引具有可比性。
        Args：qarg ( list )：来自电路的给定节点的量子比特索引列表。
        """
        self.qarg_indices = []
        for q in qarg:
            if q in self.qubits:
                self.qarg_indices.append(self.qubits.index(q))
        if len(qarg) != len(self.qarg_indices):
            self.qarg_indices = []

    def _update_carg_indices(self, carg):
        """
        更改当前电路节点的clbits索引，以便与模板量子比特列表的索引具有可比性。
        Args：carg ( list )：电路中给定节点的clbits索引列表。
        """
        self.carg_indices = []
        if carg:
            for q in carg:
                if q in self.clbits:
                    self.carg_indices.append(self.clbits.index(q))
            if len(carg) != len(self.carg_indices):
                self.carg_indices = []

    def _is_same_op(self, node_circuit, node_template):
        """
        检查两条指令是否相同。args：
        node _ circuit ( DAGDepNode )：电路中的节点。
        node _ template ( DAGDepNode )：模板中的节点。
        返回：Bool：如果相同则为true，否则为false。
        """
        return node_circuit.op.soft_compare(node_template.op)

    def _is_same_q_conf(self, node_circuit, node_template):
        """
        检查量子比特配置是否兼容。
        args：node _ circuit ( DAGDepNode )：电路中的节点。
        node _ template ( DAGDepNode )：模板中的节点。
        返回：Bool：如果可能，则为true，否则为false。
        """

        if isinstance(node_circuit.op, ControlledGate):

            c_template = node_template.op.num_ctrl_qubits

            if c_template == 1:
                return self.qarg_indices == node_template.qindices

            else:
                control_qubits_template = node_template.qindices[:c_template]
                control_qubits_circuit = self.qarg_indices[:c_template]

                if set(control_qubits_circuit) == set(control_qubits_template):

                    target_qubits_template = node_template.qindices[c_template::]
                    target_qubits_circuit = self.qarg_indices[c_template::]

                    if node_template.op.base_gate.name in [
                        "rxx",
                        "ryy",
                        "rzz",
                        "swap",
                        "iswap",
                        "ms",
                    ]:
                        return set(target_qubits_template) == set(target_qubits_circuit)
                    else:
                        return target_qubits_template == target_qubits_circuit
                else:
                    return False
        else:
            if node_template.op.name in ["rxx", "ryy", "rzz", "swap", "iswap", "ms"]:
                return set(self.qarg_indices) == set(node_template.qindices)
            else:
                return self.qarg_indices == node_template.qindices

    def _is_same_c_conf(self, node_circuit, node_template):
        """
        检查clbits配置是否兼容。
        args：node _ circuit ( DAGDepNode )：电路中的节点。
        node _ template ( DAGDepNode )：模板中的节点。
        返回：Bool：如果可能，则为true，否则为false。
        """
        if (
            node_circuit.type == "op"
            and node_circuit.op.condition
            and node_template.type == "op"
            and node_template.op.conditon
        ):
            if set(self.carg_indices) != set(node_template.cindices):
                return False
            if node_circuit.op.condition[1] != node_template.op.conditon[1]:
                return False
        return True

    def run_forward_match(self):
        """
        应用前向匹配算法，返回给定初始匹配和电路量子比特配置的匹配列表。
        """

        # 初始化DAGDependency对象的DAGDepNodes的新属性
        self._init_successors_to_visit()

        self._init_matched_with_circuit()
        self._init_matched_with_template()

        self._init_is_blocked_circuit()
        self._init_is_blocked_template()

        # 初始化匹配列表和匹配节点堆栈(电路)
        self._init_list_match()
        self._init_matched_nodes()

        # 而匹配节点的列表不是空的
        while self.matched_nodes_list:

            # 返回matching _ node _ list的第一个元素，并将其从列表中删除
            v_first = self._get_node_forward(0)
            self._remove_node_forward(0)

            # 如果没有接班人来参观就走到最后
            if not v_first.successorstovisit:
                continue

            # 获取要访问的第一个继承者的标签和节点
            label = self._get_successors_to_visit(v_first, 0)
            v = [label, self.circuit_dag_dep.get_node(label)]

            # SuccessorsToVisit属性的更新
            v_first = self._update_successor(v_first, 0)

            # 使用新的属性继承者更新matching _ node _ list以访问列表并对列表进行排序。
            self.matched_nodes_list.append([v_first.node_id, v_first])
            self.matched_nodes_list.sort(key=lambda x: x[1].successorstovisit)

            # 如果节点被阻止并且已经匹配，则转到末尾
            if v[1].isblocked | (v[1].matchedwith != []):
                continue

            # 在模板中搜索潜在的候选者
            self._find_forward_candidates(v_first.matchedwith[0])

            qarg1 = self.circuit_dag_dep.get_node(label).qindices
            carg1 = self.circuit_dag_dep.get_node(label).cindices

            # 更新量子比特和clbit的索引，以便与模板电路中的索引进行比较。
            self._update_qarg_indices(qarg1)
            self._update_carg_indices(carg1)

            match = False

            # 用于循环遍历候选项(模板)以查找匹配项。
            for i in self.candidates:

                # 如果找到匹配，则中断for循环。
                if match:
                    break

                # 比较量子比特和操作的指数，
                # if True; a match is found
                node_circuit = self.circuit_dag_dep.get_node(label)
                node_template = self.template_dag_dep.get_node(i)

                # 匹配发生的必要条件，但不是充分条件。
                if (
                    len(self.qarg_indices) != len(node_template.qindices)
                    or set(self.qarg_indices) != set(node_template.qindices)
                    or node_circuit.name != node_template.name
                ):
                    continue

                # 检查量子比特，clbit配置是否与匹配兼容，也检查操作是否相同。
                if (
                    self._is_same_q_conf(node_circuit, node_template)
                    and self._is_same_c_conf(node_circuit, node_template)
                    and self._is_same_op(node_circuit, node_template)
                ):

                    v[1].matchedwith = [i]

                    self.template_dag_dep.get_node(i).matchedwith = [label]

                    # 将新匹配追加到匹配列表中。
                    self.match.append([i, label])

                    # 为给定匹配访问(电路)的潜在继任者。
                    potential = self.circuit_dag_dep.direct_successors(label)

                    # 如果要访问的潜在继任者被阻止或匹配，则将其删除。
                    for potential_id in potential:
                        if self.circuit_dag_dep.get_node(potential_id).isblocked | (
                            self.circuit_dag_dep.get_node(potential_id).matchedwith != []
                        ):
                            potential.remove(potential_id)

                    sorted_potential = sorted(potential)

                    #  更新继任者访问属性
                    v[1].successorstovisit = sorted_potential

                    # 将更新后的节点添加到堆栈中
                    self.matched_nodes_list.append([v[0], v[1]])
                    self.matched_nodes_list.sort(key=lambda x: x[1].successorstovisit)
                    match = True
                    continue

            # 如果未找到匹配，则阻塞节点和所有的后继节点。
            if not match:
                v[1].isblocked = True
                for succ in v[1].successors:
                    self.circuit_dag_dep.get_node(succ).isblocked = True
                    if self.circuit_dag_dep.get_node(succ).matchedwith:
                        self.match.remove(
                            [self.circuit_dag_dep.get_node(succ).matchedwith[0], succ]
                        )
                        match_id = self.circuit_dag_dep.get_node(succ).matchedwith[0]
                        self.template_dag_dep.get_node(match_id).matchedwith = []
                        self.circuit_dag_dep.get_node(succ).matchedwith = []


