
from helpers import sp, nx
import math
from helpers_classes import get_emedding_coords_as_point

class Embedding:
    def __init__(self, GraphData) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.half_edges = []
        

    def start_order(self, node=0):
        self.curr_node = node
        self.curr_node_coord =  get_emedding_coords_as_point(self.embed, [self.curr_node])[0]

        self.nbs =  [n for n in nx.neighbors(self.G, self.curr_node)]
        self.nb_coords = get_emedding_coords_as_point(self.embed, self.nbs)

        



    def ccw_order(self):
        # Calculate the angle between each coordinate and the self.curr_node_coord
        self.angles = [
            (math.atan2(pt.y - self.curr_node_coord.y, pt.x - self.curr_node_coord.x), node) for node, pt in zip(self.nbs, self.nb_coords)
        ]

        # Sort the coordinates based on the angles
        self.sorted_nodes = sorted(self.angles)

        # Extract the sorted coordinates without the angles
        self.ccw_ordered_nodes = [node for angle, node in self.sorted_nodes]

    def create_half_edges(self):
        edges = [(self.curr_node, n) for n in self.ccw_ordered_nodes]
        



