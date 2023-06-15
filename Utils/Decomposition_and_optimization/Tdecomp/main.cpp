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
	clock_t start,finish; //ͳ������ʱ��
	double totaltime;

	circuit.initial();
	start = clock();
	circuit.operation(circuit.get_gate(),circuit.get_wire());
	gateVar = circuit.get_gate();
	//���չʾ                                  
	circuit.showCir(gateVar);   
	cout<<"��·��ӵĽ����ŵĸ���Ϊ��"<<circuit.calculateSgate(gateVar)<<endl;
	cout<<"���ӵ�·������ڴ��ۣ�" <<circuit.calculateNNC(gateVar)<<endl;
	cout<<"��·�����Ӵ��ۣ�" <<circuit.calculateQC(gateVar)<<endl;

	finish = clock();
	totaltime = (double)(finish - start)/CLOCKS_PER_SEC;
	cout<<"����ʱ��Ϊ"<<totaltime<<"��"<<endl;
			


	system("pause");
	return 0;

}