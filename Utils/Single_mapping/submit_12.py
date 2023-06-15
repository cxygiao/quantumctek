from ezQpy import *

username = 'qyyyyy'
password = 'wynl021002'
account = Account(username, password)

qcis_circuit = '''
H Q1
X Q1
H Q1
CZ Q1 Q2
H Q2
M Q1
M Q2
'''

query_id = account.submit_job(qcis_circuit, exp_name='GHz')

if query_id:
    result = account.query_experiment(query_id, max_wait_time=360000)
    print(result)