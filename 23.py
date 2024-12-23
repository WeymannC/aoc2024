from collections import defaultdict
from itertools import combinations

from aocd import get_data

data = get_data(day=23, year=2024)
example = r"""kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""


def build_graph(raw):
    graph = defaultdict(set)
    for connection in raw.split("\n"):
        a, b = connection.split("-")
        graph[a].add(b)
        graph[b].add(a)
    return graph

def find_triangles(graph):
    while graph:
        a, neighbors = graph.popitem()
        for b, c in combinations(neighbors, 2):
            if c in graph[b]:
                yield a,b,c
        for neighbor in neighbors:
            graph[neighbor].remove(a)

def part_1(used_input):
    graph = build_graph(used_input)
    return sum(1 if any(computer.startswith("t") for computer in members) else 0 for members in find_triangles(graph))

def bron_kerbosh(R, P, X, graph):
    if not (P | X):
        yield R
    while P:
        v = P.pop()
        yield from bron_kerbosh(R | {v}, (P | {v}) & graph[v], X & graph[v], graph)
        X.add(v)


def part_2(used_input):
    graph = build_graph(used_input)
    max_clique = max(bron_kerbosh(set(), set(graph.keys()), set(), graph), key=len)
    return ",".join(sorted(max_clique))


print(part_1(data))
print(part_2(data))
