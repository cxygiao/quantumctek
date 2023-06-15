from test.quafu import User
from test.quafu import QuantumCircuit



user = User()
user.save_apitoken("UKb_2I-TorsAegpRAuqhKAq4CN5m-J_xTbMGKTkGe7T.QfycDMzQzNxgjNxojIwhXZiwCO1cTM6ICZpJye.9JiN1IzUIJiOicGbhJCLiQ1VKJiOiAXe0Jye")

qc = QuantumCircuit(4)
test_ghz = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
h q[0];
cx q[0],q[1];
cx q[0],q[2];
cx q[0],q[3];
"""
qc.from_openqasm(test_ghz)
qc.draw_circuit()
