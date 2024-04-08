from helpers import *
from augment import *

from helpers_classes import *


class CanonicalOrder:
    def __init__(self, GraphData: GraphData) -> None:
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.corner_node_dict = GraphData.corner_node_dict
        self.order = None
        self.diff_graph_state = {}

    def run(self):
        # self.connect_outer_edges()
        self.initialize_order()
        self.find_next_node_and_update()


    def initialize_order(self):
        self.subgraph_nodes = []

        self.G.nodes[self.get_node_index("south")]["canonical_order"] = 1
        self.G.nodes[self.get_node_index("west")]["canonical_order"] = 2
        self.subgraph_nodes.extend(
            [self.get_node_index("south"), self.get_node_index("west")]
        )

        self.G_k_minus, self.G_diff = self.create_next_graphs()

        # create tracker of embedding history ..
        self.tracker = ListHistoryTracker(self.subgraph_nodes)



    def find_next_node_and_update(self):
        for order in range(2, len(self.G.nodes)):
            self.order = order

            # find next node -> shared nb of past nodes which is in self.G_diff
            v1 = self.subgraph_nodes[-2]
            v2 = self.subgraph_nodes[-1]
            candidate_nodes = [
                n for n in self.G.neighbors(v1) if n in self.G.neighbors(v2)
            ]
            self.candidate_nodes_in_G_diff = list(
                set(candidate_nodes).intersection(set(self.G_diff.nodes))
            )
            ic((v1, v2), candidate_nodes, self.candidate_nodes_in_G_diff)

            # # check part 3 of refined canonical self.order theorem -> candidate node has two nbs in self.G_diff
            for node in self.candidate_nodes_in_G_diff:
                candidates_w_2_nbs_in_G_diff = []  # TODO rename

                neighbours = {n for n in self.G.neighbors(node)}

                if len(set(self.G_diff.nodes).intersection(neighbours)) >= 2:
                    candidates_w_2_nbs_in_G_diff.append(node)
                elif len(self.G_diff.nodes) <= 2:
                    candidates_w_2_nbs_in_G_diff.append(node)
                ic(candidates_w_2_nbs_in_G_diff)
                

                assert (
                    len(candidates_w_2_nbs_in_G_diff) == 1
                ), "candidate nodes are invalid!"  # TODO issue arirses bc have sepersting triangles, ## check this.. thought that it was if it was three.. 

            next_node = candidates_w_2_nbs_in_G_diff[0]
            

            self.G.nodes[next_node]["canonical_order"] = self.order
            self.subgraph_nodes.append(next_node)
            self.tracker.append(next_node)

            self.G_k_minus, self.G_diff = self.create_next_graphs()

            self.test_biconnect()

            ic(next_node)
            ic((self.subgraph_nodes, "\n"))


    def create_next_graphs(self):
        self.G_k_minus = nx.subgraph(self.G, self.subgraph_nodes)
        self.G_diff = nx.subgraph(
            self.G, set(self.G.nodes).difference(set(self.G_k_minus.nodes))
        )
        if self.order: # 
            self.diff_graph_state[self.order] = copy.deepcopy(self.G_diff)
    
        return self.G_k_minus, self.G_diff
    
    #MARK: helpers
    def get_history(self):
        history = self.tracker.get_history()
        # history[2:]

        embed_seq = []
        for state in history[2:]:
            filtered_dict = {key: self.embed[key] for key in state if key in self.embed}
            embed_seq.append(filtered_dict)

    def test_biconnect(self):
        a = Augment(self.G_k_minus)
        a.G_biconnect = self.G_k_minus
        a.test_biconnect()

    def get_node_index(self, key):
        dict_key = get_key_by_value(self.corner_node_dict, key, object=True)
        return self.corner_node_dict[dict_key].index