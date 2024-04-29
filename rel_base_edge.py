from canonical_order_kant import KantCanonicalOrder
from edge_label import EdgeLabeling, EdgeColorings
from helpers import nx, ic


class RELBaseEdge:
    def __init__(self, REL) -> None:
        self.REL = REL
        self.curr_order = 2

    def step_base_edge_connnections(self):
        self.curr_order =  list(self.REL.co.rel_helper.keys())[1]
        self.curr_node = self.REL.get_node_index_by_order(self.curr_node)

        self.valid_nbs = self.REL.find_valid_nbs(self.curr_node)
        
    
    def create_incoming_edges(self):
        self.edges = [(self.curr_node, nb) for nb in self.valid_nbs]

    def find_base_edge(self):
        nb_orders = [self.REL.get_order_by_node_index(nb) for nb in self.valid_nbs]

        self.base_ix = nb_orders.index(min(nb_orders))

    def assign_colors(self):
        if self.base_ix == 0:
            



