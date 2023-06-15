import json

# json_data = open('/Users/qyyy/研究生/科研/多程序并行/Multiprogramming-main/paralle_mapping/error_data/ClosedBetaQC_ 66bit.json').read()
# data = json.load(json_data)

def chuli(d) :
    list = []   #用于存储字典中的键值对,元素为元组
    for i in d.items() :   #以元组的格式读取键值对
        list.append(i)   #将遍历到的元组加入列表中
    for num in range(len(list)):   #遍历列表中的元组格式的键值对
        # print(list[num][0])   #打印元组的第一个元素——键
        d = list[num][1]   #标记元组的第二个元素——值
        if isinstance(list[num][1], dict):   #当值为字典时，字典是嵌套的，递归调用函数
            chuli(d)

def readout_error(path):
    with open(path,"r", encoding="utf-8") as f:
    #with open("/Users/qyyy/研究生/科研/多程序并行/Multiprogramming-main/paralle_mapping/error_data/ClosedBetaQC_ 66bit.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    chuli(content)
    error_0 = content['readout']['readoutArray']['|0> readout fidelity']['param_list']
    error_1 = content['readout']['readoutArray']['|1> readout fidelity']['param_list']
    # print(error_0,error_1)
    qubit = content['readout']['readoutArray']['|1> readout fidelity']['qubit_used']
    qubit_index = []
    for i in qubit:
        qubit_index.append(int(i[1:]))
    # print(qubit_index)
    Readerror_list = [0 * 1 for _ in range(67)]
    for i in range(0,len(error_0)):
        Readerror_list[qubit_index[i]] = (error_0[i]+error_1[i])/2
    Readerror_list[0] = 1
    # print(Readerror_list)
    for i in range(0,67):
        if not Readerror_list[i]:
            Readerror_list[i] = 1
    # print(Readerror_list)
    return Readerror_list