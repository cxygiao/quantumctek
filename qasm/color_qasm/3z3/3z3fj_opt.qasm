OPENQASM 2.0;
include "qelib1.inc";
qreg e[3];
qreg c1[3];
qreg c2[3];
qreg c3[3];
qreg va1[3];
qreg va2[9];
qreg va3[3];
qreg va4[3];
qreg addq[1];
qreg vout[1];
qreg ea1[9];
qreg ea2[3];
qreg addq1[1];
qreg eout[1];
qreg out[1];
creg c[1];
x e[0];
x e[2];
s e[2];
s e[2];
s e[2];
x c1[0];
s c1[0];
x c1[1];
s c1[1];
x c1[2];
s c1[2];
x c2[0];
x c2[1];
x c2[2];
x c3[0];
x c3[1];
x va1[0];
h va1[0];
cx c3[2],va1[0];
tdg va1[0];
cx c3[0],va1[0];
t va1[0];
cx c3[2],va1[0];
t c3[2];
tdg va1[0];
cx c3[0],va1[0];
cx c3[0],c3[2];
tdg c3[2];
cx c3[0],c3[2];
h c3[2];
cx c2[0],c3[2];
tdg c3[2];
cx c1[0],c3[2];
t c3[2];
cx c2[0],c3[2];
t c2[0];
tdg c3[2];
cx c1[0],c3[2];
cx c1[0],c2[0];
tdg c2[0];
cx c1[0],c2[0];
t c3[2];
h c3[2];
t va1[0];
cx c3[2],va1[0];
tdg va1[0];
cx c3[0],va1[0];
t va1[0];
cx c3[2],va1[0];
t c3[2];
cx c3[0],c3[2];
tdg c3[2];
cx c3[0],c3[2];
s c3[0];
h c3[2];
cx c2[0],c3[2];
tdg c3[2];
cx c1[0],c3[2];
t c3[2];
cx c2[0],c3[2];
t c2[0];
tdg c3[2];
cx c1[0],c3[2];
cx c1[0],c2[0];
x c1[0];
tdg c2[0];
cx c1[0],c2[0];
t c3[2];
h c3[2];
x c3[2];
tdg va1[0];
cx c3[0],va1[0];
x c3[0];
t va1[0];
h va1[0];
s va1[0];
x va1[1];
h va1[1];
cx va1[0],va1[1];
tdg va1[1];
cx c3[1],va1[1];
t va1[1];
cx va1[0],va1[1];
tdg va1[1];
cx c3[1],va1[1];
t va1[1];
x va1[2];
h va1[2];
x va2[0];
h va2[0];
cx c2[0],va2[0];
tdg va2[0];
cx c1[0],va2[0];
t va2[0];
cx c2[0],va2[0];
t c2[0];
cx c1[0],c2[0];
tdg c2[0];
cx c1[0],c2[0];
tdg va2[0];
x va2[1];
h va2[1];
cx c3[0],va2[1];
tdg va2[1];
cx c1[0],va2[1];
t va2[1];
cx c3[0],va2[1];
t c3[0];
cx c1[0],c3[0];
tdg c3[0];
cx c1[0],c3[0];
cx c1[0],va2[0];
t va2[0];
h va2[0];
tdg va2[1];
cx c1[0],va2[1];
s c1[0];
t va2[1];
h va2[1];
x va2[2];
h va2[2];
cx c3[0],va2[2];
tdg va2[2];
cx c2[0],va2[2];
t va2[2];
cx c3[0],va2[2];
t c3[0];
tdg va2[2];
cx c2[0],va2[2];
s c2[0];
t va2[2];
h va2[2];
x va2[3];
h va2[3];
x va2[4];
h va2[4];
x va2[5];
x va2[6];
x va2[7];
x va2[8];
h va3[0];
cx va2[8],va3[0];
tdg va3[0];
cx va2[2],va3[0];
t va3[0];
cx va2[8],va3[0];
tdg va3[0];
cx va2[2],va3[0];
t va3[0];
t va2[8];
cx va2[2],va2[8];
tdg va2[8];
cx va2[2],va2[8];
h va2[8];
cx va2[1],va2[8];
tdg va2[8];
cx va2[0],va2[8];
t va2[8];
cx va2[1],va2[8];
t va2[1];
tdg va2[8];
cx va2[0],va2[8];
cx va2[0],va2[1];
tdg va2[1];
cx va2[0],va2[1];
t va2[8];
h va2[8];
cx va2[8],va3[0];
tdg va3[0];
cx va2[2],va3[0];
t va3[0];
cx va2[8],va3[0];
tdg va3[0];
cx va2[2],va3[0];
t va3[0];
h va3[0];
s va2[2];
t va2[8];
cx va2[2],va2[8];
tdg va2[8];
cx va2[2],va2[8];
h va2[2];
h va2[8];
cx va2[1],va2[8];
tdg va2[8];
cx va2[0],va2[8];
t va2[8];
cx va2[1],va2[8];
t va2[1];
cx va2[0],va2[1];
tdg va2[1];
cx va2[0],va2[1];
s va2[0];
h va2[1];
tdg va2[8];
cx va2[0],va2[8];
t va2[8];
h va2[8];
h va3[1];
h va3[2];
h va4[0];
cx va3[0],va4[0];
tdg va4[0];
cx va1[0],va4[0];
t va4[0];
cx va3[0],va4[0];
t va3[0];
tdg va4[0];
cx va1[0],va4[0];
cx va1[0],va3[0];
tdg va3[0];
cx va1[0],va3[0];
cx c3[1],va1[0];
tdg va1[0];
cx c3[1],va1[0];
h va1[0];
cx c2[1],va1[0];
tdg va1[0];
cx c1[1],va1[0];
t va1[0];
cx c2[1],va1[0];
t c2[1];
tdg va1[0];
cx c1[1],va1[0];
cx c1[1],c2[1];
tdg c2[1];
cx c1[1],c2[1];
t va1[0];
h va1[0];
cx va1[0],va1[1];
tdg va1[1];
cx c3[1],va1[1];
t va1[1];
cx va1[0],va1[1];
t va1[0];
cx c3[1],va1[0];
tdg va1[0];
cx c3[1],va1[0];
s c3[1];
h va1[0];
cx c2[1],va1[0];
tdg va1[0];
cx c1[1],va1[0];
t va1[0];
cx c2[1],va1[0];
t c2[1];
tdg va1[0];
cx c1[1],va1[0];
cx c1[1],c2[1];
x c1[1];
tdg c2[1];
cx c1[1],c2[1];
cx c2[1],va2[1];
t va1[0];
h va1[0];
tdg va1[1];
cx c3[1],va1[1];
x c3[1];
cx c3[1],va2[2];
t va1[1];
h va1[1];
s va1[1];
cx va1[1],va1[2];
tdg va1[2];
cx c3[2],va1[2];
t va1[2];
cx va1[1],va1[2];
tdg va1[2];
cx c3[2],va1[2];
t va1[2];
cx va3[0],va3[1];
tdg va3[1];
t va4[0];
h va4[0];
tdg va2[1];
cx c1[1],va2[1];
t va2[1];
cx c2[1],va2[1];
t c2[1];
cx c1[1],c2[1];
tdg c2[1];
cx c1[1],c2[1];
tdg va2[1];
tdg va2[2];
cx c1[1],va2[2];
t va2[2];
cx c3[1],va2[2];
t c3[1];
cx c1[1],c3[1];
tdg c3[1];
cx c1[1],c3[1];
cx c1[1],va2[1];
cx c3[1],va2[3];
t va2[1];
h va2[1];
tdg va2[2];
cx c1[1],va2[2];
t va2[2];
h va2[2];
tdg va2[3];
cx c2[1],va2[3];
t va2[3];
cx c3[1],va2[3];
t c3[1];
tdg va2[3];
cx c2[1],va2[3];
t va2[3];
h va2[3];
cx va2[3],va3[1];
t va3[1];
cx va3[0],va3[1];
t va3[0];
tdg va3[1];
cx va2[3],va3[1];
t va3[1];
cx va2[3],va3[0];
tdg va3[0];
cx va2[3],va3[0];
h va3[0];
cx va2[2],va3[0];
tdg va3[0];
cx va2[1],va3[0];
t va3[0];
cx va2[2],va3[0];
tdg va3[0];
cx va2[1],va3[0];
t va3[0];
h va3[0];
cx va3[0],va3[1];
tdg va3[1];
t va2[2];
cx va2[1],va2[2];
tdg va2[2];
cx va2[1],va2[2];
cx va2[3],va3[1];
t va3[1];
cx va3[0],va3[1];
t va3[0];
tdg va3[1];
cx va2[3],va3[1];
t va3[1];
h va3[1];
s va2[3];
cx va2[3],va3[0];
tdg va3[0];
cx va2[3],va3[0];
h va3[0];
cx va2[2],va3[0];
tdg va3[0];
cx va2[1],va3[0];
t va3[0];
cx va2[2],va3[0];
tdg va3[0];
t va2[2];
cx va2[1],va2[2];
tdg va2[2];
cx va2[1],va2[2];
s va2[1];
cx va2[1],va3[0];
t va3[0];
h va3[0];
h va2[2];
h va2[3];
h va4[1];
cx va3[1],va4[1];
tdg va4[1];
cx va1[1],va4[1];
t va4[1];
cx va3[1],va4[1];
t va3[1];
tdg va4[1];
cx va1[1],va4[1];
cx va1[1],va3[1];
tdg va3[1];
cx va1[1],va3[1];
cx c3[2],va1[1];
tdg va1[1];
cx c3[2],va1[1];
h va1[1];
cx c2[2],va1[1];
tdg va1[1];
cx c1[2],va1[1];
t va1[1];
cx c2[2],va1[1];
t c2[2];
tdg va1[1];
cx c1[2],va1[1];
cx c1[2],c2[2];
tdg c2[2];
cx c1[2],c2[2];
t va1[1];
h va1[1];
cx va1[1],va1[2];
tdg va1[2];
cx c3[2],va1[2];
t va1[2];
cx va1[1],va1[2];
t va1[1];
cx c3[2],va1[1];
tdg va1[1];
cx c3[2],va1[1];
s c3[2];
h va1[1];
cx c2[2],va1[1];
tdg va1[1];
cx c1[2],va1[1];
t va1[1];
cx c2[2],va1[1];
t c2[2];
tdg va1[1];
cx c1[2],va1[1];
cx c1[2],c2[2];
x c1[2];
tdg c2[2];
cx c1[2],c2[2];
cx c2[2],va2[2];
t va1[1];
h va1[1];
tdg va1[2];
cx c3[2],va1[2];
x c3[2];
cx c3[2],va2[3];
t va1[2];
h va1[2];
cx va3[1],va3[2];
tdg va3[2];
t va4[1];
h va4[1];
tdg va2[2];
cx c1[2],va2[2];
t va2[2];
cx c2[2],va2[2];
t c2[2];
cx c1[2],c2[2];
tdg c2[2];
cx c1[2],c2[2];
tdg va2[2];
tdg va2[3];
cx c1[2],va2[3];
t va2[3];
cx c3[2],va2[3];
t c3[2];
cx c1[2],c3[2];
tdg c3[2];
cx c1[2],c3[2];
cx c1[2],va2[2];
cx c3[2],va2[4];
t va2[2];
h va2[2];
tdg va2[3];
cx c1[2],va2[3];
t va2[3];
h va2[3];
tdg va2[4];
cx c2[2],va2[4];
t va2[4];
cx c3[2],va2[4];
t c3[2];
tdg va2[4];
cx c2[2],va2[4];
t va2[4];
h va2[4];
cx va2[4],va3[2];
t va3[2];
cx va3[1],va3[2];
t va3[1];
tdg va3[2];
cx va2[4],va3[2];
t va3[2];
cx va2[4],va3[1];
tdg va3[1];
cx va2[4],va3[1];
h va3[1];
cx va2[3],va3[1];
tdg va3[1];
cx va2[2],va3[1];
t va3[1];
cx va2[3],va3[1];
tdg va3[1];
cx va2[2],va3[1];
t va3[1];
h va3[1];
cx va3[1],va3[2];
tdg va3[2];
s va2[2];
t va2[3];
cx va2[2],va2[3];
tdg va2[3];
cx va2[2],va2[3];
cx va2[4],va3[2];
t va3[2];
cx va3[1],va3[2];
t va3[1];
tdg va3[2];
cx va2[4],va3[2];
t va3[2];
h va3[2];
s va2[4];
cx va2[4],va3[1];
tdg va3[1];
cx va2[4],va3[1];
h va3[1];
cx va2[3],va3[1];
tdg va3[1];
cx va2[2],va3[1];
t va3[1];
cx va2[3],va3[1];
tdg va3[1];
cx va2[2],va3[1];
t va3[1];
h va3[1];
t va2[3];
cx va2[2],va2[3];
tdg va2[3];
cx va2[2],va2[3];
h va4[2];
cx va3[2],va4[2];
tdg va4[2];
cx va1[2],va4[2];
t va4[2];
cx va3[2],va4[2];
t va3[2];
tdg va4[2];
cx va1[2],va4[2];
cx va1[2],va3[2];
t va1[2];
tdg va3[2];
cx va1[2],va3[2];
t va4[2];
h va4[2];
h vout[0];
cx addq[0],vout[0];
tdg vout[0];
cx va4[2],vout[0];
t vout[0];
cx addq[0],vout[0];
t addq[0];
tdg vout[0];
cx va4[2],vout[0];
t vout[0];
cx va4[2],addq[0];
tdg addq[0];
cx va4[2],addq[0];
h addq[0];
cx va4[1],addq[0];
tdg addq[0];
cx va4[0],addq[0];
t addq[0];
cx va4[1],addq[0];
tdg addq[0];
cx va4[0],addq[0];
t addq[0];
h addq[0];
cx addq[0],vout[0];
tdg vout[0];
s va4[0];
t va4[1];
cx va4[0],va4[1];
tdg va4[1];
cx va4[0],va4[1];
cx va4[2],vout[0];
t vout[0];
cx addq[0],vout[0];
t addq[0];
tdg vout[0];
cx va4[2],vout[0];
t vout[0];
h vout[0];
s va4[2];
cx va4[2],addq[0];
tdg addq[0];
cx va4[2],addq[0];
h addq[0];
cx va4[1],addq[0];
tdg addq[0];
cx va4[0],addq[0];
t addq[0];
cx va4[1],addq[0];
tdg addq[0];
cx va4[0],addq[0];
t addq[0];
h addq[0];
t va4[1];
cx va4[0],va4[1];
tdg va4[1];
cx va4[0],va4[1];
x ea1[0];
h ea1[0];
cx vout[0],ea1[0];
tdg ea1[0];
cx c1[1],ea1[0];
t ea1[0];
cx vout[0],ea1[0];
t vout[0];
tdg ea1[0];
cx c1[1],ea1[0];
cx c1[1],vout[0];
tdg vout[0];
cx c1[1],vout[0];
h vout[0];
cx c1[0],vout[0];
tdg vout[0];
cx e[0],vout[0];
t vout[0];
cx c1[0],vout[0];
tdg vout[0];
t c1[0];
cx e[0],vout[0];
t vout[0];
h vout[0];
t ea1[0];
cx vout[0],ea1[0];
tdg ea1[0];
cx c1[1],ea1[0];
t ea1[0];
cx vout[0],ea1[0];
t vout[0];
tdg ea1[0];
cx c1[1],ea1[0];
cx c1[1],vout[0];
tdg vout[0];
cx c1[1],vout[0];
h vout[0];
s c1[1];
s c1[1];
t ea1[0];
h ea1[0];
x ea1[1];
h ea1[1];
cx ea1[0],ea1[1];
tdg ea1[1];
cx c2[1],ea1[1];
t ea1[1];
cx ea1[0],ea1[1];
t ea1[0];
tdg ea1[1];
cx c2[1],ea1[1];
cx c2[1],c3[1];
tdg c3[1];
cx c2[1],c3[1];
cx c2[1],ea1[0];
tdg ea1[0];
cx c2[1],ea1[0];
h ea1[0];
cx c2[0],ea1[0];
tdg ea1[0];
cx e[0],ea1[0];
t ea1[0];
cx c2[0],ea1[0];
cx c2[0],c3[0];
tdg c3[0];
cx c2[0],c3[0];
tdg ea1[0];
cx e[0],ea1[0];
t ea1[0];
h ea1[0];
t ea1[1];
cx ea1[0],ea1[1];
tdg ea1[1];
cx c2[1],ea1[1];
t ea1[1];
cx ea1[0],ea1[1];
t ea1[0];
tdg ea1[1];
cx c2[1],ea1[1];
cx c2[1],ea1[0];
tdg ea1[0];
cx c2[1],ea1[0];
s c2[1];
s c2[1];
h ea1[0];
t ea1[1];
h ea1[1];
x ea1[2];
h ea1[2];
cx ea1[1],ea1[2];
tdg ea1[2];
cx c3[1],ea1[2];
t ea1[2];
cx ea1[1],ea1[2];
t ea1[1];
tdg ea1[2];
cx c3[1],ea1[2];
cx c3[1],ea1[1];
tdg ea1[1];
cx c3[1],ea1[1];
h ea1[1];
cx c3[0],ea1[1];
tdg ea1[1];
cx e[0],ea1[1];
t ea1[1];
cx c3[0],ea1[1];
t c3[0];
tdg ea1[1];
cx e[0],ea1[1];
cx e[0],c1[0];
tdg c1[0];
cx e[0],c1[0];
cx c1[0],vout[0];
tdg vout[0];
cx e[0],vout[0];
t vout[0];
cx c1[0],vout[0];
tdg vout[0];
t c1[0];
cx e[0],c1[0];
tdg c1[0];
cx e[0],c1[0];
cx e[0],c2[0];
tdg c2[0];
cx e[0],c2[0];
cx c2[0],ea1[0];
tdg ea1[0];
cx e[0],ea1[0];
t ea1[0];
cx c2[0],ea1[0];
t c2[0];
tdg ea1[0];
cx e[0],ea1[0];
cx e[0],c3[0];
tdg c3[0];
cx e[0],c3[0];
t ea1[0];
h ea1[0];
t ea1[1];
h ea1[1];
t ea1[2];
cx ea1[1],ea1[2];
tdg ea1[2];
cx c3[1],ea1[2];
t ea1[2];
cx ea1[1],ea1[2];
t ea1[1];
tdg ea1[2];
cx c3[1],ea1[2];
cx c3[1],ea1[1];
tdg ea1[1];
cx c3[1],ea1[1];
s c3[1];
h ea1[1];
cx c3[0],ea1[1];
tdg ea1[1];
cx e[0],ea1[1];
t ea1[1];
cx c3[0],ea1[1];
t c3[0];
tdg ea1[1];
cx e[0],ea1[1];
cx e[0],c2[0];
tdg c2[0];
cx e[0],c2[0];
cx e[0],c3[0];
tdg c3[0];
cx e[0],c3[0];
s e[0];
s e[0];
s e[0];
cx e[0],vout[0];
t vout[0];
h vout[0];
t ea1[1];
h ea1[1];
t ea1[2];
h ea1[2];
s ea1[2];
x ea1[3];
h ea1[3];
x ea1[4];
h ea1[4];
x ea1[5];
h ea1[5];
x ea1[6];
h ea1[6];
x ea1[7];
h ea1[7];
x ea1[8];
h ea2[0];
cx ea1[8],ea2[0];
tdg ea2[0];
cx ea1[2],ea2[0];
t ea2[0];
cx ea1[8],ea2[0];
tdg ea2[0];
cx ea1[2],ea2[0];
t ea2[0];
cx ea1[2],ea1[3];
tdg ea1[3];
cx c1[2],ea1[3];
t ea1[3];
cx ea1[2],ea1[3];
tdg ea1[3];
cx c1[2],ea1[3];
t ea1[3];
t ea1[8];
cx ea1[2],ea1[8];
tdg ea1[8];
cx ea1[2],ea1[8];
h ea1[8];
cx ea1[1],ea1[8];
tdg ea1[8];
cx ea1[0],ea1[8];
t ea1[8];
cx ea1[1],ea1[8];
t ea1[1];
tdg ea1[8];
cx ea1[0],ea1[8];
s ea1[0];
cx ea1[0],ea1[1];
tdg ea1[1];
cx ea1[0],ea1[1];
t ea1[8];
h ea1[8];
cx ea1[8],ea2[0];
tdg ea2[0];
cx ea1[2],ea2[0];
t ea2[0];
cx ea1[8],ea2[0];
tdg ea2[0];
cx ea1[2],ea2[0];
t ea2[0];
h ea2[0];
t ea1[8];
cx ea1[2],ea1[8];
t ea1[2];
tdg ea1[8];
cx ea1[2],ea1[8];
cx c1[2],ea1[2];
tdg ea1[2];
cx c1[2],ea1[2];
h ea1[2];
cx c1[0],ea1[2];
tdg ea1[2];
cx e[1],ea1[2];
t ea1[2];
cx c1[0],ea1[2];
t c1[0];
tdg ea1[2];
cx e[1],ea1[2];
t ea1[2];
h ea1[2];
cx ea1[2],ea1[3];
tdg ea1[3];
cx c1[2],ea1[3];
t ea1[3];
cx ea1[2],ea1[3];
t ea1[2];
tdg ea1[3];
cx c1[2],ea1[3];
s c1[2];
s c1[2];
s c1[2];
t ea1[3];
h ea1[3];
cx ea1[3],ea1[4];
tdg ea1[4];
cx c2[2],ea1[4];
t ea1[4];
cx ea1[3],ea1[4];
t ea1[3];
tdg ea1[4];
cx c2[2],ea1[4];
cx c2[2],c3[2];
tdg c3[2];
cx c2[2],c3[2];
cx c2[2],ea1[3];
tdg ea1[3];
cx c2[2],ea1[3];
h ea1[3];
cx c2[0],ea1[3];
tdg ea1[3];
cx e[1],ea1[3];
t ea1[3];
cx c2[0],ea1[3];
t c2[0];
tdg ea1[3];
cx e[1],ea1[3];
t ea1[3];
h ea1[3];
t ea1[4];
cx ea1[3],ea1[4];
tdg ea1[4];
cx c2[2],ea1[4];
t ea1[4];
cx ea1[3],ea1[4];
t ea1[3];
tdg ea1[4];
cx c2[2],ea1[4];
s c2[2];
s c2[2];
cx c2[2],ea1[3];
tdg ea1[3];
cx c2[2],ea1[3];
h ea1[3];
t ea1[4];
h ea1[4];
cx ea1[4],ea1[5];
tdg ea1[5];
cx c3[2],ea1[5];
t ea1[5];
cx ea1[4],ea1[5];
t ea1[4];
tdg ea1[5];
cx c3[2],ea1[5];
cx c3[2],ea1[4];
tdg ea1[4];
cx c3[2],ea1[4];
h ea1[4];
cx c3[0],ea1[4];
tdg ea1[4];
cx e[1],ea1[4];
t ea1[4];
cx c3[0],ea1[4];
t c3[0];
tdg ea1[4];
cx e[1],ea1[4];
s e[1];
s e[1];
s e[1];
cx e[1],c2[0];
tdg c2[0];
cx e[1],c2[0];
cx c2[0],ea1[3];
tdg ea1[3];
cx e[1],ea1[3];
t ea1[3];
cx c2[0],ea1[3];
t c2[0];
tdg ea1[3];
cx e[1],ea1[3];
cx e[1],c3[0];
tdg c3[0];
cx e[1],c3[0];
t ea1[3];
h ea1[3];
s ea1[3];
t ea1[4];
h ea1[4];
t ea1[5];
cx ea1[4],ea1[5];
tdg ea1[5];
cx c3[2],ea1[5];
t ea1[5];
cx ea1[4],ea1[5];
t ea1[4];
tdg ea1[5];
cx c3[2],ea1[5];
s c3[2];
s c3[2];
cx c3[2],ea1[4];
tdg ea1[4];
cx c3[2],ea1[4];
h ea1[4];
cx c3[0],ea1[4];
tdg ea1[4];
cx e[1],ea1[4];
t ea1[4];
cx c3[0],ea1[4];
t c3[0];
tdg ea1[4];
cx e[1],ea1[4];
cx e[1],c1[0];
tdg c1[0];
cx e[1],c1[0];
t ea1[4];
h ea1[4];
t ea1[5];
h ea1[5];
s ea1[5];
h ea1[8];
cx ea1[1],ea1[8];
tdg ea1[8];
cx ea1[0],ea1[8];
t ea1[8];
cx ea1[1],ea1[8];
t ea1[1];
tdg ea1[8];
cx ea1[0],ea1[8];
cx ea1[0],ea1[1];
tdg ea1[1];
cx ea1[0],ea1[1];
t ea1[8];
h ea2[1];
cx ea2[0],ea2[1];
tdg ea2[1];
cx ea1[5],ea2[1];
t ea2[1];
cx ea2[0],ea2[1];
t ea2[0];
tdg ea2[1];
cx ea1[5],ea2[1];
t ea2[1];
cx ea1[5],ea1[6];
tdg ea1[6];
cx c1[2],ea1[6];
t ea1[6];
cx ea1[5],ea1[6];
cx ea1[5],ea2[0];
tdg ea2[0];
cx ea1[5],ea2[0];
h ea2[0];
cx ea1[4],ea2[0];
tdg ea2[0];
cx ea1[3],ea2[0];
t ea2[0];
cx ea1[4],ea2[0];
tdg ea2[0];
cx ea1[3],ea2[0];
t ea2[0];
h ea2[0];
cx ea2[0],ea2[1];
tdg ea2[1];
t ea1[4];
cx ea1[3],ea1[4];
tdg ea1[4];
cx ea1[3],ea1[4];
cx ea1[5],ea2[1];
t ea2[1];
cx ea2[0],ea2[1];
t ea2[0];
tdg ea2[1];
cx ea1[5],ea2[1];
t ea2[1];
h ea2[1];
cx ea1[5],ea2[0];
tdg ea2[0];
t ea1[5];
cx ea1[5],ea2[0];
h ea2[0];
cx ea1[4],ea2[0];
tdg ea2[0];
cx ea1[3],ea2[0];
t ea2[0];
cx ea1[4],ea2[0];
tdg ea2[0];
cx ea1[3],ea2[0];
t ea2[0];
h ea2[0];
s ea2[0];
t ea1[4];
cx ea1[3],ea1[4];
tdg ea1[4];
cx ea1[3],ea1[4];
tdg ea1[6];
cx c1[2],ea1[6];
cx c1[2],ea1[5];
tdg ea1[5];
cx c1[2],ea1[5];
h ea1[5];
cx c1[1],ea1[5];
tdg ea1[5];
cx e[2],ea1[5];
t ea1[5];
cx c1[1],ea1[5];
t c1[1];
tdg ea1[5];
cx e[2],ea1[5];
t ea1[5];
h ea1[5];
t ea1[6];
cx ea1[5],ea1[6];
tdg ea1[6];
cx c1[2],ea1[6];
t ea1[6];
cx ea1[5],ea1[6];
t ea1[5];
tdg ea1[6];
cx c1[2],ea1[6];
cx c1[2],ea1[2];
tdg ea1[2];
cx c1[2],ea1[2];
cx c1[2],ea1[5];
h ea1[2];
cx c1[0],ea1[2];
tdg ea1[2];
cx e[1],ea1[2];
t ea1[2];
cx c1[0],ea1[2];
t c1[0];
tdg ea1[2];
cx e[1],ea1[2];
cx e[1],c1[0];
tdg c1[0];
cx e[1],c1[0];
cx e[1],c2[0];
tdg c2[0];
cx e[1],c2[0];
cx e[1],c3[0];
tdg c3[0];
cx e[1],c3[0];
t ea1[2];
h ea1[2];
tdg ea1[5];
cx c1[2],ea1[5];
h ea1[5];
t ea1[6];
h ea1[6];
cx ea1[6],ea1[7];
tdg ea1[7];
cx c2[2],ea1[7];
t ea1[7];
cx ea1[6],ea1[7];
t ea1[6];
tdg ea1[7];
cx c2[2],ea1[7];
cx c2[2],ea1[6];
tdg ea1[6];
cx c2[2],ea1[6];
h ea1[6];
cx c2[1],ea1[6];
tdg ea1[6];
cx e[2],ea1[6];
t ea1[6];
cx c2[1],ea1[6];
tdg ea1[6];
cx e[2],ea1[6];
t ea1[6];
h ea1[6];
t ea1[7];
cx ea1[6],ea1[7];
tdg ea1[7];
cx c2[2],ea1[7];
t ea1[7];
cx ea1[6],ea1[7];
t ea1[6];
tdg ea1[7];
cx c2[2],ea1[7];
cx c2[2],ea1[6];
tdg ea1[6];
cx c2[2],ea1[6];
t c2[2];
h ea1[6];
t ea1[7];
h ea1[7];
cx ea1[7],ea1[8];
tdg ea1[8];
cx c3[2],ea1[8];
t ea1[8];
cx ea1[7],ea1[8];
t ea1[7];
tdg ea1[8];
cx c3[2],ea1[8];
cx c3[2],ea1[7];
tdg ea1[7];
cx c3[2],ea1[7];
h ea1[7];
cx c3[1],ea1[7];
tdg ea1[7];
cx e[2],ea1[7];
t ea1[7];
cx c3[1],ea1[7];
t c3[1];
tdg ea1[7];
cx e[2],ea1[7];
cx e[2],c2[1];
tdg c2[1];
cx e[2],c2[1];
cx c2[1],ea1[6];
tdg ea1[6];
cx e[2],ea1[6];
t ea1[6];
cx c2[1],ea1[6];
t c2[1];
tdg ea1[6];
cx e[2],ea1[6];
cx e[2],c3[1];
tdg c3[1];
cx e[2],c3[1];
t ea1[6];
h ea1[6];
s ea1[6];
t ea1[7];
h ea1[7];
t ea1[8];
cx ea1[7],ea1[8];
tdg ea1[8];
cx c3[2],ea1[8];
t ea1[8];
cx ea1[7],ea1[8];
t ea1[7];
tdg ea1[8];
cx c3[2],ea1[8];
cx c3[2],ea1[7];
tdg ea1[7];
cx c3[2],ea1[7];
h ea1[7];
cx c3[1],ea1[7];
tdg ea1[7];
cx e[2],ea1[7];
t ea1[7];
cx c3[1],ea1[7];
t c3[1];
tdg ea1[7];
cx e[2],ea1[7];
cx e[2],c1[1];
tdg c1[1];
cx e[2],c1[1];
cx c1[1],ea1[5];
tdg ea1[5];
cx e[2],ea1[5];
t ea1[5];
cx c1[1],ea1[5];
t c1[1];
tdg ea1[5];
cx e[2],ea1[5];
cx e[2],c1[1];
tdg c1[1];
cx e[2],c1[1];
cx e[2],c2[1];
tdg c2[1];
cx e[2],c2[1];
cx e[2],c3[1];
tdg c3[1];
cx e[2],c3[1];
t ea1[5];
h ea1[5];
t ea1[7];
h ea1[7];
t ea1[8];
h ea1[8];
s ea1[8];
h ea2[2];
cx ea2[1],ea2[2];
tdg ea2[2];
cx ea1[8],ea2[2];
t ea2[2];
cx ea2[1],ea2[2];
t ea2[1];
tdg ea2[2];
cx ea1[8],ea2[2];
t ea2[2];
cx ea1[8],ea2[1];
tdg ea2[1];
cx ea1[8],ea2[1];
h ea2[1];
cx ea1[7],ea2[1];
tdg ea2[1];
cx ea1[6],ea2[1];
t ea2[1];
cx ea1[7],ea2[1];
tdg ea2[1];
cx ea1[6],ea2[1];
t ea2[1];
h ea2[1];
cx ea2[1],ea2[2];
tdg ea2[2];
t ea1[7];
cx ea1[6],ea1[7];
tdg ea1[7];
cx ea1[6],ea1[7];
cx ea1[8],ea2[2];
t ea2[2];
cx ea2[1],ea2[2];
t ea2[1];
tdg ea2[2];
cx ea1[8],ea2[2];
t ea2[2];
h ea2[2];
s ea2[2];
cx ea1[8],ea2[1];
tdg ea2[1];
cx ea1[8],ea2[1];
h ea2[1];
cx ea1[7],ea2[1];
tdg ea2[1];
cx ea1[6],ea2[1];
t ea2[1];
cx ea1[7],ea2[1];
tdg ea2[1];
cx ea1[6],ea2[1];
t ea2[1];
h ea2[1];
t ea1[7];
cx ea1[6],ea1[7];
tdg ea1[7];
cx ea1[6],ea1[7];
h eout[0];
cx addq1[0],eout[0];
tdg eout[0];
cx ea2[2],eout[0];
t eout[0];
cx addq1[0],eout[0];
t addq1[0];
tdg eout[0];
cx ea2[2],eout[0];
t eout[0];
cx ea2[2],addq1[0];
tdg addq1[0];
cx ea2[2],addq1[0];
h addq1[0];
cx ea2[1],addq1[0];
tdg addq1[0];
cx ea2[0],addq1[0];
t addq1[0];
cx ea2[1],addq1[0];
tdg addq1[0];
cx ea2[0],addq1[0];
t addq1[0];
h addq1[0];
cx addq1[0],eout[0];
tdg eout[0];
t ea2[1];
cx ea2[0],ea2[1];
tdg ea2[1];
cx ea2[0],ea2[1];
cx ea2[2],eout[0];
t eout[0];
cx addq1[0],eout[0];
t addq1[0];
tdg eout[0];
cx ea2[2],eout[0];
t eout[0];
h eout[0];
cx ea2[2],addq1[0];
tdg addq1[0];
cx ea2[2],addq1[0];
h addq1[0];
cx ea2[1],addq1[0];
tdg addq1[0];
cx ea2[0],addq1[0];
t addq1[0];
cx ea2[1],addq1[0];
tdg addq1[0];
cx ea2[0],addq1[0];
t addq1[0];
h addq1[0];
t ea2[1];
cx ea2[0],ea2[1];
tdg ea2[1];
cx ea2[0],ea2[1];
h out[0];
cx eout[0],out[0];
tdg out[0];
cx vout[0],out[0];
t out[0];
cx eout[0],out[0];
t eout[0];
tdg out[0];
cx vout[0],out[0];
t out[0];
h out[0];
cx vout[0],eout[0];
tdg eout[0];
t vout[0];
cx vout[0],eout[0];
