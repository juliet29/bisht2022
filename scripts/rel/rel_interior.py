from canonical_order_kant import KantCanonicalOrder
from edge_label import EdgeLabeling, EdgeColorings
from helpers import nx, ic


class RELInterior:
    def __init__(self, REL) -> None:
        self.REL = REL
        self.curr_order = 2
        


    def step_rel(self):
        self.get_ordered_nbs()
        self.update_outgoing_edges()
        self.update_edge_split()
        ic(self.curr_node_index, self.curr_order)
        self.curr_order+=1
        


    def get_ordered_nbs(self):
        self.curr_node_index = self.REL.get_node_index_by_order(self.curr_order)
        curr_nbs = self.REL.get_node_nbs(self.curr_node_index)

        ordered_boundary = self.REL.co.rel_helper[self.curr_order]["ordered_boundary"]

        self.ordered_nbs = []

        for node in ordered_boundary:
            if node in curr_nbs:
                self.ordered_nbs.append(node)

        assert len(self.ordered_nbs) >= 2, f"Not enough nbs of {self.curr_node_index} have been ordered: NBs={curr_nbs}, Ordered NBs = {self.ordered_nbs}"
    
    def update_outgoing_edges(self):
        self.left_edge = (self.curr_node_index, self.ordered_nbs[0])
        self.right_edge = (self.curr_node_index, self.ordered_nbs[-1])
     
        attrs = {
        self.left_edge: {"data": EdgeLabeling(0)},
        self.right_edge: {"data": EdgeLabeling(1)},
        }

        self.REL.G_rel.add_edges_from([self.left_edge, self.right_edge])
        nx.set_edge_attributes(self.REL.G_rel, attrs)


    def update_edge_split(self):
        self.REL.edge_split[EdgeColorings(0)].append(self.left_edge)
        self.REL.edge_split[EdgeColorings(1)].append(self.right_edge)