from helpers import *

def is_triangulated(G: nx.Graph):
    not_chordal = {}
    for ix, c in enumerate(nx.simple_cycles(G=G, length_bound=4)):
        if len(c) == 4:
            induced_graph = G.subgraph(c)
            if not nx.is_chordal(induced_graph):
                ic(f"{c} is not chordal, checking if all share neighbour")
                if not check_shared_neighbour(G, c):
                    ic(f"{c} do not share a neigbour")
                    return False
    return True

def check_shared_neighbour(G: nx.Graph, cycle):
    nbs = []
    for node in cycle:
        nb = set(G.neighbors(node))
        nbs.append(nb)
        # ic(node, nb)

    if set.intersection(*nbs):
        return True
    

def check_seperating_triangle(G):
    l3_cycles = sorted(nx.simple_cycles(G, 3))
    m = len(list(G.edges))
    n = len(list(G.nodes))
    # if self.DEBUG:
    # ic(len(l3_cycles), m, n, m - n + 1)
    ic(f"\n {len(l3_cycles)} three cycles ?= {m - n + 1}, where m={m}, n={n}")
    return False

