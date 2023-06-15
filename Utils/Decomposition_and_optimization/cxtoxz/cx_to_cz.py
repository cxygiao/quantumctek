from qiskit import QuantumCircuit

#将cx门分解为cz门

def cx_to_cz(circuit:QuantumCircuit):
  new_circ = QuantumCircuit(*circuit.qregs)
  for instr,qargs,cargs in circuit.data:
    if instr.name == 'cx':
      new_circ.h(qargs[1])
      new_circ.cz(qargs[1],qargs[0])
      new_circ.h(qargs[1])
    else:
      new_circ.append(instr,qargs,cargs)
  return new_circ