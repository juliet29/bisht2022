from helpers import *

def check_graph(G):
    check_triangulated_interior(G)
    alt_embed = check_planarity(G)
    check_seperating_triangle(G)
    return alt_embed

def check_planarity(G):
    planar_check, alt_embed = nx.check_planarity(G)
    assert planar_check, "Four completed graph is not planar "
    return alt_embed
    

def check_seperating_triangle(G):
    l3_cycles = sorted(nx.simple_cycles(G, 3))
    m = len(list(G.edges))
    n = len(list(G.nodes))

    ic(f"\n {len(l3_cycles)} three cycles ?= {m - n + 1}, where m={m}, n={n}")
    if len(l3_cycles) == m - n + 1:
        return 
    else:
        raise Exception("There are seperating triangles")


def check_triangulated_interior(G):
    for e in G.edges:
        if not check_shared_neighbour(G, e):
            raise Exception("Interior is not triangulated")
    return 

def check_triangulated_chordal(G):
    assert nx.is_chordal(G), "graph is not chordal"

def check_4_conencted(G):
    assert nx.is_k_edge_connected(G, 4), "not 4 connected"



# helpers
def check_shared_neighbour(G, e):
    u, v  = e
    for node in G.nodes:
        if (node, u) in G.edges and (node, v) in G.edges:
            # ic((node,v), (node,u))
            return True
    return False