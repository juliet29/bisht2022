from canonical_order_kant import KantCanonicalOrder
from edge_label import EdgeLabeling, EdgeColorings
from helpers import nx, plt, ic
from helpers_classes import show_graph_attributes



class REL2:
    def __init__(self, co:KantCanonicalOrder) -> None:
        self.co = co

        self.create_mapping()
        self.rel = nx.DiGraph()
        self.curr_order = 2
        self.edge_split = {EdgeColorings(0): [], EdgeColorings(1): []}

    def step_rel(self):
        self.get_ordered_nbs()
        self.update_outgoing_edges()
        self.update_edge_split()
        ic(self.curr_node_index, self.curr_order)
        self.curr_order+=1
        
        pass


    def get_ordered_nbs(self):
        self.curr_node_index = self.get_node_index_by_order(self.curr_order)
        curr_nbs = self.get_node_nbs(self.curr_node_index)

        ordered_boundary = self.co.rel_helper[self.curr_order]["ordered_boundary"]

        self.ordered_nbs = []
        # for nb in curr_nbs:
        #     if nb in ordered_boundary:
        #         self.ordered_nbs.append(nb)
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

        self.rel.add_edges_from([self.left_edge, self.right_edge])
        nx.set_edge_attributes(self.rel, attrs)


    def update_edge_split(self):
        self.edge_split[EdgeColorings(0)].append(self.left_edge)
        self.edge_split[EdgeColorings(1)].append(self.right_edge)


    def create_mapping(self):
        self.order_map = {} 
        self.index_map = {}
        for i in self.co.G.nodes.data():
            order = i[1]["data"].order
            index = i[0]
            self.order_map[order] = index
            self.index_map[index] = order

    def get_node_index_by_order(self, order):
        return self.order_map[order]

    def get_order_by_node_index(self, node_index):
        return self.index_map[node_index]

    def get_node_nbs(self, node_index):
        return [n for n in nx.neighbors(self.co.G, node_index)]
    
    def show_graph_data(self):
        show_graph_attributes(self.rel)

    def plot_graph(self):
        self.fig, self.axs = plt.subplots(figsize=[6,5])
        nx.draw_networkx(self.co.G, pos=self.co.embed, ax=self.axs)

        self.plot_egdes_by_color(0)
        self.plot_egdes_by_color(1)
        plt.show()



    def plot_egdes_by_color(self, side):
        color = BLUE_COLOR if side == 0 else RED_COLOR
        edges = self.edge_split[EdgeColorings(side)]

        nx.draw_networkx_edges(self.rel, pos=self.co.embed, ax=self.axs, edgelist=edges, edge_color=color, width=EDGE_WIDTH, arrows=True)



BLUE_COLOR = "#444b6e"
RED_COLOR = "#bf3100"
EDGE_WIDTH = 3 
