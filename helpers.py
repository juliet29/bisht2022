import networkx as nx
from icecream import ic

import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial import ConvexHull


# plots  

def plot_planar_embed(embed: nx.PlanarEmbedding):
    pos = nx.combinatorial_embedding_to_pos(embed)
    nx.draw_networkx(nx.Graph(embed), pos)

def plot_just_planar(G: nx.Graph):
    try:
        ic("planar");
        pos = nx.planar_layout(G)
        nx.draw_networkx(G, pos)
    except:
        nx.draw_networkx(G)


## special starting graphs 
    
def graph_from_edges(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    return G

def st_graph():
    order_a = 4
    order_b = 4
    G_a = nx.random_regular_graph(3, order_a)
    G_b = nx.random_regular_graph(2, order_b)

    node_names = [order_a + i for i in range(order_b)]
    mapping = {old_label: new_label for old_label, new_label in zip(G_b.nodes(), node_names)}
    G_b = nx.relabel_nodes(G_b, mapping)

    # connect graphs 
    G  = nx.union(G_a, G_b)
    G.add_edge(list(G_a.nodes)[0], node_names[-1])

    return G


def square_tri_graph():
    G = nx.Graph()

    # Add nodes and edges for the square
    square_nodes = [1, 2, 3, 4]
    G.add_nodes_from(square_nodes)
    square_edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
    G.add_edges_from(square_edges)

    # Add nodes and edges for the triangle
    triangle_nodes = [5, 6, 7]
    G.add_nodes_from(triangle_nodes)
    triangle_edges = [(5, 6), (6, 7), (7, 5)]
    G.add_edges_from(triangle_edges)

    # Combine both connected components
    G.add_edge(1, 5)  # Connect a node from the square to a node from the triangle

    return G


# utilities

def find_difference(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    
    # Find the elements present in set1 but not in set2
    difference1 = set1 - set2
    
    # Find the elements present in set2 but not in set1
    difference2 = set2 - set1
    
    return difference1, difference2

def line_through_points(point_pair):
    point1, point2 = point_pair
    x1, y1 = point1
    x2, y2 = point2

    # Calculate slope
    slope = (y2 - y1) / (x2 - x1)

    # Use one of the points to find y-intercept
    b = y1 - slope * x1

    return slope, b

def point_on_line(line_data, test_point):
    # skipping coincident check => getting those points from the convex hull calc. here looking for inbetween points 
    slope, b = line_data
    x, y = test_point

    expected_y = slope*x + b
    return np.isclose(y, expected_y)

def extract_convex_points(embed_arr, hull):
    boundary_points = []
    for simplex in hull.simplices:
        boundary_points.append((embed_arr[simplex[0]], embed_arr[simplex[1]]))
    return boundary_points

def find_boundary_points(G):
    # find planar embedding -> for network x, this will arrange points in triangular fashion 
    embed =  nx.planar_layout(G)
    embed_arr = np.array([embed[key] for key in sorted(embed.keys())])
    indices = np.arange(len(embed_arr))
    
    # find convex hull 
    hull = ConvexHull(embed_arr)

    known_boundary_ix = np.unique(hull.simplices)
    test_ix  = set(indices) - set(known_boundary_ix) # todo naming may be weird => points are all represented by their index  

    hull_pairs = extract_convex_points(embed_arr, hull)

    for pair in hull_pairs:
        l = line_through_points(pair)
        # check if point on line. 
        for ix in test_ix:
            if point_on_line(l, embed_arr[ix]):
                # ic("point!", ix)
                known_boundary_ix = np.append(known_boundary_ix, ix)
                # ic(known_boundary_ix)
                test_ix  = set(indices) - set(known_boundary_ix)
    
    boundary_points = embed_arr[known_boundary_ix]
    return boundary_points, known_boundary_ix



