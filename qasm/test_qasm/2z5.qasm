OPENQASM 2.0;
include "qelib1.inc";
qreg q[38];
creg c[38];
h  q[15];
cx q[11],q[15];
tdg  q[15];
cx q[10],q[15];
t  q[15];
cx q[11],q[15];
tdg  q[15];
cx q[10],q[15];
t  q[15];
t  q[11];
cx q[10],q[11];
t  q[10];
x  q[10];
tdg  q[11];
cx q[10],q[11];
cx q[11],q[15];
tdg  q[15];
cx q[10],q[15];
t  q[15];
cx q[11],q[15];
tdg  q[15];
cx q[10],q[15];
t  q[15];
h  q[15];
t  q[11];
cx q[10],q[11];
t  q[10];
x  q[10];
tdg  q[11];
cx q[10],q[11];
h  q[16];
cx q[12],q[16];
tdg  q[16];
cx q[10],q[16];
t  q[16];
cx q[12],q[16];
tdg  q[16];
cx q[10],q[16];
t  q[16];
t  q[12];
cx q[10],q[12];
t  q[10];
x  q[10];
tdg  q[12];
cx q[10],q[12];
cx q[12],q[16];
tdg  q[16];
cx q[10],q[16];
t  q[16];
cx q[12],q[16];
tdg  q[16];
cx q[10],q[16];
t  q[16];
h  q[16];
t  q[12];
cx q[10],q[12];
t  q[10];
x  q[10];
tdg  q[12];
cx q[10],q[12];
h  q[17];
cx q[13],q[17];
tdg  q[17];
cx q[10],q[17];
t  q[17];
cx q[13],q[17];
tdg  q[17];
cx q[10],q[17];
t  q[17];
t  q[13];
cx q[10],q[13];
t  q[10];
x  q[10];
tdg  q[13];
cx q[10],q[13];
cx q[13],q[17];
tdg  q[17];
cx q[10],q[17];
t  q[17];
cx q[13],q[17];
tdg  q[17];
cx q[10],q[17];
t  q[17];
h  q[17];
t  q[13];
cx q[10],q[13];
t  q[10];
x  q[10];
tdg  q[13];
cx q[10],q[13];
h  q[18];
cx q[14],q[18];
tdg  q[18];
cx q[10],q[18];
t  q[18];
cx q[14],q[18];
tdg  q[18];
cx q[10],q[18];
t  q[18];
t  q[14];
cx q[10],q[14];
t  q[10];
x  q[10];
tdg  q[14];
cx q[10],q[14];
cx q[14],q[18];
tdg  q[18];
cx q[10],q[18];
t  q[18];
cx q[14],q[18];
tdg  q[18];
t  q[14];
cx q[10],q[14];
cx q[10],q[18];
t  q[18];
h  q[18];
t  q[10];
x  q[10];
tdg  q[14];
cx q[10],q[14];
h  q[19];
cx q[12],q[19];
tdg  q[19];
cx q[11],q[19];
t  q[19];
cx q[12],q[19];
tdg  q[19];
cx q[11],q[19];
t  q[19];
t  q[12];
cx q[11],q[12];
t  q[11];
x  q[11];
tdg  q[12];
cx q[11],q[12];
cx q[12],q[19];
tdg  q[19];
cx q[11],q[19];
t  q[19];
cx q[12],q[19];
tdg  q[19];
cx q[11],q[19];
t  q[19];
h  q[19];
t  q[12];
cx q[11],q[12];
t  q[11];
x  q[11];
tdg  q[12];
cx q[11],q[12];
h  q[20];
cx q[13],q[20];
tdg  q[20];
cx q[11],q[20];
t  q[20];
cx q[13],q[20];
tdg  q[20];
cx q[11],q[20];
t  q[20];
t  q[13];
cx q[11],q[13];
t  q[11];
x  q[11];
tdg  q[13];
cx q[11],q[13];
cx q[13],q[20];
tdg  q[20];
cx q[11],q[20];
t  q[20];
cx q[13],q[20];
tdg  q[20];
cx q[11],q[20];
t  q[20];
h  q[20];
t  q[13];
cx q[11],q[13];
t  q[11];
x  q[11];
tdg  q[13];
cx q[11],q[13];
h  q[21];
cx q[14],q[21];
tdg  q[21];
cx q[11],q[21];
t  q[21];
cx q[14],q[21];
tdg  q[21];
cx q[11],q[21];
t  q[21];
t  q[14];
cx q[11],q[14];
t  q[11];
x  q[11];
tdg  q[14];
cx q[11],q[14];
cx q[14],q[21];
tdg  q[21];
cx q[11],q[21];
t  q[21];
cx q[14],q[21];
tdg  q[21];
t  q[14];
cx q[11],q[14];
cx q[11],q[21];
t  q[21];
h  q[21];
t  q[11];
x  q[11];
tdg  q[14];
cx q[11],q[14];
h  q[22];
cx q[13],q[22];
tdg  q[22];
cx q[12],q[22];
t  q[22];
cx q[13],q[22];
tdg  q[22];
cx q[12],q[22];
t  q[22];
t  q[13];
cx q[12],q[13];
t  q[12];
x  q[12];
tdg  q[13];
cx q[12],q[13];
cx q[13],q[22];
tdg  q[22];
cx q[12],q[22];
t  q[22];
cx q[13],q[22];
tdg  q[22];
cx q[12],q[22];
t  q[22];
h  q[22];
t  q[13];
cx q[12],q[13];
t  q[12];
x  q[12];
tdg  q[13];
cx q[12],q[13];
h  q[23];
cx q[14],q[23];
tdg  q[23];
cx q[12],q[23];
t  q[23];
cx q[14],q[23];
tdg  q[23];
cx q[12],q[23];
t  q[23];
t  q[14];
cx q[12],q[14];
t  q[12];
x  q[12];
tdg  q[14];
cx q[12],q[14];
cx q[14],q[23];
tdg  q[23];
cx q[12],q[23];
t  q[23];
cx q[14],q[23];
tdg  q[23];
t  q[14];
cx q[12],q[14];
cx q[12],q[23];
t  q[23];
h  q[23];
t  q[12];
x  q[12];
tdg  q[14];
cx q[12],q[14];
h  q[24];
cx q[14],q[24];
tdg  q[24];
cx q[13],q[24];
t  q[24];
cx q[14],q[24];
tdg  q[24];
cx q[13],q[24];
t  q[24];
t  q[14];
cx q[13],q[14];
t  q[13];
x  q[13];
tdg  q[14];
cx q[13],q[14];
cx q[14],q[24];
tdg  q[24];
cx q[13],q[24];
t  q[24];
cx q[14],q[24];
tdg  q[24];
cx q[13],q[24];
t  q[24];
h  q[24];
t  q[14];
cx q[13],q[14];
t  q[13];
x  q[13];
tdg  q[14];
cx q[13],q[14];
x  q[25];
h  q[25];
cx q[15],q[25];
tdg  q[25];
cx q[0],q[25];
t  q[25];
cx q[15],q[25];
t  q[15];
tdg  q[25];
cx q[0],q[25];
t  q[25];
h  q[25];
cx q[0],q[15];
tdg  q[15];
t  q[0];
cx q[0],q[15];
x  q[26];
h  q[26];
cx q[16],q[26];
tdg  q[26];
cx q[1],q[26];
t  q[26];
cx q[16],q[26];
t  q[16];
tdg  q[26];
cx q[1],q[26];
t  q[26];
h  q[26];
cx q[1],q[16];
tdg  q[16];
t  q[1];
cx q[1],q[16];
x  q[27];
h  q[27];
cx q[17],q[27];
tdg  q[27];
cx q[2],q[27];
t  q[27];
cx q[17],q[27];
t  q[17];
tdg  q[27];
cx q[2],q[27];
t  q[27];
h  q[27];
cx q[2],q[17];
tdg  q[17];
t  q[2];
cx q[2],q[17];
x  q[28];
h  q[28];
cx q[18],q[28];
tdg  q[28];
cx q[3],q[28];
t  q[28];
cx q[18],q[28];
t  q[18];
tdg  q[28];
cx q[3],q[28];
t  q[28];
h  q[28];
cx q[3],q[18];
tdg  q[18];
t  q[3];
cx q[3],q[18];
x  q[29];
h  q[29];
cx q[19],q[29];
tdg  q[29];
cx q[4],q[29];
t  q[29];
cx q[19],q[29];
t  q[19];
tdg  q[29];
cx q[4],q[29];
t  q[29];
h  q[29];
cx q[4],q[19];
tdg  q[19];
t  q[4];
cx q[4],q[19];
x  q[30];
h  q[30];
cx q[20],q[30];
tdg  q[30];
cx q[5],q[30];
t  q[30];
cx q[20],q[30];
t  q[20];
tdg  q[30];
cx q[5],q[30];
t  q[30];
h  q[30];
cx q[5],q[20];
tdg  q[20];
t  q[5];
cx q[5],q[20];
x  q[31];
h  q[31];
cx q[21],q[31];
tdg  q[31];
cx q[6],q[31];
t  q[31];
cx q[21],q[31];
t  q[21];
tdg  q[31];
cx q[6],q[31];
t  q[31];
h  q[31];
cx q[6],q[21];
tdg  q[21];
t  q[6];
cx q[6],q[21];
x  q[32];
h  q[32];
cx q[22],q[32];
tdg  q[32];
cx q[7],q[32];
t  q[32];
cx q[22],q[32];
t  q[22];
tdg  q[32];
cx q[7],q[32];
t  q[32];
h  q[32];
cx q[7],q[22];
tdg  q[22];
t  q[7];
cx q[7],q[22];
x  q[33];
h  q[33];
cx q[23],q[33];
tdg  q[33];
cx q[8],q[33];
t  q[33];
cx q[23],q[33];
t  q[23];
tdg  q[33];
cx q[8],q[33];
t  q[33];
h  q[33];
cx q[8],q[23];
tdg  q[23];
t  q[8];
cx q[8],q[23];
x  q[34];
h  q[34];
cx q[24],q[34];
tdg  q[34];
cx q[9],q[34];
t  q[34];
cx q[24],q[34];
t  q[24];
tdg  q[34];
cx q[9],q[34];
t  q[34];
h  q[34];
cx q[9],q[24];
tdg  q[24];
t  q[9];
cx q[9],q[24];
h  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[30],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
cx q[30],q[34];
tdg  q[34];
cx q[30],q[34];
h  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[29],q[34];
t  q[34];
cx q[33],q[34];
t  q[33];
cx q[29],q[33];
tdg  q[33];
cx q[29],q[33];
h  q[33];
cx q[32],q[33];
tdg  q[33];
cx q[28],q[33];
t  q[33];
cx q[32],q[33];
t  q[32];
cx q[28],q[32];
tdg  q[32];
cx q[28],q[32];
h  q[32];
cx q[31],q[32];
tdg  q[32];
cx q[27],q[32];
t  q[32];
cx q[31],q[32];
t  q[31];
tdg  q[32];
cx q[27],q[32];
cx q[27],q[31];
tdg  q[31];
cx q[27],q[31];
h  q[31];
cx q[26],q[31];
tdg  q[31];
cx q[25],q[31];
t  q[31];
cx q[26],q[31];
t  q[26];
tdg  q[31];
cx q[25],q[31];
cx q[25],q[26];
tdg  q[26];
cx q[25],q[26];
t  q[31];
h  q[31];
t  q[32];
cx q[31],q[32];
tdg  q[32];
cx q[27],q[32];
t  q[32];
cx q[31],q[32];
t  q[31];
tdg  q[32];
cx q[27],q[32];
cx q[27],q[31];
tdg  q[31];
cx q[27],q[31];
t  q[32];
h  q[32];
tdg  q[33];
cx q[28],q[33];
t  q[33];
cx q[32],q[33];
tdg  q[33];
cx q[28],q[33];
t  q[33];
cx q[32],q[33];
t  q[32];
tdg  q[33];
cx q[28],q[33];
cx q[28],q[32];
tdg  q[32];
cx q[28],q[32];
t  q[33];
h  q[33];
tdg  q[34];
cx q[29],q[34];
t  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[29],q[34];
t  q[34];
cx q[33],q[34];
t  q[33];
tdg  q[34];
cx q[29],q[34];
cx q[29],q[33];
tdg  q[33];
cx q[29],q[33];
t  q[34];
h  q[34];
tdg  q[35];
cx q[30],q[35];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[30],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
cx q[30],q[34];
tdg  q[34];
cx q[30],q[34];
h  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[29],q[34];
t  q[34];
cx q[33],q[34];
t  q[33];
cx q[29],q[33];
tdg  q[33];
cx q[29],q[33];
h  q[33];
cx q[32],q[33];
tdg  q[33];
cx q[28],q[33];
t  q[33];
cx q[32],q[33];
t  q[32];
cx q[28],q[32];
tdg  q[32];
cx q[28],q[32];
h  q[32];
cx q[31],q[32];
tdg  q[32];
cx q[27],q[32];
t  q[32];
cx q[31],q[32];
t  q[31];
tdg  q[32];
cx q[27],q[32];
cx q[27],q[31];
tdg  q[31];
cx q[27],q[31];
h  q[31];
cx q[26],q[31];
tdg  q[31];
cx q[25],q[31];
t  q[31];
cx q[26],q[31];
t  q[26];
tdg  q[31];
cx q[25],q[31];
cx q[25],q[26];
tdg  q[26];
cx q[25],q[26];
t  q[31];
h  q[31];
t  q[32];
cx q[31],q[32];
tdg  q[32];
cx q[27],q[32];
t  q[32];
cx q[31],q[32];
t  q[31];
tdg  q[32];
cx q[27],q[32];
cx q[27],q[31];
tdg  q[31];
cx q[27],q[31];
t  q[32];
h  q[32];
tdg  q[33];
cx q[28],q[33];
t  q[33];
cx q[32],q[33];
tdg  q[33];
cx q[28],q[33];
t  q[33];
cx q[32],q[33];
t  q[32];
tdg  q[33];
cx q[28],q[33];
cx q[28],q[32];
tdg  q[32];
cx q[28],q[32];
t  q[33];
h  q[33];
tdg  q[34];
cx q[29],q[34];
t  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[29],q[34];
t  q[34];
cx q[33],q[34];
t  q[33];
tdg  q[34];
cx q[29],q[34];
cx q[29],q[33];
tdg  q[33];
cx q[29],q[33];
t  q[34];
h  q[34];
tdg  q[35];
cx q[30],q[35];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
tdg  q[35];
cx q[33],q[35];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
s  q[34];
tdg  q[35];
cx q[33],q[35];
t  q[35];
h  q[35];
h  q[36];
cx q[35],q[36];
tdg  q[36];
cx q[34],q[36];
t  q[36];
cx q[35],q[36];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[34],q[35];
h  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
tdg  q[36];
cx q[34],q[36];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
s  q[34];
tdg  q[35];
cx q[33],q[35];
t  q[35];
h  q[35];
t  q[36];
cx q[35],q[36];
tdg  q[36];
cx q[34],q[36];
t  q[36];
cx q[35],q[36];
t  q[35];
tdg  q[36];
cx q[34],q[36];
cx q[34],q[35];
tdg  q[35];
cx q[34],q[35];
t  q[36];
h  q[36];
h  q[37];
cx q[36],q[37];
tdg  q[37];
cx q[35],q[37];
t  q[37];
cx q[36],q[37];
tdg  q[37];
cx q[35],q[37];
t  q[37];
t  q[36];
cx q[35],q[36];
t  q[35];
tdg  q[36];
cx q[35],q[36];
h  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
s  q[33];
s  q[33];
s  q[33];
s  q[33];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
s  q[34];
tdg  q[35];
cx q[33],q[35];
t  q[35];
h  q[35];
h  q[36];
cx q[35],q[36];
tdg  q[36];
cx q[34],q[36];
t  q[36];
cx q[35],q[36];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[34],q[35];
h  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
tdg  q[36];
cx q[34],q[36];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
s  q[31];
s  q[31];
s  q[31];
s  q[31];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
s  q[34];
tdg  q[35];
cx q[33],q[35];
t  q[33];
t  q[35];
h  q[35];
t  q[36];
cx q[35],q[36];
tdg  q[36];
cx q[34],q[36];
t  q[36];
cx q[35],q[36];
t  q[35];
tdg  q[36];
cx q[34],q[36];
cx q[34],q[35];
tdg  q[35];
cx q[34],q[35];
t  q[36];
h  q[36];
cx q[36],q[37];
tdg  q[37];
cx q[35],q[37];
t  q[37];
cx q[36],q[37];
tdg  q[37];
cx q[35],q[37];
t  q[37];
t  q[36];
cx q[35],q[36];
t  q[35];
tdg  q[36];
cx q[35],q[36];
h  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[30],q[35];
t  q[35];
cx q[34],q[35];
cx q[30],q[34];
tdg  q[34];
cx q[30],q[34];
h  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[29],q[34];
t  q[34];
cx q[33],q[34];
cx q[29],q[33];
tdg  q[33];
cx q[29],q[33];
h  q[33];
cx q[32],q[33];
tdg  q[33];
cx q[28],q[33];
t  q[33];
cx q[32],q[33];
t  q[32];
cx q[28],q[32];
tdg  q[32];
cx q[28],q[32];
h  q[32];
cx q[31],q[32];
tdg  q[32];
cx q[27],q[32];
t  q[32];
cx q[31],q[32];
t  q[31];
tdg  q[32];
cx q[27],q[32];
cx q[27],q[31];
tdg  q[31];
cx q[27],q[31];
h  q[31];
cx q[26],q[31];
tdg  q[31];
cx q[25],q[31];
t  q[31];
cx q[26],q[31];
t  q[26];
tdg  q[31];
cx q[25],q[31];
cx q[25],q[26];
tdg  q[26];
cx q[25],q[26];
t  q[31];
h  q[31];
t  q[32];
cx q[31],q[32];
tdg  q[32];
cx q[27],q[32];
t  q[32];
cx q[31],q[32];
t  q[31];
tdg  q[32];
cx q[27],q[32];
cx q[27],q[31];
tdg  q[31];
cx q[27],q[31];
t  q[32];
h  q[32];
tdg  q[33];
cx q[28],q[33];
t  q[33];
cx q[32],q[33];
tdg  q[33];
cx q[28],q[33];
t  q[33];
cx q[32],q[33];
t  q[32];
tdg  q[33];
cx q[28],q[33];
cx q[28],q[32];
tdg  q[32];
cx q[28],q[32];
t  q[33];
h  q[33];
tdg  q[34];
cx q[29],q[34];
t  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[29],q[34];
t  q[34];
cx q[33],q[34];
t  q[33];
tdg  q[34];
cx q[29],q[34];
cx q[29],q[33];
tdg  q[33];
cx q[29],q[33];
t  q[34];
h  q[34];
tdg  q[35];
cx q[30],q[35];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[30],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
cx q[30],q[34];
tdg  q[34];
cx q[30],q[34];
h  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[29],q[34];
t  q[34];
cx q[33],q[34];
t  q[33];
cx q[29],q[33];
tdg  q[33];
cx q[29],q[33];
h  q[33];
cx q[32],q[33];
tdg  q[33];
cx q[28],q[33];
t  q[33];
cx q[32],q[33];
t  q[32];
cx q[28],q[32];
tdg  q[32];
cx q[28],q[32];
h  q[32];
cx q[31],q[32];
tdg  q[32];
cx q[27],q[32];
t  q[32];
cx q[31],q[32];
t  q[31];
tdg  q[32];
cx q[27],q[32];
cx q[27],q[31];
tdg  q[31];
cx q[27],q[31];
h  q[31];
cx q[26],q[31];
tdg  q[31];
cx q[25],q[31];
t  q[31];
cx q[26],q[31];
t  q[26];
tdg  q[31];
cx q[25],q[31];
s  q[25];
s  q[25];
cx q[25],q[26];
tdg  q[26];
cx q[25],q[26];
t  q[31];
h  q[31];
t  q[32];
cx q[31],q[32];
tdg  q[32];
cx q[27],q[32];
t  q[32];
cx q[31],q[32];
t  q[31];
tdg  q[32];
cx q[27],q[32];
cx q[27],q[31];
tdg  q[31];
cx q[27],q[31];
s  q[27];
s  q[27];
s  q[27];
s  q[27];
t  q[32];
h  q[32];
tdg  q[33];
cx q[28],q[33];
t  q[33];
cx q[32],q[33];
tdg  q[33];
cx q[28],q[33];
t  q[33];
cx q[32],q[33];
t  q[32];
tdg  q[33];
cx q[28],q[33];
cx q[28],q[32];
tdg  q[32];
cx q[28],q[32];
s  q[28];
s  q[28];
s  q[28];
s  q[28];
t  q[33];
h  q[33];
tdg  q[34];
cx q[29],q[34];
t  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[29],q[34];
t  q[34];
cx q[33],q[34];
t  q[33];
tdg  q[34];
cx q[29],q[34];
cx q[29],q[33];
tdg  q[33];
cx q[29],q[33];
s  q[29];
s  q[29];
s  q[29];
s  q[29];
t  q[34];
h  q[34];
tdg  q[35];
cx q[30],q[35];
s  q[30];
s  q[30];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
tdg  q[35];
cx q[33],q[35];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
s  q[34];
tdg  q[35];
cx q[33],q[35];
t  q[35];
h  q[35];
h  q[36];
cx q[35],q[36];
tdg  q[36];
cx q[34],q[36];
t  q[36];
cx q[35],q[36];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[34],q[35];
h  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
tdg  q[36];
cx q[34],q[36];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
s  q[33];
s  q[33];
s  q[33];
s  q[33];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
s  q[31];
s  q[31];
s  q[31];
s  q[31];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
s  q[34];
tdg  q[35];
cx q[33],q[35];
t  q[35];
h  q[35];
t  q[36];
cx q[35],q[36];
tdg  q[36];
cx q[34],q[36];
t  q[36];
cx q[35],q[36];
t  q[35];
tdg  q[36];
cx q[34],q[36];
cx q[34],q[35];
tdg  q[35];
cx q[34],q[35];
t  q[36];
h  q[36];
cx q[36],q[37];
tdg  q[37];
cx q[35],q[37];
t  q[37];
cx q[36],q[37];
tdg  q[37];
cx q[35],q[37];
t  q[37];
t  q[36];
cx q[35],q[36];
t  q[35];
tdg  q[36];
cx q[35],q[36];
h  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
s  q[34];
tdg  q[35];
cx q[33],q[35];
t  q[35];
h  q[35];
h  q[36];
cx q[35],q[36];
tdg  q[36];
cx q[34],q[36];
t  q[36];
cx q[35],q[36];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[34],q[35];
h  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
tdg  q[36];
cx q[34],q[36];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
cx q[34],q[35];
tdg  q[35];
cx q[33],q[35];
t  q[35];
cx q[34],q[35];
t  q[34];
tdg  q[35];
cx q[33],q[35];
cx q[33],q[34];
tdg  q[34];
cx q[33],q[34];
h  q[34];
cx q[32],q[34];
tdg  q[34];
cx q[31],q[34];
t  q[34];
cx q[32],q[34];
t  q[32];
tdg  q[34];
cx q[31],q[34];
cx q[31],q[32];
tdg  q[32];
cx q[31],q[32];
t  q[34];
h  q[34];
t  q[35];
h  q[35];
t  q[36];
cx q[35],q[36];
tdg  q[36];
cx q[34],q[36];
t  q[36];
cx q[35],q[36];
t  q[35];
tdg  q[36];
cx q[34],q[36];
cx q[34],q[35];
t  q[34];
tdg  q[35];
cx q[34],q[35];
t  q[36];
h  q[36];
cx q[36],q[37];
tdg  q[37];
cx q[35],q[37];
t  q[37];
cx q[36],q[37];
tdg  q[37];
cx q[35],q[37];
t  q[37];
h  q[37];
t  q[36];
cx q[35],q[36];
t  q[35];
tdg  q[36];
cx q[35],q[36];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
measure q[4] -> c[4];
measure q[5] -> c[5];
measure q[6] -> c[6];
measure q[7] -> c[7];
measure q[8] -> c[8];
measure q[9] -> c[9];
measure q[10] -> c[10];
measure q[11] -> c[11];
measure q[12] -> c[12];
measure q[13] -> c[13];
measure q[14] -> c[14];
measure q[15] -> c[15];
measure q[16] -> c[16];
measure q[17] -> c[17];
measure q[18] -> c[18];
measure q[19] -> c[19];
measure q[20] -> c[20];
measure q[21] -> c[21];
measure q[22] -> c[22];
measure q[23] -> c[23];
measure q[24] -> c[24];
measure q[25] -> c[25];
measure q[26] -> c[26];
measure q[27] -> c[27];
measure q[28] -> c[28];
measure q[29] -> c[29];
measure q[30] -> c[30];
measure q[31] -> c[31];
measure q[32] -> c[32];
measure q[33] -> c[33];
measure q[34] -> c[34];
measure q[35] -> c[35];
measure q[36] -> c[36];
measure q[37] -> c[37];
