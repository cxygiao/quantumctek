
"""
模板匹配所有可能的量子比特配置和初始匹配。 它返回从此算法获得的所有匹配项的列表。

"""

import itertools

from qiskit.circuit.controlledgate import ControlledGate
from qiskit.transpiler.passes.optimization.template_matching.forward_match import ForwardMatch
from qiskit.transpiler.passes.optimization.template_matching.backward_match import BackwardMatch


class TemplateMatching:
    """
    Class TemplatingMatching allows to apply the full template matching algorithm.
    """

    def __init__(
        self,
        circuit_dag_dep,
        template_dag_dep,
        heuristics_qubits_param=None,
        heuristics_backward_param=None,
    ):
        """
        创建一个带有必要参数的TemplateMatching对象。
        Args:
            circuit_dag_dep (QuantumCircuit): circuit.
            template_dag_dep (QuantumCircuit): template.
            heuristics_backward_param (list[int]): [length, survivor]
            heuristics_qubits_param (list[int]): [length]
        """
        self.circuit_dag_dep = circuit_dag_dep
        self.template_dag_dep = template_dag_dep
        self.match_list = []
        self.heuristics_qubits_param = (
            heuristics_qubits_param if heuristics_qubits_param is not None else []
        )
        self.heuristics_backward_param = (
            heuristics_backward_param if heuristics_backward_param is not None else []
        )

    def _list_first_match_new(self, node_circuit, node_template, n_qubits_t, n_clbits_t):
        """
        返回电路的量子比特列表，给定第一个匹配，未知量子比特被替换为- 1。
        Args:
            node_circuit (DAGDepNode): First match node in the circuit.
            node_template (DAGDepNode): First match node in the template.
            n_qubits_t (int): number of qubit in the template.
            n_clbits_t (int): number of classical bit in the template.
        Returns:
            list: list of qubits to consider in circuit (with specific order).
        """
        l_q = []

        # Controlled gate
        if isinstance(node_circuit.op, ControlledGate) and node_template.op.num_ctrl_qubits > 1:
            control = node_template.op.num_ctrl_qubits
            control_qubits_circuit = node_circuit.qindices[:control]
            not_control_qubits_circuit = node_circuit.qindices[control::]

            # 对称基门
            if node_template.op.base_gate.name not in ["rxx", "ryy", "rzz", "swap", "iswap", "ms"]:
                for control_perm_q in itertools.permutations(control_qubits_circuit):
                    control_perm_q = list(control_perm_q)
                    l_q_sub = [-1] * n_qubits_t
                    for q in node_template.qindices:
                        node_circuit_perm = control_perm_q + not_control_qubits_circuit
                        l_q_sub[q] = node_circuit_perm[node_template.qindices.index(q)]
                    l_q.append(l_q_sub)
            # 不是对称的基本门
            else:
                for control_perm_q in itertools.permutations(control_qubits_circuit):
                    control_perm_q = list(control_perm_q)
                    for not_control_perm_q in itertools.permutations(not_control_qubits_circuit):
                        not_control_perm_q = list(not_control_perm_q)
                        l_q_sub = [-1] * n_qubits_t
                        for q in node_template.qindices:
                            node_circuit_perm = control_perm_q + not_control_perm_q
                            l_q_sub[q] = node_circuit_perm[node_template.qindices.index(q)]
                        l_q.append(l_q_sub)
        # Not controlled
        else:
            # Symmetric gate
            if node_template.op.name not in ["rxx", "ryy", "rzz", "swap", "iswap", "ms"]:
                l_q_sub = [-1] * n_qubits_t
                for q in node_template.qindices:
                    l_q_sub[q] = node_circuit.qindices[node_template.qindices.index(q)]
                l_q.append(l_q_sub)
            # Not symmetric
            else:
                for perm_q in itertools.permutations(node_circuit.qindices):
                    l_q_sub = [-1] * n_qubits_t
                    for q in node_template.qindices:
                        l_q_sub[q] = perm_q[node_template.qindices.index(q)]
                    l_q.append(l_q_sub)

        # Classical control
        if not node_template.cindices or not node_circuit.cindices:
            l_c = []
        else:
            l_c = [-1] * n_clbits_t
            for c in node_template.cindices:
                l_c[c] = node_circuit[node_template.cindices.index(c)]

        return l_q, l_c

    def _sublist(self, lst, exclude, length):
        """
        函数返回给定长度的所有可能组合，考虑排除的元素列表。
        Args:
            lst (list): 来自电路的量子比特索引列表。
            exclude (list): 来自第一个匹配电路门的量子比特列表。
            length (int): 要返回的列表长度(模板量子比特数-来自第一个匹配模板门的量子比特数)。
        产量：迭代程序：迭代程序的可能列表。
        """
        for sublist in itertools.combinations([e for e in lst if e not in exclude], length):
            yield list(sublist)

    def _list_qubit_clbit_circuit(self, list_first_match, permutation):
        """
       返回电路量子比特和clbit列表的函数给出一个置换和一个初始匹配。
        Args：list _ first _ matching ( list )：初始匹配的量子比特索引列表。
        排列( list )：电路量子比特的可能排列。
        返回：list：给定置换和初始匹配的电路量子比特列表。
        """
        list_circuit = []

        counter = 0

        for elem in list_first_match:
            if elem == -1:
                list_circuit.append(permutation[counter])
                counter = counter + 1
            else:
                list_circuit.append(elem)

        return list_circuit

    def _add_match(self, backward_match_list):
        """
        方法仅在列表中尚未包含匹配项时才在列表中添加匹配项。
        如果匹配已经在列表中，则将量子比特配置追加到现有匹配中。
        Args:
            backward_match_list (list): match from the backward part of the
            algorithm.
        """

        already_in = False

        for b_match in backward_match_list:
            for l_match in self.match_list:
                if b_match.match == l_match.match:
                    index = self.match_list.index(l_match)
                    self.match_list[index].qubit.append(b_match.qubit[0])
                    already_in = True

            if not already_in:
                self.match_list.append(b_match)

    def _explore_circuit(self, node_id_c, node_id_t, n_qubits_t, length):
        """
       探索node _ id _ c (直到给定的长度)的后续节点。
        Args:
            node_id_c (int): first match id in the circuit.
            node_id_t (int): first match id in the template.
            n_qubits_t (int): number of qubits in the template.
            length (int): 接班人探索的长度。
        Returns:
            list: 对node _ id _ c的" length "后继节点进行Qubits配置
        """
        template_nodes = range(node_id_t + 1, self.template_dag_dep.size())
        circuit_nodes = range(0, self.circuit_dag_dep.size())
        successors_template = self.template_dag_dep.get_node(node_id_t).successors

        counter = 1
        qubit_set = set(self.circuit_dag_dep.get_node(node_id_c).qindices)
        if 2 * len(successors_template) > len(template_nodes):
            successors = self.circuit_dag_dep.get_node(node_id_c).successors
            for succ in successors:
                qarg = self.circuit_dag_dep.get_node(succ).qindices
                if (len(qubit_set | set(qarg))) <= n_qubits_t and counter <= length:
                    qubit_set = qubit_set | set(qarg)
                    counter += 1
                elif (len(qubit_set | set(qarg))) > n_qubits_t:
                    return list(qubit_set)
            return list(qubit_set)

        else:
            not_successors = list(
                set(circuit_nodes) - set(self.circuit_dag_dep.get_node(node_id_c).successors)
            )
            candidate = [
                not_successors[j]
                for j in range(len(not_successors) - 1, len(not_successors) - 1 - length, -1)
            ]

            for not_succ in candidate:
                qarg = self.circuit_dag_dep.get_node(not_succ).qindices
                if counter <= length and (len(qubit_set | set(qarg))) <= n_qubits_t:
                    qubit_set = qubit_set | set(qarg)
                    counter += 1
                elif (len(qubit_set | set(qarg))) > n_qubits_t:
                    return list(qubit_set)
            return list(qubit_set)

    def run_template_matching(self):
        """
        运行完整的算法，找到给定模板和电路的所有最大匹配。
        首先，它修复了电路的配置，由于第一次匹配。
        然后它探索电路的所有兼容的量子比特配置。
        对于每个量子比特配置，我们首先应用算法的Forward部分，然后应用算法的Backward部分。
        存储给定配置的最长匹配项。最后对存储的匹配列表进行排序。
        """

        # Get the number of qubits/clbits for both circuit and template.
        n_qubits_c = len(self.circuit_dag_dep.qubits)
        n_clbits_c = len(self.circuit_dag_dep.clbits)

        n_qubits_t = len(self.template_dag_dep.qubits)
        n_clbits_t = len(self.template_dag_dep.clbits)

        # 对模板和电路的指标进行循环。
        for template_index in range(0, self.template_dag_dep.size()):
            for circuit_index in range(0, self.circuit_dag_dep.size()):
                # 操作与Parameter Expresss匹配。
                if self.circuit_dag_dep.get_node(circuit_index).op.soft_compare(
                    self.template_dag_dep.get_node(template_index).op
                ):

                    qarg_c = self.circuit_dag_dep.get_node(circuit_index).qindices
                    carg_c = self.circuit_dag_dep.get_node(circuit_index).cindices

                    qarg_t = self.template_dag_dep.get_node(template_index).qindices
                    carg_t = self.template_dag_dep.get_node(template_index).cindices

                    node_id_c = circuit_index
                    node_id_t = template_index

                    # 修复给定第一个匹配的量子比特和clbits配置。

                    all_list_first_match_q, list_first_match_c = self._list_first_match_new(
                        self.circuit_dag_dep.get_node(circuit_index),
                        self.template_dag_dep.get_node(template_index),
                        n_qubits_t,
                        n_clbits_t,
                    )

                    list_circuit_q = list(range(0, n_qubits_c))
                    list_circuit_c = list(range(0, n_clbits_c))

                    # 如果量子比特启发式的参数给定，那么提取电路中后继者(长度( int ) )的量子比特列表。

                    if self.heuristics_qubits_param:
                        heuristics_qubits = self._explore_circuit(
                            node_id_c, node_id_t, n_qubits_t, self.heuristics_qubits_param[0]
                        )
                    else:
                        heuristics_qubits = []

                    for sub_q in self._sublist(list_circuit_q, qarg_c, n_qubits_t - len(qarg_t)):
                        # If the heuristics qubits are a subset of the given qubits configuration,
                        # then this configuration is accepted.
                        if set(heuristics_qubits).issubset(set(sub_q) | set(qarg_c)):
                            # Permute the qubit configuration.
                            for perm_q in itertools.permutations(sub_q):
                                perm_q = list(perm_q)
                                for list_first_match_q in all_list_first_match_q:
                                    list_qubit_circuit = self._list_qubit_clbit_circuit(
                                        list_first_match_q, perm_q
                                    )

                                    # Check for clbits configurations if there are clbits.
                                    if list_circuit_c:
                                        for sub_c in self._sublist(
                                            list_circuit_c, carg_c, n_clbits_t - len(carg_t)
                                        ):
                                            for perm_c in itertools.permutations(sub_c):
                                                perm_c = list(perm_c)

                                                list_clbit_circuit = self._list_qubit_clbit_circuit(
                                                    list_first_match_c, perm_c
                                                )

                                                # Apply the forward match part of the algorithm.
                                                forward = ForwardMatch(
                                                    self.circuit_dag_dep,
                                                    self.template_dag_dep,
                                                    node_id_c,
                                                    node_id_t,
                                                    list_qubit_circuit,
                                                    list_clbit_circuit,
                                                )
                                                forward.run_forward_match()

                                                # Apply the backward match part of the algorithm.
                                                backward = BackwardMatch(
                                                    forward.circuit_dag_dep,
                                                    forward.template_dag_dep,
                                                    forward.match,
                                                    node_id_c,
                                                    node_id_t,
                                                    list_qubit_circuit,
                                                    list_clbit_circuit,
                                                    self.heuristics_backward_param,
                                                )

                                                backward.run_backward_match()

                                                # Add the matches to the list.
                                                self._add_match(backward.match_final)
                                    else:
                                        # Apply the forward match part of the algorithm.
                                        forward = ForwardMatch(
                                            self.circuit_dag_dep,
                                            self.template_dag_dep,
                                            node_id_c,
                                            node_id_t,
                                            list_qubit_circuit,
                                        )
                                        forward.run_forward_match()

                                        # Apply the backward match part of the algorithm.
                                        backward = BackwardMatch(
                                            forward.circuit_dag_dep,
                                            forward.template_dag_dep,
                                            forward.match,
                                            node_id_c,
                                            node_id_t,
                                            list_qubit_circuit,
                                            [],
                                            self.heuristics_backward_param,
                                        )
                                        backward.run_backward_match()

                                        # Add the matches to the list.
                                        self._add_match(backward.match_final)

        # 根据匹配项的长度(递减顺序)对匹配项列表进行排序。
        self.match_list.sort(key=lambda x: len(x.match), reverse=True)
