#include <vector>
#include <iostream>
#include <fstream>
#include "time.h"
#include "circuit.h"
using namespace std;

int main()
{
	Circuit circuit;
	list<Gate> gateVar;
	clock_t start,finish; //统计运行时间
	double totaltime;

	circuit.initial();
	start = clock();
	circuit.operation(circuit.get_gate(),circuit.get_wire());
	gateVar = circuit.get_gate();
	//结果展示                                  
	circuit.showCir(gateVar);   
	cout<<"电路添加的交换门的个数为："<<circuit.calculateSgate(gateVar)<<endl;
	cout<<"量子电路的最近邻代价：" <<circuit.calculateNNC(gateVar)<<endl;
	cout<<"电路的量子代价：" <<circuit.calculateQC(gateVar)<<endl;

	finish = clock();
	totaltime = (double)(finish - start)/CLOCKS_PER_SEC;
	cout<<"运行时间为"<<totaltime<<"秒"<<endl;
			


	system("pause");
	return 0;

}