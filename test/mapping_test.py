from ezQpy import *

# login_key在 https://www.quantumcomputer.ac.cn/User  下的SDK密钥
account = Account(login_key='156c0c94fb2e6faaea15bae44ec03646', machine_name='ClosedBetaQC')

qcis_circuit = '''
H Q7
X Q1
H Q1
CZ Q7 Q2
H Q1
M Q7
M Q1
'''

qcis_circuit = account.qcis_mapping_isq(qcis_circuit)

print(qcis_circuit)