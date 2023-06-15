
cir = [['h', 16], [11, 16], ['tdg', 16], [15, 22], [22, 15], [15, 22], [22, 16], ['t', 16], [11, 16], ['tdg', 16], [22, 16], ['t', 16], ['t', 11], [11, 16], [16, 11], [11, 16], [22, 16], ['t', 22], ['x', 22], ['tdg', 16], [22, 16], [16, 11], ['tdg', 11], [11, 16], [16, 11], [11, 16], [22, 16], ['t', 16], [11, 16], ['tdg', 16], [22, 16], ['t', 16], ['h', 16], ['t', 11], [22, 11], ['t', 22], ['x', 22], ['tdg', 11], [22, 11], ['x', 10], ['h', 10], [16, 10], ['tdg', 10], [4, 10], ['t', 10], [16, 10], ['t', 16], ['tdg', 10], [4, 10], ['t', 10], ['h', 10], [4, 16], ['tdg', 16], ['t', 4], [4, 16], [10, 3]]

f = open("/Utils/Parallel_mapping/Result_66/cir_list", 'w')
for i in cir:
    if isinstance(i[0],str):
        if i[0]=='h':
            f.write('H ')
            f.write('Q'+str(i[1]))
            f.write('\n')
        elif i[0]=='tdg':
            f.write('TDG ')
            f.write('Q' + str(i[1]))
            f.write('\n')
        elif i[0]=='s':
            f.write('S ')
            f.write('Q' + str(i[1]))
            f.write('\n')
        elif i[0]=='t':
            f.write('T ')
            f.write('Q' + str(i[1]))
            f.write('\n')
        elif i[0]=='x':
            f.write('X ')
            f.write('Q' + str(i[1]))
            f.write('\n')
    else:
        f.write('H ')
        f.write('Q' + str(i[1]))
        f.write('\n')
        f.write('CZ ')
        f.write('Q' + str(i[1]))
        f.write(' ')
        f.write('Q' + str(i[0]))
        f.write('\n')
        f.write('H ')
        f.write('Q' + str(i[1]))
        f.write('\n')
