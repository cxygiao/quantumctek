OPENQASM 2.0;
include "qelib1.inc";
qreg q[39];
s q[3];
s q[11];
cx q[11],q[15];
cx q[2],q[15];
cx q[15],q[16];
h q[16];
cx q[2],q[16];
tdg q[16];
cx q[1],q[16];
t q[16];
cx q[2],q[16];
tdg q[16];
cx q[1],q[16];
t q[16];
cx q[15],q[16];
tdg q[16];
t q[2];
cx q[1],q[2];
tdg q[2];
cx q[1],q[2];
cx q[1],q[16];
t q[16];
cx q[15],q[16];
t q[15];
cx q[1],q[15];
tdg q[15];
cx q[1],q[15];
tdg q[16];
cx q[1],q[17];
cx q[2],q[17];
h q[17];
cx q[15],q[17];
tdg q[17];
cx q[1],q[17];
t q[17];
cx q[15],q[17];
t q[15];
tdg q[17];
cx q[1],q[17];
t q[17];
cx q[2],q[17];
tdg q[17];
cx q[1],q[17];
t q[17];
cx q[2],q[17];
tdg q[17];
t q[2];
cx q[1],q[2];
tdg q[2];
cx q[1],q[2];
cx q[2],q[19];
cx q[3],q[19];
cx q[11],q[20];
cx q[3],q[20];
h q[20];
cx q[19],q[20];
tdg q[20];
cx q[11],q[20];
t q[20];
cx q[19],q[20];
t q[19];
tdg q[20];
cx q[11],q[20];
cx q[11],q[19];
tdg q[19];
cx q[11],q[19];
t q[20];
cx q[11],q[20];
tdg q[20];
cx q[3],q[20];
t q[20];
cx q[11],q[20];
cx q[11],q[13];
tdg q[20];
cx q[3],q[20];
t q[20];
h q[20];
cx q[20],q[21];
h q[21];
cx q[19],q[21];
tdg q[21];
cx q[1],q[21];
t q[21];
cx q[19],q[21];
t q[19];
tdg q[21];
cx q[1],q[21];
t q[21];
cx q[20],q[21];
tdg q[21];
cx q[1],q[21];
t q[21];
cx q[20],q[21];
t q[20];
cx q[1],q[20];
tdg q[20];
cx q[1],q[20];
tdg q[21];
cx q[1],q[22];
cx q[3],q[22];
h q[22];
cx q[20],q[22];
tdg q[22];
cx q[1],q[22];
t q[22];
cx q[20],q[22];
t q[20];
tdg q[22];
cx q[1],q[22];
t q[22];
cx q[3],q[22];
tdg q[22];
cx q[1],q[22];
t q[22];
cx q[3],q[22];
tdg q[22];
cx q[3],q[11];
tdg q[11];
cx q[3],q[11];
cx q[1],q[3];
tdg q[3];
cx q[1],q[3];
h q[24];
cx q[3],q[24];
tdg q[24];
cx q[2],q[24];
t q[24];
cx q[3],q[24];
tdg q[24];
cx q[2],q[24];
t q[24];
h q[24];
t q[3];
cx q[2],q[3];
t q[2];
tdg q[3];
cx q[2],q[3];
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
tdg q[24];
cx q[11],q[24];
t q[11];
t q[25];
h q[25];
cx q[25],q[26];
h q[26];
cx q[24],q[26];
tdg q[26];
cx q[1],q[26];
t q[26];
cx q[24],q[26];
t q[24];
tdg q[26];
cx q[1],q[26];
t q[26];
cx q[25],q[26];
tdg q[26];
cx q[1],q[26];
t q[26];
cx q[25],q[26];
t q[25];
tdg q[26];
cx q[1],q[26];
cx q[1],q[25];
tdg q[25];
cx q[1],q[25];
t q[26];
h q[26];
h q[27];
cx q[25],q[27];
tdg q[27];
cx q[1],q[27];
t q[27];
cx q[25],q[27];
t q[25];
tdg q[27];
cx q[1],q[27];
s q[1];
s q[1];
s q[1];
s q[1];
s q[1];
cx q[1],q[16];
cx q[1],q[17];
cx q[1],q[21];
cx q[1],q[22];
cx q[1],q[13];
cx q[1],q[15];
tdg q[15];
cx q[1],q[15];
cx q[1],q[19];
t q[16];
h q[16];
t q[17];
h q[17];
cx q[17],q[18];
h q[18];
cx q[16],q[18];
tdg q[18];
tdg q[19];
cx q[1],q[19];
t q[1];
cx q[1],q[20];
tdg q[20];
cx q[1],q[20];
cx q[1],q[24];
t q[21];
h q[21];
t q[22];
h q[22];
cx q[22],q[23];
h q[23];
cx q[21],q[23];
tdg q[23];
tdg q[24];
cx q[1],q[24];
cx q[1],q[25];
tdg q[25];
cx q[1],q[25];
t q[27];
h q[27];
cx q[27],q[28];
h q[28];
cx q[26],q[28];
tdg q[28];
cx q[10],q[28];
t q[28];
cx q[26],q[28];
t q[26];
tdg q[28];
cx q[10],q[28];
t q[28];
cx q[27],q[28];
tdg q[28];
cx q[10],q[28];
t q[28];
cx q[27],q[28];
t q[27];
tdg q[28];
cx q[10],q[28];
cx q[10],q[27];
tdg q[27];
cx q[10],q[27];
s q[10];
s q[10];
s q[10];
cx q[10],q[18];
t q[18];
cx q[16],q[18];
t q[16];
tdg q[18];
cx q[10],q[18];
cx q[10],q[23];
t q[18];
cx q[17],q[18];
tdg q[18];
t q[23];
cx q[21],q[23];
t q[21];
tdg q[23];
cx q[10],q[23];
t q[23];
cx q[22],q[23];
tdg q[23];
t q[28];
h q[28];
cx q[27],q[28];
h q[27];
cx q[28],q[27];
tdg q[27];
cx q[0],q[27];
t q[27];
cx q[28],q[27];
tdg q[27];
cx q[0],q[27];
s q[0];
s q[0];
cx q[0],q[12];
cx q[10],q[12];
cx q[10],q[14];
cx q[10],q[16];
x q[12];
cx q[13],q[14];
x q[13];
h q[14];
cx q[13],q[14];
tdg q[14];
cx q[0],q[14];
t q[14];
cx q[13],q[14];
t q[13];
tdg q[14];
cx q[0],q[14];
cx q[0],q[13];
tdg q[13];
cx q[0],q[13];
h q[13];
t q[14];
h q[14];
cx q[14],q[13];
tdg q[13];
cx q[0],q[13];
t q[13];
cx q[14],q[13];
tdg q[13];
cx q[0],q[13];
t q[13];
h q[13];
t q[14];
cx q[0],q[14];
tdg q[14];
cx q[0],q[14];
tdg q[16];
cx q[10],q[16];
cx q[10],q[18];
t q[18];
cx q[17],q[18];
t q[17];
tdg q[18];
cx q[10],q[18];
cx q[10],q[17];
tdg q[17];
cx q[10],q[17];
cx q[10],q[21];
t q[18];
h q[18];
cx q[17],q[18];
h q[17];
cx q[18],q[17];
tdg q[17];
cx q[0],q[17];
t q[17];
cx q[18],q[17];
tdg q[17];
cx q[0],q[17];
t q[17];
h q[17];
x q[17];
t q[18];
cx q[0],q[18];
t q[0];
tdg q[18];
cx q[0],q[18];
tdg q[21];
cx q[10],q[21];
cx q[10],q[23];
t q[23];
cx q[22],q[23];
t q[22];
tdg q[23];
cx q[10],q[23];
cx q[10],q[22];
tdg q[22];
cx q[10],q[22];
cx q[10],q[26];
t q[23];
h q[23];
cx q[22],q[23];
h q[22];
cx q[23],q[22];
tdg q[22];
cx q[0],q[22];
t q[22];
cx q[23],q[22];
tdg q[22];
cx q[0],q[22];
t q[22];
h q[22];
x q[22];
t q[23];
cx q[0],q[23];
tdg q[23];
cx q[0],q[23];
tdg q[26];
cx q[10],q[26];
t q[27];
h q[27];
t q[28];
cx q[0],q[28];
tdg q[28];
cx q[0],q[28];
h q[30];
cx q[27],q[30];
tdg q[30];
cx q[4],q[30];
t q[30];
cx q[27],q[30];
tdg q[30];
cx q[4],q[30];
t q[30];
h q[30];
cx q[4],q[29];
cx q[27],q[29];
t q[27];
x q[29];
cx q[4],q[27];
tdg q[27];
t q[4];
cx q[4],q[27];
h q[32];
cx q[30],q[32];
tdg q[32];
cx q[5],q[32];
t q[32];
cx q[30],q[32];
tdg q[32];
cx q[5],q[32];
t q[32];
h q[32];
cx q[5],q[31];
cx q[30],q[31];
t q[30];
x q[31];
cx q[5],q[30];
tdg q[30];
t q[5];
cx q[5],q[30];
h q[34];
cx q[32],q[34];
tdg q[34];
cx q[6],q[34];
t q[34];
cx q[32],q[34];
tdg q[34];
cx q[6],q[34];
t q[34];
h q[34];
cx q[6],q[33];
cx q[32],q[33];
t q[32];
x q[33];
cx q[6],q[32];
tdg q[32];
t q[6];
cx q[6],q[32];
h q[36];
cx q[34],q[36];
tdg q[36];
cx q[7],q[36];
t q[36];
cx q[34],q[36];
tdg q[36];
cx q[7],q[36];
t q[36];
h q[36];
cx q[7],q[35];
cx q[34],q[35];
t q[34];
x q[35];
cx q[7],q[34];
tdg q[34];
t q[7];
cx q[7],q[34];
h q[38];
cx q[36],q[38];
tdg q[38];
cx q[8],q[38];
t q[38];
cx q[36],q[38];
tdg q[38];
cx q[8],q[38];
t q[38];
h q[38];
cx q[8],q[37];
cx q[36],q[37];
t q[36];
x q[37];
cx q[8],q[36];
tdg q[36];
t q[8];
cx q[8],q[36];
cx q[9],q[38];