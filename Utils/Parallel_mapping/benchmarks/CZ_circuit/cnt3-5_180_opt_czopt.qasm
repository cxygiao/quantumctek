OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
creg c[16];
h q[0];
t q[0];
t q[1];
h q[2];
t q[2];
h q[3];
t q[3];
t q[4];
h q[5];
t q[5];
h q[6];
t q[6];
t q[7];
h q[8];
t q[8];
h q[9];
t q[9];
t q[10];
t q[11];
h q[12];
t q[12];
t q[13];
h q[13];
t q[14];
cz q[13],q[14];
h q[13];
h q[14];
h q[15];
t q[15];
cz q[14],q[15];
h q[14];
tdg q[14];
h q[14];
h q[15];
cz q[15],q[13];
cz q[14],q[13];
h q[14];
tdg q[14];
h q[14];
h q[15];
t q[15];
cz q[14],q[15];
h q[14];
h q[15];
cz q[15],q[13];
tdg q[13];
h q[13];
cz q[13],q[14];
h q[13];
t q[13];
h q[13];
cz q[13],q[11];
h q[11];
cz q[11],q[12];
h q[11];
tdg q[11];
h q[11];
h q[12];
h q[13];
cz q[12],q[13];
cz q[11],q[13];
h q[11];
tdg q[11];
h q[11];
h q[12];
t q[12];
cz q[11],q[12];
h q[11];
h q[12];
cz q[12],q[13];
h q[12];
t q[12];
tdg q[13];
h q[13];
cz q[13],q[11];
h q[11];
t q[11];
h q[13];
t q[13];
h q[13];
t q[14];
t q[15];
h q[15];
cz q[15],q[14];
h q[14];
cz q[14],q[11];
h q[11];
h q[14];
tdg q[14];
h q[14];
h q[15];
cz q[11],q[15];
h q[11];
t q[11];
cz q[14],q[15];
h q[14];
tdg q[14];
h q[14];
cz q[14],q[11];
h q[11];
cz q[11],q[15];
t q[11];
cz q[13],q[11];
h q[11];
cz q[11],q[12];
h q[11];
tdg q[11];
h q[11];
h q[12];
h q[13];
cz q[12],q[13];
cz q[11],q[13];
h q[11];
tdg q[11];
h q[11];
h q[12];
t q[12];
cz q[11],q[12];
h q[11];
h q[12];
cz q[12],q[13];
t q[12];
h q[12];
cz q[12],q[10];
h q[10];
h q[12];
tdg q[13];
h q[13];
cz q[13],q[11];
h q[11];
t q[11];
h q[13];
t q[13];
h q[14];
tdg q[15];
h q[15];
cz q[15],q[14];
t q[14];
h q[15];
t q[15];
h q[15];
cz q[15],q[14];
h q[14];
cz q[14],q[11];
h q[11];
h q[14];
tdg q[14];
h q[14];
h q[15];
cz q[11],q[15];
h q[11];
t q[11];
cz q[14],q[15];
h q[14];
tdg q[14];
h q[14];
cz q[14],q[11];
h q[11];
cz q[11],q[15];
h q[11];
t q[11];
cz q[10],q[11];
h q[10];
tdg q[10];
h q[10];
h q[11];
cz q[11],q[12];
cz q[10],q[12];
h q[10];
tdg q[10];
h q[10];
h q[11];
t q[11];
cz q[10],q[11];
h q[10];
h q[11];
cz q[11],q[12];
t q[11];
h q[11];
tdg q[12];
h q[12];
cz q[12],q[10];
t q[10];
cz q[11],q[10];
h q[10];
h q[11];
h q[12];
t q[12];
h q[12];
h q[14];
tdg q[15];
h q[15];
cz q[15],q[14];
h q[14];
t q[14];
h q[15];
t q[15];
h q[15];
cz q[15],q[13];
h q[13];
cz q[13],q[14];
h q[13];
tdg q[13];
h q[13];
h q[14];
h q[15];
cz q[14],q[15];
cz q[13],q[15];
h q[13];
tdg q[13];
h q[13];
h q[14];
t q[14];
cz q[13],q[14];
h q[13];
h q[14];
cz q[14],q[15];
tdg q[15];
t q[15];
cz q[12],q[15];
h q[12];
h q[15];
cz q[15],q[9];
h q[15];
tdg q[15];
h q[15];
h q[9];
cz q[9],q[12];
cz q[15],q[12];
h q[15];
tdg q[15];
h q[15];
h q[9];
t q[9];
cz q[15],q[9];
h q[15];
h q[9];
cz q[9],q[12];
tdg q[12];
h q[12];
cz q[12],q[15];
h q[12];
t q[12];
h q[12];
h q[15];
t q[15];
cz q[10],q[15];
h q[10];
tdg q[10];
h q[10];
h q[15];
cz q[15],q[11];
cz q[10],q[11];
h q[10];
tdg q[10];
h q[10];
h q[15];
t q[15];
cz q[10],q[15];
h q[10];
h q[15];
cz q[15],q[11];
tdg q[11];
h q[11];
cz q[11],q[10];
t q[10];
h q[11];
t q[11];
h q[11];
cz q[11],q[10];
h q[10];
h q[11];
t q[15];
cz q[12],q[15];
h q[12];
h q[15];
h q[9];
t q[9];
cz q[15],q[9];
h q[15];
tdg q[15];
h q[15];
h q[9];
cz q[9],q[12];
cz q[15],q[12];
tdg q[12];
h q[15];
tdg q[15];
h q[15];
h q[9];
t q[9];
cz q[15],q[9];
h q[15];
h q[9];
cz q[9],q[12];
h q[12];
cz q[12],q[15];
h q[12];
t q[12];
h q[15];
t q[15];
cz q[10],q[15];
h q[10];
tdg q[10];
h q[10];
h q[15];
cz q[15],q[11];
cz q[10],q[11];
h q[10];
tdg q[10];
h q[10];
h q[15];
t q[15];
cz q[10],q[15];
h q[10];
h q[15];
cz q[15],q[11];
tdg q[11];
h q[11];
cz q[11],q[10];
h q[10];
t q[10];
h q[11];
t q[11];
h q[11];
cz q[11],q[12];
h q[11];
h q[12];
cz q[12],q[10];
h q[10];
cz q[10],q[11];
h q[10];
t q[10];
h q[12];
tdg q[12];
h q[12];
cz q[12],q[11];
h q[12];
tdg q[12];
h q[12];
cz q[12],q[10];
h q[10];
cz q[10],q[11];
tdg q[11];
h q[12];
t q[15];
t q[9];
h q[9];
cz q[9],q[7];
h q[7];
cz q[7],q[8];
h q[7];
tdg q[7];
h q[7];
h q[8];
h q[9];
cz q[8],q[9];
cz q[7],q[9];
h q[7];
tdg q[7];
h q[7];
h q[8];
t q[8];
cz q[7],q[8];
h q[7];
h q[8];
cz q[8],q[9];
t q[8];
h q[8];
tdg q[9];
h q[9];
cz q[9],q[7];
t q[7];
cz q[8],q[7];
h q[7];
h q[8];
h q[9];
t q[9];
h q[9];
cz q[9],q[15];
h q[15];
cz q[15],q[6];
h q[15];
tdg q[15];
h q[15];
h q[6];
h q[9];
cz q[6],q[9];
cz q[15],q[9];
h q[15];
tdg q[15];
h q[15];
h q[6];
t q[6];
cz q[15],q[6];
h q[15];
h q[6];
cz q[6],q[9];
h q[6];
t q[6];
tdg q[9];
h q[9];
cz q[9],q[15];
h q[15];
t q[15];
cz q[7],q[15];
h q[15];
cz q[15],q[8];
h q[15];
t q[15];
h q[7];
tdg q[7];
h q[7];
cz q[7],q[8];
h q[7];
tdg q[7];
h q[7];
cz q[7],q[15];
h q[15];
cz q[15],q[8];
t q[15];
h q[7];
tdg q[8];
h q[8];
cz q[8],q[7];
t q[7];
h q[8];
t q[8];
h q[8];
cz q[8],q[7];
h q[7];
h q[8];
h q[9];
t q[9];
h q[9];
cz q[9],q[15];
h q[15];
cz q[15],q[6];
h q[15];
tdg q[15];
h q[15];
h q[6];
h q[9];
cz q[6],q[9];
cz q[15],q[9];
h q[15];
tdg q[15];
h q[15];
h q[6];
t q[6];
cz q[15],q[6];
h q[15];
h q[6];
cz q[6],q[9];
t q[6];
h q[6];
cz q[6],q[4];
h q[4];
cz q[4],q[5];
h q[4];
tdg q[4];
h q[4];
h q[5];
h q[6];
cz q[5],q[6];
cz q[4],q[6];
h q[4];
tdg q[4];
h q[4];
h q[5];
t q[5];
cz q[4],q[5];
h q[4];
h q[5];
cz q[5],q[6];
t q[5];
h q[5];
tdg q[6];
h q[6];
cz q[6],q[4];
t q[4];
cz q[5],q[4];
h q[4];
h q[5];
h q[6];
t q[6];
h q[6];
tdg q[9];
h q[9];
cz q[9],q[15];
h q[15];
t q[15];
cz q[7],q[15];
h q[15];
cz q[15],q[8];
h q[15];
t q[15];
h q[7];
tdg q[7];
h q[7];
cz q[7],q[8];
h q[7];
tdg q[7];
h q[7];
cz q[7],q[15];
h q[15];
cz q[15],q[8];
t q[15];
cz q[6],q[15];
h q[15];
cz q[15],q[3];
h q[15];
tdg q[15];
h q[15];
h q[3];
h q[6];
cz q[3],q[6];
cz q[15],q[6];
h q[15];
tdg q[15];
h q[15];
h q[3];
t q[3];
cz q[15],q[3];
h q[15];
h q[3];
cz q[3],q[6];
h q[3];
t q[3];
tdg q[6];
h q[6];
cz q[6],q[15];
h q[15];
t q[15];
cz q[4],q[15];
h q[15];
cz q[15],q[5];
h q[15];
t q[15];
h q[4];
tdg q[4];
h q[4];
cz q[4],q[5];
h q[4];
tdg q[4];
h q[4];
cz q[4],q[15];
h q[15];
cz q[15],q[5];
t q[15];
h q[4];
tdg q[5];
h q[5];
cz q[5],q[4];
t q[4];
h q[5];
t q[5];
h q[5];
cz q[5],q[4];
h q[4];
h q[5];
h q[6];
t q[6];
h q[6];
cz q[6],q[15];
h q[15];
cz q[15],q[3];
h q[15];
tdg q[15];
h q[15];
h q[3];
h q[6];
cz q[3],q[6];
cz q[15],q[6];
h q[15];
tdg q[15];
h q[15];
h q[3];
t q[3];
cz q[15],q[3];
h q[15];
h q[3];
cz q[3],q[6];
t q[3];
h q[3];
cz q[3],q[1];
h q[1];
cz q[1],q[2];
h q[1];
tdg q[1];
h q[1];
h q[2];
h q[3];
cz q[2],q[3];
cz q[1],q[3];
h q[1];
tdg q[1];
h q[1];
h q[2];
t q[2];
cz q[1],q[2];
h q[1];
h q[2];
cz q[2],q[3];
t q[2];
h q[2];
tdg q[3];
h q[3];
cz q[3],q[1];
t q[1];
cz q[2],q[1];
h q[1];
h q[2];
h q[3];
t q[3];
h q[3];
tdg q[6];
h q[6];
cz q[6],q[15];
h q[15];
t q[15];
cz q[4],q[15];
h q[15];
cz q[15],q[5];
h q[15];
t q[15];
h q[4];
tdg q[4];
h q[4];
cz q[4],q[5];
h q[4];
tdg q[4];
h q[4];
cz q[4],q[15];
h q[15];
cz q[15],q[5];
t q[15];
cz q[3],q[15];
h q[15];
cz q[15],q[0];
h q[0];
h q[15];
tdg q[15];
h q[15];
h q[3];
cz q[0],q[3];
h q[0];
t q[0];
cz q[15],q[3];
h q[15];
tdg q[15];
h q[15];
cz q[15],q[0];
h q[0];
cz q[0],q[3];
h q[0];
t q[0];
h q[15];
tdg q[3];
h q[3];
cz q[3],q[15];
h q[15];
t q[15];
cz q[1],q[15];
h q[1];
tdg q[1];
h q[1];
h q[15];
cz q[15],q[2];
cz q[1],q[2];
h q[1];
tdg q[1];
h q[1];
h q[15];
t q[15];
cz q[1],q[15];
h q[1];
h q[15];
cz q[15],q[2];
t q[15];
tdg q[2];
h q[2];
cz q[2],q[1];
t q[1];
h q[2];
t q[2];
h q[2];
cz q[2],q[1];
h q[1];
h q[2];
h q[3];
t q[3];
h q[3];
cz q[3],q[15];
h q[15];
cz q[15],q[0];
h q[0];
h q[15];
tdg q[15];
h q[15];
h q[3];
cz q[0],q[3];
h q[0];
t q[0];
cz q[15],q[3];
h q[15];
tdg q[15];
h q[15];
cz q[15],q[0];
h q[0];
cz q[0],q[3];
h q[15];
tdg q[3];
h q[3];
cz q[3],q[15];
h q[15];
t q[15];
cz q[1],q[15];
h q[1];
tdg q[1];
h q[1];
h q[15];
cz q[15],q[2];
cz q[1],q[2];
h q[1];
tdg q[1];
h q[1];
h q[15];
t q[15];
cz q[1],q[15];
h q[1];
h q[15];
cz q[15],q[2];
tdg q[2];
h q[2];
cz q[2],q[1];
h q[1];
t q[1];
h q[2];
t q[2];
h q[2];
h q[3];
t q[3];
cz q[2],q[3];
h q[2];
h q[3];
cz q[3],q[1];
h q[1];
cz q[1],q[2];
h q[1];
t q[1];
h q[3];
tdg q[3];
h q[3];
cz q[3],q[2];
h q[3];
tdg q[3];
h q[3];
cz q[3],q[1];
h q[1];
cz q[1],q[2];
tdg q[2];
h q[3];
h q[4];
tdg q[5];
h q[5];
cz q[5],q[4];
h q[4];
t q[4];
h q[5];
t q[5];
h q[5];
h q[6];
t q[6];
cz q[5],q[6];
h q[5];
h q[6];
cz q[6],q[4];
h q[4];
cz q[4],q[5];
h q[4];
t q[4];
h q[6];
tdg q[6];
h q[6];
cz q[6],q[5];
h q[6];
tdg q[6];
h q[6];
cz q[6],q[4];
h q[4];
cz q[4],q[5];
tdg q[5];
h q[6];
h q[7];
tdg q[8];
h q[8];
cz q[8],q[7];
h q[7];
t q[7];
h q[8];
t q[8];
h q[8];
h q[9];
t q[9];
cz q[8],q[9];
h q[8];
h q[9];
cz q[9],q[7];
h q[7];
cz q[7],q[8];
h q[7];
t q[7];
h q[9];
tdg q[9];
h q[9];
cz q[9],q[8];
h q[9];
tdg q[9];
h q[9];
cz q[9],q[7];
h q[7];
cz q[7],q[8];
tdg q[8];
h q[9];
