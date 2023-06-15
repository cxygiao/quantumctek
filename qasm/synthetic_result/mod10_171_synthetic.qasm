OPENQASM 2.0;
include "qelib1.inc";
qreg q[66];
creg c[66];
cx q[25],q[19];
measure q[25] -> c[25];
measure q[19] -> c[19];