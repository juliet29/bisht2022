from helpers import *

def simple_four_con_graph():
    pos = [(-3,0), (0,4),(0,8), (3,4), (6,2), (3,0), (0,-4), (0,0) ]
    outer_edges = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,0)]
    inner_edges = [(7,1), (1,3), (3,5), (5,7), (1,5)]
    edges_connecting_outer = [(0,2), (2,4), (4,6), (6,0)]
    
    edges = outer_edges + inner_edges + edges_connecting_outer
    G = nx.Graph()
    G.add_edges_from(edges)
    embed = {k:np.array(v) for (k,v) in enumerate(pos)}

    return G, embed

def name_corner_nodes():
    corner_nodes = [CornerNode(index=0, name=CardinalDirections.WEST), 
    CornerNode(index=2, name=CardinalDirections.NORTH), 
    CornerNode(index=4, name=CardinalDirections.EAST), 
    CornerNode(index=6, name=CardinalDirections.SOUTH), ]
    corner_node_dict = {k: v for k, v in zip(list(range(4)), corner_nodes)}

    return corner_node_dict

def create_graph():
    G, embed = simple_four_con_graph()
    corner_node_dict = name_corner_nodes()
    graph_data = GraphData(G, embed, corner_node_dict)

    return graph_data

graph_data = create_graph()