import networkx as nx


class Map:
    # sl result is a dict, i.e., a mapping from logical qubits to physical qubits
    def __init__(self, result):
        self.__subMap = []
        self.__gMap = []
        if type(result) is not dict:  # dict 字典
            print("Class Map __init__() argument type error! dict expected!")
            exit()
        if result:
            for key in result:
                self.__subMap.append(key)
                self.__gMap.append(result[key])

    def subMap(self):
        return self.__subMap

    def gMap(self):
        return self.__gMap

    # type = 0, g=subGraph; type = 1, g=graph
    def neighbor(self, g, type):

        if not (type == 1 or type == 0):
            print("Class Map neighbor() argument value error! type expected 0 or 1!")
            exit()

        if type:
            curMap = self.__gMap
        else:
            curMap = self.__subMap

        neighbor_set = set()
        for x in curMap:
            for q in nx.all_neighbors(g, x):
                neighbor_set.add(q)

        neighbor = list(neighbor_set - set(curMap))

        return neighbor
