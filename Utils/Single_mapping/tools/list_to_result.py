from qiskit import QuantumCircuit

def quantum_cir(cir:list,n):
    circ = QuantumCircuit(n)
    meas = QuantumCircuit(n,n)
    for i in cir:
        if isinstance(i[0],str):
            if i[0]=='h':
                circ.h(i[1])
            elif i[0]=='tdg':
                circ.tdg(i[1])
            elif i[0]=='s':
                circ.s(i[1])
            elif i[0]=='t':
                circ.t(i[1])
            elif i[0] == 'x':
                circ.x(i[1])
        else:
            circ.h(i[1])
            circ.cz(i[1],i[0])
            circ.h(i[1])
    return circ

# if __name__ == '__main__':
#     List = [[32, 25], [25, 32], [32, 26], [26, 21],['t', 26], [21, 26], ['tdg', 26], [32, 26], ['t', 26], ['h', 26],
#             ['t', 21], [32, 21], ['t', 32], ['x', 32], ['tdg', 21], [32, 21], ['x', 20], ['h', 20], [26, 20],
#             ['h', 16], ['t', 11], [22, 11], ['t', 22], ['x', 22], ['tdg', 11], [22, 11], ['x', 10], ['h', 10], [16, 10],
#             ['tdg', 10], [4, 10], ['t', 10], [16, 10], ['t', 16], ['tdg', 10], [4, 10], ['t', 10], ['h', 10], [4, 16],
#             ['tdg', 16], ['t', 4], [4, 16], [10, 3]]
#     cir = quantum_cir(List,67)
#     print(cir)