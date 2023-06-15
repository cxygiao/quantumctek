from quantumctek.quantumctek.Utils.Decomposition_and_optimization.template_optimization import TemplateOptimization
from qiskit import QuantumCircuit
from qiskit.circuit.library import CCXGate
from quantumctek.quantumctek.Utils.Decomposition_and_optimization.template import (template_1,template_2,template_3,template_4,
template_5,template_14,template_15,template_16,template_17,template_18,template_19,template_20)
from quantumctek.quantumctek.Utils.Decomposition_and_optimization.cxtoxz.cx_to_cz import cx_to_cz
from qiskit.converters.circuit_to_dag import circuit_to_dag
from qiskit.converters.dag_to_circuit import dag_to_circuit
import matplotlib.pyplot as plt

#读取QASM文件
circuit = QuantumCircuit.from_qasm_file('E:/qiskit/quantumctek/quantumctek/Utils/Decomposition_and_optimization/test/test.qasm')
print(circuit.size())

#CCX门分解为Clifford门库
fj = circuit.decompose(CCXGate)
print(fj.size())

#将线路转换为DAG
dag = circuit_to_dag(fj)
#可以根据情况在模板库template中选择不同的模板
topt = TemplateOptimization(template_list=[template_2(),template_3(),template_14(),
                                           template_15(),template_16()])
#模板匹配优化
optdag = topt.run(dag)
#优化后DAG转换为线路
optc = dag_to_circuit(optdag)
print(optc.size())

#分解cx门为cz门
fjcz = cx_to_cz(optc)
print(fjcz.size())

dag1 = circuit_to_dag(fjcz)
topt1 = TemplateOptimization(template_list=[template_1(),template_3(),template_16(),
                                            template_17(),template_19(),template_20()])
optdag1 = topt1.run(dag1)
optc1 = dag_to_circuit(optdag1)
print(optc1.size())

#保存到文件
# qasm = optc.qasm()
#
# with open('3z4fj_czopt.qasm', 'w') as f:
#   f.write(qasm)