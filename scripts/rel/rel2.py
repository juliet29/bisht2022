import matplotlib.pyplot as plt
from copy import deepcopy
import networkx as nx

from canonical_order_kant import KantCanonicalOrder
from edge_label import EdgeLabeling, EdgeColorings

from helpers import ic
from helpers_classes import show_graph_attributes
from stgraph_data import  STGraphData
from rel_interior import RELInterior
from rel_corners import RELCorners
from rel_base_edge import RELBaseEdge



class REL2:
    def __init__(self, co:KantCanonicalOrder) -> None:
        self.co = co

        self.G_rel = nx.DiGraph()
        self.edge_split = {EdgeColorings(0): [], EdgeColorings(1): []}

        self.remove_corner_connections()
        self.create_mapping()

        self.RELBaseEdge = RELBaseEdge(self)
        self.RELCorners = RELCorners(self)
        self.RELInterior = RELInterior(self)

    def create_REL(self):
        self.order_corners()
        n_goal_edges = len(self.G_no_corner_connect.edges)
        cntr = 0
        while True:
            self.step_order_base_edge()
            if len(self.G_rel.edges) >= n_goal_edges:
                ic("ending, sufficient edges")
                self.split_REL()
                break

            cntr+=1
            if cntr > n_goal_edges:
                raise Exception("too many iterations, not enough edges")
            

    def order_corners(self):
        self.RELCorners.order_all_corners()

    def step_order_base_edge(self):
        self.RELBaseEdge.step_base_edge_connnections()
            
    def split_REL(self):
        self.G_blue = nx.DiGraph(self.edge_split[EdgeColorings.LEFT_BLUE])
        s, t = self.check_st_graph(self.G_blue)
        self.vertical_st = STGraphData(self.G_blue, self.co.embed, s, t)

        self.G_red = nx.DiGraph(self.edge_split[EdgeColorings.RIGHT_RED])
        s,t = self.check_st_graph(self.G_red)
        self.horizontal_st = STGraphData(self.G_red, self.co.embed, s, t)

    def check_st_graph(self, G):
        sources = [x for x in G.nodes() if G.out_degree(x)>0 and G.in_degree(x)==0]
        targets = [x for x in G.nodes() if G.out_degree(x)==0 and G.in_degree(x)>0]
        assert len(sources) == 1, f"# source nodes != 1, {sources}"
        assert len(targets) == 1, f"# target nodes != 1, {targets}"
        return sources[0], targets[0] 



    def remove_corner_connections(self):
        # TODO seems like should be a higher level attribute .. 
        self.corner_nodes = [v.index for v in self.co.corner_node_dict.values()] 
        edges_to_ignore = []
        for e in self.co.G.edges:
            if e[0] in self.corner_nodes and e[1] in self.corner_nodes:
                edges_to_ignore.append(e)


        self.G_no_corner_connect = deepcopy(self.co.G)
        self.G_no_corner_connect.remove_edges_from(edges_to_ignore)

    def find_valid_nbs(self, order, boundary="unordered_boundary"):
        curr_node_index = self.get_node_index_by_order(order)
        curr_nbs = self.get_node_nbs(curr_node_index)

        boundary_list = self.co.rel_helper[order][boundary]

        valid_nbs = []

        for node in boundary_list:
            if node in curr_nbs:
                valid_nbs.append(node)

        return valid_nbs



    def create_mapping(self):
        self.order_map = {} 
        self.index_map = {}
        for i in self.G_no_corner_connect.nodes.data():
            order = i[1]["data"].order
            index = i[0]
            self.order_map[order] = index
            self.index_map[index] = order

    def get_node_index_by_order(self, order):
        return self.order_map[order]

    def get_order_by_node_index(self, node_index):
        return self.index_map[node_index]

    def get_node_nbs(self, node_index):
        return [n for n in nx.neighbors(self.G_no_corner_connect, node_index)]
    
    def show_graph_data(self):
        show_graph_attributes(self.G_rel)

    def plot_graph(self):
        # NOTE: plotting with corner connections, even though not ordering with them 
        self.fig, self.axs = plt.subplots(figsize=[6,5])
        nx.draw_networkx(self.co.G, pos=self.co.embed, ax=self.axs)

        self.plot_egdes_by_color(0)
        self.plot_egdes_by_color(1)
        plt.show()


    def plot_egdes_by_color(self, side):
        color = BLUE_COLOR if side == 0 else RED_COLOR
        width = EDGE_WIDTH*2 if side ==0 else EDGE_WIDTH
        edges = self.edge_split[EdgeColorings(side)]

        nx.draw_networkx_edges(self.G_rel, pos=self.co.embed, ax=self.axs, edgelist=edges, edge_color=color, width=width, arrows=True)



BLUE_COLOR = "#444b6e"
RED_COLOR = "#bf3100"
EDGE_WIDTH = 3 
