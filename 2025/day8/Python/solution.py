from collections import Counter
from typing import Annotated
from dataclasses import dataclass
from functools import reduce

Point = Annotated[tuple[int, ...], "tuple of coordinates of a point"]

@dataclass
class Edge:
    distance: float
    point1: Point
    point2: Point

    # for unpacking
    def __iter__(self):
        return iter((self.distance, self.point1, self.point2))

    # for sorting
    def __lt__(self, other: "Edge"):
        return self.distance < other.distance

class DisjointSet:
    def __init__(self, points: list[Point]):
        self.encoding: dict[Point, int] = {}
        self.decoding: dict[int, Point] = {}
        for i, point in enumerate(points):
            self.encoding[point] = i
            self.decoding[i] = point

        self.parent = list(range(len(points)))
        self.rnak = [1] * len(points)
    
    def find(self, p: Point) -> int:
        """Find the root of el's tree, with path compression."""
        pe: int = self.encoding[p]
        while self.parent[pe] != pe:
            self.parent[pe] = self.parent[self.parent[pe]]
            pe = self.parent[pe]
        return pe
    
    def union(self, el1: Point, el2: Point) -> int:
        """
        Merge the trees containing el1 and el2.

        If they are in the same set, do nothing.
        Else attach the tree with the smaller height to the tree with the larger height.
        """
        tree1 = self.find(el1)
        tree2 = self.find(el2)
        if tree1 != tree2:
            if self.rnak[tree1] < self.rnak[tree2]:
                self.parent[tree1] = tree2
            elif self.rnak[tree1] > self.rnak[tree2]:
                self.parent[tree2] = tree1
            else:
                self.parent[tree2] = tree1
                self.rnak[tree1] += 1

        return tree1 if self.parent[tree2] == tree1 else tree2



def kruskals(points: list[Point], edges: list[Edge], connections: int):
    edges = sorted(edges)
    ds = DisjointSet(points)

    for count, edge in enumerate(edges):
        if count == connections:
            break
        if ds.find(edge.point1) != ds.find(edge.point2):
            ds.union(edge.point1, edge.point2)
    return ds


def kruskals2(points: list[Point], edges: list[Edge], connections: int):
    edges = sorted(edges)
    ds = DisjointSet(points)

    mul = 0
    for count, edge in enumerate(edges):
        if count == len(edges) - 1:
            break
        if ds.find(edge.point1) != ds.find(edge.point2):
            ds.union(edge.point1, edge.point2)
            mul = edge.point1[0] * edge.point2[0]
    return mul


def dist(q: Point, p: Point) -> float:
    distance = 0
    for qi, pi in zip(q, p):
        distance += (qi - pi) ** 2
    return distance ** .5


def solve(input_file: str, connections: int) -> tuple[int, int]:
    points = [tuple(map(int, line.split(","))) for line in open(input_file, 'r')]
    edges: list[Edge] = []
    for i, point1 in enumerate(points[:-1]):
        for point2 in points[i + 1:]:
            edges.append(Edge(dist(point1, point2), point1, point2))

    ds = kruskals(points, edges, connections)
    roots = [ds.find(p) for p in points]
    top3 = sorted(Counter(roots).values(), reverse=True)[:3]

    return reduce((lambda x, y: x * y), top3), kruskals2(points, edges, connections)

ex_input_file = '../ex_input.in'
input_file = '../input.in'
print(f"Input: '{ex_input_file}'; Output: {solve(ex_input_file, 10)}")
print(f"Input: '{input_file}'; Output: {solve(input_file, 1000)}")