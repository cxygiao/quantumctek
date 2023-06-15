# from Tua_refresh import dist
from Utils.Parallel_mapping.circuit_tran import Tua_dist


def cost(C, a, tau, LD, G,way):
    '''定义一个生成新映射的函数
    拿到已经过滤过的swap序列
    每一个新的映射下计算该步骤为后续所有门带来的影响--代价函数
    '''


    #print('列表展示',wayindex[12][0])
    # print('最短距离', wayindex)
    dist1 = []
    dist2 = []
    c = []
    LD = []
    for i in range(0,len(C)):
        LD.append(i)
    for i in LD: #剩下的门去重
        # c.append(C[i])
        c.append([C[i],len(C)-i]) #门+门序
    # c = list(choose.unique_everseen(c, key=frozenset))
    # print('剩下的门', c)

    dist1 = Tua_dist.distNew(c,tau,way,dist1)


    newTau = a[1]
    # print('新映射',newTau)
    dist2 = Tua_dist.distNew(c, newTau, way, dist2)

    cost = 0
    for i in range(len(dist1)):
        if dist1[i][1] >= dist2[i][1]:  #[[[6,1],9,12],[[4,1],8,0]]
            cost += dist2[i][0][1]
    # print('门序代价',cost)
        # else:
        #     break
        #
        # if dist1[i][1] >= dist2[i][1]:
        #     cost += 1


    return cost
