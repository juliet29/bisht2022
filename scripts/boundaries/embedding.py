
from helpers import nx
import math
from helpers_classes import get_emedding_coords_as_point
from angles import calc_angles_complex

class Embedding:
    def __init__(self, GraphData) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.half_edges = {}

    def get_graph_embedding(self):
        for node in self.G.nodes:
            self.curr_node = node 
            self.get_node_embedding()


    def get_node_embedding(self):
        self.create_coords_for_node()
        self.ccw_order()
        self.create_half_edges()

    def create_coords_for_node(self):
        self.curr_node_coord =  get_emedding_coords_as_point(self.embed, [self.curr_node])[0]
        self.nbs =  [n for n in nx.neighbors(self.G, self.curr_node)]
        self.nb_coords = get_emedding_coords_as_point(self.embed, self.nbs)

        
    def ccw_order(self):
        self.angles = [
            (self.calc_angles_complex(pt), node) for node, pt in zip(self.nbs, self.nb_coords)
        ]

        self.sorted_nodes = sorted(self.angles, reverse=True)
        self.ccw_ordered_nodes = [node for angle, node in self.sorted_nodes]


    def create_half_edges(self):
        self.half_edges[self.curr_node] = [(self.curr_node, n) for n in self.ccw_ordered_nodes]
   

    def calc_angles_complex(self, point):
        angle = calc_angles_complex(origin=self.curr_node_coord, point=point)
        return angle 

        



