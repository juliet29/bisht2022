from canonical_order_kant import KantCanonicalOrder
from edge_label import EdgeLabeling, EdgeColorings
from helpers import nx, ic


class RELBaseEdge:
    def __init__(self, REL) -> None:
        self.REL = REL
        self.curr_order =  list(self.REL.co.rel_helper.keys())[1]


    def step_base_edge_connnections(self):
        self.skip = False
        self.create_incoming_edges()
        if self.skip == False:
            self.find_base_edge()
            self.assign_colors()
        self.curr_order-=1

        
    def create_incoming_edges(self):
        self.curr_node = self.REL.get_node_index_by_order(self.curr_order)
        if self.curr_node in self.REL.corner_nodes:
            ic(f"skipping {self.curr_node} bc it is a corner node")
            self.skip = True
            return 
        self.valid_nbs = self.REL.find_valid_nbs(self.curr_order)
        ic(self.curr_node, self.valid_nbs)

        assert len(self.valid_nbs) > 0, f"No valid nbs for {self.curr_node}"

        self.edges = [(nb, self.curr_node) for nb in self.valid_nbs]


    def find_base_edge(self):
        nb_orders = [self.REL.get_order_by_node_index(nb) for nb in self.valid_nbs]
        self.base_ix = nb_orders.index(min(nb_orders))

    def assign_colors(self):
        if self.base_ix == 0:
            self.color_edges(self.edges[0], EdgeColorings.RIGHT_RED)
            self.color_edges(self.edges[1:], EdgeColorings.LEFT_BLUE)

        elif self.base_ix == len(self.valid_nbs) - 1:
            self.color_edges(self.edges[0:-1], EdgeColorings.RIGHT_RED)
            self.color_edges(self.edges[-1], EdgeColorings.LEFT_BLUE)

        else:
            self.color_edges(self.edges[0:self.base_ix], EdgeColorings.RIGHT_RED)
            self.color_edges(self.edges[self.base_ix:], EdgeColorings.LEFT_BLUE)


    def color_edges(self, edges, color:EdgeColorings):
        self.edges_to_color = edges
        if type(edges) == tuple:
            edges = [edges]
        self.attrs =  {e: {"data": EdgeLabeling(color)} for e in edges}

        self.REL.G_rel.add_edges_from(edges)
        nx.set_edge_attributes(self.REL.G_rel, self.attrs)

        self.REL.edge_split[color].extend(edges)    


