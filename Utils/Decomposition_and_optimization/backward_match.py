"""
反向模板匹配，它需要一个初始匹配、一个量子比特的配置、电路和模板作为输入，
以及从正向匹配中获得的列表。 结果是模板和电路之间的匹配列表。
"""
import heapq

from qiskit.circuit.controlledgate import ControlledGate

class Match:
    """
    表示匹配及其量子比特配置的对象。
    """
    def __init__(self, match, qubit, clbit):
        """
        创建一个带有必要参数的 Match 类。
         参数：
             match（list）：匹配门的列表。
             qubit (list)：量子比特配置列表。
             clbit(list)：clbits配置列表。
        """
        # Match list
        self.match = match
        # Qubits list for circuit
        self.qubit = [qubit]
        # Clbits for template
        self.clbit = [clbit]

class MatchingScenarios:
    """
    表示匹配场景的类。
    """
    def __init__(
        self, circuit_matched, circuit_blocked, template_matched, template_blocked, matches, counter
    ):
        """
         创建一个带有必要参数的 MatchingScenarios 类。
         参数：
             circuit_matched (list)：电路中匹配属性的列表。
             circuit_blocked(list)：电路中被阻塞属性的列表。
             template_matched(list)：模板中匹配属性的列表。
             template_blocked(list)：模板中被阻塞的属性列表。
             matches (list):匹配列表。
             counter (int)：已经考虑的电路门数量的计数器。
        """
        self.circuit_matched = circuit_matched
        self.template_matched = template_matched
        self.circuit_blocked = circuit_blocked
        self.template_blocked = template_blocked
        self.matches = matches
        self.counter = counter


class MatchingScenariosList:
    """
    定义匹配场景列表的对象，带有追加和弹出元素的方法。
    """

    def __init__(self):
        """
        创建一个空的 MatchingScenariosList。
        """
        self.matching_scenarios_list = []

    def append_scenario(self, matching):
        """
       将场景附加到列表中。
         参数：
             matching（MatchingScenarios）：匹配的一个场景。
        """
        self.matching_scenarios_list.append(matching)

    def pop_scenario(self):
        """
        弹出列表的第一个场景。
         回报：
             MatchingScenarios：匹配的场景。
        """
        # 弹出第一个 MatchingScenario 并返回它
        first = self.matching_scenarios_list[0]
        self.matching_scenarios_list.pop(0)
        return first


class BackwardMatch:
    """
    BackwardMatch 类允许运行模板匹配算法的反向部分。
    """
    def __init__(
        self,
        circuit_dag_dep,
        template_dag_dep,
        forward_matches,
        node_id_c,
        node_id_t,
        qubits,
        clbits=None,
        heuristics_backward_param=None,
    ):
        """
        创建一个带有必要参数的 ForwardMatch 类。
         参数：
             circuit_dag_dep (DAGDependency)：dag依赖形式的电路。
             template_dag_dep (DAGDependency)：dag 依赖形式的模板。
             forward_matches(list)：正向获取的匹配列表。
             node_id_c (int)：电路中匹配的第一个门的索引。
             node_id_t (int)：模板中匹配的第一个门的索引。
             qubits (list)：电路中考虑的量子位列表。
             clbits (list)：电路中考虑的 clbits 列表。
             heuristics_backward_param (list)：包含应用启发式的两个参数（长度和幸存者）的列表。
        """
        self.circuit_dag_dep = circuit_dag_dep.copy()
        self.template_dag_dep = template_dag_dep.copy()
        self.qubits = qubits
        self.clbits = clbits if clbits is not None else []
        self.node_id_c = node_id_c
        self.node_id_t = node_id_t
        self.forward_matches = forward_matches
        self.match_final = []
        self.heuristics_backward_param = (
            heuristics_backward_param if heuristics_backward_param is not None else []
        )
        self.matching_list = MatchingScenariosList()

    def _gate_indices(self):
        """
        返回第一个场景不匹配且未阻塞的门列表的函数。
         返回：
             列表：门 ID 列表。
        """
        gate_indices = []

        current_dag = self.circuit_dag_dep

        for node in current_dag.get_nodes():
            if (not node.matchedwith) and (not node.isblocked):
                gate_indices.append(node.node_id)
        gate_indices.reverse()
        return gate_indices

    def _find_backward_candidates(self, template_blocked, matches):
        """
        返回模板 dag 中可能的后向候选列表的函数。
         参数：
             template_blocked(list)：在模板电路中被阻塞的属性列表。
             matches (list)：匹配列表。
         返回：
             list：后向候选人（id）的列表。
        """
        template_block = []

        for node_id in range(self.node_id_t, self.template_dag_dep.size()):
            if template_blocked[node_id]:
                template_block.append(node_id)

        matches_template = sorted(match[0] for match in matches)

        successors = self.template_dag_dep.get_node(self.node_id_t).successors
        potential = []
        for index in range(self.node_id_t + 1, self.template_dag_dep.size()):
            if (index not in successors) and (index not in template_block):
                potential.append(index)

        candidates_indices = list(set(potential) - set(matches_template))
        candidates_indices = sorted(candidates_indices)
        candidates_indices.reverse()

        return candidates_indices

    def _update_qarg_indices(self, qarg):
        """
        更改当前电路节点的 qubits 索引，以便与模板 qubits 列表的索引进行比较。
         参数：
             qarg（list）：给定门电路的量子比特索引列表。
         返回：
             list：量子比特的电路索引更新。
        """
        qarg_indices = []
        for q in qarg:
            if q in self.qubits:
                qarg_indices.append(self.qubits.index(q))
        if len(qarg) != len(qarg_indices):
            qarg_indices = []
        return qarg_indices

    def _update_carg_indices(self, carg):
        """
        更改当前电路节点的 clbits 索引，以便与模板 qubits 列表的索引进行比较。
         参数：
             carg (list)：给定门电路的 clbits 索引列表。
         返回：
             list：clbits 的电路索引更新。
        """
        carg_indices = []
        if carg:
            for q in carg:
                if q in self.clbits:
                    carg_indices.append(self.clbits.index(q))
            if len(carg) != len(carg_indices):
                carg_indices = []
        return carg_indices

    def _is_same_op(self, node_circuit, node_template):
        """
        检查两个指令是否相同。
         参数：
             node_circuit (DAGDepNode)：电路中的节点。
             node_template (DAGDepNode)：模板中的节点。
         返回：
             bool：如果相同，则为 True，否则为 False。
        """
        return node_circuit.op == node_template.op

    def _is_same_q_conf(self, node_circuit, node_template, qarg_circuit):
        """
        检查量子比特配置是否兼容。
         参数：
             node_circuit (DAGDepNode)：电路中的节点。
             node_template (DAGDepNode)：模板中的节点。
             qarg_circuit（list）：电路中指令的量子比特配置。
         返回：
             bool：如果可能，则为 True，否则为 False。
        """
        # 如果门受到控制，则必须将控制量子位作为集合进行比较。
        if isinstance(node_circuit.op, ControlledGate):

            c_template = node_template.op.num_ctrl_qubits

            if c_template == 1:
                return qarg_circuit == node_template.qindices

            else:
                control_qubits_template = node_template.qindices[:c_template]
                control_qubits_circuit = qarg_circuit[:c_template]

                if set(control_qubits_circuit) == set(control_qubits_template):

                    target_qubits_template = node_template.qindices[c_template::]
                    target_qubits_circuit = qarg_circuit[c_template::]

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
        # 对于非受控门，对称门的量子位索引可以作为集合进行比较
        # 但是对于非对称门，量子位索引必须作为列表进行比较。
        else:
            if node_template.op.name in ["rxx", "ryy", "rzz", "swap", "iswap", "ms"]:
                return set(qarg_circuit) == set(node_template.qindices)
            else:
                return qarg_circuit == node_template.qindices

    def _is_same_c_conf(self, node_circuit, node_template, carg_circuit):
        """
        检查 clbits 配置是否兼容。
         参数：
             node_circuit (DAGDepNode)：电路中的节点。
             node_template (DAGDepNode)：模板中的节点。
             carg_circuit(list)：电路中指令的clbits配置。
         回报：
             bool：如果可能，则为 True，否则为 False。
        """
        if (
            node_circuit.type == "op"
            and node_circuit.op.condition
            and node_template.type == "op"
            and node_template.op.condition
        ):
            if set(carg_circuit) != set(node_template.cindices):
                return False
            if node_circuit.op.condition[1] != node_template.op.conditon[1]:
                return False
        return True

    def _init_matched_blocked_list(self):
        """
        初始化被阻止和匹配的属性列表。
         回报：
             元组[列表，列表，列表，列表]：
             第一个列表包含电路中匹配的属性，
             第二个列表包含电路中被阻塞的属性 ，
             第三个列表包含模板中匹配的属性，
             第四个列表包含模板中被组塞的属性 。
        """
        circuit_matched = []
        circuit_blocked = []

        for node in self.circuit_dag_dep.get_nodes():
            circuit_matched.append(node.matchedwith)
            circuit_blocked.append(node.isblocked)

        template_matched = []
        template_blocked = []

        for node in self.template_dag_dep.get_nodes():
            template_matched.append(node.matchedwith)
            template_blocked.append(node.isblocked)

        return circuit_matched, circuit_blocked, template_matched, template_blocked

    def _backward_heuristics(self, gate_indices, length, survivor):
        """
        在反向匹配算法中切割树的启发式
         参数：
             gate_indices (list)：电路中的候选列表。
             length (int): 切割树的深度，切割操作在每个长度重复一次。
             survivor （int）：幸存者分支的数量。
        """
        # 设置不同场景的计数器列表。
        list_counter = []

        for scenario in self.matching_list.matching_scenarios_list:
            list_counter.append(scenario.counter)

        metrics = []
        # 如果所有场景都有相同的计数器并且计数器可以被长度整除。
        if list_counter.count(list_counter[0]) == len(list_counter) and list_counter[0] <= len(
            gate_indices
        ):
            if (list_counter[0] - 1) % length == 0:
                # 列表指标包含每个场景的指标结果。
                for scenario in self.matching_list.matching_scenarios_list:
                    metrics.append(self._backward_metrics(scenario))
                # 对于给定的幸存者数量，仅选择具有更高指标的场景。
                largest = heapq.nlargest(survivor, range(len(metrics)), key=lambda x: metrics[x])
                self.matching_list.matching_scenarios_list = [
                    i
                    for j, i in enumerate(self.matching_list.matching_scenarios_list)
                    if j in largest
                ]

    def _backward_metrics(self, scenario):
        """
       启发式在反向匹配算法中切割树。
         参数：
             scenario（MatchingScenarios）：给定匹配的场景。
         回报：
             int：给定场景的匹配长度。
        """
        return len(scenario.matches)

    def run_backward_match(self):
        """
        应用前向匹配算法并返回给定初始匹配和电路量子比特配置的匹配列表。
        """
        match_store_list = []

        counter = 1

        # 初始化 matchwith 和 isblocked 的属性列表。
        (
            circuit_matched,
            circuit_blocked,
            template_matched,
            template_blocked,
        ) = self._init_matched_blocked_list()

        # 第一个场景存储在 MatchingScenariosList() 中。
        first_match = MatchingScenarios(
            circuit_matched,
            circuit_blocked,
            template_matched,
            template_blocked,
            self.forward_matches,
            counter,
        )

        self.matching_list = MatchingScenariosList()
        self.matching_list.append_scenario(first_match)

        # 设置可以匹配的电路索引。
        gate_indices = self._gate_indices()

        number_of_gate_to_match = (
            self.template_dag_dep.size() - (self.node_id_t - 1) - len(self.forward_matches)
        )

        # 场景堆栈不为空。
        while self.matching_list.matching_scenarios_list:

            # 如果给定参数，则应用启发式方法。
            if self.heuristics_backward_param:
                self._backward_heuristics(
                    gate_indices,
                    self.heuristics_backward_param[0],
                    self.heuristics_backward_param[1],
                )

            scenario = self.matching_list.pop_scenario()

            circuit_matched = scenario.circuit_matched
            circuit_blocked = scenario.circuit_blocked
            template_matched = scenario.template_matched
            template_blocked = scenario.template_blocked
            matches_scenario = scenario.matches
            counter_scenario = scenario.counter

            # 部分匹配列表来自向后匹配。
            match_backward = [
                match for match in matches_scenario if match not in self.forward_matches
            ]

            # 如果计数器大于列表的长度，则存储匹配项
            # 电路中的候选人。 或者如果剩下要匹配的门数与
            # 匹配的后面部分的长度。
            if (
                counter_scenario > len(gate_indices)
                or len(match_backward) == number_of_gate_to_match
            ):
                matches_scenario.sort(key=lambda x: x[0])
                match_store_list.append(Match(matches_scenario, self.qubits, self.clbits))
                continue

            # 第一个电路候选人。
            circuit_id = gate_indices[counter_scenario - 1]
            node_circuit = self.circuit_dag_dep.get_node(circuit_id)

            # 如果电路候选被阻塞，则只改变计数器。
            if circuit_blocked[circuit_id]:
                matching_scenario = MatchingScenarios(
                    circuit_matched,
                    circuit_blocked,
                    template_matched,
                    template_blocked,
                    matches_scenario,
                    counter_scenario + 1,
                )
                self.matching_list.append_scenario(matching_scenario)
                continue

            # 模板中的候选人。
            candidates_indices = self._find_backward_candidates(template_blocked, matches_scenario)
            # 更新电路中的 qubits/clbits 索引，以便
            # 与模板中的相媲美。
            qarg1 = node_circuit.qindices
            carg1 = node_circuit.cindices

            qarg1 = self._update_qarg_indices(qarg1)
            carg1 = self._update_carg_indices(carg1)

            global_match = False
            global_broken = []

            # 循环遍历候选模板。
            for template_id in candidates_indices:

                node_template = self.template_dag_dep.get_node(template_id)
                qarg2 = self.template_dag_dep.get_node(template_id).qindices

                # 匹配发生的必要但非充分条件。
                if (
                    len(qarg1) != len(qarg2)
                    or set(qarg1) != set(qarg2)
                    or node_circuit.name != node_template.name
                ):
                    continue

                # 检查 qubit、clbit 配置是否兼容匹配，
                # 还要检查操作是否相同。
                if (
                    self._is_same_q_conf(node_circuit, node_template, qarg1)
                    and self._is_same_c_conf(node_circuit, node_template, carg1)
                    and self._is_same_op(node_circuit, node_template)
                ):

                    # 如果匹配，则复制属性。
                    circuit_matched_match = circuit_matched.copy()
                    circuit_blocked_match = circuit_blocked.copy()

                    template_matched_match = template_matched.copy()
                    template_blocked_match = template_blocked.copy()

                    matches_scenario_match = matches_scenario.copy()

                    block_list = []
                    broken_matches_match = []

                    # 循环检查匹配是否未连接，在这种情况下
                    # 后续匹配被阻止且不匹配。
                    for potential_block in self.template_dag_dep.successors(template_id):
                        if not template_matched_match[potential_block]:
                            template_blocked_match[potential_block] = True
                            block_list.append(potential_block)
                            for block_id in block_list:
                                for succ_id in self.template_dag_dep.successors(block_id):
                                    template_blocked_match[succ_id] = True
                                    if template_matched_match[succ_id]:
                                        new_id = template_matched_match[succ_id][0]
                                        circuit_matched_match[new_id] = []
                                        template_matched_match[succ_id] = []
                                        broken_matches_match.append(succ_id)

                    if broken_matches_match:
                        global_broken.append(True)
                    else:
                        global_broken.append(False)

                    new_matches_scenario_match = [
                        elem
                        for elem in matches_scenario_match
                        if elem[0] not in broken_matches_match
                    ]

                    condition = True

                    for back_match in match_backward:
                        if back_match not in new_matches_scenario_match:
                            condition = False
                            break

                    # 第一个选项贪婪匹配。
                    if ([self.node_id_t, self.node_id_c] in new_matches_scenario_match) and (
                        condition or not match_backward
                    ):
                        template_matched_match[template_id] = [circuit_id]
                        circuit_matched_match[circuit_id] = [template_id]
                        new_matches_scenario_match.append([template_id, circuit_id])

                        new_matching_scenario = MatchingScenarios(
                            circuit_matched_match,
                            circuit_blocked_match,
                            template_matched_match,
                            template_blocked_match,
                            new_matches_scenario_match,
                            counter_scenario + 1,
                        )
                        self.matching_list.append_scenario(new_matching_scenario)

                        global_match = True

            if global_match:
                circuit_matched_block_s = circuit_matched.copy()
                circuit_blocked_block_s = circuit_blocked.copy()

                template_matched_block_s = template_matched.copy()
                template_blocked_block_s = template_blocked.copy()

                matches_scenario_block_s = matches_scenario.copy()

                circuit_blocked_block_s[circuit_id] = True

                broken_matches = []

                # 第二个选项，不是贪婪匹配，阻止所有继任者（将门推到右边）。
                for succ in self.circuit_dag_dep.get_node(circuit_id).successors:
                    circuit_blocked_block_s[succ] = True
                    if circuit_matched_block_s[succ]:
                        broken_matches.append(succ)
                        new_id = circuit_matched_block_s[succ][0]
                        template_matched_block_s[new_id] = []
                        circuit_matched_block_s[succ] = []

                new_matches_scenario_block_s = [
                    elem for elem in matches_scenario_block_s if elem[1] not in broken_matches
                ]

                condition_not_greedy = True

                for back_match in match_backward:
                    if back_match not in new_matches_scenario_block_s:
                        condition_not_greedy = False
                        break

                if ([self.node_id_t, self.node_id_c] in new_matches_scenario_block_s) and (
                    condition_not_greedy or not match_backward
                ):
                    new_matching_scenario = MatchingScenarios(
                        circuit_matched_block_s,
                        circuit_blocked_block_s,
                        template_matched_block_s,
                        template_blocked_block_s,
                        new_matches_scenario_block_s,
                        counter_scenario + 1,
                    )
                    self.matching_list.append_scenario(new_matching_scenario)

                # 第三种选择：阻止后继者破坏匹配，
                # 我们还考虑了阻止所有前辈的可能性（将门推到左侧）。
                if broken_matches and all(global_broken):

                    circuit_matched_block_p = circuit_matched.copy()
                    circuit_blocked_block_p = circuit_blocked.copy()

                    template_matched_block_p = template_matched.copy()
                    template_blocked_block_p = template_blocked.copy()

                    matches_scenario_block_p = matches_scenario.copy()

                    circuit_blocked_block_p[circuit_id] = True

                    for pred in self.circuit_dag_dep.get_node(circuit_id).predecessors:
                        circuit_blocked_block_p[pred] = True

                    matching_scenario = MatchingScenarios(
                        circuit_matched_block_p,
                        circuit_blocked_block_p,
                        template_matched_block_p,
                        template_blocked_block_p,
                        matches_scenario_block_p,
                        counter_scenario + 1,
                    )
                    self.matching_list.append_scenario(matching_scenario)

            # 如果没有匹配，则有三个选项。
            if not global_match:

                circuit_blocked[circuit_id] = True

                following_matches = []

                successors = self.circuit_dag_dep.get_node(circuit_id).successors
                for succ in successors:
                    if circuit_matched[succ]:
                        following_matches.append(succ)

                # 第一个选项，电路门不干扰，因为没有后续匹配并且没有前任.
                predecessors = self.circuit_dag_dep.get_node(circuit_id).predecessors

                if not predecessors or not following_matches:

                    matching_scenario = MatchingScenarios(
                        circuit_matched,
                        circuit_blocked,
                        template_matched,
                        template_blocked,
                        matches_scenario,
                        counter_scenario + 1,
                    )
                    self.matching_list.append_scenario(matching_scenario)

                else:

                    circuit_matched_nomatch = circuit_matched.copy()
                    circuit_blocked_nomatch = circuit_blocked.copy()

                    template_matched_nomatch = template_matched.copy()
                    template_blocked_nomatch = template_blocked.copy()

                    matches_scenario_nomatch = matches_scenario.copy()

                    # 第二种选择，所有前辈都被阻止（电路门向左移动）。
                    for pred in predecessors:
                        circuit_blocked[pred] = True

                    matching_scenario = MatchingScenarios(
                        circuit_matched,
                        circuit_blocked,
                        template_matched,
                        template_blocked,
                        matches_scenario,
                        counter_scenario + 1,
                    )
                    self.matching_list.append_scenario(matching_scenario)

                    # 第三种选择，所有前辈都被阻止（电路门向右移动）。

                    broken_matches = []

                    successors = self.circuit_dag_dep.get_node(circuit_id).successors

                    for succ in successors:
                        circuit_blocked_nomatch[succ] = True
                        if circuit_matched_nomatch[succ]:
                            broken_matches.append(succ)
                            circuit_matched_nomatch[succ] = []

                    new_matches_scenario_nomatch = [
                        elem for elem in matches_scenario_nomatch if elem[1] not in broken_matches
                    ]

                    condition_block = True

                    for back_match in match_backward:
                        if back_match not in new_matches_scenario_nomatch:
                            condition_block = False
                            break

                    if ([self.node_id_t, self.node_id_c] in matches_scenario_nomatch) and (
                        condition_block or not match_backward
                    ):
                        new_matching_scenario = MatchingScenarios(
                            circuit_matched_nomatch,
                            circuit_blocked_nomatch,
                            template_matched_nomatch,
                            template_blocked_nomatch,
                            new_matches_scenario_nomatch,
                            counter_scenario + 1,
                        )
                        self.matching_list.append_scenario(new_matching_scenario)

        length = max(len(m.match) for m in match_store_list)

        # 以最大长度存储匹配项。
        for scenario in match_store_list:
            if (len(scenario.match) == length) and not any(
                scenario.match == x.match for x in self.match_final
            ):
                self.match_final.append(scenario)


