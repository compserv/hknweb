from typing import Dict, List


class Edge:
    """
    An directed edge FROM a TO b.
    """

    def __init__(self, a: int, b: int, weight: float):
        self.a, self.b, self.weight = a, b, weight

    def __lt__(self, other: "Edge") -> bool:
        return self.weight < other.weight

    def __eq__(self, other: "Edge") -> bool:
        return self.weight == other.weight


class Pair:
    def __init__(self, b: int, weight: float):
        self.b, self.weight = b, weight


class Graph:
    def __init__(self, num_nodes: int):
        self.num_nodes: int = num_nodes

        self.neighbors: Dict[int, List[Pair]] = {i: [] for i in range(self.num_nodes)}

    def add_edge(self, a: int, b: int, weight: float) -> None:
        self.neighbors[a].append(Pair(b, weight))
        self.neighbors[b].append(Pair(a, weight))

    def get_neighbors(self, a: int) -> List[Pair]:
        return self.neighbors[a]
