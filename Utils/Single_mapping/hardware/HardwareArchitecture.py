import logging
import networkx as nx

logging.basicConfig()
logging.root.setLevel(logging.WARNING)


class HardwareArchitecture(nx.DiGraph):
    def __init__(self, incoming_graph_data=None, **kwargs):
        super().__init__(incoming_graph_data, **kwargs)
        self._qubit_number = 0

    def add_qubit(self, **qubit_data) -> int:
        self.add_node(self._qubit_number, **qubit_data)
        self._qubit_number += 1
        return self._qubit_number

    def add_link(self, qubit1: int, qubit2: int, **link_data):
        self.add_edge(qubit1, qubit2, **link_data)

    @property
    def qubit_number(self):
        return self._qubit_number


