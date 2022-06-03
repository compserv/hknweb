from typing import Dict, List

from collections import namedtuple


Edge = namedtuple("Edge", "weight a b")
Pair = namedtuple("Pair", "weight b")


class Graph:
    def __init__(self, num_nodes: int):
        self.neighbors: Dict[int, List[Pair]] = {i: [] for i in range(num_nodes)}

    def add_edge(self, a: int, b: int, weight: float) -> None:
        self.neighbors[a].append(Pair(weight, b))
        self.neighbors[b].append(Pair(weight, a))

    def get_neighbors(self, a: int) -> List[Pair]:
        return self.neighbors[a]
