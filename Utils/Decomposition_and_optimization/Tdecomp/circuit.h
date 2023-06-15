#ifndef CIRCUIT_H_
#define CIRCUIT_H_
#include<string>
#include<vector>
#include<list>

using namespace std;

#define locaN 2
#define locaN2 1 //����

struct Gate
{
	int id; //�����
	string name;  //����������   
	vector<string> lines;  //�ŵ���    
	vector<string> controls;  //������
	vector<string> targets;  //Ŀ����
	int c;  //����λ������
	int NNC; //����ڴ���
};

class Circuit
{
private:
	list<Gate> gates;
	vector<string> wires; //���·����
	int n; //��·����
	int gnum; //ԭʼ��·�ŵĸ���
	

public:
	Circuit();
	~Circuit();
    list<Gate> get_gate(){return gates;} //����˽�г�Ա����
	int get_gnum(){return gnum;} //����˽�г�Ա����
	vector<string> get_wire(){return wires;}

	//��real�ļ�
	void initial(); //��.real�ļ�
	
	//�ֽ��·MCT_NCV
	void toffTransNcv( Gate tempToffGate, list<Gate> &gateVar );  //MCT�ſ�ת����NCV�ſ�
	
	//�����ǰհ�㷨
	int ngLookahead( list<Gate>::iterator iter, list<Gate> &gateVar, vector<string> &line );  //Algorithm_1������downSwapCount��ֵ   
	int ngLookahead_1( list<Gate>::iterator iter, list<Gate> &gateVar ); //����downSwapCost
	int ngLookahead_2( list<Gate>::iterator iter, list<Gate> &gateVar );  //����upSwapCost
	int ngLookahead_3( list<Gate>::iterator iter,list <Gate> &gateVar ); //����upDownSwapCost
	int FindGr(list<Gate>::iterator iter,list<Gate>::iterator moveit,list <Gate> &gateVar); //ȷ��Gr
	int calculateDGpr(list<Gate>::iterator iter,list<Gate>::iterator gr); //����GpGr��dSC
    int calculateUGpr(list<Gate>::iterator iter,list<Gate>::iterator gr); //����GpGr��uSC
	void insertSwap(list<Gate> &gateVar, vector<string> &line);  //���뽻���ţ�ʵ������ڣ��㷨2
	
	//���뽻���ţ�����ı�
	void insertSwapPro( list<Gate>::iterator it, char swapTempConLine, char swapTempTarLine, list<Gate> &gateVar);  //����SWAP��
	//��G.p��downSwap�󣬶Ժ��������������ŵ���λ���иı䡣��Swap�ŵ���λΪ���ݽ��б仯(ע�⸴��)��
	void changeLineDown( list<Gate>::iterator it, char swapTempConLine, char swapTempTarLine, list<Gate> &gateVar);
	//��G.p��upSwap�󣬶Ժ��������������ŵ���λ���иı䣬��Swap�ŵ���λΪ���ݽ��б仯(ע�⸴��)��
	void changeLineUp( list<Gate>::iterator it, char swapTempConLine, char swapTempTarLine, list<Gate> &gateVar);
	
	//����ת��
	void charToString(const char &charVar,string &stringVar); //charת��Ϊstring
	
	//�����ӵ�·�Ļ�������
    void updateNNC(list<Gate> &gateVar);  //���㵥���ŵ�NNC������mSCn����ֵ(ע�⼰ʱ����)
	void updateGate(list<Gate> &gateVar); //������
	void reorderGateId(list<Gate> &gateVar); //�Ե�·�������±��
	void showCir(list<Gate> &gateVar);  //��ʾ��·
	void removeSwap(list <Gate> &gateVar);  //ʹ��deletion ruleɾ������������swap��
	int calculateNNC(list <Gate> &gateVar);  //�������ӵ�·������ڴ���
	int calculateSgate(list <Gate> &gateVar);  //�����·�Ľ����ŵĸ���
	int calculateQC(list <Gate> &gateVar);  //ͳ�Ƶ�·���Ӵ���
	void removeGate(list<Gate> &gateVar); //ɾ��������
	//void ReorderGate(list<Gate> &gateVar); //���������ŵ�˳�򣬽����ƶ���NNC��С�������������ƶ�

	void ReorderLine(list <Gate> &gateVar,vector<string> &line); //��������Ϊճ�ϵ�·����

	//������
	void operation(list<Gate> &gateVar,vector<string> &line); //�Ե�·�ľ������

	void reorderGate(list<Gate> &gateVar);
	int changeGateOrder(list<Gate>::iterator iter, list<Gate> &gateVar);


};

    



#endif