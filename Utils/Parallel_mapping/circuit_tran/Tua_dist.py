'''
最短距离更新
'''

def distNew(c, tau, wayindex, dist): #[[[6,1],9],[[4,1],8]]
    for i in c: #剩下的门在原映射状态下的最短距离
        if not isinstance(i[0][1],str):
            x = tau.index(i[0][1])
            y = tau.index(i[0][2])
            if x > y:
                for j in wayindex:
                    if [y, x] == j[0]:
                        dist.append([i, j[1]])
            else:
                for j in wayindex:
                    if [x, y] == j[0]:
                        dist.append([i, j[1]])
    return dist







