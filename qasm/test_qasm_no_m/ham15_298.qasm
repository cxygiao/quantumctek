OPENQASM 2.0;
include "qelib1.inc";
qreg q[45];
cx q[13],q[15];
cx q[2],q[15];
cx q[14],q[16];
cx q[2],q[16];
h q[16];
cx q[15],q[16];
tdg q[16];
cx q[14],q[16];
t q[16];
cx q[15],q[16];
t q[15];
tdg q[16];
cx q[14],q[16];
cx q[14],q[15];
t q[14];
tdg q[15];
cx q[14],q[15];
t q[16];
h q[16];
h q[16];
cx q[14],q[16];
tdg q[16];
cx q[2],q[16];
t q[16];
cx q[14],q[16];
t q[14];
tdg q[16];
cx q[2],q[16];
t q[16];
h q[16];
cx q[2],q[14];
tdg q[14];
t q[2];
cx q[2],q[14];
cx q[12],q[17];
cx q[2],q[17];
h q[17];
cx q[16],q[17];
tdg q[17];
cx q[12],q[17];
t q[17];
cx q[16],q[17];
t q[16];
tdg q[17];
cx q[12],q[17];
cx q[12],q[16];
t q[12];
tdg q[16];
cx q[12],q[16];
t q[17];
h q[17];
h q[17];
cx q[12],q[17];
tdg q[17];
cx q[2],q[17];
t q[17];
cx q[12],q[17];
t q[12];
tdg q[17];
cx q[2],q[17];
t q[17];
h q[17];
cx q[2],q[12];
tdg q[12];
t q[2];
cx q[2],q[12];
cx q[11],q[18];
cx q[2],q[18];
h q[18];
cx q[17],q[18];
tdg q[18];
cx q[11],q[18];
t q[18];
cx q[17],q[18];
t q[17];
tdg q[18];
cx q[11],q[18];
cx q[11],q[17];
t q[11];
tdg q[17];
cx q[11],q[17];
t q[18];
h q[18];
h q[18];
cx q[11],q[18];
tdg q[18];
cx q[2],q[18];
t q[18];
cx q[11],q[18];
t q[11];
tdg q[18];
cx q[2],q[18];
t q[18];
h q[18];
cx q[2],q[11];
tdg q[11];
t q[2];
cx q[2],q[11];
cx q[8],q[18];
x q[18];
cx q[5],q[18];
x q[18];
cx q[0],q[18];
x q[18];
cx q[7],q[18];
x q[18];
cx q[3],q[18];
x q[18];
cx q[1],q[18];
x q[18];
x q[18];
cx q[11],q[19];
cx q[17],q[19];
h q[19];
cx q[11],q[19];
tdg q[19];
cx q[2],q[19];
t q[19];
cx q[11],q[19];
t q[11];
tdg q[19];
cx q[2],q[19];
t q[19];
h q[19];
h q[19];
cx q[17],q[19];
tdg q[19];
cx q[2],q[11];
tdg q[11];
t q[2];
cx q[2],q[11];
cx q[11],q[19];
t q[19];
cx q[17],q[19];
t q[17];
tdg q[19];
cx q[11],q[19];
cx q[11],q[17];
t q[11];
tdg q[17];
cx q[11],q[17];
t q[19];
h q[19];
cx q[9],q[19];
x q[19];
cx q[8],q[19];
x q[19];
cx q[6],q[19];
x q[19];
cx q[4],q[19];
x q[19];
cx q[3],q[19];
x q[19];
cx q[1],q[19];
x q[19];
cx q[12],q[20];
cx q[16],q[20];
h q[20];
cx q[12],q[20];
tdg q[20];
cx q[2],q[20];
t q[20];
cx q[12],q[20];
t q[12];
tdg q[20];
cx q[2],q[20];
cx q[2],q[12];
tdg q[12];
t q[2];
cx q[2],q[12];
t q[20];
h q[20];
h q[20];
cx q[16],q[20];
tdg q[20];
cx q[12],q[20];
t q[20];
cx q[16],q[20];
t q[16];
tdg q[20];
cx q[12],q[20];
cx q[12],q[16];
t q[12];
tdg q[16];
cx q[12],q[16];
t q[20];
h q[20];
cx q[2],q[21];
h q[21];
cx q[20],q[21];
tdg q[21];
cx q[11],q[21];
t q[21];
cx q[20],q[21];
t q[20];
tdg q[21];
cx q[11],q[21];
cx q[11],q[20];
t q[11];
tdg q[20];
cx q[11],q[20];
t q[21];
h q[21];
h q[21];
cx q[11],q[21];
tdg q[21];
cx q[2],q[21];
t q[21];
cx q[11],q[21];
t q[11];
tdg q[21];
cx q[2],q[21];
cx q[2],q[11];
tdg q[11];
t q[2];
cx q[2],q[11];
t q[21];
h q[21];
cx q[9],q[21];
x q[21];
cx q[5],q[21];
x q[21];
cx q[7],q[21];
x q[21];
cx q[4],q[21];
x q[21];
cx q[3],q[21];
x q[21];
cx q[10],q[21];
x q[21];
cx q[20],q[22];
h q[22];
cx q[11],q[22];
tdg q[22];
cx q[2],q[22];
t q[22];
cx q[11],q[22];
t q[11];
tdg q[22];
cx q[2],q[22];
cx q[2],q[11];
tdg q[11];
t q[2];
cx q[2],q[11];
t q[22];
h q[22];
h q[22];
cx q[20],q[22];
tdg q[22];
cx q[11],q[22];
t q[22];
cx q[20],q[22];
t q[20];
tdg q[22];
cx q[11],q[22];
cx q[11],q[20];
t q[11];
tdg q[20];
cx q[11],q[20];
t q[22];
h q[22];
cx q[6],q[22];
x q[22];
cx q[0],q[22];
x q[22];
cx q[7],q[22];
x q[22];
cx q[4],q[22];
x q[22];
cx q[1],q[22];
x q[22];
cx q[10],q[22];
x q[22];
h q[23];
cx q[14],q[23];
tdg q[23];
cx q[13],q[23];
t q[23];
cx q[14],q[23];
t q[14];
tdg q[23];
cx q[13],q[23];
cx q[13],q[14];
t q[13];
tdg q[14];
cx q[13],q[14];
t q[23];
h q[23];
cx q[14],q[23];
h q[24];
cx q[23],q[24];
tdg q[24];
cx q[12],q[24];
t q[24];
cx q[23],q[24];
t q[23];
tdg q[24];
cx q[12],q[24];
cx q[12],q[23];
t q[12];
tdg q[23];
cx q[12],q[23];
t q[24];
h q[24];
cx q[12],q[24];
h q[25];
cx q[24],q[25];
tdg q[25];
cx q[11],q[25];
t q[25];
cx q[24],q[25];
t q[24];
tdg q[25];
cx q[11],q[25];
cx q[11],q[24];
t q[11];
tdg q[24];
cx q[11],q[24];
t q[25];
h q[25];
cx q[11],q[25];
cx q[0],q[25];
x q[25];
cx q[11],q[26];
h q[26];
cx q[24],q[26];
tdg q[26];
cx q[11],q[26];
t q[26];
cx q[24],q[26];
t q[24];
tdg q[26];
cx q[11],q[26];
cx q[11],q[24];
t q[11];
tdg q[24];
cx q[11],q[24];
t q[26];
h q[26];
cx q[24],q[26];
cx q[1],q[26];
x q[26];
cx q[2],q[27];
h q[27];
cx q[15],q[27];
tdg q[27];
cx q[14],q[27];
t q[27];
cx q[15],q[27];
t q[15];
tdg q[27];
cx q[14],q[27];
cx q[14],q[15];
t q[14];
tdg q[15];
cx q[14],q[15];
t q[27];
h q[27];
h q[27];
cx q[14],q[27];
tdg q[27];
cx q[2],q[27];
t q[27];
cx q[14],q[27];
t q[14];
tdg q[27];
cx q[2],q[27];
cx q[2],q[14];
tdg q[14];
t q[2];
cx q[2],q[14];
t q[27];
h q[27];
cx q[27],q[28];
h q[28];
cx q[12],q[28];
tdg q[28];
cx q[2],q[28];
t q[28];
cx q[12],q[28];
t q[12];
tdg q[28];
cx q[2],q[28];
cx q[2],q[12];
tdg q[12];
t q[2];
cx q[2],q[12];
t q[28];
h q[28];
h q[28];
cx q[27],q[28];
tdg q[28];
cx q[12],q[28];
t q[28];
cx q[27],q[28];
t q[27];
tdg q[28];
cx q[12],q[28];
cx q[12],q[27];
t q[12];
tdg q[27];
cx q[12],q[27];
t q[28];
h q[28];
cx q[2],q[29];
h q[29];
cx q[28],q[29];
tdg q[29];
cx q[11],q[29];
t q[29];
cx q[28],q[29];
t q[28];
tdg q[29];
cx q[11],q[29];
cx q[11],q[28];
t q[11];
tdg q[28];
cx q[11],q[28];
t q[29];
h q[29];
h q[29];
cx q[11],q[29];
tdg q[29];
cx q[2],q[29];
t q[29];
cx q[11],q[29];
t q[11];
tdg q[29];
cx q[2],q[29];
cx q[2],q[11];
tdg q[11];
t q[2];
cx q[2],q[11];
t q[29];
h q[29];
cx q[12],q[30];
h q[30];
cx q[23],q[30];
tdg q[30];
cx q[12],q[30];
t q[30];
cx q[23],q[30];
t q[23];
tdg q[30];
cx q[12],q[30];
cx q[12],q[23];
t q[12];
tdg q[23];
cx q[12],q[23];
t q[30];
h q[30];
cx q[23],q[30];
cx q[11],q[31];
h q[31];
cx q[30],q[31];
tdg q[31];
cx q[11],q[31];
t q[31];
cx q[30],q[31];
t q[30];
tdg q[31];
cx q[11],q[31];
cx q[11],q[30];
t q[11];
tdg q[30];
cx q[11],q[30];
t q[31];
h q[31];
cx q[30],q[31];
cx q[3],q[31];
x q[31];
h q[32];
cx q[14],q[32];
tdg q[32];
cx q[13],q[32];
t q[32];
cx q[14],q[32];
t q[14];
tdg q[32];
cx q[13],q[32];
cx q[13],q[14];
t q[13];
tdg q[14];
cx q[13],q[14];
t q[32];
h q[32];
cx q[13],q[32];
h q[33];
cx q[32],q[33];
tdg q[33];
cx q[12],q[33];
t q[33];
cx q[32],q[33];
t q[32];
tdg q[33];
cx q[12],q[33];
cx q[12],q[32];
t q[12];
tdg q[32];
cx q[12],q[32];
t q[33];
h q[33];
cx q[12],q[33];
h q[34];
cx q[33],q[34];
tdg q[34];
cx q[11],q[34];
t q[34];
cx q[33],q[34];
t q[33];
tdg q[34];
cx q[11],q[34];
cx q[11],q[33];
t q[11];
tdg q[33];
cx q[11],q[33];
t q[34];
h q[34];
cx q[11],q[34];
cx q[4],q[34];
x q[34];
cx q[11],q[35];
h q[35];
cx q[33],q[35];
tdg q[35];
cx q[11],q[35];
t q[35];
cx q[33],q[35];
t q[33];
tdg q[35];
cx q[11],q[35];
cx q[11],q[33];
t q[11];
tdg q[33];
cx q[11],q[33];
t q[35];
h q[35];
cx q[33],q[35];
cx q[5],q[35];
x q[35];
cx q[12],q[36];
h q[36];
cx q[32],q[36];
tdg q[36];
cx q[12],q[36];
t q[36];
cx q[32],q[36];
t q[32];
tdg q[36];
cx q[12],q[36];
cx q[12],q[32];
t q[12];
tdg q[32];
cx q[12],q[32];
t q[36];
h q[36];
cx q[32],q[36];
h q[37];
cx q[36],q[37];
tdg q[37];
cx q[11],q[37];
t q[37];
cx q[36],q[37];
t q[36];
tdg q[37];
cx q[11],q[37];
cx q[11],q[36];
t q[11];
tdg q[36];
cx q[11],q[36];
t q[37];
h q[37];
cx q[11],q[37];
cx q[6],q[37];
x q[37];
cx q[11],q[38];
h q[38];
cx q[36],q[38];
tdg q[38];
cx q[11],q[38];
t q[38];
cx q[36],q[38];
t q[36];
tdg q[38];
cx q[11],q[38];
cx q[11],q[36];
t q[11];
tdg q[36];
cx q[11],q[36];
t q[38];
h q[38];
cx q[36],q[38];
cx q[7],q[38];
x q[38];
cx q[14],q[39];
h q[39];
cx q[14],q[39];
tdg q[39];
cx q[13],q[39];
t q[39];
cx q[14],q[39];
t q[14];
tdg q[39];
cx q[13],q[39];
cx q[13],q[14];
t q[13];
tdg q[14];
cx q[13],q[14];
t q[39];
h q[39];
cx q[13],q[39];
h q[40];
cx q[39],q[40];
tdg q[40];
cx q[12],q[40];
t q[40];
cx q[39],q[40];
t q[39];
tdg q[40];
cx q[12],q[40];
cx q[12],q[39];
t q[12];
tdg q[39];
cx q[12],q[39];
t q[40];
h q[40];
cx q[12],q[40];
h q[41];
cx q[40],q[41];
tdg q[41];
cx q[11],q[41];
t q[41];
cx q[40],q[41];
t q[40];
tdg q[41];
cx q[11],q[41];
cx q[11],q[40];
t q[11];
tdg q[40];
cx q[11],q[40];
t q[41];
h q[41];
cx q[11],q[41];
cx q[8],q[41];
x q[41];
cx q[11],q[42];
h q[42];
cx q[40],q[42];
tdg q[42];
cx q[11],q[42];
t q[42];
cx q[40],q[42];
t q[40];
tdg q[42];
cx q[11],q[42];
cx q[11],q[40];
t q[11];
tdg q[40];
cx q[11],q[40];
t q[42];
h q[42];
cx q[40],q[42];
cx q[9],q[42];
x q[42];
cx q[12],q[43];
h q[43];
cx q[39],q[43];
tdg q[43];
cx q[12],q[43];
t q[43];
cx q[39],q[43];
t q[39];
tdg q[43];
cx q[12],q[43];
cx q[12],q[39];
t q[12];
tdg q[39];
cx q[12],q[39];
t q[43];
h q[43];
cx q[39],q[43];
h q[44];
cx q[43],q[44];
tdg q[44];
cx q[11],q[44];
t q[44];
cx q[43],q[44];
t q[43];
tdg q[44];
cx q[11],q[44];
cx q[11],q[43];
t q[11];
tdg q[43];
cx q[11],q[43];
t q[44];
h q[44];
cx q[11],q[44];
cx q[10],q[44];
x q[44];
