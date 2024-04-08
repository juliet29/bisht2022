from helpers import *
from augment import *

from helpers_classes import *

from four_complete_locations import *


class KantCanonicalOrder:
    def __init__(self, GraphData: GraphData) -> None:
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.corner_node_dict = GraphData.corner_node_dict
        self.order = None
        self.diff_graph_state = {}


    def initialize_order(self):
        for number in list(range(3)):
            node_index = get_index_by_cardinal_direction(CardinalDirections(number), self.corner_node_dict) # TODO -> put this in a different class..

            if number < 2:
                order = number + 1
            else:
                order = len(self.G.nodes)

            self.G.nodes[node_index]["canonical_order_data"] = NodeCanonicalOrder(index=node_index, order=order)

    