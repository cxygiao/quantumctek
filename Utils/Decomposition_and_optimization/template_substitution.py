
"""
模板匹配替换，给定一个最大匹配列表，它会在电路中替换它们并创建一个新的优化 dag 版本的电路。
"""
import copy

from qiskit.circuit import ParameterExpression
from qiskit.dagcircuit.dagcircuit import DAGCircuit
from qiskit.dagcircuit.dagdependency import DAGDependency
from qiskit.converters.dagdependency_to_dag import dagdependency_to_dag


class SubstitutionConfig:
    """
    类来存储给定匹配替换的配置，其中电路门、模板门、量子比特和clbit与电路中的匹配前体。
    """

    def __init__(
        self,
        circuit_config,
        template_config,
        pred_block,
        qubit_config,
        template_dag_dep,
        clbit_config=None,
    ):
        self.template_dag_dep = template_dag_dep
        self.circuit_config = circuit_config
        self.template_config = template_config
        self.qubit_config = qubit_config
        self.clbit_config = clbit_config if clbit_config is not None else []
        self.pred_block = pred_block

    def has_parameters(self):
        """确保模板没有参数。"""
        for node in self.template_dag_dep.get_nodes():
            for param in node.op.params:
                if isinstance(param, ParameterExpression):
                    return True

        return False


class TemplateSubstitution:
    """
    类从最大匹配列表中运行替换算法
    """

    def __init__(self, max_matches, circuit_dag_dep, template_dag_dep, user_cost_dict=None):
        """
        用必要的参数初始化TemplateSubstitution。
        args：max _ match ( list )：从运行模板匹配算法中获得的最大匹配列表。
        circuit _ dag _ dep ( DAGDependency )：dag依赖形式的电路。
        template _ dag _ dep ( DAGDependency )：dag依赖形式的模板。
        user _ cost _ dict ( Optional [ dict ] )：用户提供的成本字典，它将覆盖默认的成本字典。
        """

        self.match_stack = max_matches
        self.circuit_dag_dep = circuit_dag_dep
        self.template_dag_dep = template_dag_dep

        self.substitution_list = []
        self.unmatched_list = []
        self.dag_dep_optimized = DAGDependency()
        self.dag_optimized = DAGCircuit()

        if user_cost_dict is not None:
            self.cost_dict = dict(user_cost_dict)
        else:
            self.cost_dict = {
                "id": 0,
                "x": 1,
                "y": 1,
                "z": 1,
                "h": 1,
                "t": 1,
                "tdg": 1,
                "s": 1,
                "sdg": 1,
                "u1": 1,
                "u2": 2,
                "u3": 2,
                "rx": 1,
                "ry": 1,
                "rz": 1,
                "r": 2,
                "cx": 2,
                "cy": 4,
                "cz": 4,
                "ch": 8,
                "swap": 6,
                "iswap": 8,
                "rxx": 9,
                "ryy": 9,
                "rzz": 5,
                "rzx": 7,
                "ms": 9,
                "cu3": 10,
                "crx": 10,
                "cry": 10,
                "crz": 10,
                "ccx": 21,
                "rccx": 12,
                "c3x": 96,
                "rc3x": 24,
                "c4x": 312,
                "p": 1,
            }

    def _pred_block(self, circuit_sublist, index):
        """
        它返回电路给定部分的前件。Args：circuit _ sublist ( list )：电路中匹配的门的列表。
        index ( int )：匹配组的索引。
        返回：列表：列出前人对当前匹配电路的配置。
        """
        predecessors = set()
        for node_id in circuit_sublist:
            predecessors = predecessors | set(self.circuit_dag_dep.get_node(node_id).predecessors)

        exclude = set()
        for elem in self.substitution_list[:index]:
            exclude = exclude | set(elem.circuit_config) | set(elem.pred_block)

        pred = list(predecessors - set(circuit_sublist) - exclude)
        pred.sort()

        return pred

    def _quantum_cost(self, left, right):
        """
        比较模板的两个部分，如果减少了量子成本，则返回True。
        Args：左(列表)：模板中匹配节点列表。
        右(列表)：待替换节点列表。
        returns：bool：如果降低了量子成本，则为true
        """
        cost_left = 0
        for i in left:
            cost_left += self.cost_dict[self.template_dag_dep.get_node(i).name]

        cost_right = 0
        for j in right:
            cost_right += self.cost_dict[self.template_dag_dep.get_node(j).name]

        return cost_left > cost_right

    def _rules(self, circuit_sublist, template_sublist, template_complement):
        """
       用于决定匹配是否为替换的一组规则。
        Args:
            Circuit _ sublist ( list )：电路中匹配的门列表。
            template _ sublist ( list )：模板中匹配的节点列表。
            template _ complete ( list )：模板中未匹配的门列表。
            返回：bool：如果匹配尊重给定规则进行替换则为true，否则为False。
        """

        if self._quantum_cost(template_sublist, template_complement):
            for elem in circuit_sublist:
                for config in self.substitution_list:
                    if any(elem == x for x in config.circuit_config):
                        return False
            return True
        else:
            return False

    def _template_inverse(self, template_list, template_sublist, template_complement):
        """
        模板电路实现标识运算符，然后给定模板中的匹配列表，它返回将被替换的模板的逆部分。
        Args:
            tEmplate _ list ( list )：模板中所有门的列表。
            template _ sublist ( list )：电路中匹配的门的列表。
            template _ complete ( list )：模板中不匹配的门的列表。
            返回：列表：将替代电路匹配的模板逆序部分。
        """
        inverse = template_complement
        left = []
        right = []

        pred = set()
        for index in template_sublist:
            pred = pred | set(self.template_dag_dep.get_node(index).predecessors)
        pred = list(pred - set(template_sublist))

        succ = set()
        for index in template_sublist:
            succ = succ | set(self.template_dag_dep.get_node(index).successors)
        succ = list(succ - set(template_sublist))

        comm = list(set(template_list) - set(pred) - set(succ))

        for elem in inverse:
            if elem in pred:
                left.append(elem)
            elif elem in succ:
                right.append(elem)
            elif elem in comm:
                right.append(elem)

        left.sort()
        right.sort()

        left.reverse()
        right.reverse()

        total = left + right
        return total

    def _substitution_sort(self):
        """
        对替换列表进行排序。
        """
        ordered = False
        while not ordered:
            ordered = self._permutation()

    def _permutation(self):
        """
        如果第一组在第二组有前辈，则执行两组比赛。
        Returns:
            Bool：如果匹配组的顺序正确，则为True，否则为False。
        """
        for scenario in self.substitution_list:
            predecessors = set()
            for match in scenario.circuit_config:
                predecessors = predecessors | set(self.circuit_dag_dep.get_node(match).predecessors)
            predecessors = predecessors - set(scenario.circuit_config)
            index = self.substitution_list.index(scenario)
            for scenario_b in self.substitution_list[index::]:
                if set(scenario_b.circuit_config) & predecessors:

                    index1 = self.substitution_list.index(scenario)
                    index2 = self.substitution_list.index(scenario_b)

                    scenario_pop = self.substitution_list.pop(index2)
                    self.substitution_list.insert(index1, scenario_pop)
                    return False
        return True

    def _remove_impossible(self):
        """
        删除匹配的组，如果它们在另一个组中都有前辈，则它们不兼容。
        """
        list_predecessors = []
        remove_list = []

        # 首先删除模板中存在参数的任何场景。
        for scenario in self.substitution_list:
            if scenario.has_parameters():
                remove_list.append(scenario)

        # 为每组匹配初始化前件。
        for scenario in self.substitution_list:
            predecessors = set()
            for index in scenario.circuit_config:
                predecessors = predecessors | set(self.circuit_dag_dep.get_node(index).predecessors)
            list_predecessors.append(predecessors)

        # 检查两组匹配是否不相容。
        for scenario_a in self.substitution_list:
            if scenario_a in remove_list:
                continue
            index_a = self.substitution_list.index(scenario_a)
            circuit_a = scenario_a.circuit_config
            for scenario_b in self.substitution_list[index_a + 1 : :]:
                if scenario_b in remove_list:
                    continue
                index_b = self.substitution_list.index(scenario_b)
                circuit_b = scenario_b.circuit_config
                if (set(circuit_a) & list_predecessors[index_b]) and (
                    set(circuit_b) & list_predecessors[index_a]
                ):
                    remove_list.append(scenario_b)

        # 从列表中删除不兼容的组。
        if remove_list:
            self.substitution_list = [
                scenario for scenario in self.substitution_list if scenario not in remove_list
            ]

    def _substitution(self):
        """
        从最大匹配列表中，它选择将使用哪一个，并为每个替换(模板反转,匹配的前身)提供必要的细节。
        """

        while self.match_stack:

            # 获取列表的第一个匹配场景
            current = self.match_stack.pop(0)

            current_match = current.match
            current_qubit = current.qubit
            current_clbit = current.clbit

            template_sublist = [x[0] for x in current_match]
            circuit_sublist = [x[1] for x in current_match]
            circuit_sublist.sort()

            # Fake绑定模板中的任意参数
            template = self._attempt_bind(template_sublist, circuit_sublist)

            if template is None:
                continue

            template_list = range(0, self.template_dag_dep.size())
            template_complement = list(set(template_list) - set(template_sublist))

            # 如果匹配符合规则，则将其添加到列表中。
            if self._rules(circuit_sublist, template_sublist, template_complement):
                template_sublist_inverse = self._template_inverse(
                    template_list, template_sublist, template_complement
                )

                config = SubstitutionConfig(
                    circuit_sublist,
                    template_sublist_inverse,
                    [],
                    current_qubit,
                    template,
                    current_clbit,
                )
                self.substitution_list.append(config)

        # 删除不兼容的匹配项。
        self._remove_impossible()

        # 首先根据匹配(回路)中最小的指标对匹配进行排序。
        self.substitution_list.sort(key=lambda x: x.circuit_config[0])

        # 由于其他组的前身而更改组的位置。
        self._substitution_sort()

        for scenario in self.substitution_list:
            index = self.substitution_list.index(scenario)
            scenario.pred_block = self._pred_block(scenario.circuit_config, index)

        circuit_list = []
        for elem in self.substitution_list:
            circuit_list = circuit_list + elem.circuit_config + elem.pred_block

        # 无与伦比的门不是任何一组匹配的前身。
        self.unmatched_list = sorted(
            list(set(range(0, self.circuit_dag_dep.size())) - set(circuit_list))
        )

    def run_dag_opt(self):
        """
        它运行替换算法并创建优化的DAGCircuit ( )。
        """
        self._substitution()

        dag_dep_opt = DAGDependency()

        dag_dep_opt.name = self.circuit_dag_dep.name

        qregs = list(self.circuit_dag_dep.qregs.values())
        cregs = list(self.circuit_dag_dep.cregs.values())

        for register in qregs:
            dag_dep_opt.add_qreg(register)

        for register in cregs:
            dag_dep_opt.add_creg(register)

        already_sub = []

        if self.substitution_list:
            # 在不同的匹配上循环。
            for group in self.substitution_list:

                circuit_sub = group.circuit_config
                template_inverse = group.template_config

                pred = group.pred_block

                qubit = group.qubit_config[0]

                if group.clbit_config:
                    clbit = group.clbit_config[0]
                else:
                    clbit = []

                # 首先将给定匹配的所有前件相加。
                for elem in pred:
                    node = self.circuit_dag_dep.get_node(elem)
                    inst = node.op.copy()
                    dag_dep_opt.add_op_node(inst, node.qargs, node.cargs)
                    already_sub.append(elem)

                already_sub = already_sub + circuit_sub

                # 然后加入模板的逆。
                for index in template_inverse:
                    all_qubits = self.circuit_dag_dep.qubits
                    qarg_t = group.template_dag_dep.get_node(index).qindices
                    qarg_c = [qubit[x] for x in qarg_t]
                    qargs = [all_qubits[x] for x in qarg_c]

                    all_clbits = self.circuit_dag_dep.clbits
                    carg_t = group.template_dag_dep.get_node(index).cindices

                    if all_clbits and clbit:
                        carg_c = [clbit[x] for x in carg_t]
                        cargs = [all_clbits[x] for x in carg_c]
                    else:
                        cargs = []
                    node = group.template_dag_dep.get_node(index)
                    inst = node.op.copy()

                    dag_dep_opt.add_op_node(inst.inverse(), qargs, cargs)

            # 添加无与伦比的门。
            for node_id in self.unmatched_list:
                node = self.circuit_dag_dep.get_node(node_id)
                inst = node.op.copy()
                dag_dep_opt.add_op_node(inst, node.qargs, node.cargs)

            dag_dep_opt._add_successors()
        # 如果没有有效匹配，则返回原始dag。
        else:
            dag_dep_opt = self.circuit_dag_dep

        self.dag_dep_optimized = dag_dep_opt
        self.dag_optimized = dagdependency_to_dag(dag_dep_opt)

    def _attempt_bind(self, template_sublist, circuit_sublist):
        """
       复制模板并尝试绑定任何参数，即尝试求解有效的参数赋值，template _ sublist和circuit _ sublist匹配到参数的赋值。
       例如模板
        .. parsed-literal::
                 ┌───────────┐                  ┌────────┐
            q_0: ┤ P(-1.0*β) ├──■────────────■──┤0       ├
                 ├───────────┤┌─┴─┐┌──────┐┌─┴─┐│  CZ(β) │
            q_1: ┤ P(-1.0*β) ├┤ X ├┤ P(β) ├┤ X ├┤1       ├
                 └───────────┘└───┘└──────┘└───┘└────────┘
        应该只在电路中最大匹配一次
        .. parsed-literal::
                 ┌───────┐
            q_0: ┤ P(-2) ├──■────────────■────────────────────────────
                 ├───────┤┌─┴─┐┌──────┐┌─┴─┐┌──────┐
            q_1: ┤ P(-2) ├┤ X ├┤ P(2) ├┤ X ├┤ P(3) ├──■────────────■──
                 └┬──────┤└───┘└──────┘└───┘└──────┘┌─┴─┐┌──────┐┌─┴─┐
            q_2: ─┤ P(3) ├──────────────────────────┤ X ├┤ P(3) ├┤ X ├
                  └──────┘                          └───┘└──────┘└───┘
        然而，直到尝试绑定被调用时，软匹配将由于参数而找到两个匹配。
        第一次匹配可以满足β = 2。然而，第二次匹配将意味着β = 3和β = -3，这是不可能的。
        Attempt bind通过求解由子模板中的参数表达式和子电路门中参数的值给出的方程组来检测不一致。
        如果找到一个解决方案，那么匹配是有效的，并分配参数。如果没有，则不返回。
        Args:
            template_sublist (list): part of the matched template.
            circuit_sublist (list): part of the matched circuit.
        Returns:
           DAGDependency：绑定参数的模板的深度副本。如果没有绑定满足参数约束，则返回None。
        """
        import sympy as sym
        from sympy.parsing.sympy_parser import parse_expr

        circuit_params, template_params = [], []

        template_dag_dep = copy.deepcopy(self.template_dag_dep)

        for idx, t_idx in enumerate(template_sublist):
            qc_idx = circuit_sublist[idx]
            circuit_params += self.circuit_dag_dep.get_node(qc_idx).op.params
            template_params += template_dag_dep.get_node(t_idx).op.params

        # 创建假绑定命令并检查
        equations, symbols, sol, fake_bind = [], set(), {}, {}
        for t_idx, params in enumerate(template_params):
            if isinstance(params, ParameterExpression):
                equations.append(sym.Eq(parse_expr(str(params)), circuit_params[t_idx]))
                for param in params.parameters:
                    symbols.add(param)

        if not symbols:
            return template_dag_dep

        # 通过求解结果方程检查兼容性
        sym_sol = sym.solve(equations)
        for key in sym_sol:
            try:
                sol[str(key)] = float(sym_sol[key])
            except TypeError:
                return None

        if not sol:
            return None

        for param in symbols:
            fake_bind[param] = sol[str(param)]

        for node in template_dag_dep.get_nodes():
            bound_params = []

            for param in node.op.params:
                if isinstance(param, ParameterExpression):
                    try:
                        bound_params.append(float(param.bind(fake_bind)))
                    except KeyError:
                        return None
                else:
                    bound_params.append(param)

            node.op.params = bound_params

        return template_dag_dep