OPENQASM 2.0;
include "qelib1.inc";

qreg node[5];
creg c[5];
cx node[3],node[4];
cx node[4],node[3];
cx node[1],node[3];
cx node[3],node[1];
cx node[2],node[1];
cx node[3],node[4];
cx node[1],node[2];
cx node[1],node[2];
cx node[0],node[1];
gate bridge bridgeq0,bridgeq1,bridgeq2 {
u3(0.5*pi,1.5*pi,0.5*pi) bridgeq0;
u3(0.5*pi,1.5*pi,0.5*pi) bridgeq1;
u3(0.5*pi,1.5*pi,0.5*pi) bridgeq2;
u3(0.0*pi,1.5*pi,1.0*pi) bridgeq0;
u3(0.0*pi,1.5*pi,1.5*pi) bridgeq1;
u3(0.0*pi,1.5*pi,1.5*pi) bridgeq2;
u3(1.5*pi,0.0*pi,0.0*pi) bridgeq0;
u3(0.5*pi,1.5*pi,0.5*pi) bridgeq1;
u3(0.5*pi,1.5*pi,0.5*pi) bridgeq2;
cx bridgeq0,bridgeq1;
u3(0.5*pi,0.0*pi,0.5*pi) bridgeq0;
u3(1.0*pi,1.5*pi,0.5*pi) bridgeq1;
u3(1.0*pi,1.5*pi,0.5*pi) bridgeq0;
u3(1.0*pi,0.0*pi,0.0*pi) bridgeq1;
u3(0.5*pi,0.0*pi,1.0*pi) bridgeq0;
u3(0.5*pi,1.5*pi,0.5*pi) bridgeq1;
u3(0.5*pi,1.5*pi,0.5*pi) bridgeq0;
u3(0.0*pi,1.5*pi,1.0*pi) bridgeq1;
u3(0.0*pi,1.5*pi,1.0*pi) bridgeq0;
u3(1.5*pi,0.0*pi,0.0*pi) bridgeq1;
u3(1.5*pi,0.0*pi,0.0*pi) bridgeq0;
cx bridgeq1,bridgeq2;
u3(0.5*pi,0.0*pi,0.5*pi) bridgeq1;
u3(1.0*pi,1.5*pi,0.5*pi) bridgeq2;
u3(1.0*pi,1.5*pi,0.5*pi) bridgeq1;
u3(1.0*pi,0.0*pi,0.0*pi) bridgeq2;
u3(0.5*pi,0.0*pi,1.0*pi) bridgeq1;
u3(0.5*pi,1.5*pi,0.5*pi) bridgeq2;
u3(0.5*pi,1.5*pi,0.5*pi) bridgeq1;
u3(0.0*pi,1.5*pi,1.5*pi) bridgeq2;
u3(0.0*pi,1.5*pi,1.5*pi) bridgeq1;
u3(0.5*pi,1.5*pi,0.5*pi) bridgeq2;
u3(0.5*pi,1.5*pi,0.5*pi) bridgeq1;
cx bridgeq0,bridgeq1;
u3(0.5*pi,0.0*pi,0.5*pi) bridgeq0;
u3(1.0*pi,1.5*pi,0.5*pi) bridgeq1;
u3(1.0*pi,1.5*pi,0.5*pi) bridgeq0;
u3(1.0*pi,0.0*pi,0.0*pi) bridgeq1;
u3(0.5*pi,0.0*pi,1.0*pi) bridgeq0;
u3(0.5*pi,1.5*pi,0.5*pi) bridgeq1;
u3(0.0*pi,1.5*pi,1.0*pi) bridgeq1;
u3(1.5*pi,0.0*pi,0.0*pi) bridgeq1;
cx bridgeq1,bridgeq2;
u3(0.5*pi,0.0*pi,0.5*pi) bridgeq1;
u3(1.0*pi,1.5*pi,0.5*pi) bridgeq2;
u3(1.0*pi,1.5*pi,0.5*pi) bridgeq1;
u3(1.0*pi,0.0*pi,0.0*pi) bridgeq2;
u3(0.5*pi,0.0*pi,1.0*pi) bridgeq1;
}
bridge node[2],node[1],node[0];
cx node[2],node[1];
cx node[0],node[1];
bridge node[2],node[1],node[0];
cx node[1],node[2];
cx node[1],node[3];
bridge node[4],node[3],node[1];
cx node[4],node[3];
cx node[1],node[3];
bridge node[4],node[3],node[1];
cx node[1],node[2];
cx node[3],node[4];
cx node[0],node[1];
cx node[3],node[4];
bridge node[2],node[1],node[0];
cx node[2],node[1];
cx node[0],node[1];
bridge node[2],node[1],node[0];
cx node[1],node[2];
cx node[1],node[3];
bridge node[4],node[3],node[1];
cx node[4],node[3];
cx node[1],node[3];
bridge node[4],node[3],node[1];
measure node[1] -> c[3];
cx node[3],node[4];
swap node[2],node[1];
cx node[1],node[3];
cx node[0],node[1];
bridge node[3],node[1],node[0];
cx node[3],node[1];
cx node[0],node[1];
swap node[3],node[1];
cx node[1],node[0];
cx node[3],node[1];
measure node[1] -> c[2];
cx node[3],node[4];
swap node[0],node[1];
cx node[1],node[3];
bridge node[4],node[3],node[1];
cx node[4],node[3];
cx node[1],node[3];
bridge node[4],node[3],node[1];
cx node[3],node[4];
measure node[4] -> c[1];
cx node[1],node[3];
measure node[1] -> c[0];
measure node[3] -> c[4];
