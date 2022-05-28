from typing import List, Set, Tuple, Union

import random

from queue import PriorityQueue
from itertools import product

from hknweb.tutoring.scheduler.data import Data
from hknweb.tutoring.scheduler.weighting import Weighting
from hknweb.tutoring.scheduler.graph import Edge, Graph
from hknweb.tutoring.scheduler.tutoring import Slot, Tutor


class Matcher:
    class AssignDTO:
        def __init__(self, num_tutors: int) -> None:
            self.num_tutors = num_tutors

        def init_assign(self) -> None:
            self.graph: Graph = Graph(self.n)
            self.prices: List[float] = [0.0] * self.n
            self.partner: List[int] = [-1] * self.n
            self.matched: List[bool] = [False] * self.n

        def init_matching(self) -> None:
            self.prev: List[int] = [-1] * self.n
            self.vis: List[bool] = [False] * self.n
            self.ovis: List[int] = [0] * self.n
            self.delta: List[float] = [0.0] * self.n


    def __init__(self, data: Data, weighting: Weighting):
        self.data, self.weighting = data, weighting

        self.n: int = len(self.data.tutors) + len(self.data.slots)

    def match(self) -> None:
        two_hour_tutors: List[int] = [t.num_assignments == 2 for t in self.data.tutors]

        # Try to assign all slots one tutor
        # This may allow one tutor to go into multiple slots
        # Not sure why this has to be run twice
        unused_slot_idxs: Set[int] = set(range(len(self.data.slots)))
        for _ in range(2):
            self.assign(unused_slot_idxs, two_hour_tutors)

        # One more time to make sure all tutors have enough slots
        # This will allow some slots to have more than one person
        # However now all slots can be used
        unused_slot_idxs: Set[int] = set(range(len(self.data.slots)))
        self.assign(unused_slot_idxs, two_hour_tutors)

        # Now allow committee members to be assigned
        self.assign(unused_slot_idxs, list(range(len(self.data.tutors))))

    def assign(self, unused_slot_idxs: Set[int], tutor_idxs_to_assign: List[int]) -> None:
        # Initialize graph
        assign_dto = self.AssignDTO(len(self.data.tutors))
        assign_dto.init_assign()

        retrieve_tutor = lambda i: (i, self.data.tutors[i])
        valid_tutor_idx = lambda _, tutor: len(tutor.slots) < tutor.num_assignments
        tutor_idxs: List[Tuple[int, Tutor]] = list(filter(valid_tutor_idx, map(retrieve_tutor, tutor_idxs_to_assign)))
        retrieve_slot = lambda i: (i, self.data.slots[i])
        slot_idxs: List[Tuple[int, Slot]] = list(map(retrieve_slot, unused_slot_idxs))

        random.shuffle(tutor_idxs)
        random.shuffle(slot_idxs)

        for (tutor_idx, tutor), (slot_idx, slot) in product(tutor_idxs, slot_idxs):
            # This case naturally doesn't let us assign 2 of the same slot to one tutor.
            if tutor.conflict(slot):
                continue

            r: float = self.weighting.weight(tutor, slot);
            if r <= -10:
                continue

            self.updateMatching(assign_dto, tutor_idx, slot_idx + assign_dto.num_tutors, r)

        # Assign partners
        for i, tutor in enumerate(self.data.tutors):
            if assign_dto.partner[i] == -1:
                continue

            k = assign_dto.partner[i] - assign_dto.num_tutors
            slot = retrieve_slot(k)

            tutor.assign(slot)
            slot.assign(tutor)

            unused_slot_idxs.remove(k)

    def update_matching(
        self, assign_dto: "Matcher.AssignDTO", a: int, b: int, weight: float,
    ) -> None:
        graph = assign_dto.graph
        prices = assign_dto.prices
        matched = assign_dto.matched
        partner = assign_dto.partner

        graph.add_edge(a, b, weight)
        d: float = weight - prices[a] - prices[b]
        if d <= 0:  # no need to further process this case
            return

        # Get a feasible matching
        prices[a] += d
        # Rematch a and b if necessary, since price matching is no longer on tight edges
        if matched[a]:
            matched[partner[a]] = False
            partner[partner[a]] = -1

        if matched[b]:
            matched[partner[b]] = False
            partner[partner[b]] = -1

        matched[a] = True
        matched[b] = True
        partner[a] = b
        partner[b] = a

        assign_dto.init_matching()

        # Now try to find all augmenting paths
        # Should be at most 2, since we remove at most 1 matched pair, and we
        # Can add at most one new matched pair
        while True:
            idx, end = self.find_augmenting_path(assign_dto)
            self.update_prices(assign_dto, idx)
            if end == -1:
                break

            self.augment_path(assign_dto, end)

    def find_augmenting_path(assign_dto: "Matcher.AssignDTO") -> Union[int, int]:
        """
        Finds an augmenting path and returns the end node we can follow prev pointers to recreate path
        Running time is O(M log M), M is number of edges (which is usually about N^2)
        """
        price = assign_dto.price
        partner = assign_dto.partner
        matched = assign_dto.matched
        delta = assign_dto.delta
        ovis = assign_dto.ovis
        vis = assign_dto.vis
        prev = assign_dto.prev
        num_tutors = assign_dto.num_tutors
        graph = assign_dto.graph

        idx = -1
        C: float = 0.0
        pq = PriorityQueue()
        for i in range(num_tutors):
            if not matched[i]:
                for node in graph.get_neighbors(i):
                    pq.put(Edge(i, node.b, price[i] + price[node.b] - node.weight))

                idx += 1
                ovis[idx] = i

        end: int = -1
        while pq:
            f: Edge = pq.get()
            if vis[f.b]:
                continue

            vis[f.b] = True
            prev[f.b] = f.a

            v: float = f.weight - C
            C += v
            delta[idx] += v

            if not matched[f.b]:
                end = f.b
                break

            l = partner[f.b]
            for node in graph.get_neighbors(l):
                if not vis[node.b]:
                    pq.add(Edge(l, node.b, price[l] + price[node.b] - node.weight + C));

            ovis[idx + 1] = f.b
            ovis[idx + 2] = l
            idx += 2

        return idx, end

    @staticmethod
    def update_prices(assign_dto: "Matcher.AssignDTO", idx: int) -> None:
        """
        Keeps prices up to date. Running time: O(N), N is number of nodes
        """
        price = assign_dto.price
        delta = assign_dto.delta
        ovis = assign_dto.ovis
        num_tutors = assign_dto.num_tutors

        k: int = 0
        while idx >= 0:
            k += delta[idx]
            if ovis[idx] < num_tutors:
                price[ovis[idx]] -= k
            else:
                price[ovis[idx]] += k
            idx -= 1

    @staticmethod
    def augment_path(assign_dto: "Matcher.AssignDTO", end: int) -> None:
        """
        Switches path parities. Running time: O(N), N is number of nodes
        """
        partner = assign_dto.partner
        matched = assign_dto.matched
        prev = assign_dto.prev

        while end != -1:
            matched[end] = True
            matched[prev[end]] = True
            partner[end] = prev[end]
            next = partner[prev[end]]
            partner[prev[end]] = end
            end = next
