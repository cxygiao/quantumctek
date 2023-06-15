#include "circuit.h"
#include <fstream>
#include <sstream>
#include <iterator>
#include <iostream>
#include <iomanip>

Circuit::Circuit()
{
}

Circuit::~Circuit()
{
}

//读.real文件，存电路
void Circuit::initial()
{
	//初始化、定义变量
	gates.clear(); //清空门
	n = 0;  //线根数
	gnum = 0;  //原始门个数
	ifstream inCircuit;
	string readFileName; //读取的文件名
	
	cout<<"请输入要读文件名:";
	cin>>readFileName;
	inCircuit.open("F:\\workspace\\Paper\\NearestNeighborCircuit\\NearestNeighborCircuit\\Benchmark\\" + readFileName);
	if (!inCircuit.is_open())  
	{
		cout<<"\n不能打开文件！"<<endl;
		cout<<"程序终止！"<<endl;
	}

	//按行获取数据
	string gateDataStr;  
	string lable;
	while ( getline( inCircuit,gateDataStr ) ) //读入一行数据，gateData为缓存.
	{
		istringstream record(gateDataStr);
		record >> lable;
		if (lable == ".numvars") //线数
		{
			record >> n;
		}
		if (lable == ".variables") //存线
		{
			string var;
			while (record >> var)
				wires.push_back(var);
		}
		if (lable == ".begin")
		{
			while ( getline( inCircuit,gateDataStr ) )
			{
				if (gateDataStr == ".end")
					break;
				else if (gateDataStr == "") //遇空行读下一行，直至.end时才结束读取
				{

				}
				else
				{
					istringstream record(gateDataStr);
					gnum++;
					Gate g;
					string wire; 	
					g.id = gnum;
					record >> g.name; //门类型
					while (record >> wire)
					{			
						g.controls.push_back(wire);	
						g.lines.push_back(wire);
					}
					g.targets.push_back(g.controls.back()); 
					g.controls.pop_back(); 
					g.c = g.controls.size(); //控制位的个数
					g.NNC = -1; //初始化NNC
					gates.push_back(g);
				}
			}
		}
	}

}

//char转换成string
void Circuit:: charToString(const char &charVar,string &stringVar)
{
	stringstream stream;
	stream << charVar;
	stringVar = stream.str();
}

//对电路进行重新编号
void Circuit:: reorderGateId(list<Gate> &gateVar)
{
	int i = 1;
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end(); ++it, ++i)
	{
		it->id = i;
	}
}

//显示电路
void Circuit:: showCir(list<Gate> &gateVar)  
{
	cout<<setfill(' ')<<setw(20)<<"id"<<setfill(' ')<<setw(20)<<"controls"
		<<setfill(' ')<<setw(20)<<"targets"<<endl;
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end(); ++it)
	{
		if (it->name == "t1")
		{
			cout<<"NOT门"<<setfill(' ')<<setw(12)<<it->id<<setfill(' ')<<setw(20)<<char(32)
				<<setfill(' ')<<setw(20)<<it->targets.at(0)<<endl;
		} 
		else if (it->name == "t2")
		{
			cout<<"CNOT门"<<setfill(' ')<<setw(11)<<it->id<<setfill(' ')<<setw(20)<<it->controls.at(0)   
				<<setfill(' ')<<setw(20)<<it->targets.at(0)<<endl;
		} 
		else if (it->name == "v2")
		{
			cout<<"V门"<<setfill(' ')<<setw(14)<<it->id<<setfill(' ')<<setw(20)<<it->controls.at(0)
				<<setfill(' ')<<setw(20)<<it->targets.at(0)<<endl;
		} 
		else if (it->name == "v+") 
		{
			cout<<"V+门"<<setfill(' ')<<setw(13)<<it->id<<setfill(' ')<<setw(20)<<it->controls.at(0)
				<<setfill(' ')<<setw(20)<<it->targets.at(0)<<endl;
		}
		else  
		{
			cout<<"SWAP门"<<setfill(' ')<<setw(11)<<it->id<<setfill(' ')<<setw(20)<<it->targets.at(0)
				<<setfill(' ')<<setw(20)<<it->targets.at(1)<<endl;
		}
	}
}

//转换MCT
void Circuit:: toffTransNcv(Gate tempToffGate, list<Gate> &gateVar) 
{
	vector<Gate> toffToNcv; //一个Toffoli门转换为5个基本量子门
	vector<Gate> mctdec; //分解控制位大于2的Toffoli门
	vector<string> emptyline; //存放空闲线
	int emptylineNum = 0; //空闲线的个数

	//控制位是否>2
	if(tempToffGate.c == 2) //分解2控制位toffoli门
	{
		//分情况讨论，按规则限定好
		if ( tempToffGate.NNC == -1 )  //设定刚输入时均为-1
		{
			for ( int i = 0; i < 5; ++i )  
			{
				Gate tempGate;  //临时变量用于量子门输入的缓存
				tempGate.id = tempToffGate.id + i;  //更新由Toffoli门分解得到的基本量子门的ID
				if( i == 0 || i == 2 )
				{
					tempGate.controls.push_back(tempToffGate.controls.at(1)); 
					tempGate.lines.push_back(tempToffGate.controls.at(1));
				}
				else
				{
					tempGate.controls.push_back(tempToffGate.controls.at(0));
					tempGate.lines.push_back(tempToffGate.controls.at(0));
				}
				if ( i == 0 || i == 4 )
				{
					tempGate.name = "v2";
					tempGate.c = 1;
					tempGate.targets.push_back(tempToffGate.targets.at(0));
					tempGate.lines.push_back(tempToffGate.targets.at(0));
				}
				else if( i == 1 || i == 3 )
				{
					tempGate.name = "t2";
					tempGate.c = 1;
					tempGate.targets.push_back(tempToffGate.controls.at(1));
					tempGate.lines.push_back(tempToffGate.controls.at(1));
				}
				else
				{
					tempGate.name = "v+";
					tempGate.c = 1;
					tempGate.targets.push_back(tempToffGate.targets.at(0));
					tempGate.lines.push_back(tempToffGate.targets.at(0));
				}
				toffToNcv.push_back(tempGate);  //将临时变量的缓存内容存到toffToNcv数组中
			}
		}
		else if ( tempToffGate.NNC == -2 ) //转换为转置
		{
			for ( int i = 0; i < 5; ++i )  
			{
				Gate tempGate;  //临时变量用于量子门输入的缓存
				tempGate.id = tempToffGate.id + i;  //更新由Toffoli门分解得到的基本量子门的ID
				if( i == 0 || i == 1 || i == 3 )
				{
					tempGate.controls.push_back(tempToffGate.controls.at(0)); 
					tempGate.lines.push_back(tempToffGate.controls.at(0));
				}
				else
				{
					tempGate.controls.push_back(tempToffGate.controls.at(1));
					tempGate.lines.push_back(tempToffGate.controls.at(1));
				}
				if ( i == 0 || i == 4 )
				{
					tempGate.name = "v+";
					tempGate.c = 1;
					tempGate.targets.push_back(tempToffGate.targets.at(0));
					tempGate.lines.push_back(tempToffGate.targets.at(0));
				}
				else if( i == 1 || i == 3 )
				{
					tempGate.name = "t2";
					tempGate.c = 1;
					tempGate.targets.push_back(tempToffGate.controls.at(1));
					tempGate.lines.push_back(tempToffGate.controls.at(1));
				}
				else
				{
					tempGate.name = "v2";
					tempGate.c = 1;
					tempGate.targets.push_back(tempToffGate.targets.at(0));
					tempGate.lines.push_back(tempToffGate.targets.at(0));
				}
				toffToNcv.push_back(tempGate);  //将临时变量的缓存内容存到toffToNcv数组中
			}
		}
		
		
		//将分解toffoli门后得到的NCV门有序插入到量子电路中
		list <Gate>::reverse_iterator it;
		for (it = gateVar.rbegin(); it->name != tempToffGate.name; ++it)
		{
			//找到指向tempToffGate的it
		}
		//在tempToffGate门之前插入分解之后的NCV门库
		list <Gate> ::iterator iter((++it).base());
		gateVar.insert(iter, toffToNcv.begin(), toffToNcv.end()); 
		//根据位置删除量子电路中的Toffoli门(tempToffGate) (*****注意erase()的返回值*****)
		it = list<Gate>::reverse_iterator(gateVar.erase(it.base())); 
		vector <Gate>().swap(toffToNcv); //释放内存
	}
	//控制位>2
	else
	{
		//判断是否需要添加辅助位
		if ( tempToffGate.c == n - 1 ) //需要添加辅助位
		{
			string b;
			charToString('a'+n,b);
			wires.push_back(b);
			n++;		
		}
		
		//判断空闲线是哪几条
		for (int i = 0; i < n; i++)
		{
			int flag = 0;
			for (int j = 0; j <= tempToffGate.c; j++) //取等号表示要加一个目标位的线
			{
				if ( wires.at(i) == tempToffGate.lines.at(j) )
				{
					flag = 1;
					break; //跳出内循环
				}
			}
			if ( flag == 0 ) //说明此线空闲
			{
				emptylineNum++;
				emptyline.push_back(wires.at(i));
			}
		}

		//判断属于哪一种分解方法
		if ( tempToffGate.c <= (int)ceil(n/2.0) ) //属于第一种
		{
			//产生新的门
			
			//左侧一半
			for (int i = 0; i < tempToffGate.c-2; i++)
			{
				Gate tempGate;  //临时变量用于量子门输入的缓存
				string tempname = "t" + to_string(3) ;//符号上要多一位
				tempGate.name = tempname;
				tempGate.id = tempToffGate.id + i;  //更新由Toffoli门分解得到的基本量子门的ID
				tempGate.c = 2; //转换后均是2控制Toffoli
				tempGate.NNC = -1; //为-1时直接转换，-2时转换成转置
				tempGate.controls.push_back(tempToffGate.controls.at(tempToffGate.c - 1 - i));
				tempGate.lines.push_back(tempToffGate.controls.at(tempToffGate.c - 1 - i));
				tempGate.controls.push_back(emptyline.at(emptylineNum-1-i)); //在空闲线的位置
				tempGate.lines.push_back(emptyline.at(emptylineNum-1-i));
				if ( i == 0) //第一个门
				{
					tempGate.targets.push_back(tempToffGate.targets.at(0));
					tempGate.lines.push_back(tempToffGate.targets.at(0));
					mctdec.push_back(tempGate);
				}
				else
				{
					tempGate.targets.push_back(mctdec.at(i-1).controls.at(1)); //与前一个门的第二个控制位相同
					tempGate.lines.push_back(mctdec.at(i-1).controls.at(1));
					mctdec.push_back(tempGate);
				}
			}
			
			//中间最高的门
			Gate tempGate;  //临时变量用于量子门输入的缓存
			string tempname = "t" + to_string(3) ;//符号上要多一位
			tempGate.name = tempname;
			tempGate.id = tempToffGate.id + tempToffGate.c-2;  //更新由Toffoli门分解得到的基本量子门的ID
			tempGate.c = 2; //转换后均是2控制Toffoli
			tempGate.NNC = -1; //为-1时直接转换，-2时转换成转置
			tempGate.controls.push_back(tempToffGate.controls.at(0));
			tempGate.controls.push_back(tempToffGate.controls.at(1));
			tempGate.targets.push_back(mctdec.at(tempToffGate.c-3).controls.at(1));
			mctdec.push_back(tempGate);
			
			//左侧另一半
			for (int i = 0; i < tempToffGate.c-2; i++)
			{
				Gate tempGate;  //临时变量用于量子门输入的缓存
				string tempname = "t" + to_string(3) ;//符号上要多一位
				tempGate.name = tempname;
				tempGate.id = tempToffGate.id + tempToffGate.c-1 + i;  //更新由Toffoli门分解得到的基本量子门的ID
				tempGate.c = 2; //转换后均是2控制Toffoli
				tempGate.NNC = -2; //为-1时直接转换，-2时转换成转置
				tempGate.controls.push_back(mctdec.at(tempToffGate.c-3-i).controls.at(0));
				tempGate.lines.push_back(mctdec.at(tempToffGate.c-3-i).controls.at(0));
				tempGate.controls.push_back(mctdec.at(tempToffGate.c-3-i).controls.at(1)); 
				tempGate.lines.push_back(mctdec.at(tempToffGate.c-3-i).controls.at(1));
				tempGate.targets.push_back(mctdec.at(tempToffGate.c-3-i).targets.at(0)); 
				tempGate.lines.push_back(mctdec.at(tempToffGate.c-3-i).targets.at(0));
				mctdec.push_back(tempGate);
			}	
			
			//右侧  将mectdec中除首尾依次压进去
			vector <Gate> tempmctdec;  //临时存储截取的门
			for ( vector <Gate>::iterator it = mctdec.begin()+1; it < mctdec.end()-1; it++)
			{
				Gate tempGate;  //临时变量用于量子门输入的缓存
				tempGate.name = it->name;
				tempGate.id = it->id;  
				tempGate.c = it->c; //转换后均是2控制Toffoli
				if ( it->controls.at(0) != tempToffGate.controls.at(0) ) //不是最高的门 NNC相同
				{
					tempGate.NNC = it->NNC;
				}
				else  //是最高的门 NNC相反，取-2
				{
					tempGate.NNC = -2;
				}
				tempGate.controls = it->controls;
				tempGate.targets = it->targets;
				tempmctdec.push_back(tempGate);
			}
			//将两个vector连接
			mctdec.insert(mctdec.end(),tempmctdec.begin(),tempmctdec.end());	
			
			//插入新门，删除原门
			list <Gate>::reverse_iterator it;
			for (it = gateVar.rbegin(); it->name != tempToffGate.name; ++it)
			{
				//找到指向tempToffGate的it
			}
			//在tempToffGate门之前插入分解之后的NCV门库
			list <Gate> ::iterator iter((++it).base());
			gateVar.insert(iter, mctdec.begin(), mctdec.end());
			//根据位置删除量子电路中的Toffoli门(tempToffGate) (*****注意erase()的返回值*****)
			it = list<Gate>::reverse_iterator(gateVar.erase(it.base()));  
			vector <Gate>().swap(mctdec);
		}
		else //属于第二种
		{
			//产生新门
			for (int i = 0; i < 4; i++)
			{
				Gate tempGate;  //临时变量用于量子门输入的缓存
				tempGate.id = tempToffGate.id + i;  //更新由Toffoli门分解得到的基本量子门的ID
				if ( i == 0 || i == 2 )
				{
					string tempname = "t" + to_string((int)(ceil(n/2.0)+1)) ;//符号上要多一位
					tempGate.name = tempname;
					tempGate.c = (int)(ceil(n/2.0)); //存放控制位的个数
					for (int j = 0; j < tempGate.c; j++)
					{
						tempGate.controls.push_back(tempToffGate.controls.at(j));
						tempGate.lines.push_back(tempToffGate.controls.at(j));
					}
					tempGate.targets.push_back(emptyline.at(emptylineNum-1));
					tempGate.lines.push_back(emptyline.at(emptylineNum-1));
					mctdec.push_back(tempGate);
				}
				else
				{
					string tempname = "t" + to_string((tempToffGate.c - (int)ceil(n/2.0) + 2)) ;//符号上要多一位
					tempGate.name = tempname;
					tempGate.c = tempToffGate.c - (int)ceil(n/2.0) + 1; //存放控制位的个数
					if ( tempGate.c <= 2 ) //直接进入情况一的化解
					{
						if ( i == 1 )
						{
							tempGate.NNC = -1;
						}
						else //i == 3
						{
							tempGate.NNC = -2;
						}
					}
					for (int j = 0; j < tempGate.c - 1; j++)
					{
						tempGate.controls.push_back(tempToffGate.controls.at(ceil(n/2.0)+j));  
						tempGate.lines.push_back(tempToffGate.controls.at(ceil(n/2.0)+j));
					}
					tempGate.controls.push_back(mctdec.at(0).targets.at(0));
					tempGate.lines.push_back(mctdec.at(0).targets.at(0));
					tempGate.targets.push_back(tempToffGate.targets.at(0));
					tempGate.lines.push_back(tempToffGate.targets.at(0));
					mctdec.push_back(tempGate);
				}
			}
			
			//删除原门
			list <Gate>::reverse_iterator it;
			for (it = gateVar.rbegin(); it->name != tempToffGate.name; ++it)
			{
				//找到指向tempToffGate的it
			}
			//在tempToffGate门之前插入分解之后的NCV门库
			list <Gate> ::iterator iter((++it).base());
			gateVar.insert(iter, mctdec.begin(), mctdec.end());
			//根据位置删除量子电路中的Toffoli门(tempToffGate) (*****注意erase()的返回值*****)
			it = list<Gate>::reverse_iterator(gateVar.erase(it.base()));  
			vector <Gate>().swap(mctdec);
		}
	}
}

//删除冗余门
void Circuit:: removeGate(list<Gate> &gateVar)
{
	vector<string> temptargetss; //临时存储目标线
	vector<string> tempcontrolss; //临时存储控制线
	int flag = 0; //控制是否有门可以删去
	int i = 0;
	int add = 0; //控制是否需要多加1
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end();)  
	{
		if ( i == gateVar.size()-1 )  //电路只有一个门
		{
			break;
		}
		if ( it == (--gateVar.end()) )  //遍历到最后一个门
		{
			break;
		}
		if ( it->name == "v2" || it->name == "v+" || it->name == "t2" )  //v和v+门、两个cnot门相消
		{
			//清除缓存
			tempcontrolss.clear();
			temptargetss.clear();
			add = 0;
			list<Gate>::iterator moveit = ++it;
			it--;	
			for (; moveit != gateVar.end();) 
			{
				if ( moveit->name == "t1" ) //跳过not   
				{
					flag = 1;
					temptargetss.push_back(moveit->targets.at(0));
					moveit++;
					continue;
				}
				if ( moveit->name == "s" ) //跳过swap
				{
					flag = 1;
					temptargetss.push_back(moveit->targets.at(0));
					temptargetss.push_back(moveit->targets.at(1));
					moveit++;
					continue;
				}
				if ( (it->controls == moveit->controls)&&(it->targets == moveit->targets)  )
				{
					//消除相邻的门
					if ( tempcontrolss.empty() ) //为空
					{
						if ( temptargetss.empty() ) //为空
						{
							add = 1;
						}
					}
					for (vector<string>::iterator iter = temptargetss.begin(); iter != temptargetss.end();) //判断两者之间的门   
					{
						if ( *iter == moveit->controls.at(0) ) //moveit所指门的控制位所在线上有目标位
						{
							flag = 1;
							break;
						}
						else
						{
							flag = 0;
							iter++;
						}
					}
					if ( flag == 0 )
					{
						for (vector<string>::iterator iter = tempcontrolss.begin(); iter != tempcontrolss.end();)
						{
							if ( *iter == moveit->targets.at(0) ) //moveit所指门的目标位所在线上有控制位
							{
								flag = 1;
								break;
							}
							else
							{
								flag = 0;
								iter++;
							}
						}
					}
					if ( flag == 0 ) //判断门是哪种类型
					{
						if ( it->name == "t2" && moveit->name == "t2" ) //两个cnot
						{
							it = gateVar.erase(it); //注意：此时it和moveit的指向均后移一个
							if ( add == 1 ) //删除相邻门，需要后移两位
							{
								it++;
							}
							moveit = gateVar.erase(moveit);
							break;
						}
						else if ( (it->name == "v2" && moveit->name == "v+") || (it->name == "v+" && moveit->name == "v2")) //一个v一个v+
						{
							it = gateVar.erase(it);
							if ( add == 1 )
							{
								it++;
							}
							moveit = gateVar.erase(moveit);
							break;
						}
						else
						{
							flag = 1;
							temptargetss.push_back(moveit->targets.at(0));
							tempcontrolss.push_back(moveit->controls.at(0));
							moveit++;
						}
					}
					else
					{
						flag = 1;
						temptargetss.push_back(moveit->targets.at(0));
						tempcontrolss.push_back(moveit->controls.at(0));
						moveit++;
					}
				}
				else
				{
					flag = 1;
					temptargetss.push_back(moveit->targets.at(0));
					tempcontrolss.push_back(moveit->controls.at(0));
					moveit++;
				}
			}
		}
		else if ( it->name == "t1" ) //not门
		{
			//清除缓存
			tempcontrolss.clear();
			temptargetss.clear();
			add = 0;
			list<Gate>::iterator moveit = ++it;
			it--;
			for (; moveit != gateVar.end();)
			{
				if ( moveit->name == "t1" )
				{
					if ( it->targets == moveit->targets )
					{
						//消除相邻的门
						if ( tempcontrolss.empty() ) //为空
						{						
							add = 1;							
						}
						//判断目标位所在线前面有没有控制线
						for (vector<string>::iterator iter = tempcontrolss.begin(); iter != tempcontrolss.end();)
						{
							if ( *iter == moveit->targets.at(0) ) //moveit所指门的目标位所在线上有控制位
							{
								flag = 1;
								break;
							}
							else
							{
								flag = 0;
								iter++;
							}
						}
						if ( flag == 0 )
						{
							it = gateVar.erase(it);
							if ( add == 1 )
							{
								it++;
							}
							moveit = gateVar.erase(moveit);
							break;
						}
						else
						{
							flag = 1;
							moveit++;
						}
					}
					else
					{
						flag = 1;
						moveit++;
					}
				}
				else //moveit不为not门
				{
					flag = 1;					
					if ( moveit->name == "s" )  //moveit为交换门
					{
						tempcontrolss.push_back(moveit->targets.at(0));
						tempcontrolss.push_back(moveit->targets.at(1));
					}
					else
					{
						tempcontrolss.push_back(moveit->controls.at(0));
					}
					moveit++;
				}

			}
		}
		else if ( it->name == "s" ) //swap门  此处是删除的是非相邻的交换门
		{
			//清除缓存
			tempcontrolss.clear();
			temptargetss.clear();
			add = 0;
			list<Gate>::iterator moveit = ++it;
			it--;
			for (; moveit != gateVar.end();)
			{
				if ( moveit->name == "s" )
				{
					if ( ((it->targets.at(0) == moveit->targets.at(0))&&(it->targets.at(1) == moveit->targets.at(1))) ||
						((it->targets.at(0) == moveit->targets.at(1))&&(it->targets.at(1) == moveit->targets.at(0))))
					{
						//消除相邻的门
						if ( tempcontrolss.empty() ) //为空
						{
							if ( temptargetss.empty() ) //为空
							{
								add = 1;
							}
						}
						//判断目标位所在线有没有控制位或目标位
						for (vector<string>::iterator iter = tempcontrolss.begin(); iter != tempcontrolss.end();)
						{
							if ( *iter == moveit->targets.at(0) || *iter == moveit->targets.at(1) )
							{
								flag = 1;
								break;
							}
							else
							{
								flag = 0;
								iter++;
							}
						}
						if ( flag == 0 )
						{
							for (vector<string>::iterator iter = temptargetss.begin(); iter != temptargetss.end();)
							{
								if ( *iter == moveit->targets.at(0) || *iter == moveit->targets.at(1) )
								{
									flag = 1;
									break;
								}
								else
								{
									flag = 0;
									iter++;
								}
							}
						}
						if ( flag == 0 ) //可以删除门
						{
							it = gateVar.erase(it);
							if ( add == 1 )
							{
								it++;
							}
							moveit = gateVar.erase(moveit);
							break;
						}
						else //中间有其他门
						{
							flag = 1;			
							temptargetss.push_back(moveit->targets.at(0));				
							temptargetss.push_back(moveit->targets.at(1));
							moveit++;
						}
					}
					else //moveit是交换门
					{
						flag = 1;
						temptargetss.push_back(moveit->targets.at(0));				
						temptargetss.push_back(moveit->targets.at(1));
						moveit++;
					}
				}
				else //moveit不是交换门
				{
					flag = 1;
					if ( moveit->name == "t1" ) //moveit为not门
					{
						temptargetss.push_back(moveit->targets.at(0));	
					}
					else
					{
						temptargetss.push_back(moveit->targets.at(0));	
						tempcontrolss.push_back(moveit->controls.at(0));	
					}			
					moveit++;
				}
			}
		}
		if ( flag == 1 )
		{
			flag = 0;	
			it++;
			i++;
		}	
	}
}

//计算单个门的NNC
void Circuit:: updateNNC(list<Gate> &gateVar)
{
	//计算量子门目标位和控制位之间的距离
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end(); ++it)    
	{
		if (it->name == "t1" || it->name == "s")  
		{
			it->NNC = 0;
		}
		else
		{
			it->NNC = abs(it->targets.at(0).at(0) - it->controls.at(0).at(0)) - 1;  
		}
	}
}

//更新单个门，主要swap的存线
void Circuit:: updateGate(list<Gate> &gateVar)
{
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end(); ++it)
	{
		if ( it->lines.empty() )
		{
			if ( it->name == "t1" )
			{
				it->lines.push_back(it->targets.at(0));
			}
			else if ( it->name == "t2" || it->name == "v2" || it->name == "v+" )
			{
				it->lines.push_back(it->controls.at(0));
				it->lines.push_back(it->targets.at(0));
			}
			else
			{
				it->lines.push_back(it->targets.at(0));
				it->lines.push_back(it->targets.at(1));
			}
		}	
	}
}

//计算downSwapCost
int Circuit:: ngLookahead_1( list<Gate>::iterator iter, list<Gate> &gateVar) 
{
	int downSwapCost = 0;

	//iter是最后一个门
	if ((unsigned int)iter->id == gateVar.size())
	{
		downSwapCost += abs(iter->controls.at(0).at(0) - iter->targets.at(0).at(0)) - 1;
		return downSwapCost;
	}
	
	list <Gate>::iterator moveIt = iter;  //定义一个移动的迭代器，用于移动访问电路中的量子门
	++moveIt;
    if (moveIt->name == "s" ) //要定位到非交换门的
	{
		++moveIt;
	}
	
	//顺序计算自G.p开始的后继G.n的Swap Cost
	for(int i = 0;i < locaN; ++i)  
	{
		if ((unsigned int)iter->id < gateVar.size())
		{
			//不计算Similar
			if (moveIt->name == "t1" || moveIt->name == "s" || (iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0) && 
				iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0)) || 
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0) && 
				iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0)))
			{
				//判断跳过的门是否是最后一个门
				if ( moveIt->id == gateVar.size() ) 
				{
					downSwapCost += 0;
					break;				
				}
				else
				{
					++moveIt;
					continue;
				}	
			}
			if (((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) < moveIt->targets.at(0).at(0)) && 
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) < moveIt->controls.at(0).at(0)) && 
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) < moveIt->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0)))||
				((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) 
				&& (iter->targets < moveIt->targets) && (iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{	
				downSwapCost += moveIt->NNC;  //注意迭代器moveIt所指向的位置(之前moveIt已做了++运算).
			}
			else if (((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) > moveIt->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) > moveIt->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) > moveIt->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) > moveIt->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				downSwapCost += ( moveIt->NNC + iter->NNC );  
			} 
			else if (((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) < moveIt->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				(( iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) < moveIt->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				(( iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) < moveIt->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) < moveIt->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				downSwapCost += ( moveIt->NNC - iter->NNC );
			}
			else if ((( iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) > moveIt->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) > moveIt->controls.at(0).at(0)) && 
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) > moveIt->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) > moveIt->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				downSwapCost += moveIt->NNC;  
			}
			else if (((iter->controls.at(0).at(0) < moveIt->targets.at(0).at(0)) &&
				(moveIt->targets.at(0).at(0) < iter->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->targets.at(0).at(0) < moveIt->controls.at(0).at(0)) &&
				(moveIt->controls.at(0).at(0) < iter->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->controls.at(0).at(0) < moveIt->controls.at(0).at(0)) &&
				(moveIt->controls.at(0).at(0) < iter->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->targets.at(0).at(0) < moveIt->targets.at(0).at(0)) &&
				(moveIt->targets.at(0).at(0) < iter->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				downSwapCost += ( iter->NNC - ( moveIt->NNC + 1 ) );
			}
			else if (((iter->controls.at(0).at(0) > moveIt->targets.at(0).at(0)) &&
				(moveIt->targets.at(0).at(0) > iter->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->targets.at(0).at(0) > moveIt->controls.at(0).at(0)) &&
				(moveIt->controls.at(0).at(0) > iter->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->controls.at(0).at(0) > moveIt->controls.at(0).at(0)) &&
				(moveIt->controls.at(0).at(0) > iter->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->targets.at(0).at(0) > moveIt->targets.at(0).at(0)) && 
				(moveIt->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{ 
				downSwapCost += ( moveIt->NNC + 1 );  
			}
			else  //iter->controls.at(0).at(0) <(>) iter->targets.at(0).at(0)
			{
				downSwapCost = abs(iter->controls.at(0).at(0) - iter->targets.at(0).at(0)) - 1;
			}
		
			if ((unsigned int)moveIt->id < gateVar.size())
			{
				++moveIt;
			}
			else
			{
				break;
			}
		}
	}
	return downSwapCost;
}

//计算upSwapCost
int Circuit:: ngLookahead_2( list<Gate>::iterator iter, list <Gate> &gateVar)  
{
	int upSwapCost = 0;
	
	//iter是最后一个门
	if ((unsigned int)iter->id == gateVar.size())
	{
		upSwapCost += abs(iter->controls.at(0).at(0) - iter->targets.at(0).at(0)) - 1;
		return upSwapCost;
	}

	list <Gate>::iterator moveIt = iter;  //定义一个移动的迭代器，用于移动访问电路中的量子门
	++moveIt;
	if (moveIt->name == "s" ) //要定位到非交换门的
	{
		++moveIt;
	}

	for(int i = 0;i < locaN; ++i)  //顺序计算自G.p开始的后继G.n的Swap Cost
	{
		if ((unsigned int)iter->id < gateVar.size())
		{
			//不计算Similar
			if (moveIt->name == "t1" || moveIt->name == "s" || (iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0) && 
				iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0)) || 
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0) && 
				iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0)))
			{
				//判断跳过的门是否是最后一个门
				if ( moveIt->id == gateVar.size() )
				{
					upSwapCost += 0;
					break;
				}
				else
				{
					++moveIt;
					continue;
				}
			}
			if (((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) < moveIt->targets.at(0).at(0)) && 
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) < moveIt->controls.at(0).at(0)) && 
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) < moveIt->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) < moveIt->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{	
				upSwapCost += ( moveIt->NNC + iter->NNC );  
			}
			else if (((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) > moveIt->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) > moveIt->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) > moveIt->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) > moveIt->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				upSwapCost += moveIt->NNC;
			} 
			else if (((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) < moveIt->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				(( iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) < moveIt->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) < moveIt->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) < moveIt->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				upSwapCost += moveIt->NNC;
			}
			else if (((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) > moveIt->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				(( iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) > moveIt->controls.at(0).at(0)) && 
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				(( iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) > moveIt->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				(( iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) > moveIt->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				upSwapCost += ( moveIt->NNC - iter->NNC );
			}
			else if (((iter->controls.at(0).at(0) < moveIt->targets.at(0).at(0) ) &&
				(moveIt->targets.at(0).at(0) < iter->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->targets.at(0).at(0) < moveIt->controls.at(0).at(0)) && 
				(moveIt->controls.at(0).at(0) < iter->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->controls.at(0).at(0) < moveIt->controls.at(0).at(0)) &&
				(moveIt->controls.at(0).at(0) < iter->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->targets.at(0).at(0) < moveIt->targets.at(0).at(0)) && 
				(moveIt->targets.at(0).at(0) < iter->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				upSwapCost += ( moveIt->NNC + 1 );
			}
			else if (((iter->controls.at(0).at(0) > moveIt->targets.at(0).at(0)) && 
				( moveIt->targets.at(0).at(0) > iter->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->targets.at(0).at(0) > moveIt->controls.at(0).at(0)) && 
				( moveIt->controls.at(0).at(0) > iter->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->controls.at(0).at(0) > moveIt->controls.at(0).at(0)) && 
				(moveIt->controls.at(0).at(0) > iter->targets.at(0).at(0) ) &&
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->targets.at(0).at(0) > moveIt->targets.at(0).at(0)) && 
				(moveIt->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				upSwapCost += ( iter->NNC - ( moveIt->NNC + 1 ) );
			}
			else  //iter->controls.at(0).at(0) <(>) iter->targets.at(0).at(0)
			{
				upSwapCost += abs( iter->targets.at(0).at(0) - iter->controls.at(0).at(0)) -  1 ;  //修改处。。。。。。。。。。。。。。。。。。。。。。
			}

			if ((unsigned int)moveIt->id < gateVar.size())
			{
				++moveIt;
			}
			else
			{
				break;
			}
		}
	}
	return upSwapCost;
}

//计算upDownSwapCost
int Circuit:: ngLookahead_3( list<Gate>::iterator iter,list <Gate> &gateVar )  
{
	int upDownSwapCost = 0;

	//iter是最后一个门
	if ((unsigned int)iter->id == gateVar.size())
	{
		upDownSwapCost = -1;
		return upDownSwapCost;
	}

	list <Gate>::iterator moveIt = iter;  //定义一个移动的迭代器，用于移动访问电路中的量子门
	++moveIt;
	
	for( int i = 0;i < locaN; ++i )  //顺序计算自G.p开始的后继G.n的Swap Cost
	{
		if ((unsigned int)iter->id < gateVar.size())
		{
			//不计算Similar
			if ( moveIt->name == "t1" || (iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0) && 
				iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0)) || 
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0) && 
				iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0)))
			{
				if ( moveIt->id == gateVar.size() )
				{
					upDownSwapCost += 0;
					break;
				}
				++moveIt;
				continue;
			}

			int judgegr = 0;
			if (((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) < moveIt->targets.at(0).at(0)) && 
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) < moveIt->controls.at(0).at(0)) && 
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
				( iter->controls.at(0).at(0) < moveIt->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) < moveIt->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{	
				judgegr = FindGr(iter,moveIt,gateVar);
				//判断Gr
				if ( judgegr == 1 ) //Gr是Gn后一个门
				{
					upDownSwapCost += moveIt->NNC + calculateDGpr(iter,++moveIt);
					moveIt--; //还原
				}
				else if ( judgegr == 0 )  //Gr = Gp
				{
					upDownSwapCost += 0;
				}
				else if ( judgegr == 2 ) //Gr是Gn前一个门
				{
					upDownSwapCost += moveIt->NNC + calculateDGpr(iter,--moveIt);
					moveIt++; //还原
				}
				else //Gr不存在
				{
					upDownSwapCost = -1; //区分不存在情况
					break;
	
				} 
			}
			else if (((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) > moveIt->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) > moveIt->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) > moveIt->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) > moveIt->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				judgegr = FindGr(iter,moveIt,gateVar);
				//判断Gr
				if ( judgegr == 1 ) //Gr是Gn后一个门
				{
					upDownSwapCost += moveIt->NNC + calculateUGpr(iter,++moveIt);
					moveIt--; //还原
				}
				else if ( judgegr == 0 )  //Gr = Gp
				{
					upDownSwapCost += 0;
				}
				else if ( judgegr == 2 ) //Gr是Gn前一个门
				{
					upDownSwapCost += moveIt->NNC + calculateUGpr(iter,--moveIt);
					moveIt++; //还原
				}
				else //Gr不存在
				{
					upDownSwapCost = -1; //区分不存在情况
					break;
				} 
			} 
			else if (((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) < moveIt->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) < moveIt->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) < moveIt->controls.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) < moveIt->targets.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				judgegr = FindGr(iter,moveIt,gateVar);
				//判断Gr
				if ( judgegr == 1 ) //Gr是Gn后一个门
				{
					upDownSwapCost += moveIt->NNC - calculateUGpr(iter,++moveIt);
					moveIt--; //还原
				}
				else if ( judgegr == 0 )  //Gr = Gp
				{
					upDownSwapCost += 0;
				}
				else if ( judgegr == 2 ) //Gr是Gn前一个门
				{
					upDownSwapCost += moveIt->NNC - calculateUGpr(iter,--moveIt);
					moveIt++; //还原
				}
				else //Gr不存在
				{
					upDownSwapCost = -1; //区分不存在情况
					break;
				} 
			}
			else if (((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) > moveIt->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) > moveIt->controls.at(0).at(0)) && 
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) > moveIt->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) && 
				(iter->controls.at(0).at(0) > moveIt->targets.at(0).at(0)) && 
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				judgegr = FindGr(iter,moveIt,gateVar);
				//判断Gr
				if ( judgegr == 1 ) //Gr是Gn后一个门
				{
					upDownSwapCost += moveIt->NNC - calculateDGpr(iter,++moveIt);
					moveIt--; //还原
				}
				else if ( judgegr == 0 )  //Gr = Gp
				{
					upDownSwapCost += 0;
				}
				else if ( judgegr == 2 ) //Gr是Gn前一个门
				{
					upDownSwapCost += moveIt->NNC - calculateDGpr(iter,--moveIt);
					moveIt++; //还原
				}
				else //Gr不存在
				{
					upDownSwapCost = -1; //区分不存在情况
					break;
				} 
			}
			else if (((iter->controls.at(0).at(0) < moveIt->targets.at(0).at(0)) &&
				(moveIt->targets.at(0).at(0) < iter->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				((iter->targets.at(0).at(0) < moveIt->controls.at(0).at(0)) && 
				(moveIt->controls.at(0).at(0) < iter->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0))) || 
				((iter->controls.at(0).at(0) < moveIt->controls.at(0).at(0)) &&
				(moveIt->controls.at(0).at(0) < iter->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0))) ||
				((iter->targets.at(0).at(0) < moveIt->targets.at(0).at(0)) && 
				(moveIt->targets.at(0).at(0) < iter->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				judgegr = FindGr(iter,moveIt,gateVar);
				//判断Gr
				if ( judgegr == 1 ) //Gr是Gn后一个门
				{
					upDownSwapCost += abs( moveIt->NNC -(++moveIt)->NNC );
					moveIt--; //还原
				}
				else if ( judgegr == 0 )  //Gr = Gp
				{
					upDownSwapCost += 0;
				}
				else if ( judgegr == 2 ) //Gr是Gn前一个门
				{
					upDownSwapCost += abs( moveIt->NNC - (--moveIt)->NNC );
					moveIt++; //还原
				}
				else //Gr不存在
				{
					upDownSwapCost = -1; //区分不存在情况
					break;
				} 
			}
			else if (((iter->controls.at(0).at(0) > moveIt->targets.at(0).at(0)) &&
				(moveIt->targets.at(0).at(0) > iter->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0))) || 
				(( iter->targets.at(0).at(0) > moveIt->controls.at(0).at(0)) &&
				(moveIt->controls.at(0).at(0) > iter->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0)) ) || 
				((iter->controls.at(0).at(0) > moveIt->controls.at(0).at(0)) &&
				(moveIt->controls.at(0).at(0) > iter->targets.at(0).at(0)) &&
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0)) ) ||
				((iter->targets.at(0).at(0) > moveIt->targets.at(0).at(0)) && 
				(moveIt->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
				(iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0))))
			{
				judgegr = FindGr(iter,moveIt,gateVar);
				//判断Gr
				if ( judgegr == 1 ) //Gr是Gn后一个门
				{
					upDownSwapCost += abs( moveIt->NNC -(++moveIt)->NNC );
					moveIt--; //还原
				}
				else if ( judgegr == 0 )  //Gr = Gp
				{
					upDownSwapCost += 0;
				}
				else if ( judgegr == 2 ) //Gr是Gn前一个门
				{
					upDownSwapCost += abs( moveIt->NNC -(--moveIt)->NNC );
					moveIt++; //还原
				}
				else //Gr不存在
				{
					upDownSwapCost = -1; //区分不存在情况
					break;
				} 
			}
			if ((unsigned int)moveIt->id < gateVar.size())
			{
				++moveIt;
			}
			else
			{
				break;
			}
		}
	}
	return upDownSwapCost;
}

//确定Gr函数
int Circuit:: FindGr(list<Gate>::iterator iter,list<Gate>::iterator moveit,list <Gate> &gateVar)
{
	int flag1 = 0; //（Gp,Gn）满足case c 则为1
	int flag2 = 0; //（Gp,Gr）满足case c 则为1
	int flag3 = 0; //特殊情况：gr在gn前

	if ( locaN == 2 )
	{
		//只做N=2，因此这边代码通用性不强
		list <Gate>::iterator gr;

		//特殊情况：1、moveit前一个是not门，后一个门取不到   Gn为最后一个门
		//          2、gr所指代门是not门
		//          3、gr是gn的前一个门
		if ( (moveit->id - iter->id) > 1 || moveit->id == gateVar.size() ) //特殊情况1
		{
			list <Gate>::iterator tempgr = --moveit;
			moveit++;
			if ( (moveit->id - iter->id) > 1 && tempgr->name != "t1" ) //gr是gn的前一个门
			{
				flag3 = 1;
				gr = --moveit;
				moveit++;
			}
			else
			{
				gr = moveit;
			}

		}
		else
		{
			gr = moveit;  //从Gp开始，依次定义三个指针
			++gr;
			if ( gr->name == "t1" ) //特殊情况2
			{
				gr = moveit;
			}
		}



		//检测（Gp,Gn）是否满足case c
		if ( (iter->controls.at(0).at(0) < moveit->targets.at(0).at(0) && moveit->targets.at(0).at(0) < iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == moveit->controls.at(0).at(0)) ||
			(iter->controls.at(0).at(0) > moveit->targets.at(0).at(0) && moveit->targets.at(0).at(0) > iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == moveit->controls.at(0).at(0)) ||
			(iter->targets.at(0).at(0) < moveit->controls.at(0).at(0) && moveit->controls.at(0).at(0) < iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == moveit->targets.at(0).at(0)) ||
			(iter->targets.at(0).at(0) > moveit->controls.at(0).at(0) && moveit->controls.at(0).at(0) > iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == moveit->targets.at(0).at(0)) ||
			(iter->controls.at(0).at(0) < moveit->controls.at(0).at(0) && moveit->controls.at(0).at(0) < iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == moveit->targets.at(0).at(0)) ||
			(iter->controls.at(0).at(0) > moveit->controls.at(0).at(0) && moveit->controls.at(0).at(0) > iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == moveit->targets.at(0).at(0)) ||
			(iter->targets.at(0).at(0) < moveit->targets.at(0).at(0) && moveit->targets.at(0).at(0) < iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == moveit->controls.at(0).at(0)) ||
			(iter->targets.at(0).at(0) > moveit->targets.at(0).at(0) && moveit->targets.at(0).at(0) > iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == moveit->controls.at(0).at(0)) )
		{
			flag1 = 1;
		}

		//检测（Gp,Gr）是否满足case c
		if ( (iter->controls.at(0).at(0) < gr->targets.at(0).at(0) && gr->targets.at(0).at(0) < iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == gr->controls.at(0).at(0)) ||
			(iter->controls.at(0).at(0) > gr->targets.at(0).at(0) && gr->targets.at(0).at(0) > iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == gr->controls.at(0).at(0)) ||
			(iter->targets.at(0).at(0) < gr->controls.at(0).at(0) && gr->controls.at(0).at(0) < iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == gr->targets.at(0).at(0)) ||
			(iter->targets.at(0).at(0) > gr->controls.at(0).at(0) && gr->controls.at(0).at(0) > iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == gr->targets.at(0).at(0)) ||
			(iter->controls.at(0).at(0) < gr->controls.at(0).at(0) && gr->controls.at(0).at(0) < iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == gr->targets.at(0).at(0)) ||
			(iter->controls.at(0).at(0) > gr->controls.at(0).at(0) && gr->controls.at(0).at(0) > iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == gr->targets.at(0).at(0)) ||
			(iter->targets.at(0).at(0) < gr->targets.at(0).at(0) && gr->targets.at(0).at(0) < iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == gr->controls.at(0).at(0)) ||
			(iter->targets.at(0).at(0) > gr->targets.at(0).at(0) && gr->targets.at(0).at(0) > iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == gr->controls.at(0).at(0)) )
		{
			flag2 = 1;
		}


		if ( flag3 == 1 )
		{
			if ( flag2 == 1 )
			{
				return 2; //表示Gr是Gn前一个门
			}
			else if ( flag1 == 1 )
			{
				return 0; //均符合时选后面一个，故表示Gr = Gn
			}
			else
			{
				return -1; //表示Gr不存在，无需计算
			}

		}

		if ( flag1 == 1 )
		{
			if ( flag2 == 1 && moveit != gr )
			{
				return 1; //表示Gr是Gn后一个门
			}
			else
			{
				return 0; //表示Gr = Gn
			}
		}
		else
		{
			if ( flag2 ==1 )
			{
				return 1; //表示Gr是Gn后一个门
			}
			else
			{
				return -1; //表示Gr不存在，无需计算
			}
		}

	}
	else if ( locaN == 1 ) //N = 1
	{
		//此时moveit就是gr，只要判断（Gp，Gr）是否满足case c

		if ( (iter->controls.at(0).at(0) < moveit->targets.at(0).at(0) && moveit->targets.at(0).at(0) < iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == moveit->controls.at(0).at(0)) ||
			(iter->controls.at(0).at(0) > moveit->targets.at(0).at(0) && moveit->targets.at(0).at(0) > iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == moveit->controls.at(0).at(0)) ||
			(iter->targets.at(0).at(0) < moveit->controls.at(0).at(0) && moveit->controls.at(0).at(0) < iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == moveit->targets.at(0).at(0)) ||
			(iter->targets.at(0).at(0) > moveit->controls.at(0).at(0) && moveit->controls.at(0).at(0) > iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == moveit->targets.at(0).at(0)) ||
			(iter->controls.at(0).at(0) < moveit->controls.at(0).at(0) && moveit->controls.at(0).at(0) < iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == moveit->targets.at(0).at(0)) ||
			(iter->controls.at(0).at(0) > moveit->controls.at(0).at(0) && moveit->controls.at(0).at(0) > iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == moveit->targets.at(0).at(0)) ||
			(iter->targets.at(0).at(0) < moveit->targets.at(0).at(0) && moveit->targets.at(0).at(0) < iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == moveit->controls.at(0).at(0)) ||
			(iter->targets.at(0).at(0) > moveit->targets.at(0).at(0) && moveit->targets.at(0).at(0) > iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == moveit->controls.at(0).at(0)) )
		{
			flag1 = 1; //满足case c
			return 0; //Gn就是Gr
		}
		else
		{
			return -1; //Gr不存在
		}
	}
	

}

//计算GpGr的dSC
int Circuit:: calculateDGpr(list<Gate>::iterator iter,list<Gate>::iterator gr)  
{
	int temp = 0;
	if (((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) < gr->targets.at(0).at(0)) && 
		(iter->controls.at(0).at(0) == gr->controls.at(0).at(0))) || 
		((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) &&
		(iter->targets.at(0).at(0) < gr->controls.at(0).at(0)) && 
		(iter->targets.at(0).at(0) == gr->targets.at(0).at(0))) || 
		((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) < gr->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) == gr->targets.at(0).at(0)))||
		((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) 
		&& (iter->targets < gr->targets) && (iter->targets.at(0).at(0) == gr->controls.at(0).at(0))))
	{	
		temp += gr->NNC;  //注意迭代器gr所指向的位置(之前gr已做了++运算).
	}
	else if (((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) > gr->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->controls.at(0).at(0))) || 
		((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) &&
		(iter->targets.at(0).at(0) > gr->controls.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->targets.at(0).at(0))) || 
		((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
		(iter->controls.at(0).at(0) > gr->controls.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->targets.at(0).at(0))) ||
		((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) && 
		(iter->targets.at(0).at(0) > gr->targets.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->controls.at(0).at(0))))
	{
		temp += ( gr->NNC + iter->NNC );  
	} 
	else if (((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) && 
		(iter->targets.at(0).at(0) < gr->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->controls.at(0).at(0))) || 
		(( iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) &&
		(iter->controls.at(0).at(0) < gr->controls.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->targets.at(0).at(0))) || 
		(( iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) && 
		(iter->targets.at(0).at(0) < gr->controls.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->targets.at(0).at(0))) ||
		((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) < gr->targets.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->controls.at(0).at(0))))
	{
		temp += ( gr->NNC - iter->NNC );
	}
	else if ((( iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) &&
		(iter->targets.at(0).at(0) > gr->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->controls.at(0).at(0))) || 
		((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) > gr->controls.at(0).at(0)) && 
		(iter->targets.at(0).at(0) == gr->targets.at(0).at(0))) || 
		((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) && 
		(iter->targets.at(0).at(0) > gr->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) == gr->targets.at(0).at(0))) ||
		((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) > gr->targets.at(0).at(0)) && 
		(iter->targets.at(0).at(0) == gr->controls.at(0).at(0))))
	{
		temp += gr->NNC;  
	}
	else if (((iter->controls.at(0).at(0) < gr->targets.at(0).at(0)) &&
		(gr->targets.at(0).at(0) < iter->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->controls.at(0).at(0))) || 
		((iter->targets.at(0).at(0) < gr->controls.at(0).at(0)) &&
		(gr->controls.at(0).at(0) < iter->controls.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->targets.at(0).at(0))) || 
		((iter->controls.at(0).at(0) < gr->controls.at(0).at(0)) &&
		(gr->controls.at(0).at(0) < iter->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->targets.at(0).at(0))) ||
		((iter->targets.at(0).at(0) < gr->targets.at(0).at(0)) &&
		(gr->targets.at(0).at(0) < iter->controls.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->controls.at(0).at(0))))
	{
		temp += ( iter->NNC - ( gr->NNC + 1 ) );
	}
	else if (((iter->controls.at(0).at(0) > gr->targets.at(0).at(0)) &&
		(gr->targets.at(0).at(0) > iter->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->controls.at(0).at(0))) || 
		((iter->targets.at(0).at(0) > gr->controls.at(0).at(0)) &&
		(gr->controls.at(0).at(0) > iter->controls.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->targets.at(0).at(0))) || 
		((iter->controls.at(0).at(0) > gr->controls.at(0).at(0)) &&
		(gr->controls.at(0).at(0) > iter->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->targets.at(0).at(0))) ||
		((iter->targets.at(0).at(0) > gr->targets.at(0).at(0)) && 
		(gr->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->controls.at(0).at(0))))
	{ 
		temp += ( gr->NNC + 1 );  
	}

	return temp;

}

//计算GpGr的uSC
int Circuit:: calculateUGpr(list<Gate>::iterator iter,list<Gate>::iterator gr)
{
	int temp = 0;
	if (((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) &&
		(iter->controls.at(0).at(0) < gr->targets.at(0).at(0)) && 
		(iter->controls.at(0).at(0) == gr->controls.at(0).at(0))) || 
		((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) && 
		(iter->targets.at(0).at(0) < gr->controls.at(0).at(0)) && 
		(iter->targets.at(0).at(0) == gr->targets.at(0).at(0))) || 
		((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) < gr->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) == gr->targets.at(0).at(0))) ||
		((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) && 
		(iter->targets.at(0).at(0) < gr->targets.at(0).at(0)) && 
		(iter->targets.at(0).at(0) == gr->controls.at(0).at(0))))
	{	
		temp += ( gr->NNC + iter->NNC );  
	}
	else if (((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
		(iter->controls.at(0).at(0) > gr->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->controls.at(0).at(0))) || 
		((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) &&
		(iter->targets.at(0).at(0) > gr->controls.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->targets.at(0).at(0))) || 
		((iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
		(iter->controls.at(0).at(0) > gr->controls.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->targets.at(0).at(0))) ||
		((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) &&
		(iter->targets.at(0).at(0) > gr->targets.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->controls.at(0).at(0))))
	{
		temp += gr->NNC;
	} 
	else if (((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) && 
		(iter->targets.at(0).at(0) < gr->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->controls.at(0).at(0))) || 
		(( iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) &&
		(iter->controls.at(0).at(0) < gr->controls.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->targets.at(0).at(0))) || 
		((iter->controls.at(0).at(0) < iter->targets.at(0).at(0)) &&
		(iter->targets.at(0).at(0) < gr->controls.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->targets.at(0).at(0))) ||
		((iter->targets.at(0).at(0) < iter->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) < gr->targets.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->controls.at(0).at(0))))
	{
		temp += gr->NNC;
	}
	else if (((iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) && 
		(iter->targets.at(0).at(0) > gr->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->controls.at(0).at(0))) || 
		(( iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
		(iter->controls.at(0).at(0) > gr->controls.at(0).at(0)) && 
		(iter->targets.at(0).at(0) == gr->targets.at(0).at(0))) || 
		(( iter->controls.at(0).at(0) > iter->targets.at(0).at(0)) && 
		(iter->targets.at(0).at(0) > gr->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) == gr->targets.at(0).at(0))) ||
		(( iter->targets.at(0).at(0) > iter->controls.at(0).at(0)) && 
		(iter->controls.at(0).at(0) > gr->targets.at(0).at(0)) && 
		(iter->targets.at(0).at(0) == gr->controls.at(0).at(0))))
	{
		temp += ( gr->NNC - iter->NNC );
	}
	else if (((iter->controls.at(0).at(0) < gr->targets.at(0).at(0) ) &&
		(gr->targets.at(0).at(0) < iter->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->controls.at(0).at(0))) || 
		((iter->targets.at(0).at(0) < gr->controls.at(0).at(0)) && 
		(gr->controls.at(0).at(0) < iter->controls.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->targets.at(0).at(0))) || 
		((iter->controls.at(0).at(0) < gr->controls.at(0).at(0)) &&
		(gr->controls.at(0).at(0) < iter->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->targets.at(0).at(0))) ||
		((iter->targets.at(0).at(0) < gr->targets.at(0).at(0)) && 
		(gr->targets.at(0).at(0) < iter->controls.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->controls.at(0).at(0))))
	{
		temp += ( gr->NNC + 1 );
	}
	else if (((iter->controls.at(0).at(0) > gr->targets.at(0).at(0)) && 
		( gr->targets.at(0).at(0) > iter->targets.at(0).at(0)) &&
		(iter->controls.at(0).at(0) == gr->controls.at(0).at(0))) || 
		((iter->targets.at(0).at(0) > gr->controls.at(0).at(0)) && 
		( gr->controls.at(0).at(0) > iter->controls.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->targets.at(0).at(0))) || 
		((iter->controls.at(0).at(0) > gr->controls.at(0).at(0)) && 
		(gr->controls.at(0).at(0) > iter->targets.at(0).at(0) ) &&
		(iter->controls.at(0).at(0) == gr->targets.at(0).at(0))) ||
		((iter->targets.at(0).at(0) > gr->targets.at(0).at(0)) && 
		(gr->targets.at(0).at(0) > iter->controls.at(0).at(0)) &&
		(iter->targets.at(0).at(0) == gr->controls.at(0).at(0))))
	{
		temp += ( iter->NNC - ( gr->NNC + 1 ) );
	}
	return temp;
}

//前瞻算法
int Circuit:: ngLookahead(list<Gate>::iterator iter, list<Gate> &gateVar, vector<string> &line)  //invoke ngLookahead_1/2/3，index即等价于(定位)id
{
	//变量的初始化
	int upSwapCost = 0;
    int downSwapCost = 0;
	int upDownSwapCost = 0;
	int tempDownSwapCount = 0;  //临时存储downSwapCount
	int insertSwapApproFlag = 0;  //不同的值对应不同Swap门的插入方法(down：0；up：1；upDown：2) 默认下移

	//串行方式
	downSwapCost = ngLookahead_1( iter,gateVar );
	upSwapCost = ngLookahead_2( iter,gateVar );
	upDownSwapCost = ngLookahead_3(iter,gateVar);

	//确定insertSwapApproFlag的值(即确定Swap门插入的方法)
	if ( upDownSwapCost == -1 ) //Gr不存在
	{
		tempDownSwapCount =  __min(downSwapCost, upSwapCost);
		if (upSwapCost < downSwapCost )
		{
			insertSwapApproFlag = 1; //上移
		}
	}
	else
	{
		//取三个钟最小的
		tempDownSwapCount =  __min(downSwapCost, upSwapCost);
		if ( upDownSwapCost < tempDownSwapCount )
		{
			tempDownSwapCount = upDownSwapCost;
			insertSwapApproFlag = 2; //上下移

		}
		else if ( upSwapCost < downSwapCost )
		{
			insertSwapApproFlag = 1; //上移
		}
	}

	//公式计算完成后，根据tempDownSwapCount取小情况对线位进行变化，确定Swap门的插入方法。并在index所对应的门前进行插入
	//第一步：insertSwapPro()
	//第二步：reorderid()
	//第三步：changeLineDown() Or changeLineUp()

	if (insertSwapApproFlag == 0)  //down
	{
		while (iter->NNC > 0)  //当iter对应的门非最近邻
		{
			if (iter->controls.at(0).at(0) > iter->targets.at(0).at(0))  //如果控制位大于目标位
			{
				int i = 0; //确定交换线序的下标
				i = iter->targets.at(0).at(0) - 97;
				swap(line.at(i),line.at(i+1));
				insertSwapPro(iter, iter->targets.at(0).at(0), char(iter->targets.at(0).at(0) + 1), gateVar);  
				reorderGateId(gateVar);  
				//对iter及其后面的门进行线位的改变
				changeLineDown(iter, iter->targets.at(0).at(0), char(iter->targets.at(0).at(0) + 1), gateVar); 
			}
			else  //目标位大于控制位
			{
				int i = 0; //确定交换线序的下标
				i = iter->controls.at(0).at(0) - 97;
                swap(line.at(i),line.at(i+1));
				insertSwapPro(iter, iter->controls.at(0).at(0), char(iter->controls.at(0).at(0) + 1), gateVar);  
				reorderGateId(gateVar);  
				//对iter及其后面的门进行线位的改变
				changeLineDown(iter, iter->controls.at(0).at(0), char(iter->controls.at(0).at(0) + 1), gateVar);  
			}
		}
	}
	else if ( insertSwapApproFlag == 1 ) //up
	{
		while (iter->NNC > 0)  
		{
			if (iter->controls.at(0).at(0) > iter->targets.at(0).at(0))  //如果控制位大于目标位
			{
				int i = 0; //确定交换线序的下标
				i = iter->controls.at(0).at(0) - 97;
				swap(line.at(i-1),line.at(i));
				insertSwapPro(iter, char(iter->controls.at(0).at(0) - 1), char(iter->controls.at(0).at(0)), gateVar);  
				reorderGateId(gateVar);  
				//对iter及其后面的门进行线位的改变
				changeLineUp(iter, char(iter->controls.at(0).at(0) - 1), char(iter->controls.at(0).at(0)),gateVar);  
			}
			else  //目标位大于控制位
			{
				int i = 0; //确定交换线序的下标
				i = iter->targets.at(0).at(0) - 97;
				swap(line.at(i-1),line.at(i));
				insertSwapPro(iter, char(iter->targets.at(0).at(0) - 1), char(iter->targets.at(0).at(0)), gateVar);  
				reorderGateId(gateVar);  
				//对iter及其后面的门进行线位的改变
				changeLineUp(iter, char(iter->targets.at(0).at(0) - 1), char(iter->targets.at(0).at(0)), gateVar);  
			}
		}
	}
	else  //上、下移
	{
		//规定：取一半，一半上移、一半下移，多出的执行下移
		while (iter->NNC - iter->NNC/2.0 >= 1)  //上移
		{
			if (iter->controls.at(0).at(0) > iter->targets.at(0).at(0))  //如果控制位大于目标位
			{
				int i = 0; //确定交换线序的下标
				i = iter->controls.at(0).at(0) - 97;
				swap(line.at(i-1),line.at(i));
				insertSwapPro(iter, char(iter->controls.at(0).at(0) - 1), char(iter->controls.at(0).at(0)), gateVar);  
				reorderGateId(gateVar);  
				//对iter及其后面的门进行线位的改变
				changeLineUp(iter, char(iter->controls.at(0).at(0) - 1), char(iter->controls.at(0).at(0)),gateVar);  
			}
			else  //目标位大于控制位
			{
				int i = 0; //确定交换线序的下标
				i = iter->targets.at(0).at(0) - 97;
				swap(line.at(i-1),line.at(i));
				insertSwapPro(iter, char(iter->targets.at(0).at(0) - 1), char(iter->targets.at(0).at(0)), gateVar);  
				reorderGateId(gateVar);  
				//对iter及其后面的门进行线位的改变
				changeLineUp(iter, char(iter->targets.at(0).at(0) - 1), char(iter->targets.at(0).at(0)), gateVar);  
			}
		}
		while (iter->NNC > 0)  //下移
		{
			if (iter->controls.at(0).at(0) > iter->targets.at(0).at(0))  //如果控制位大于目标位
			{
				int i = 0; //确定交换线序的下标
				i = iter->targets.at(0).at(0) - 97;
				swap(line.at(i),line.at(i+1));
				insertSwapPro(iter, iter->targets.at(0).at(0), char(iter->targets.at(0).at(0) + 1), gateVar);  
				reorderGateId(gateVar);  
				//对iter及其后面的门进行线位的改变
				changeLineDown(iter, iter->targets.at(0).at(0), char(iter->targets.at(0).at(0) + 1), gateVar); 
			}
			else  //目标位大于控制位
			{
				int i = 0; //确定交换线序的下标
				i = iter->controls.at(0).at(0) - 97;
                swap(line.at(i),line.at(i+1));
				insertSwapPro(iter, iter->controls.at(0).at(0), char(iter->controls.at(0).at(0) + 1), gateVar);  
				reorderGateId(gateVar);  
				//对iter及其后面的门进行线位的改变
				changeLineDown(iter, iter->controls.at(0).at(0), char(iter->controls.at(0).at(0) + 1), gateVar);  
			}
		}
	}
	updateGate(gateVar);
	return tempDownSwapCount;
}

//单个量子门前插入交换门,本质上就是在Gp前面插入一个交换门
void Circuit:: insertSwapPro(list<Gate>::iterator it, char tempSwaptargetsLow, char tempSwaptargetsHigh, list<Gate> &gateVar)  
{
	Gate upSwapGate;
	string tempStrSwaptargetsLow;
	string tempStrSwaptargetsHigh;
	upSwapGate.name = "s"; 
	charToString(tempSwaptargetsLow, tempStrSwaptargetsLow);
	charToString(tempSwaptargetsHigh, tempStrSwaptargetsHigh);
	upSwapGate.targets.push_back(tempStrSwaptargetsLow);
	upSwapGate.targets.push_back(tempStrSwaptargetsHigh);
	gateVar.insert(it, upSwapGate);
}

//插入交换门后下移位置
void Circuit:: changeLineDown(list<Gate>::iterator it, char swapTempcontrols, char swapTemptargets, list<Gate> &gateVar)
{
	//模拟Swap门的插入。遍历电路，根据目标位与控制位的位置关系，对门的位置进行改变。
	for (list <Gate>::iterator traverIt = it; traverIt != gateVar.end(); ++traverIt)
	{
		if(traverIt->name == "t1" || traverIt->name == "t2" || traverIt->name == "v2" || 
			traverIt->name == "v+")  //not、c-not、v、v+
		{
			updateNNC(gateVar);
			if (traverIt->NNC > 0)  //traverIt对应的量子门非近邻 
			{
				if (traverIt->controls.at(0).at(0) > traverIt->targets.at(0).at(0))
				{
					if (traverIt->targets.at(0).at(0) == swapTempcontrols)
					{
						++(traverIt->targets.at(0).at(0));
					}
					else if (traverIt->targets.at(0).at(0) == swapTemptargets)
					{
						--(traverIt->targets.at(0).at(0));
					}
					else if (traverIt->controls.at(0).at(0) == swapTempcontrols)
					{
						++(traverIt->controls.at(0).at(0));
					}
					else if (traverIt->controls.at(0).at(0) == swapTemptargets)
					{
						--(traverIt->controls.at(0).at(0));
					}
				}
				else  //traverIt->controls.at(0).at(0) < traverIt->targets.at(0).at(0)  
				{
					if (traverIt->targets.at(0).at(0) == swapTempcontrols)
					{
						++(traverIt->targets.at(0).at(0));
					}
					else if (traverIt->targets.at(0).at(0) == swapTemptargets)
					{
						--(traverIt->targets.at(0).at(0));
					}
					else if (traverIt->controls.at(0).at(0) == swapTempcontrols)
					{
						++(traverIt->controls.at(0).at(0));
					}
					else if (traverIt->controls.at(0).at(0) == swapTemptargets)
					{
						--(traverIt->controls.at(0).at(0));
					}
				}
				updateNNC(gateVar);  //更新电路中各量子门的NNC
			}
			else  //traverIt->NNC == 0：最近邻状态以及NOT门
			{
				if (traverIt->name != "t1")  //CNOT门，V门，V+门
				{
					if (traverIt->controls.at(0).at(0) > traverIt->targets.at(0).at(0))
					{
						if (traverIt->controls.at(0).at(0) == swapTemptargets)
						{
							--(traverIt->controls.at(0).at(0));
							++(traverIt->targets.at(0).at(0));
						}
						else if (traverIt->targets.at(0).at(0) == swapTemptargets)  //bug找自Fig.7(b)  
						{
							--(traverIt->targets.at(0).at(0));
						}
						else if (traverIt->controls.at(0).at(0) == swapTempcontrols)
						{
							++(traverIt->controls.at(0).at(0));
						}
					}
					else  //traverIt->controls.at(0).at(0) < traverIt->targets.at(0).at(0)  
					{
						if (traverIt->targets.at(0).at(0) == swapTemptargets)
						{
							--(traverIt->targets.at(0).at(0));
							++(traverIt->controls.at(0).at(0));
						}
						else if (traverIt->controls.at(0).at(0) == swapTemptargets)
						{
							--(traverIt->controls.at(0).at(0));
						}
						else if (traverIt->targets.at(0).at(0) == swapTempcontrols)
						{
							++(traverIt->targets.at(0).at(0));
						}
					}
				}
				else  //NOT门
				{
					if (traverIt->targets.at(0).at(0) == swapTempcontrols)  //如果NOT门的目标位和traverIt对应的控制位相等
					{
						traverIt->targets.at(0).at(0) = swapTemptargets;
					}
					if (traverIt->targets.at(0).at(0) == swapTemptargets)  //如果NOT门的目标位和traverIt对应的目标位相等
					{
						traverIt->targets.at(0).at(0) = swapTempcontrols;
					}
				}
				updateNNC(gateVar);  //更新电路中各量子门的NNC
			}
		}	
	}
}

//插入交换门后上移位置
void Circuit:: changeLineUp(list<Gate>::iterator it, char swapTempcontrols, char swapTemptargets, list<Gate> &gateVar)
{
	//模拟Swap门的插入。遍历电路，根据目标位与控制位的位置关系，对门的位置进行改变。
	for (list <Gate>::iterator traverIt = it; traverIt != gateVar.end(); ++traverIt)
	{
		if(traverIt->name == "t1" || traverIt->name == "t2" || traverIt->name == "v2" || 
			traverIt->name == "v+")  //not、c-not、v、v+
		{
			updateNNC(gateVar);  //更新电路中各量子门的NNC
			if (traverIt->NNC > 0)  //traverIt对应的量子门非近邻
			{
				if (traverIt->controls.at(0).at(0) > traverIt->targets.at(0).at(0))
				{
					if (traverIt->targets.at(0).at(0) == swapTempcontrols)
					{
						++(traverIt->targets.at(0).at(0)); 
					}
					else if (traverIt->targets.at(0).at(0) == swapTemptargets)
					{
						--(traverIt->targets.at(0).at(0));
					}
					else if (traverIt->controls.at(0).at(0) == swapTempcontrols)
					{
						++(traverIt->controls.at(0).at(0));
					}
					else if (traverIt->controls.at(0).at(0) == swapTemptargets)
					{
						--(traverIt->controls.at(0).at(0));
					}
				}
				else  //traverIt->controls.at(0).at(0) < traverIt->targets.at(0).at(0)  
				{
					if (traverIt->targets.at(0).at(0) == swapTempcontrols)
					{
						++(traverIt->targets.at(0).at(0));
					}
					else if (traverIt->targets.at(0).at(0) == swapTemptargets)
					{
						--(traverIt->targets.at(0).at(0));
					}
					else if (traverIt->controls.at(0).at(0) == swapTempcontrols)
					{
						++(traverIt->controls.at(0).at(0));
					}
					else if (traverIt->controls.at(0).at(0) == swapTemptargets)
					{
						--(traverIt->controls.at(0).at(0));
					}
				}
				updateNNC(gateVar);  //更新电路中各量子门的NNC
			}
			else  //traverIt->NNC == 0：最近邻状态以及NOT门
			{
				if (traverIt->name != "t1")  //CNOT门，V门，V+门  
				{
					if (traverIt->controls.at(0).at(0) > traverIt->targets.at(0).at(0))
					{
						if (traverIt->controls.at(0).at(0) == swapTemptargets)
						{
							--(traverIt->controls.at(0).at(0));
							++(traverIt->targets.at(0).at(0));
						}
						else if (traverIt->controls.at(0).at(0) == swapTempcontrols)
						{
							++(traverIt->controls.at(0).at(0));
						}
						else if (traverIt->targets.at(0).at(0) == swapTemptargets)
						{
							--(traverIt->targets.at(0).at(0));
						}
					}
					else  //traverIt->controls.at(0).at(0) < traverIt->targets.at(0).at(0)  
					{
						if (traverIt->targets.at(0).at(0) == swapTemptargets)
						{
							--(traverIt->targets.at(0).at(0));
							++(traverIt->controls.at(0).at(0));  
						}
						else if (traverIt->targets.at(0).at(0) == swapTempcontrols)
						{
							++(traverIt->targets.at(0).at(0));
						}
						else if (traverIt->controls.at(0).at(0) == swapTemptargets)
						{
							--(traverIt->controls.at(0).at(0));
						}
					}
				}
				else  //NOT门
				{
					if (traverIt->targets.at(0).at(0) == swapTempcontrols)  //如果NOT门的目标位和traverIt对应的控制位相等
					{
						traverIt->targets.at(0).at(0) = swapTemptargets;
					}
					if (traverIt->targets.at(0).at(0) == swapTemptargets)  //如果NOT门的目标位和traverIt对应的目标位相等
					{
						traverIt->targets.at(0).at(0) = swapTempcontrols;
					}
				}
				updateNNC(gateVar);  //更新电路中各量子门的NNC
			}
		}	
	}
}

//插入交换门，实现最近邻
void Circuit:: insertSwap(list<Gate> &gateVar,vector<string> &line)
{
	int downSwapCount = 0;
	updateNNC(gateVar);  //初始化电路中量子门的NNC
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end();it++ )
	{
		//前瞻交换门序
		if ( it->name != "t1" )
		{
			do
			{
				changeGateOrder(it,gateVar);
				reorderGateId(gateVar);
			} while (changeGateOrder(it,gateVar) == 1); //=0即没有交换位置
			//changeGateOrder(it,gateVar); //将NNC=0的左移		
		}
		//前瞻添加交换门
		if (it->NNC > 0)
		{
			downSwapCount += ngLookahead(it,gateVar,line);
		}
		reorderGateId(gateVar);	
	}
	updateNNC(gateVar); //更新NNC
}

//计算电路的最近邻代价
int Circuit:: calculateNNC(list<Gate> &gateVar)
{
	int nncNum = 0;
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end(); ++it)
	{
		if (it->name == "t1" || it->name == "s")
		{
			continue;
		}
		nncNum += it->NNC;
	}
	return nncNum;
}

//删除冗余交换门
void Circuit:: removeSwap(list<Gate> &gateVar)  
{
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end();)
	{
		list<Gate>::iterator tempIt = ++it;
		--it;
		//如果满足deletion rule，则对SWAP门进行删除
		if ( it->name == "s" && tempIt->name == "s" ) 
		{
			if (((it->targets.at(0).at(0) == tempIt->targets.at(0).at(0)) && (it->targets.at(1).at(0) == tempIt->targets.at(1).at(0))) ||
				 ((it->targets.at(0).at(0) == tempIt->targets.at(1).at(0)) && (it->targets.at(1).at(0) == tempIt->targets.at(0).at(0))))
			{
				it = gateVar.erase(it);
				it = gateVar.erase(it);
			}
			else
				++it;
		}
		else
			++it;
	}
}

//统计电路交换门的个数
int Circuit:: calculateSgate(list<Gate> &gateVar)
{
	int snum = 0;
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end();it++)
	{

		if ( it->name == "s") //遇到交换门 ++
		{
			snum++;
		}
	}
	return snum ;
}

//统计电路量子代价
int Circuit:: calculateQC(list<Gate> &gateVar)  
{
	int quantumCost = 0;
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end(); ++it)
	{
		if (it->name != "s")
		{
			++quantumCost;
		}
		else
		{
			quantumCost = quantumCost + 3;
		}
	}
	return quantumCost;
}

//插入交换门改变线序
void Circuit:: ReorderLine(list<Gate> &gateVar,vector<string> &line)
{
	int j = 0; //控制line0
	int i = 0; //控制line1

	//判断是否需要添加线
	if ( line.size() < wires.size() ) //需要添加辅助位
	{
		string b;
		charToString('a'+n-1,b);
		line.push_back(b);
	}

	//添加交换门，变为原始线序
	for (; j < n; i++) //控制line1
	{
		if (line.at(i) == wires.at(j) && i != j) //line.at(i)需要上移
		{
			while ( line.at(j) != wires.at(j) )
			{
				Gate upSwapGate;
				upSwapGate.name = "s"; 
				upSwapGate.targets.push_back(wires.at(i-1));
				upSwapGate.targets.push_back(wires.at(i));
				swap(line.at(i),line.at(i-1));
				gateVar.push_back(upSwapGate);
				i--;
			}
			j++;
			i = 0;
		}
		else if ( i== n-1 )
		{
			j++;
			i = 0;
		}
		
	}
}

//交换门序（前瞻）
void Circuit:: reorderGate(list<Gate> &gateVar)
{
	updateNNC(gateVar);
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end();it++ )
	{
		if ( it->name != "t1" )
		{
			changeGateOrder(it,gateVar); //前瞻交换门的顺序			
		}
		reorderGateId(gateVar); //排序号
	}
}

//交换门序
int Circuit::changeGateOrder(list<Gate>::iterator iter, list<Gate> &gateVar) //返回值确定是否进行了位置的交换
{
	int FLAG = 0; //=1则进行了位置的交换

	if ((unsigned int)iter->id == gateVar.size() ) 
	{
		return FLAG; //最后一个门直接不进行操作
	}

	//前瞻N，判断是否可以进行交换，比较NNC，将NNC小的前移
	
	list<Gate>::iterator moveIt = iter;  //定义一个移动的迭代器，用于移动访问电路中的量子门
	++moveIt;

	int flagc = 0; //=1则不能交换
	int flagt = 0;
	vector<string> temptargets; //临时存储目标线
	vector<string> tempcontrols; //临时存储控制线
	temptargets.clear();
	tempcontrols.clear();
	//iter信息存入
	temptargets.push_back(iter->targets.at(0));
	tempcontrols.push_back(iter->controls.at(0));

	for(int i = 0;i < locaN2; ++i)  
	{
		//判断是否可以交换
		if ( moveIt->name == "t1" ) 
		{
			temptargets.push_back(moveIt->targets.at(0));
			if ( moveIt->id == gateVar.size() ) //最后一个门
			{
				break;
			}
			else
			{
				if (moveIt->id - iter->id < locaN2)
				{
					moveIt++;
				    continue;
				}
				else // NOT门的一种特殊情况
				{
					//检测是否可以交换
					for (int i = 0; i < tempcontrols.size(); i++) //检测moveit的控制位
					{
						if ( flagc == 1 )  //优化算法，当目标位冲突时没有必要再验证控制位
						{
							break;
						}
						if ( moveIt->targets.at(0) == tempcontrols.at(i) )
						{
							flagc = 1;
							break;
						}
					}
				}
				
			}			
		}
		else //检测moveit的控制位和目标位
		{
			for (int i = 0; i < tempcontrols.size(); i++) //检测moveit的目标位
			{
				if ( moveIt->targets.at(0) == tempcontrols.at(i) )
				{
					flagc = 1; 
					break;
				}
			}
			for (int i = 0; i < temptargets.size(); i++) //检测moveit的控制位
			{
				if ( flagc == 1 )  //优化算法，当目标位冲突时没有必要再验证控制位
				{
					break;
				}
				if ( moveIt->controls.at(0) == temptargets.at(i) )
				{
					flagt = 1; 
					break;
				}
			}
		}
		if ( flagc == 1 || flagt == 1 ) //不能交换
		{
			temptargets.push_back(moveIt->targets.at(0));
			tempcontrols.push_back(moveIt->controls.at(0));
			//重置flagc和flagt
			flagc = 0;
			flagt = 0;
			if ( moveIt->id == gateVar.size() ) //最后一个门
			{
				break;
			}
			else
			{
				moveIt++;
				continue;
			}
		}
		else //可以交换
		{
			//比较NNC
			if (moveIt->name != "t1")
			{
				if ( moveIt->NNC == 0 ) //前移
				{
					FLAG = 1;
					temptargets.push_back(moveIt->targets.at(0));
					tempcontrols.push_back(moveIt->controls.at(0));
					gateVar.insert(iter,*moveIt);
					list<Gate>::iterator temp = moveIt;
					if ( moveIt->id == gateVar.size() - 1 ) //最后一个门 因为多一个门，所以-1
					{
						gateVar.erase(temp); //删门
						break;
					}
					else
					{
						moveIt++;
						gateVar.erase(temp); //删门
						continue;
					}	
				}
				else //不动
				{
					temptargets.push_back(moveIt->targets.at(0));
					tempcontrols.push_back(moveIt->controls.at(0));
					if ( moveIt->id == gateVar.size() ) //最后一个门
					{
						break;
					}
					else
					{
						moveIt++;
						continue;
					}
				}
			}
			else //可以交换的是NOT门
			{
				FLAG = 1;
				temptargets.push_back(moveIt->targets.at(0));
				gateVar.insert(iter,*moveIt);
				list<Gate>::iterator temp = moveIt;
				if ( moveIt->id == gateVar.size() - 1 ) //最后一个门 因为多一个门，所以-1
				{
					gateVar.erase(temp); //删门
					break;
				}
				else
				{
					moveIt++;
					gateVar.erase(temp); //删门
					continue;
				}	
			}
			
			
		}
	}
	return FLAG;
}

//对电路的具体操作
void Circuit:: operation(list<Gate> &gateVar,vector<string> &line)
{
	reorderGateId(gateVar);

	//分解
	for ( list<Gate>::reverse_iterator iter = gateVar.rbegin(); iter != gateVar.rend(); )
	{
		if (iter->name != "t1" && iter->name != "t2" && iter->name != "v2" && iter->name != "v+")
		{
			toffTransNcv(*iter,gateVar);
		}
		else
		{
			iter++;
		}
	}
	
	//更新line
	line = wires; 
	                                
	reorderGateId(gateVar);
	
	//删除冗余门、调整更新门的顺序
	removeGate(gateVar);	
	reorderGateId(gateVar);

	//启发式前瞻交换门的顺序
	//reorderGate(gateVar);
	//reorderGateId(gateVar);
	
	//前瞻法实现LNN
	insertSwap(gateVar,line);  
	
	//更新电路门ID，删除冗余门
	removeGate(gateVar);
	reorderGateId(gateVar);
	
	//更新gates
	gates = gateVar; //必须加这句，不然gates不变化
}
