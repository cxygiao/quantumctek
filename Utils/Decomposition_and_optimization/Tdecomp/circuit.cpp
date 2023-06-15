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

//��.real�ļ������·
void Circuit::initial()
{
	//��ʼ�����������
	gates.clear(); //�����
	n = 0;  //�߸���
	gnum = 0;  //ԭʼ�Ÿ���
	ifstream inCircuit;
	string readFileName; //��ȡ���ļ���
	
	cout<<"������Ҫ���ļ���:";
	cin>>readFileName;
	inCircuit.open("F:\\workspace\\Paper\\NearestNeighborCircuit\\NearestNeighborCircuit\\Benchmark\\" + readFileName);
	if (!inCircuit.is_open())  
	{
		cout<<"\n���ܴ��ļ���"<<endl;
		cout<<"������ֹ��"<<endl;
	}

	//���л�ȡ����
	string gateDataStr;  
	string lable;
	while ( getline( inCircuit,gateDataStr ) ) //����һ�����ݣ�gateDataΪ����.
	{
		istringstream record(gateDataStr);
		record >> lable;
		if (lable == ".numvars") //����
		{
			record >> n;
		}
		if (lable == ".variables") //����
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
				else if (gateDataStr == "") //�����ж���һ�У�ֱ��.endʱ�Ž�����ȡ
				{

				}
				else
				{
					istringstream record(gateDataStr);
					gnum++;
					Gate g;
					string wire; 	
					g.id = gnum;
					record >> g.name; //������
					while (record >> wire)
					{			
						g.controls.push_back(wire);	
						g.lines.push_back(wire);
					}
					g.targets.push_back(g.controls.back()); 
					g.controls.pop_back(); 
					g.c = g.controls.size(); //����λ�ĸ���
					g.NNC = -1; //��ʼ��NNC
					gates.push_back(g);
				}
			}
		}
	}

}

//charת����string
void Circuit:: charToString(const char &charVar,string &stringVar)
{
	stringstream stream;
	stream << charVar;
	stringVar = stream.str();
}

//�Ե�·�������±��
void Circuit:: reorderGateId(list<Gate> &gateVar)
{
	int i = 1;
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end(); ++it, ++i)
	{
		it->id = i;
	}
}

//��ʾ��·
void Circuit:: showCir(list<Gate> &gateVar)  
{
	cout<<setfill(' ')<<setw(20)<<"id"<<setfill(' ')<<setw(20)<<"controls"
		<<setfill(' ')<<setw(20)<<"targets"<<endl;
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end(); ++it)
	{
		if (it->name == "t1")
		{
			cout<<"NOT��"<<setfill(' ')<<setw(12)<<it->id<<setfill(' ')<<setw(20)<<char(32)
				<<setfill(' ')<<setw(20)<<it->targets.at(0)<<endl;
		} 
		else if (it->name == "t2")
		{
			cout<<"CNOT��"<<setfill(' ')<<setw(11)<<it->id<<setfill(' ')<<setw(20)<<it->controls.at(0)   
				<<setfill(' ')<<setw(20)<<it->targets.at(0)<<endl;
		} 
		else if (it->name == "v2")
		{
			cout<<"V��"<<setfill(' ')<<setw(14)<<it->id<<setfill(' ')<<setw(20)<<it->controls.at(0)
				<<setfill(' ')<<setw(20)<<it->targets.at(0)<<endl;
		} 
		else if (it->name == "v+") 
		{
			cout<<"V+��"<<setfill(' ')<<setw(13)<<it->id<<setfill(' ')<<setw(20)<<it->controls.at(0)
				<<setfill(' ')<<setw(20)<<it->targets.at(0)<<endl;
		}
		else  
		{
			cout<<"SWAP��"<<setfill(' ')<<setw(11)<<it->id<<setfill(' ')<<setw(20)<<it->targets.at(0)
				<<setfill(' ')<<setw(20)<<it->targets.at(1)<<endl;
		}
	}
}

//ת��MCT
void Circuit:: toffTransNcv(Gate tempToffGate, list<Gate> &gateVar) 
{
	vector<Gate> toffToNcv; //һ��Toffoli��ת��Ϊ5������������
	vector<Gate> mctdec; //�ֽ����λ����2��Toffoli��
	vector<string> emptyline; //��ſ�����
	int emptylineNum = 0; //�����ߵĸ���

	//����λ�Ƿ�>2
	if(tempToffGate.c == 2) //�ֽ�2����λtoffoli��
	{
		//��������ۣ��������޶���
		if ( tempToffGate.NNC == -1 )  //�趨������ʱ��Ϊ-1
		{
			for ( int i = 0; i < 5; ++i )  
			{
				Gate tempGate;  //��ʱ������������������Ļ���
				tempGate.id = tempToffGate.id + i;  //������Toffoli�ŷֽ�õ��Ļ��������ŵ�ID
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
				toffToNcv.push_back(tempGate);  //����ʱ�����Ļ������ݴ浽toffToNcv������
			}
		}
		else if ( tempToffGate.NNC == -2 ) //ת��Ϊת��
		{
			for ( int i = 0; i < 5; ++i )  
			{
				Gate tempGate;  //��ʱ������������������Ļ���
				tempGate.id = tempToffGate.id + i;  //������Toffoli�ŷֽ�õ��Ļ��������ŵ�ID
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
				toffToNcv.push_back(tempGate);  //����ʱ�����Ļ������ݴ浽toffToNcv������
			}
		}
		
		
		//���ֽ�toffoli�ź�õ���NCV��������뵽���ӵ�·��
		list <Gate>::reverse_iterator it;
		for (it = gateVar.rbegin(); it->name != tempToffGate.name; ++it)
		{
			//�ҵ�ָ��tempToffGate��it
		}
		//��tempToffGate��֮ǰ����ֽ�֮���NCV�ſ�
		list <Gate> ::iterator iter((++it).base());
		gateVar.insert(iter, toffToNcv.begin(), toffToNcv.end()); 
		//����λ��ɾ�����ӵ�·�е�Toffoli��(tempToffGate) (*****ע��erase()�ķ���ֵ*****)
		it = list<Gate>::reverse_iterator(gateVar.erase(it.base())); 
		vector <Gate>().swap(toffToNcv); //�ͷ��ڴ�
	}
	//����λ>2
	else
	{
		//�ж��Ƿ���Ҫ��Ӹ���λ
		if ( tempToffGate.c == n - 1 ) //��Ҫ��Ӹ���λ
		{
			string b;
			charToString('a'+n,b);
			wires.push_back(b);
			n++;		
		}
		
		//�жϿ��������ļ���
		for (int i = 0; i < n; i++)
		{
			int flag = 0;
			for (int j = 0; j <= tempToffGate.c; j++) //ȡ�Ⱥű�ʾҪ��һ��Ŀ��λ����
			{
				if ( wires.at(i) == tempToffGate.lines.at(j) )
				{
					flag = 1;
					break; //������ѭ��
				}
			}
			if ( flag == 0 ) //˵�����߿���
			{
				emptylineNum++;
				emptyline.push_back(wires.at(i));
			}
		}

		//�ж�������һ�ַֽⷽ��
		if ( tempToffGate.c <= (int)ceil(n/2.0) ) //���ڵ�һ��
		{
			//�����µ���
			
			//���һ��
			for (int i = 0; i < tempToffGate.c-2; i++)
			{
				Gate tempGate;  //��ʱ������������������Ļ���
				string tempname = "t" + to_string(3) ;//������Ҫ��һλ
				tempGate.name = tempname;
				tempGate.id = tempToffGate.id + i;  //������Toffoli�ŷֽ�õ��Ļ��������ŵ�ID
				tempGate.c = 2; //ת�������2����Toffoli
				tempGate.NNC = -1; //Ϊ-1ʱֱ��ת����-2ʱת����ת��
				tempGate.controls.push_back(tempToffGate.controls.at(tempToffGate.c - 1 - i));
				tempGate.lines.push_back(tempToffGate.controls.at(tempToffGate.c - 1 - i));
				tempGate.controls.push_back(emptyline.at(emptylineNum-1-i)); //�ڿ����ߵ�λ��
				tempGate.lines.push_back(emptyline.at(emptylineNum-1-i));
				if ( i == 0) //��һ����
				{
					tempGate.targets.push_back(tempToffGate.targets.at(0));
					tempGate.lines.push_back(tempToffGate.targets.at(0));
					mctdec.push_back(tempGate);
				}
				else
				{
					tempGate.targets.push_back(mctdec.at(i-1).controls.at(1)); //��ǰһ���ŵĵڶ�������λ��ͬ
					tempGate.lines.push_back(mctdec.at(i-1).controls.at(1));
					mctdec.push_back(tempGate);
				}
			}
			
			//�м���ߵ���
			Gate tempGate;  //��ʱ������������������Ļ���
			string tempname = "t" + to_string(3) ;//������Ҫ��һλ
			tempGate.name = tempname;
			tempGate.id = tempToffGate.id + tempToffGate.c-2;  //������Toffoli�ŷֽ�õ��Ļ��������ŵ�ID
			tempGate.c = 2; //ת�������2����Toffoli
			tempGate.NNC = -1; //Ϊ-1ʱֱ��ת����-2ʱת����ת��
			tempGate.controls.push_back(tempToffGate.controls.at(0));
			tempGate.controls.push_back(tempToffGate.controls.at(1));
			tempGate.targets.push_back(mctdec.at(tempToffGate.c-3).controls.at(1));
			mctdec.push_back(tempGate);
			
			//�����һ��
			for (int i = 0; i < tempToffGate.c-2; i++)
			{
				Gate tempGate;  //��ʱ������������������Ļ���
				string tempname = "t" + to_string(3) ;//������Ҫ��һλ
				tempGate.name = tempname;
				tempGate.id = tempToffGate.id + tempToffGate.c-1 + i;  //������Toffoli�ŷֽ�õ��Ļ��������ŵ�ID
				tempGate.c = 2; //ת�������2����Toffoli
				tempGate.NNC = -2; //Ϊ-1ʱֱ��ת����-2ʱת����ת��
				tempGate.controls.push_back(mctdec.at(tempToffGate.c-3-i).controls.at(0));
				tempGate.lines.push_back(mctdec.at(tempToffGate.c-3-i).controls.at(0));
				tempGate.controls.push_back(mctdec.at(tempToffGate.c-3-i).controls.at(1)); 
				tempGate.lines.push_back(mctdec.at(tempToffGate.c-3-i).controls.at(1));
				tempGate.targets.push_back(mctdec.at(tempToffGate.c-3-i).targets.at(0)); 
				tempGate.lines.push_back(mctdec.at(tempToffGate.c-3-i).targets.at(0));
				mctdec.push_back(tempGate);
			}	
			
			//�Ҳ�  ��mectdec�г���β����ѹ��ȥ
			vector <Gate> tempmctdec;  //��ʱ�洢��ȡ����
			for ( vector <Gate>::iterator it = mctdec.begin()+1; it < mctdec.end()-1; it++)
			{
				Gate tempGate;  //��ʱ������������������Ļ���
				tempGate.name = it->name;
				tempGate.id = it->id;  
				tempGate.c = it->c; //ת�������2����Toffoli
				if ( it->controls.at(0) != tempToffGate.controls.at(0) ) //������ߵ��� NNC��ͬ
				{
					tempGate.NNC = it->NNC;
				}
				else  //����ߵ��� NNC�෴��ȡ-2
				{
					tempGate.NNC = -2;
				}
				tempGate.controls = it->controls;
				tempGate.targets = it->targets;
				tempmctdec.push_back(tempGate);
			}
			//������vector����
			mctdec.insert(mctdec.end(),tempmctdec.begin(),tempmctdec.end());	
			
			//�������ţ�ɾ��ԭ��
			list <Gate>::reverse_iterator it;
			for (it = gateVar.rbegin(); it->name != tempToffGate.name; ++it)
			{
				//�ҵ�ָ��tempToffGate��it
			}
			//��tempToffGate��֮ǰ����ֽ�֮���NCV�ſ�
			list <Gate> ::iterator iter((++it).base());
			gateVar.insert(iter, mctdec.begin(), mctdec.end());
			//����λ��ɾ�����ӵ�·�е�Toffoli��(tempToffGate) (*****ע��erase()�ķ���ֵ*****)
			it = list<Gate>::reverse_iterator(gateVar.erase(it.base()));  
			vector <Gate>().swap(mctdec);
		}
		else //���ڵڶ���
		{
			//��������
			for (int i = 0; i < 4; i++)
			{
				Gate tempGate;  //��ʱ������������������Ļ���
				tempGate.id = tempToffGate.id + i;  //������Toffoli�ŷֽ�õ��Ļ��������ŵ�ID
				if ( i == 0 || i == 2 )
				{
					string tempname = "t" + to_string((int)(ceil(n/2.0)+1)) ;//������Ҫ��һλ
					tempGate.name = tempname;
					tempGate.c = (int)(ceil(n/2.0)); //��ſ���λ�ĸ���
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
					string tempname = "t" + to_string((tempToffGate.c - (int)ceil(n/2.0) + 2)) ;//������Ҫ��һλ
					tempGate.name = tempname;
					tempGate.c = tempToffGate.c - (int)ceil(n/2.0) + 1; //��ſ���λ�ĸ���
					if ( tempGate.c <= 2 ) //ֱ�ӽ������һ�Ļ���
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
			
			//ɾ��ԭ��
			list <Gate>::reverse_iterator it;
			for (it = gateVar.rbegin(); it->name != tempToffGate.name; ++it)
			{
				//�ҵ�ָ��tempToffGate��it
			}
			//��tempToffGate��֮ǰ����ֽ�֮���NCV�ſ�
			list <Gate> ::iterator iter((++it).base());
			gateVar.insert(iter, mctdec.begin(), mctdec.end());
			//����λ��ɾ�����ӵ�·�е�Toffoli��(tempToffGate) (*****ע��erase()�ķ���ֵ*****)
			it = list<Gate>::reverse_iterator(gateVar.erase(it.base()));  
			vector <Gate>().swap(mctdec);
		}
	}
}

//ɾ��������
void Circuit:: removeGate(list<Gate> &gateVar)
{
	vector<string> temptargetss; //��ʱ�洢Ŀ����
	vector<string> tempcontrolss; //��ʱ�洢������
	int flag = 0; //�����Ƿ����ſ���ɾȥ
	int i = 0;
	int add = 0; //�����Ƿ���Ҫ���1
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end();)  
	{
		if ( i == gateVar.size()-1 )  //��·ֻ��һ����
		{
			break;
		}
		if ( it == (--gateVar.end()) )  //���������һ����
		{
			break;
		}
		if ( it->name == "v2" || it->name == "v+" || it->name == "t2" )  //v��v+�š�����cnot������
		{
			//�������
			tempcontrolss.clear();
			temptargetss.clear();
			add = 0;
			list<Gate>::iterator moveit = ++it;
			it--;	
			for (; moveit != gateVar.end();) 
			{
				if ( moveit->name == "t1" ) //����not   
				{
					flag = 1;
					temptargetss.push_back(moveit->targets.at(0));
					moveit++;
					continue;
				}
				if ( moveit->name == "s" ) //����swap
				{
					flag = 1;
					temptargetss.push_back(moveit->targets.at(0));
					temptargetss.push_back(moveit->targets.at(1));
					moveit++;
					continue;
				}
				if ( (it->controls == moveit->controls)&&(it->targets == moveit->targets)  )
				{
					//�������ڵ���
					if ( tempcontrolss.empty() ) //Ϊ��
					{
						if ( temptargetss.empty() ) //Ϊ��
						{
							add = 1;
						}
					}
					for (vector<string>::iterator iter = temptargetss.begin(); iter != temptargetss.end();) //�ж�����֮�����   
					{
						if ( *iter == moveit->controls.at(0) ) //moveit��ָ�ŵĿ���λ����������Ŀ��λ
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
							if ( *iter == moveit->targets.at(0) ) //moveit��ָ�ŵ�Ŀ��λ���������п���λ
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
					if ( flag == 0 ) //�ж�������������
					{
						if ( it->name == "t2" && moveit->name == "t2" ) //����cnot
						{
							it = gateVar.erase(it); //ע�⣺��ʱit��moveit��ָ�������һ��
							if ( add == 1 ) //ɾ�������ţ���Ҫ������λ
							{
								it++;
							}
							moveit = gateVar.erase(moveit);
							break;
						}
						else if ( (it->name == "v2" && moveit->name == "v+") || (it->name == "v+" && moveit->name == "v2")) //һ��vһ��v+
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
		else if ( it->name == "t1" ) //not��
		{
			//�������
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
						//�������ڵ���
						if ( tempcontrolss.empty() ) //Ϊ��
						{						
							add = 1;							
						}
						//�ж�Ŀ��λ������ǰ����û�п�����
						for (vector<string>::iterator iter = tempcontrolss.begin(); iter != tempcontrolss.end();)
						{
							if ( *iter == moveit->targets.at(0) ) //moveit��ָ�ŵ�Ŀ��λ���������п���λ
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
				else //moveit��Ϊnot��
				{
					flag = 1;					
					if ( moveit->name == "s" )  //moveitΪ������
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
		else if ( it->name == "s" ) //swap��  �˴���ɾ�����Ƿ����ڵĽ�����
		{
			//�������
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
						//�������ڵ���
						if ( tempcontrolss.empty() ) //Ϊ��
						{
							if ( temptargetss.empty() ) //Ϊ��
							{
								add = 1;
							}
						}
						//�ж�Ŀ��λ��������û�п���λ��Ŀ��λ
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
						if ( flag == 0 ) //����ɾ����
						{
							it = gateVar.erase(it);
							if ( add == 1 )
							{
								it++;
							}
							moveit = gateVar.erase(moveit);
							break;
						}
						else //�м���������
						{
							flag = 1;			
							temptargetss.push_back(moveit->targets.at(0));				
							temptargetss.push_back(moveit->targets.at(1));
							moveit++;
						}
					}
					else //moveit�ǽ�����
					{
						flag = 1;
						temptargetss.push_back(moveit->targets.at(0));				
						temptargetss.push_back(moveit->targets.at(1));
						moveit++;
					}
				}
				else //moveit���ǽ�����
				{
					flag = 1;
					if ( moveit->name == "t1" ) //moveitΪnot��
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

//���㵥���ŵ�NNC
void Circuit:: updateNNC(list<Gate> &gateVar)
{
	//����������Ŀ��λ�Ϳ���λ֮��ľ���
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

//���µ����ţ���Ҫswap�Ĵ���
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

//����downSwapCost
int Circuit:: ngLookahead_1( list<Gate>::iterator iter, list<Gate> &gateVar) 
{
	int downSwapCost = 0;

	//iter�����һ����
	if ((unsigned int)iter->id == gateVar.size())
	{
		downSwapCost += abs(iter->controls.at(0).at(0) - iter->targets.at(0).at(0)) - 1;
		return downSwapCost;
	}
	
	list <Gate>::iterator moveIt = iter;  //����һ���ƶ��ĵ������������ƶ����ʵ�·�е�������
	++moveIt;
    if (moveIt->name == "s" ) //Ҫ��λ���ǽ����ŵ�
	{
		++moveIt;
	}
	
	//˳�������G.p��ʼ�ĺ��G.n��Swap Cost
	for(int i = 0;i < locaN; ++i)  
	{
		if ((unsigned int)iter->id < gateVar.size())
		{
			//������Similar
			if (moveIt->name == "t1" || moveIt->name == "s" || (iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0) && 
				iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0)) || 
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0) && 
				iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0)))
			{
				//�ж����������Ƿ������һ����
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
				downSwapCost += moveIt->NNC;  //ע�������moveIt��ָ���λ��(֮ǰmoveIt������++����).
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

//����upSwapCost
int Circuit:: ngLookahead_2( list<Gate>::iterator iter, list <Gate> &gateVar)  
{
	int upSwapCost = 0;
	
	//iter�����һ����
	if ((unsigned int)iter->id == gateVar.size())
	{
		upSwapCost += abs(iter->controls.at(0).at(0) - iter->targets.at(0).at(0)) - 1;
		return upSwapCost;
	}

	list <Gate>::iterator moveIt = iter;  //����һ���ƶ��ĵ������������ƶ����ʵ�·�е�������
	++moveIt;
	if (moveIt->name == "s" ) //Ҫ��λ���ǽ����ŵ�
	{
		++moveIt;
	}

	for(int i = 0;i < locaN; ++i)  //˳�������G.p��ʼ�ĺ��G.n��Swap Cost
	{
		if ((unsigned int)iter->id < gateVar.size())
		{
			//������Similar
			if (moveIt->name == "t1" || moveIt->name == "s" || (iter->controls.at(0).at(0) == moveIt->controls.at(0).at(0) && 
				iter->targets.at(0).at(0) == moveIt->targets.at(0).at(0)) || 
				(iter->controls.at(0).at(0) == moveIt->targets.at(0).at(0) && 
				iter->targets.at(0).at(0) == moveIt->controls.at(0).at(0)))
			{
				//�ж����������Ƿ������һ����
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
				upSwapCost += abs( iter->targets.at(0).at(0) - iter->controls.at(0).at(0)) -  1 ;  //�޸Ĵ���������������������������������������������
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

//����upDownSwapCost
int Circuit:: ngLookahead_3( list<Gate>::iterator iter,list <Gate> &gateVar )  
{
	int upDownSwapCost = 0;

	//iter�����һ����
	if ((unsigned int)iter->id == gateVar.size())
	{
		upDownSwapCost = -1;
		return upDownSwapCost;
	}

	list <Gate>::iterator moveIt = iter;  //����һ���ƶ��ĵ������������ƶ����ʵ�·�е�������
	++moveIt;
	
	for( int i = 0;i < locaN; ++i )  //˳�������G.p��ʼ�ĺ��G.n��Swap Cost
	{
		if ((unsigned int)iter->id < gateVar.size())
		{
			//������Similar
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
				//�ж�Gr
				if ( judgegr == 1 ) //Gr��Gn��һ����
				{
					upDownSwapCost += moveIt->NNC + calculateDGpr(iter,++moveIt);
					moveIt--; //��ԭ
				}
				else if ( judgegr == 0 )  //Gr = Gp
				{
					upDownSwapCost += 0;
				}
				else if ( judgegr == 2 ) //Gr��Gnǰһ����
				{
					upDownSwapCost += moveIt->NNC + calculateDGpr(iter,--moveIt);
					moveIt++; //��ԭ
				}
				else //Gr������
				{
					upDownSwapCost = -1; //���ֲ��������
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
				//�ж�Gr
				if ( judgegr == 1 ) //Gr��Gn��һ����
				{
					upDownSwapCost += moveIt->NNC + calculateUGpr(iter,++moveIt);
					moveIt--; //��ԭ
				}
				else if ( judgegr == 0 )  //Gr = Gp
				{
					upDownSwapCost += 0;
				}
				else if ( judgegr == 2 ) //Gr��Gnǰһ����
				{
					upDownSwapCost += moveIt->NNC + calculateUGpr(iter,--moveIt);
					moveIt++; //��ԭ
				}
				else //Gr������
				{
					upDownSwapCost = -1; //���ֲ��������
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
				//�ж�Gr
				if ( judgegr == 1 ) //Gr��Gn��һ����
				{
					upDownSwapCost += moveIt->NNC - calculateUGpr(iter,++moveIt);
					moveIt--; //��ԭ
				}
				else if ( judgegr == 0 )  //Gr = Gp
				{
					upDownSwapCost += 0;
				}
				else if ( judgegr == 2 ) //Gr��Gnǰһ����
				{
					upDownSwapCost += moveIt->NNC - calculateUGpr(iter,--moveIt);
					moveIt++; //��ԭ
				}
				else //Gr������
				{
					upDownSwapCost = -1; //���ֲ��������
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
				//�ж�Gr
				if ( judgegr == 1 ) //Gr��Gn��һ����
				{
					upDownSwapCost += moveIt->NNC - calculateDGpr(iter,++moveIt);
					moveIt--; //��ԭ
				}
				else if ( judgegr == 0 )  //Gr = Gp
				{
					upDownSwapCost += 0;
				}
				else if ( judgegr == 2 ) //Gr��Gnǰһ����
				{
					upDownSwapCost += moveIt->NNC - calculateDGpr(iter,--moveIt);
					moveIt++; //��ԭ
				}
				else //Gr������
				{
					upDownSwapCost = -1; //���ֲ��������
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
				//�ж�Gr
				if ( judgegr == 1 ) //Gr��Gn��һ����
				{
					upDownSwapCost += abs( moveIt->NNC -(++moveIt)->NNC );
					moveIt--; //��ԭ
				}
				else if ( judgegr == 0 )  //Gr = Gp
				{
					upDownSwapCost += 0;
				}
				else if ( judgegr == 2 ) //Gr��Gnǰһ����
				{
					upDownSwapCost += abs( moveIt->NNC - (--moveIt)->NNC );
					moveIt++; //��ԭ
				}
				else //Gr������
				{
					upDownSwapCost = -1; //���ֲ��������
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
				//�ж�Gr
				if ( judgegr == 1 ) //Gr��Gn��һ����
				{
					upDownSwapCost += abs( moveIt->NNC -(++moveIt)->NNC );
					moveIt--; //��ԭ
				}
				else if ( judgegr == 0 )  //Gr = Gp
				{
					upDownSwapCost += 0;
				}
				else if ( judgegr == 2 ) //Gr��Gnǰһ����
				{
					upDownSwapCost += abs( moveIt->NNC -(--moveIt)->NNC );
					moveIt++; //��ԭ
				}
				else //Gr������
				{
					upDownSwapCost = -1; //���ֲ��������
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

//ȷ��Gr����
int Circuit:: FindGr(list<Gate>::iterator iter,list<Gate>::iterator moveit,list <Gate> &gateVar)
{
	int flag1 = 0; //��Gp,Gn������case c ��Ϊ1
	int flag2 = 0; //��Gp,Gr������case c ��Ϊ1
	int flag3 = 0; //���������gr��gnǰ

	if ( locaN == 2 )
	{
		//ֻ��N=2�������ߴ���ͨ���Բ�ǿ
		list <Gate>::iterator gr;

		//���������1��moveitǰһ����not�ţ���һ����ȡ����   GnΪ���һ����
		//          2��gr��ָ������not��
		//          3��gr��gn��ǰһ����
		if ( (moveit->id - iter->id) > 1 || moveit->id == gateVar.size() ) //�������1
		{
			list <Gate>::iterator tempgr = --moveit;
			moveit++;
			if ( (moveit->id - iter->id) > 1 && tempgr->name != "t1" ) //gr��gn��ǰһ����
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
			gr = moveit;  //��Gp��ʼ�����ζ�������ָ��
			++gr;
			if ( gr->name == "t1" ) //�������2
			{
				gr = moveit;
			}
		}



		//��⣨Gp,Gn���Ƿ�����case c
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

		//��⣨Gp,Gr���Ƿ�����case c
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
				return 2; //��ʾGr��Gnǰһ����
			}
			else if ( flag1 == 1 )
			{
				return 0; //������ʱѡ����һ�����ʱ�ʾGr = Gn
			}
			else
			{
				return -1; //��ʾGr�����ڣ��������
			}

		}

		if ( flag1 == 1 )
		{
			if ( flag2 == 1 && moveit != gr )
			{
				return 1; //��ʾGr��Gn��һ����
			}
			else
			{
				return 0; //��ʾGr = Gn
			}
		}
		else
		{
			if ( flag2 ==1 )
			{
				return 1; //��ʾGr��Gn��һ����
			}
			else
			{
				return -1; //��ʾGr�����ڣ��������
			}
		}

	}
	else if ( locaN == 1 ) //N = 1
	{
		//��ʱmoveit����gr��ֻҪ�жϣ�Gp��Gr���Ƿ�����case c

		if ( (iter->controls.at(0).at(0) < moveit->targets.at(0).at(0) && moveit->targets.at(0).at(0) < iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == moveit->controls.at(0).at(0)) ||
			(iter->controls.at(0).at(0) > moveit->targets.at(0).at(0) && moveit->targets.at(0).at(0) > iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == moveit->controls.at(0).at(0)) ||
			(iter->targets.at(0).at(0) < moveit->controls.at(0).at(0) && moveit->controls.at(0).at(0) < iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == moveit->targets.at(0).at(0)) ||
			(iter->targets.at(0).at(0) > moveit->controls.at(0).at(0) && moveit->controls.at(0).at(0) > iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == moveit->targets.at(0).at(0)) ||
			(iter->controls.at(0).at(0) < moveit->controls.at(0).at(0) && moveit->controls.at(0).at(0) < iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == moveit->targets.at(0).at(0)) ||
			(iter->controls.at(0).at(0) > moveit->controls.at(0).at(0) && moveit->controls.at(0).at(0) > iter->targets.at(0).at(0) && iter->controls.at(0).at(0) == moveit->targets.at(0).at(0)) ||
			(iter->targets.at(0).at(0) < moveit->targets.at(0).at(0) && moveit->targets.at(0).at(0) < iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == moveit->controls.at(0).at(0)) ||
			(iter->targets.at(0).at(0) > moveit->targets.at(0).at(0) && moveit->targets.at(0).at(0) > iter->controls.at(0).at(0) && iter->targets.at(0).at(0) == moveit->controls.at(0).at(0)) )
		{
			flag1 = 1; //����case c
			return 0; //Gn����Gr
		}
		else
		{
			return -1; //Gr������
		}
	}
	

}

//����GpGr��dSC
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
		temp += gr->NNC;  //ע�������gr��ָ���λ��(֮ǰgr������++����).
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

//����GpGr��uSC
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

//ǰհ�㷨
int Circuit:: ngLookahead(list<Gate>::iterator iter, list<Gate> &gateVar, vector<string> &line)  //invoke ngLookahead_1/2/3��index���ȼ���(��λ)id
{
	//�����ĳ�ʼ��
	int upSwapCost = 0;
    int downSwapCost = 0;
	int upDownSwapCost = 0;
	int tempDownSwapCount = 0;  //��ʱ�洢downSwapCount
	int insertSwapApproFlag = 0;  //��ͬ��ֵ��Ӧ��ͬSwap�ŵĲ��뷽��(down��0��up��1��upDown��2) Ĭ������

	//���з�ʽ
	downSwapCost = ngLookahead_1( iter,gateVar );
	upSwapCost = ngLookahead_2( iter,gateVar );
	upDownSwapCost = ngLookahead_3(iter,gateVar);

	//ȷ��insertSwapApproFlag��ֵ(��ȷ��Swap�Ų���ķ���)
	if ( upDownSwapCost == -1 ) //Gr������
	{
		tempDownSwapCount =  __min(downSwapCost, upSwapCost);
		if (upSwapCost < downSwapCost )
		{
			insertSwapApproFlag = 1; //����
		}
	}
	else
	{
		//ȡ��������С��
		tempDownSwapCount =  __min(downSwapCost, upSwapCost);
		if ( upDownSwapCost < tempDownSwapCount )
		{
			tempDownSwapCount = upDownSwapCost;
			insertSwapApproFlag = 2; //������

		}
		else if ( upSwapCost < downSwapCost )
		{
			insertSwapApproFlag = 1; //����
		}
	}

	//��ʽ������ɺ󣬸���tempDownSwapCountȡС�������λ���б仯��ȷ��Swap�ŵĲ��뷽��������index����Ӧ����ǰ���в���
	//��һ����insertSwapPro()
	//�ڶ�����reorderid()
	//��������changeLineDown() Or changeLineUp()

	if (insertSwapApproFlag == 0)  //down
	{
		while (iter->NNC > 0)  //��iter��Ӧ���ŷ������
		{
			if (iter->controls.at(0).at(0) > iter->targets.at(0).at(0))  //�������λ����Ŀ��λ
			{
				int i = 0; //ȷ������������±�
				i = iter->targets.at(0).at(0) - 97;
				swap(line.at(i),line.at(i+1));
				insertSwapPro(iter, iter->targets.at(0).at(0), char(iter->targets.at(0).at(0) + 1), gateVar);  
				reorderGateId(gateVar);  
				//��iter���������Ž�����λ�ĸı�
				changeLineDown(iter, iter->targets.at(0).at(0), char(iter->targets.at(0).at(0) + 1), gateVar); 
			}
			else  //Ŀ��λ���ڿ���λ
			{
				int i = 0; //ȷ������������±�
				i = iter->controls.at(0).at(0) - 97;
                swap(line.at(i),line.at(i+1));
				insertSwapPro(iter, iter->controls.at(0).at(0), char(iter->controls.at(0).at(0) + 1), gateVar);  
				reorderGateId(gateVar);  
				//��iter���������Ž�����λ�ĸı�
				changeLineDown(iter, iter->controls.at(0).at(0), char(iter->controls.at(0).at(0) + 1), gateVar);  
			}
		}
	}
	else if ( insertSwapApproFlag == 1 ) //up
	{
		while (iter->NNC > 0)  
		{
			if (iter->controls.at(0).at(0) > iter->targets.at(0).at(0))  //�������λ����Ŀ��λ
			{
				int i = 0; //ȷ������������±�
				i = iter->controls.at(0).at(0) - 97;
				swap(line.at(i-1),line.at(i));
				insertSwapPro(iter, char(iter->controls.at(0).at(0) - 1), char(iter->controls.at(0).at(0)), gateVar);  
				reorderGateId(gateVar);  
				//��iter���������Ž�����λ�ĸı�
				changeLineUp(iter, char(iter->controls.at(0).at(0) - 1), char(iter->controls.at(0).at(0)),gateVar);  
			}
			else  //Ŀ��λ���ڿ���λ
			{
				int i = 0; //ȷ������������±�
				i = iter->targets.at(0).at(0) - 97;
				swap(line.at(i-1),line.at(i));
				insertSwapPro(iter, char(iter->targets.at(0).at(0) - 1), char(iter->targets.at(0).at(0)), gateVar);  
				reorderGateId(gateVar);  
				//��iter���������Ž�����λ�ĸı�
				changeLineUp(iter, char(iter->targets.at(0).at(0) - 1), char(iter->targets.at(0).at(0)), gateVar);  
			}
		}
	}
	else  //�ϡ�����
	{
		//�涨��ȡһ�룬һ�����ơ�һ�����ƣ������ִ������
		while (iter->NNC - iter->NNC/2.0 >= 1)  //����
		{
			if (iter->controls.at(0).at(0) > iter->targets.at(0).at(0))  //�������λ����Ŀ��λ
			{
				int i = 0; //ȷ������������±�
				i = iter->controls.at(0).at(0) - 97;
				swap(line.at(i-1),line.at(i));
				insertSwapPro(iter, char(iter->controls.at(0).at(0) - 1), char(iter->controls.at(0).at(0)), gateVar);  
				reorderGateId(gateVar);  
				//��iter���������Ž�����λ�ĸı�
				changeLineUp(iter, char(iter->controls.at(0).at(0) - 1), char(iter->controls.at(0).at(0)),gateVar);  
			}
			else  //Ŀ��λ���ڿ���λ
			{
				int i = 0; //ȷ������������±�
				i = iter->targets.at(0).at(0) - 97;
				swap(line.at(i-1),line.at(i));
				insertSwapPro(iter, char(iter->targets.at(0).at(0) - 1), char(iter->targets.at(0).at(0)), gateVar);  
				reorderGateId(gateVar);  
				//��iter���������Ž�����λ�ĸı�
				changeLineUp(iter, char(iter->targets.at(0).at(0) - 1), char(iter->targets.at(0).at(0)), gateVar);  
			}
		}
		while (iter->NNC > 0)  //����
		{
			if (iter->controls.at(0).at(0) > iter->targets.at(0).at(0))  //�������λ����Ŀ��λ
			{
				int i = 0; //ȷ������������±�
				i = iter->targets.at(0).at(0) - 97;
				swap(line.at(i),line.at(i+1));
				insertSwapPro(iter, iter->targets.at(0).at(0), char(iter->targets.at(0).at(0) + 1), gateVar);  
				reorderGateId(gateVar);  
				//��iter���������Ž�����λ�ĸı�
				changeLineDown(iter, iter->targets.at(0).at(0), char(iter->targets.at(0).at(0) + 1), gateVar); 
			}
			else  //Ŀ��λ���ڿ���λ
			{
				int i = 0; //ȷ������������±�
				i = iter->controls.at(0).at(0) - 97;
                swap(line.at(i),line.at(i+1));
				insertSwapPro(iter, iter->controls.at(0).at(0), char(iter->controls.at(0).at(0) + 1), gateVar);  
				reorderGateId(gateVar);  
				//��iter���������Ž�����λ�ĸı�
				changeLineDown(iter, iter->controls.at(0).at(0), char(iter->controls.at(0).at(0) + 1), gateVar);  
			}
		}
	}
	updateGate(gateVar);
	return tempDownSwapCount;
}

//����������ǰ���뽻����,�����Ͼ�����Gpǰ�����һ��������
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

//���뽻���ź�����λ��
void Circuit:: changeLineDown(list<Gate>::iterator it, char swapTempcontrols, char swapTemptargets, list<Gate> &gateVar)
{
	//ģ��Swap�ŵĲ��롣������·������Ŀ��λ�����λ��λ�ù�ϵ�����ŵ�λ�ý��иı䡣
	for (list <Gate>::iterator traverIt = it; traverIt != gateVar.end(); ++traverIt)
	{
		if(traverIt->name == "t1" || traverIt->name == "t2" || traverIt->name == "v2" || 
			traverIt->name == "v+")  //not��c-not��v��v+
		{
			updateNNC(gateVar);
			if (traverIt->NNC > 0)  //traverIt��Ӧ�������ŷǽ��� 
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
				updateNNC(gateVar);  //���µ�·�и������ŵ�NNC
			}
			else  //traverIt->NNC == 0�������״̬�Լ�NOT��
			{
				if (traverIt->name != "t1")  //CNOT�ţ�V�ţ�V+��
				{
					if (traverIt->controls.at(0).at(0) > traverIt->targets.at(0).at(0))
					{
						if (traverIt->controls.at(0).at(0) == swapTemptargets)
						{
							--(traverIt->controls.at(0).at(0));
							++(traverIt->targets.at(0).at(0));
						}
						else if (traverIt->targets.at(0).at(0) == swapTemptargets)  //bug����Fig.7(b)  
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
				else  //NOT��
				{
					if (traverIt->targets.at(0).at(0) == swapTempcontrols)  //���NOT�ŵ�Ŀ��λ��traverIt��Ӧ�Ŀ���λ���
					{
						traverIt->targets.at(0).at(0) = swapTemptargets;
					}
					if (traverIt->targets.at(0).at(0) == swapTemptargets)  //���NOT�ŵ�Ŀ��λ��traverIt��Ӧ��Ŀ��λ���
					{
						traverIt->targets.at(0).at(0) = swapTempcontrols;
					}
				}
				updateNNC(gateVar);  //���µ�·�и������ŵ�NNC
			}
		}	
	}
}

//���뽻���ź�����λ��
void Circuit:: changeLineUp(list<Gate>::iterator it, char swapTempcontrols, char swapTemptargets, list<Gate> &gateVar)
{
	//ģ��Swap�ŵĲ��롣������·������Ŀ��λ�����λ��λ�ù�ϵ�����ŵ�λ�ý��иı䡣
	for (list <Gate>::iterator traverIt = it; traverIt != gateVar.end(); ++traverIt)
	{
		if(traverIt->name == "t1" || traverIt->name == "t2" || traverIt->name == "v2" || 
			traverIt->name == "v+")  //not��c-not��v��v+
		{
			updateNNC(gateVar);  //���µ�·�и������ŵ�NNC
			if (traverIt->NNC > 0)  //traverIt��Ӧ�������ŷǽ���
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
				updateNNC(gateVar);  //���µ�·�и������ŵ�NNC
			}
			else  //traverIt->NNC == 0�������״̬�Լ�NOT��
			{
				if (traverIt->name != "t1")  //CNOT�ţ�V�ţ�V+��  
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
				else  //NOT��
				{
					if (traverIt->targets.at(0).at(0) == swapTempcontrols)  //���NOT�ŵ�Ŀ��λ��traverIt��Ӧ�Ŀ���λ���
					{
						traverIt->targets.at(0).at(0) = swapTemptargets;
					}
					if (traverIt->targets.at(0).at(0) == swapTemptargets)  //���NOT�ŵ�Ŀ��λ��traverIt��Ӧ��Ŀ��λ���
					{
						traverIt->targets.at(0).at(0) = swapTempcontrols;
					}
				}
				updateNNC(gateVar);  //���µ�·�и������ŵ�NNC
			}
		}	
	}
}

//���뽻���ţ�ʵ�������
void Circuit:: insertSwap(list<Gate> &gateVar,vector<string> &line)
{
	int downSwapCount = 0;
	updateNNC(gateVar);  //��ʼ����·�������ŵ�NNC
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end();it++ )
	{
		//ǰհ��������
		if ( it->name != "t1" )
		{
			do
			{
				changeGateOrder(it,gateVar);
				reorderGateId(gateVar);
			} while (changeGateOrder(it,gateVar) == 1); //=0��û�н���λ��
			//changeGateOrder(it,gateVar); //��NNC=0������		
		}
		//ǰհ��ӽ�����
		if (it->NNC > 0)
		{
			downSwapCount += ngLookahead(it,gateVar,line);
		}
		reorderGateId(gateVar);	
	}
	updateNNC(gateVar); //����NNC
}

//�����·������ڴ���
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

//ɾ�����ཻ����
void Circuit:: removeSwap(list<Gate> &gateVar)  
{
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end();)
	{
		list<Gate>::iterator tempIt = ++it;
		--it;
		//�������deletion rule�����SWAP�Ž���ɾ��
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

//ͳ�Ƶ�·�����ŵĸ���
int Circuit:: calculateSgate(list<Gate> &gateVar)
{
	int snum = 0;
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end();it++)
	{

		if ( it->name == "s") //���������� ++
		{
			snum++;
		}
	}
	return snum ;
}

//ͳ�Ƶ�·���Ӵ���
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

//���뽻���Ÿı�����
void Circuit:: ReorderLine(list<Gate> &gateVar,vector<string> &line)
{
	int j = 0; //����line0
	int i = 0; //����line1

	//�ж��Ƿ���Ҫ�����
	if ( line.size() < wires.size() ) //��Ҫ��Ӹ���λ
	{
		string b;
		charToString('a'+n-1,b);
		line.push_back(b);
	}

	//��ӽ����ţ���Ϊԭʼ����
	for (; j < n; i++) //����line1
	{
		if (line.at(i) == wires.at(j) && i != j) //line.at(i)��Ҫ����
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

//��������ǰհ��
void Circuit:: reorderGate(list<Gate> &gateVar)
{
	updateNNC(gateVar);
	for (list<Gate>::iterator it = gateVar.begin(); it != gateVar.end();it++ )
	{
		if ( it->name != "t1" )
		{
			changeGateOrder(it,gateVar); //ǰհ�����ŵ�˳��			
		}
		reorderGateId(gateVar); //�����
	}
}

//��������
int Circuit::changeGateOrder(list<Gate>::iterator iter, list<Gate> &gateVar) //����ֵȷ���Ƿ������λ�õĽ���
{
	int FLAG = 0; //=1�������λ�õĽ���

	if ((unsigned int)iter->id == gateVar.size() ) 
	{
		return FLAG; //���һ����ֱ�Ӳ����в���
	}

	//ǰհN���ж��Ƿ���Խ��н������Ƚ�NNC����NNCС��ǰ��
	
	list<Gate>::iterator moveIt = iter;  //����һ���ƶ��ĵ������������ƶ����ʵ�·�е�������
	++moveIt;

	int flagc = 0; //=1���ܽ���
	int flagt = 0;
	vector<string> temptargets; //��ʱ�洢Ŀ����
	vector<string> tempcontrols; //��ʱ�洢������
	temptargets.clear();
	tempcontrols.clear();
	//iter��Ϣ����
	temptargets.push_back(iter->targets.at(0));
	tempcontrols.push_back(iter->controls.at(0));

	for(int i = 0;i < locaN2; ++i)  
	{
		//�ж��Ƿ���Խ���
		if ( moveIt->name == "t1" ) 
		{
			temptargets.push_back(moveIt->targets.at(0));
			if ( moveIt->id == gateVar.size() ) //���һ����
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
				else // NOT�ŵ�һ���������
				{
					//����Ƿ���Խ���
					for (int i = 0; i < tempcontrols.size(); i++) //���moveit�Ŀ���λ
					{
						if ( flagc == 1 )  //�Ż��㷨����Ŀ��λ��ͻʱû�б�Ҫ����֤����λ
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
		else //���moveit�Ŀ���λ��Ŀ��λ
		{
			for (int i = 0; i < tempcontrols.size(); i++) //���moveit��Ŀ��λ
			{
				if ( moveIt->targets.at(0) == tempcontrols.at(i) )
				{
					flagc = 1; 
					break;
				}
			}
			for (int i = 0; i < temptargets.size(); i++) //���moveit�Ŀ���λ
			{
				if ( flagc == 1 )  //�Ż��㷨����Ŀ��λ��ͻʱû�б�Ҫ����֤����λ
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
		if ( flagc == 1 || flagt == 1 ) //���ܽ���
		{
			temptargets.push_back(moveIt->targets.at(0));
			tempcontrols.push_back(moveIt->controls.at(0));
			//����flagc��flagt
			flagc = 0;
			flagt = 0;
			if ( moveIt->id == gateVar.size() ) //���һ����
			{
				break;
			}
			else
			{
				moveIt++;
				continue;
			}
		}
		else //���Խ���
		{
			//�Ƚ�NNC
			if (moveIt->name != "t1")
			{
				if ( moveIt->NNC == 0 ) //ǰ��
				{
					FLAG = 1;
					temptargets.push_back(moveIt->targets.at(0));
					tempcontrols.push_back(moveIt->controls.at(0));
					gateVar.insert(iter,*moveIt);
					list<Gate>::iterator temp = moveIt;
					if ( moveIt->id == gateVar.size() - 1 ) //���һ���� ��Ϊ��һ���ţ�����-1
					{
						gateVar.erase(temp); //ɾ��
						break;
					}
					else
					{
						moveIt++;
						gateVar.erase(temp); //ɾ��
						continue;
					}	
				}
				else //����
				{
					temptargets.push_back(moveIt->targets.at(0));
					tempcontrols.push_back(moveIt->controls.at(0));
					if ( moveIt->id == gateVar.size() ) //���һ����
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
			else //���Խ�������NOT��
			{
				FLAG = 1;
				temptargets.push_back(moveIt->targets.at(0));
				gateVar.insert(iter,*moveIt);
				list<Gate>::iterator temp = moveIt;
				if ( moveIt->id == gateVar.size() - 1 ) //���һ���� ��Ϊ��һ���ţ�����-1
				{
					gateVar.erase(temp); //ɾ��
					break;
				}
				else
				{
					moveIt++;
					gateVar.erase(temp); //ɾ��
					continue;
				}	
			}
			
			
		}
	}
	return FLAG;
}

//�Ե�·�ľ������
void Circuit:: operation(list<Gate> &gateVar,vector<string> &line)
{
	reorderGateId(gateVar);

	//�ֽ�
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
	
	//����line
	line = wires; 
	                                
	reorderGateId(gateVar);
	
	//ɾ�������š����������ŵ�˳��
	removeGate(gateVar);	
	reorderGateId(gateVar);

	//����ʽǰհ�����ŵ�˳��
	//reorderGate(gateVar);
	//reorderGateId(gateVar);
	
	//ǰհ��ʵ��LNN
	insertSwap(gateVar,line);  
	
	//���µ�·��ID��ɾ��������
	removeGate(gateVar);
	reorderGateId(gateVar);
	
	//����gates
	gates = gateVar; //�������䣬��Ȼgates���仯
}
