from ezQpy import *

username = "cxygiao"
password = "cxc112233"
account = Account(username, password)

qcis_circuit = ''' 
H Q1 
H Q2 
CZ Q1 Q2
H Q2 
H Q3 
CZ Q2 Q3
H Q3 
M Q1 
M Q2 
M Q3 
'''

query_id = account.submit_job(qcis_circuit, exp_name='GHz')

if query_id:
    result = account.query_experiment(query_id, max_wait_time=360000)
    print(result)
    value = result['000']
    print(value)
    f = open("results.txt", 'w')
    f.write(str(value))
    f.close()