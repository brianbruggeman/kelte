import typing
from dataclasses import dataclass, field


class Node:
    ...


@dataclass
class Edge:
    start: Node = field(default_factory=Node)
    end: Node = field(default_factory=Node)
    data: typing.Any = None

    @property
    def identifier(self):
        return tuple(self.start.identifier), tuple(self.end.identifier)

    def __hash__(self):
        return hash(self.identifier)


@dataclass
class DirectedEdge(Edge):

    def __init__(self, start, end, data):
        super().__init__(start, end, data)
        if self not in self.start.edges:
            self.start.edges.append(self)


@dataclass
class UndirectedEdge(Edge):

    def __init__(self, start, end, data):
        super().__init__(start, end, data)
        if self not in self.start.edges:
            self.start.edges.append(self)
        if self not in self.end.edges:
            self.end.edges.append(self)


@dataclass
class Node:
    identifier: typing.Any = None
    data: typing.Any = None
    edges: typing.List[Edge] = field(default_factory=list)

    @property
    def neighbors(self):
        for edge in self.edges:
            if edge.start == self:
                yield edge.end
            elif edge.end == self:
                yield edge.start

    def connect(self, other, data=None, directed=True):
        if not directed:
            edge = UndirectedEdge(self, other, data)
        else:
            edge = DirectedEdge(self, other, data)
        self.edges.append(edge)

    def disconnect(self, other, data, directed=None):
        matched_edges = []
        for index, edge in enumerate(self.edges):
            if edge.end == other:
                matched_edges.append((index, edge))
            elif directed is not True and edge.start == other:
                matched_edges.append((index, edge))
        for index, matched_edge in reversed(matched_edges):
            if matched_edge.data == data:
                self.edges.pop(index)

    def neighbors_in_range(self, range: int = 1):
        if range:
            for edge in self.edges:
                if edge.start == self:
                    yield from edge.end.neighbors_in_range(range=range - 1)
                elif edge.end == self:
                    yield from edge.start.neighbors_in_range(range=range - 1)

    def __hash__(self):
        return hash(tuple(self.identifier))


@dataclass
class Graph:
    nodes: typing.Dict[typing.Any, Node] = field(default_factory=dict)

    def __contains__(self, other):
        return other.identifier in self.nodes
