OPENQASM 2.0;
include "qelib1.inc";
qreg q[66];
creg c[66];
cx q[31],q[25];
cx q[25],q[19];
cx q[19],q[13];
cx q[13],q[20];
cx q[25],q[31];
cx q[19],q[25];
cx q[13],q[19];
cx q[20],q[13];
cx q[13],q[20];
cx q[31],q[25];
cx q[25],q[19];
cx q[19],q[13];
cx q[13],q[20];
cx q[19],q[13];
cx q[25],q[19];
cx q[31],q[25];

measure q[13] -> c[13];
measure q[19] -> c[19];
measure q[20] -> c[20];
measure q[25] -> c[25];
measure q[31] -> c[31];

