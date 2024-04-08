from helpers import *
from augment import *

from helpers_classes import *


class KantCanonicalOrder:
    def __init__(self, GraphData: GraphData) -> None:
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.corner_node_dict = GraphData.corner_node_dict
        self.order = None
        self.diff_graph_state = {}


    def initialize_order(self):
        self.subgraph_nodes = []

        self.G.nodes[self.get_node_index("south")]["canonical_order"] = 1
        self.G.nodes[self.get_node_index("west")]["canonical_order"] = 2
        self.subgraph_nodes.extend(
            [self.get_node_index("south"), self.get_node_index("west")]
        )

        self.G_k_minus, self.G_diff = self.create_next_graphs()

    