import networkx as nx
from icecream import ic


# plots and utilities 

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


def find_difference(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    
    # Find the elements present in set1 but not in set2
    difference1 = set1 - set2
    
    # Find the elements present in set2 but not in set1
    difference2 = set2 - set1
    
    return difference1, difference2




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