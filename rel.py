import networkx as nx
from icecream import ic
from helpers import *
from augment import *

class REL:
    def __init__(self, G, embed, corner_node_data) -> None:
        self.G = G
        self.embed = embed
        self.corner_node_data = self.corner_node_data


    # helpers
    def get_node_index(self, key):
        dict_key = get_key_by_value(self.corner_node_data, key, object=True)
        return self.corner_node_data[dict_key].node
    
    def create_next_graphs(self, self.subgraph_nodes):
        G_k_minus = nx.subgraph(self.G, self.subgraph_nodes)
        G_diff = nx.subgraph(self.G, set(self.G.nodes).difference(set(G_k_minus.nodes)))
        return G_k_minus, G_diff
    
    def connect_outer_edges(self): 
        #TODO move to own four connect class?
        ix = self.get_node_index # create alias
        edges = [(ix("south"), ix("east")),
                (ix("east"), ix("north")),
                (ix("north"), ix("west")),
                (ix("west"), ix("south")),
                (ix("south"), ix("north")),
                ]
        self.G.add_edges_from(edges)


    def initialize_order(self):
        self.G.nodes[self.get_node_index("south")]["canonical_order"] = 1
        self.G.nodes[self.get_node_index("west")]["canonical_order"] = 2
        # define the subgraph 
        self.subgraph_nodes = []
        self.subgraph_nodes.extend([self.get_node_index("south"), self.get_node_index("west")])
        G_k_minus, G_diff = self.create_next_graphs(G, self.subgraph_nodes)


    def find_next_node_and_update(self):
        for order in range(2, len(self.G.nodes)):

            # find next node -> shared nb of past nodes which is in G_diff 
            v1 = self.subgraph_nodes[-2]
            v2 = self.subgraph_nodes[-1]
            candidate_nodes = [n for n in G.neighbors(v1) if n in G.neighbors(v2)]
            candidate_nodes_in_G_diff = list(set(candidate_nodes).intersection(set(G_diff.nodes)))
            # ic((v1, v2), candidate_nodes, candidate_nodes_in_G_diff)

            # # check part 3 of refined canonical order theorem -> candidate node has two nbs in G_diff
            for node in candidate_nodes_in_G_diff:
                true_candidate_nodes = [] # TODO rename 

                neighbours = {n for n in G.neighbors(node)}

                if len(set(G_diff.nodes).intersection(neighbours)) >= 2:
                    true_candidate_nodes.append(node)
                elif len(G_diff.nodes) <= 2: 
                    true_candidate_nodes.append(node)

                assert len(true_candidate_nodes) == 1, "candidate nodes are invalid!"

            next_node = true_candidate_nodes[0]
            # ic((true_candidate_nodes, next_node))
            ic(self.subgraph_nodes)
            

            G.nodes[next_node]["canonical_order"] = order

            self.subgraph_nodes.append(next_node)
            # tracker.append(next_node)
        
            G_k_minus, G_diff = self.create_next_graphs(G, self.subgraph_nodes)

    
    
    def test_biconnect(self):
        a = Augment(G_k_minus)
        a.G_biconnect = G_k_minus
        a.test_biconnect()


    




