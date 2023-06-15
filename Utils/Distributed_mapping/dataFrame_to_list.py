def dataframe_to_list(dataFrame):
    df = dataFrame
    df_list = df.values.tolist()
    Gate_list = []
    Gate_list_new = []
    print('列表',df_list)
    for i in df_list:
        print(i)
        if i[0] == 'h ':
            Gate_list.append([i[0],i[2]])
        elif i[0] == 'CZ':
            Gate_list.append([i[1], i[2]])
        elif i[0] == 'tdg ':
            Gate_list.append([i[0],i[2]])
        elif i[0] == 't ':
            Gate_list.append([i[0],i[2]])
        elif i[0] == 'x ':
            Gate_list.append([i[0],i[2]])
    for i in Gate_list:
        if isinstance(i[0],str):
            gatename = i[0].rstrip()
            gate=[gatename,i[1]]
            Gate_list_new.append(gate)
        else:
            Gate_list_new.append(i)
    return Gate_list_new