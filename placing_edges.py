from helpers import * 

from four_complete import *
from four_complete_locations import *
from graph_checks import *

from canonical_order import *

from canonical_order_kant import *
from crossing_min import *


bottom_data = get_saved_graph_data("BOTTOM")
side_data = get_saved_graph_data()

graph_data = side_data


f = FourComplete(graph_data)
f.get_boundary_cyle()
f.generate_dividing_indices()
f.divide_boundary_cycle()
f.ensure_no_cips()
f.paths

b = BoundaryCycle(copy.deepcopy(graph_data))
locs = FourCompleteLocations(copy.deepcopy(graph_data), f.boundary, f.paths, b.boundary_line_string)
locs.run()

cm = CrossingMin(locs.data, b.boundary_line_string)
cm.run()


def find_irregular_cycle(c):
    # TODO could make more efficient by checking only the cycles that have crossing edge numbers in them ..
    pairs = get_pairs_in_cycle(c) 
    matching_crossing_edges = []
    for pair in pairs: 
        for edge in cm.crossing_edges:
            if edge_match(pair, edge):
                matching_crossing_edges.append(edge)
    return matching_crossing_edges


def get_pairs_in_cycle(cycle_list):
    looped_cycle = cycle(cycle_list)
    pairs = []
    for ix, (i,j) in enumerate(pairwise(looped_cycle)):
        pairs.append((i,j))
        if ix >= 2:
            break

    return pairs

def edge_match(e1, e2):
    return frozenset(e1) == frozenset(e2)







def prepare_to_create_ring(cycle, pair):
    if len(pair) == 1:
        pair = pair[0]
        curve_coords = [c for c in cm.G.edges[pair]["curved_edge_data"].coords]
        node_roles = get_node_roles(cycle, pair)

        boundary1 = node_roles["crossing_e1"][1] + node_roles["normal"][1] + node_roles["crossing_e2"][1]
        ring = create_ring(boundary1, curve_coords)
        return ring
    elif len(pair) == 2:
        curve_coords1 = [c for c in cm.G.edges[pair[0]]["curved_edge_data"].coords]
        curve_coords2 = [c for c in cm.G.edges[pair[1]]["curved_edge_data"].coords]
        return curve_coords1, curve_coords2

    else:
        raise Exception("more than 2 curved pairs!")

    
def get_node_roles(cycle_list, crossing_edge):
    node_roles = { "crossing_e1": None, "normal": None, "crossing_e2": None}
    for node in cycle_list:
        if node in crossing_edge:
            # crossing edge node 1
            if not node_roles["crossing_e1"]:
                node_roles["crossing_e1"] = create_node_data(node)
            else: 
                node_roles["crossing_e2"] = create_node_data(node)
        else:
            node_roles["normal"] = create_node_data(node)

    return node_roles

def create_ring(boundary1, curve_coords):
    ring = None 
    try:
        joined = curve_coords + boundary1
        ring = sp.LinearRing(joined)
        assert ring.is_simple
    except AssertionError:
            try:
                joined = curve_coords + list(reversed(boundary1))
                ring = sp.LinearRing(joined)
                assert ring.is_simple, "ring is still not simple"
            except AssertionError:
                return ring, curve_coords, boundary1
    return ring

def create_node_data(node):
    loc = get_emedding_coords(cm.embed, [node])[0]
    return (node, [tuple(loc)])
    

