import networkx as nx
from icecream import ic
from helpers import *
from augment import *

class CanonicalOrder:
    def __init__(self, GraphData:GraphData) -> None:
        self.G = GraphData.graph
        self.embed = GraphData.embed
        self.corner_node_data = GraphData.corner_node_data

    def run(self):
        self.connect_outer_edges()
        self.initialize_order()
        self.find_next_node_and_update()

    
    # action starts 
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
        self.subgraph_nodes = []

        self.G.nodes[self.get_node_index("south")]["canonical_order"] = 1
        self.G.nodes[self.get_node_index("west")]["canonical_order"] = 2
        self.subgraph_nodes.extend([self.get_node_index("south"), self.get_node_index("west")])

        # define the subgraph
        self.G_k_minus, self.G_diff = self.create_next_graphs()


    def find_next_node_and_update(self):
        for order in range(2, len(self.G.nodes)):

            # find next node -> shared nb of past nodes which is in self.G_diff 
            v1 = self.subgraph_nodes[-2]
            v2 = self.subgraph_nodes[-1]
            candidate_nodes = [n for n in self.G.neighbors(v1) if n in self.G.neighbors(v2)]
            self.candidate_nodes_in_G_diff = list(set(candidate_nodes).intersection(set(self.G_diff.nodes)))
            # ic((v1, v2), candidate_nodes, self.candidate_nodes_in_G_diff)

            # # check part 3 of refined canonical order theorem -> candidate node has two nbs in self.G_diff
            for node in self.candidate_nodes_in_G_diff:
                true_candidate_nodes = [] # TODO rename 

                neighbours = {n for n in self.G.neighbors(node)}

                if len(set(self.G_diff.nodes).intersection(neighbours)) >= 2:
                    true_candidate_nodes.append(node)
                elif len(self.G_diff.nodes) <= 2: 
                    true_candidate_nodes.append(node)

                assert len(true_candidate_nodes) == 1, "candidate nodes are invalid!" # TODO issue arirses bc have sepersting triangles

            next_node = true_candidate_nodes[0]
            # ic((true_candidate_nodes, next_node))
            # ic(self.subgraph_nodes)
            

            self.G.nodes[next_node]["canonical_order"] = order
            self.subgraph_nodes.append(next_node)
        
            self.G_k_minus, self.G_diff = self.create_next_graphs()

            self.test_biconnect()

    # helpers
    def get_node_index(self, key):
        dict_key = get_key_by_value(self.corner_node_data, key, object=True)
        return self.corner_node_data[dict_key].node
    
    def create_next_graphs(self):
        self.G_k_minus = nx.subgraph(self.G, self.subgraph_nodes)
        self.G_diff = nx.subgraph(self.G, set(self.G.nodes).difference(set(self.G_k_minus.nodes)))
        return self.G_k_minus, self.G_diff
    
    def test_biconnect(self):
        a = Augment(self.G_k_minus)
        a.G_biconnect = self.G_k_minus
        a.test_biconnect()

    
    



    




