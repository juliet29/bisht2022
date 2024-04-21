from helpers import *
from augment import *

from helpers_classes import *

from four_complete_locations import *
from canonical_order_node import *


class KantCanonicalOrder:
    def __init__(self, GraphData: GraphData) -> None:
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.corner_node_dict = GraphData.corner_node_dict
        self.order = None
        self.diff_graph_state = {}
        # NOTE: canonical order is indexed 1,2,... while nodes are indexed 0,1,2, ... 
        self.vn = len(self.G.nodes) - 1


    def initialize_order(self):
        self.initialize_all_nodes()
        self.update_starting_nodes()
        # self.update_vn()

    def initialize_all_nodes(self):
        for node_index in self.G.nodes:
            self.G.nodes[node_index]["data"] = NodeCanonicalOrder(index=node_index, order=-99)


    def update_starting_nodes(self):
        # cardinal updates
        for number in list(range(2)):
            # u = v1 ⇒ v_south , u=v2 ⇒ v_west, w = v_n ⇒ v_north 
            # (following kindermann)
            node_index = get_index_by_cardinal_direction(CardinalDirections(number), self.corner_node_dict) 
            
            self.G.nodes[node_index]["data"] = NodeCanonicalOrder(index=node_index, order=number+1)
        # ending node updates
        self.G.nodes[self.vn]["data"].visited = 2


    # def update_vn(self):
    #     self.vn-=1
       

    #     # self.G.nodes[(self.vn-1)]["data"].visited = 2
    #     # TODO should be counting down .. 

    