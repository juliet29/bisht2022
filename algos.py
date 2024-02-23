import networkx as nx
from icecream import ic

# algo based on Bisht 2022

# plots and utilities 

def plot_planar_embed(embed: nx.PlanarEmbedding):
    pos = nx.combinatorial_embedding_to_pos(embed)
    nx.draw_networkx(nx.Graph(embed), pos)

def plot_just_planar(G: nx.Graph):
    try:
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


## graph augmentation algorithms 

def check_block(node, blocks):
    # see what blocks a node belongs to
    indices = []
    set_members = []
    for index, my_set in enumerate(blocks):
        if node in my_set:
            indices.append(index)
            set_members.append(my_set)

    return indices, set_members


def biconnect(G1):
    G = G1.copy()
    cut_vertices = list(nx.articulation_points(G))
    ic(cut_vertices)

    for v in cut_vertices:
        # find vertices adjacent to x (ie neighbours of x?)
        neighbors = list(G.neighbors(v))
        blocks = list(nx.biconnected_components(G))
        ic("\n");
        ic(v, neighbors)
        for curr_item, next_item in zip(neighbors, neighbors[1:]):
            curr_block, curr_block_members = check_block(curr_item, blocks)
            next_block, next_block_members = check_block(next_item, blocks)
            ic(curr_item, curr_block_members)
            ic(next_item, next_block_members)
            if not set(curr_block) & set(next_block):
                edge = (curr_item, next_item)
                ic(f"No overlap between {edge}. Adding edge")
                # add edges between vertices 
                G.add_edge(curr_item, next_item)

    return G

def test_biconnect(G):
    # check that graph is biconnected => no articulation points
    assert len(list(nx.articulation_points(G))) == 0


def triangulate(G1):
    G, alpha = nx.complete_to_chordal_graph(G1.copy()) 
    return G

def test_triangulation(G):
    assert nx.is_chordal(G)
    
def seperating_triangle_check(G):
    l3_cycles = sorted(nx.simple_cycles(G, 3))
    m = len(list(G.edges))
    n = len(list(G.nodes))
    ic(len(l3_cycles), m, n, m-n+1);
    assert len(l3_cycles) == m-n+1







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