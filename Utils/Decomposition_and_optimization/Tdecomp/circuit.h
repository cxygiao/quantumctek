#ifndef CIRCUIT_H_
#define CIRCUIT_H_
#include<string>
#include<vector>
#include<list>

using namespace std;

#define locaN 2
#define locaN2 1 //换门

struct Gate
{
	int id; //门序号
	string name;  //量子门名称   
	vector<string> lines;  //门的线    
	vector<string> controls;  //控制线
	vector<string> targets;  //目标线
	int c;  //控制位的数量
	int NNC; //最近邻代价
};

class Circuit
{
private:
	list<Gate> gates;
	vector<string> wires; //存电路的线
	int n; //电路线数
	int gnum; //原始电路门的个数
	

public:
	Circuit();
	~Circuit();
    list<Gate> get_gate(){return gates;} //访问私有成员变量
	int get_gnum(){return gnum;} //访问私有成员变量
	vector<string> get_wire(){return wires;}

	//读real文件
	void initial(); //读.real文件
	
	//分解电路MCT_NCV
	void toffTransNcv( Gate tempToffGate, list<Gate> &gateVar );  //MCT门库转换成NCV门库
	
	//最近邻前瞻算法
	int ngLookahead( list<Gate>::iterator iter, list<Gate> &gateVar, vector<string> &line );  //Algorithm_1：计算downSwapCount的值   
	int ngLookahead_1( list<Gate>::iterator iter, list<Gate> &gateVar ); //计算downSwapCost
	int ngLookahead_2( list<Gate>::iterator iter, list<Gate> &gateVar );  //计算upSwapCost
	int ngLookahead_3( list<Gate>::iterator iter,list <Gate> &gateVar ); //计算upDownSwapCost
	int FindGr(list<Gate>::iterator iter,list<Gate>::iterator moveit,list <Gate> &gateVar); //确定Gr
	int calculateDGpr(list<Gate>::iterator iter,list<Gate>::iterator gr); //计算GpGr的dSC
    int calculateUGpr(list<Gate>::iterator iter,list<Gate>::iterator gr); //计算GpGr的uSC
	void insertSwap(list<Gate> &gateVar, vector<string> &line);  //插入交换门，实现最近邻，算法2
	
	//插入交换门，线序改变
	void insertSwapPro( list<Gate>::iterator it, char swapTempConLine, char swapTempTarLine, list<Gate> &gateVar);  //插入SWAP门
	//对G.p做downSwap后，对后面满足条件的门的线位进行改变。以Swap门的线位为依据进行变化(注意复用)。
	void changeLineDown( list<Gate>::iterator it, char swapTempConLine, char swapTempTarLine, list<Gate> &gateVar);
	//对G.p做upSwap后，对后面满足条件的门的线位进行改变，以Swap门的线位为依据进行变化(注意复用)。
	void changeLineUp( list<Gate>::iterator it, char swapTempConLine, char swapTempTarLine, list<Gate> &gateVar);
	
	//类型转换
	void charToString(const char &charVar,string &stringVar); //char转化为string
	
	//对量子电路的基本操作
    void updateNNC(list<Gate> &gateVar);  //计算单个门的NNC，更新mSCn的数值(注意及时更新)
	void updateGate(list<Gate> &gateVar); //更新门
	void reorderGateId(list<Gate> &gateVar); //对电路进行重新编号
	void showCir(list<Gate> &gateVar);  //显示电路
	void removeSwap(list <Gate> &gateVar);  //使用deletion rule删除符合条件的swap门
	int calculateNNC(list <Gate> &gateVar);  //计算量子电路的最近邻代价
	int calculateSgate(list <Gate> &gateVar);  //计算电路的交换门的个数
	int calculateQC(list <Gate> &gateVar);  //统计电路量子代价
	void removeGate(list<Gate> &gateVar); //删除冗余门
	//void ReorderGate(list<Gate> &gateVar); //调整更新门的顺序，将可移动且NNC较小的量子门往左移动

	void ReorderLine(list <Gate> &gateVar,vector<string> &line); //调整线序，为粘合电路服务

	//操作集
	void operation(list<Gate> &gateVar,vector<string> &line); //对电路的具体操作

	void reorderGate(list<Gate> &gateVar);
	int changeGateOrder(list<Gate>::iterator iter, list<Gate> &gateVar);


};

    



#endif