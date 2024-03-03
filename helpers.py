import networkx as nx
from icecream import ic

import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial import ConvexHull


# simple classes


class SeperatingTriangle:
    def __init__(self, cycle: list, inner_node: int) -> None:
        self.cycle = cycle
        self.inner_node = inner_node
        self.target_edge: tuple = None

    def __repr__(self):
        return f"SeperatingTriangle({self.cycle}, {self.inner_node}, {self.target_edge})"  # TODO automatically return dictionary ..


# plots
def plot_planar_embed(embed: nx.PlanarEmbedding):
    pos = nx.combinatorial_embedding_to_pos(embed)
    nx.draw_networkx(nx.Graph(embed), pos)

def plot_planar(G, old_pos=None):
    # ic(old_pos)
    pos = old_pos if old_pos else nx.planar_layout(G)
    pos = nx.draw_networkx(G, pos)
    return pos

def plot_just_planar(G: nx.Graph, pos=None):
    try:
        if not pos:
            pos = nx.planar_layout(G)
        nx.draw_networkx(G, pos)
        return pos
    except:
        ic("not planar")
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
    mapping = {
        old_label: new_label for old_label, new_label in zip(G_b.nodes(), node_names)
    }
    G_b = nx.relabel_nodes(G_b, mapping)

    # connect graphs
    G = nx.union(G_a, G_b)
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
def total_length(list_of_lists):
    return sum(len(sublist) for sublist in list_of_lists)

def find_difference(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    # Find the elements present in set1 but not in set2
    difference1 = set1 - set2

    # Find the elements present in set2 but not in set1
    difference2 = set2 - set1

    return difference1, difference2


def find_line_through_points(point_pair):
    point1, point2 = point_pair  # tuple of coordinate pts
    x1, y1 = point1
    x2, y2 = point2

    # Calculate slope
    slope = (y2 - y1) / (x2 - x1)

    # Use one of the points to find y-intercept
    b = y1 - slope * x1
    # todo turn output into class
    return slope, b


def check_point_on_line(line_data, test_point):
    # here looking for inbetween points
    slope, y_intercept = line_data
    x, y = test_point

    expected_y = slope * x + y_intercept
    return np.isclose(y, expected_y)


def check_parallel(slope_1, slope_2):
    return np.isclose(slope_1, slope_2)


def extract_convex_points(embed_arr, hull):
    # points that lie on outer most corners of graph embedding
    boundary_points = []
    for simplex in hull.simplices:
        boundary_points.append((embed_arr[simplex[0]], embed_arr[simplex[1]]))
    return boundary_points


def find_min_max_coordinates(coordinates):
    if not coordinates:
        return None

    # Convert the list of arrays into a numpy array for efficient manipulation
    coordinates_array = np.array(coordinates)

    # Extract x and y coordinates into separate arrays
    x_coords = coordinates_array[:, 0]
    y_coords = coordinates_array[:, 1]

    # Find min and max values for x and y coordinates
    min_x = np.min(x_coords)
    max_x = np.max(x_coords)
    min_y = np.min(y_coords)
    max_y = np.max(y_coords)

    return (min_x, max_x), (min_y, max_y)


def check_point_in_hull(domain, point):
    x_domain, y_domain = domain
    x, y = point

    return x_domain[0] < x < x_domain[1] and y_domain[0] < y < y_domain[1]


def new_node_pos(n1, n2):
    # assuming point will be on edge between two nodes
    n1_x = n1[0]
    n2_x = n2[0]

    n1_y = n1[1]
    n2_y = n2[1]

    if np.isclose(n1_x, n2_x):
        ic("same x", n1_x, n2_x)
        n_x = n1_x
        n_y = np.mean([n1_y, n2_y])
    elif np.isclose(n1_y, n2_y):
        ic("same y", n1_y, n2_y)
        n_x = np.mean([n1_x, n2_x])
        n_y = n1_y
    else:
        ic("neither same")
        n_x = np.mean([n1_x, n2_x])
        n_y = np.mean([n1_y, n2_y])

    return (n_x, n_y)


