from Qubit_f import swap
from shortway import way
from choose import unique_everseen #嵌套列表去重

def dist(c, tau, wayindex, dist):
    for i in c: #剩下的门在原映射状态下的最短距离
        x = tau.index(i[0])
        y = tau.index(i[1])

        if x > y:
            for j in wayindex:
                if [y, x] == j[0]:
                    dist.append([i, j[1]])
        else:
            for j in wayindex:
                if [x, y] == j[0]:
                    dist.append([i, j[1]])
    return dist







