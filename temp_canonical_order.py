# set canonical order of original 
G.nodes[get_node_index("south")]["canonical_order"] = 1
G.nodes[get_node_index("west")]["canonical_order"] = 2


# define the subgraph 
subgraph_nodes = []
subgraph_nodes.append(get_node_index("south"))
subgraph_nodes.append(get_node_index("west"))
G_k_minus = nx.subgraph(G, subgraph_nodes)
G_diff = set(G.nodes).difference(set(G_k_minus.nodes))


for order in range(2, len(G.nodes)):
    # find next node 
    v1 = subgraph_nodes[-2]
    v2 = subgraph_nodes[-1]
    candidate_nodes = [n for n in G.neighbors(v1) if n in G.neighbors(v2)]


    # filter candidate nodes
    for node in candidate_nodes:
        true_candidate_nodes = []

        neighbours = {n for n in G.neighbors(node)}
        neighbours
        ic(G_diff, neighbours);

        if len(G_diff.intersection(neighbours)) >= 2:
            true_candidate_nodes.append(node)

        assert true_candidate_nodes, "candidate nodes are invalid!"

    if len(true_candidate_nodes) == 1:
        pass # TODO break if only one node left.. 

    # dummy assignment for now
    next_node = true_candidate_nodes[0]


    G.nodes[next_node]["canonical_order"] = order

    subgraph_nodes.append(next_node)
    G_k_minus = nx.subgraph(G, subgraph_nodes)
    G_diff = set(G.nodes).difference(set(G_k_minus.nodes))