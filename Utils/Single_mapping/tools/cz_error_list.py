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

def read_error_cz(path):
    with open(path,"r", encoding="utf-8") as f:
    #with open("/Users/qyyy/研究生/科研/多程序并行/Multiprogramming-main/paralle_mapping/error_data/ClosedBetaQC_ 66bit.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    chuli(content)
    toCzerror = content['twoQubitGate']['czGate']['gate error']['param_list']
    toQubit = content['twoQubitGate']['czGate']['gate error']['qubit_used']
    toGate = content['overview']['coupler_map']
    # print(toCzerror,len(toCzerror))
    # print(toQubit,len(toQubit))
    # print(toGate)

    Gate_list = []
    for i in toQubit:
        gate = toGate[i]
        Gate_list.append(gate)

    Error_list_cz = [[1] * 67 for _ in range(67)]
    # print(Error_list_cz)
    index = 0
    for i in toCzerror:
        m = int(Gate_list[index][0][1:])
        n = int(Gate_list[index][1][1:])
        index = index + 1
        Error_list_cz[m][n] = i/100
        Error_list_cz[n][m] = i/100
    # print(Error_list_cz)
    return Error_list_cz


# if __name__ == '__main__':
#     read_error_cz('/Users/qyyy/研究生/科研/多程序并行/Multiprogramming-main/paralle_mapping/error_data/ClosedBetaQC_ 66bit.json')
