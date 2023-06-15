import numpy as np

from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.dagcircuit import DAGDependency
from qiskit.converters.circuit_to_dagdependency import circuit_to_dagdependency
from qiskit.converters.dagdependency_to_circuit import dagdependency_to_circuit
from qiskit.converters.dag_to_dagdependency import dag_to_dagdependency
from qiskit.converters.dagdependency_to_dag import dagdependency_to_dag
from qiskit.transpiler.basepasses import TransformationPass
from qiskit.circuit.library.templates import template_nct_2a_1, template_nct_2a_2, template_nct_2a_3
from qiskit.quantum_info.operators.operator import Operator
from qiskit.transpiler.exceptions import TranspilerError
from quantumctek.quantumctek.Utils.Decomposition_and_optimization.template_substitution import TemplateSubstitution
from quantumctek.quantumctek.Utils.Decomposition_and_optimization.template_matching import TemplateMatching
from quantumctek.quantumctek.Utils.Decomposition_and_optimization.maximal_matches import MaximalMatches


class TemplateOptimization(TransformationPass):
    """
    Class for the template optimization pass.
    """

    def __init__(
        self,
        template_list=None,
        heuristics_qubits_param=None,
        heuristics_backward_param=None,
        user_cost_dict=None,
    ):
        super().__init__()
        # If no template is given; the template are set as x-x, cx-cx, ccx-ccx.
        if template_list is None:
            template_list = [template_nct_2a_1(), template_nct_2a_2(), template_nct_2a_3()]

        self.template_list = template_list
        self.heuristics_qubits_param = (
            heuristics_qubits_param if heuristics_qubits_param is not None else []
        )
        self.heuristics_backward_param = (
            heuristics_backward_param if heuristics_backward_param is not None else []
        )

        self.user_cost_dict = user_cost_dict

    def run(self, dag):
        """
        Args:
            dag(DAGCircuit): DAG circuit.
        Returns:
            DAGCircuit: optimized DAG circuit.
        Raises:
            TranspilerError: If the template has not the right form or
             if the output circuit acts differently as the input circuit.
        """
        circuit_dag = dag
        circuit_dag_dep = dag_to_dagdependency(circuit_dag)

        for template in self.template_list:
            if not isinstance(template, (QuantumCircuit, DAGDependency)):
                raise TranspilerError("A template is a Quantumciruit or a DAGDependency.")

            if len(template.qubits) > len(circuit_dag_dep.qubits):
                continue

            identity = np.identity(2 ** len(template.qubits), dtype=complex)
            try:
                if isinstance(template, DAGDependency):
                    data = Operator(dagdependency_to_circuit(template)).data
                else:
                    data = Operator(template).data

                comparison = np.allclose(data, identity)

                if not comparison:
                    raise TranspilerError(
                        "A template is a Quantumciruit() that performs the identity."
                    )
            except TypeError:
                pass

            if isinstance(template, QuantumCircuit):
                template_dag_dep = circuit_to_dagdependency(template)
            else:
                template_dag_dep = template

            template_m = TemplateMatching(
                circuit_dag_dep,
                template_dag_dep,
                self.heuristics_qubits_param,
                self.heuristics_backward_param,
            )

            template_m.run_template_matching()

            matches = template_m.match_list

            if matches:
                maximal = MaximalMatches(matches)
                maximal.run_maximal_matches()
                max_matches = maximal.max_match_list

                substitution = TemplateSubstitution(
                    max_matches,
                    template_m.circuit_dag_dep,
                    template_m.template_dag_dep,
                    self.user_cost_dict,
                )
                substitution.run_dag_opt()

                circuit_dag_dep = substitution.dag_dep_optimized
            else:
                continue
        circuit_dag = dagdependency_to_dag(circuit_dag_dep)
        return circuit_dag
