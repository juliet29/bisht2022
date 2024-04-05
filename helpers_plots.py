import networkx as nx
import os 
import pickle


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
        print("not planar")
        nx.draw_networkx(G)


#MARK: special starting graphs

def get_saved_graph_data(type=None):
    path = "saved_graphs/after_sep_tri"
    
    if type == "BOTTOM":
        final_path = os.path.join(path, "bottom_node", "data.p")
    else:
        final_path = os.path.join(path, "side_node", "data.p")
    
    res = pickle.load(open(final_path, "rb") )
    return res



def graph_from_edges(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    return G


def st_graph(seed=4):
    order_a = 4
    order_b = 4
    G_a = nx.random_regular_graph(3, order_a, seed)
    G_b = nx.random_regular_graph(2, order_b, seed)

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

