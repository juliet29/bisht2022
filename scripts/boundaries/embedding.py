
from helpers import nx
import math
from helpers_classes import get_emedding_coords_as_point

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
        # ref: https://stackoverflow.com/questions/41855695/sorting-list-of-two-dimensional-coordinates-by-clockwise-angle-using-python/41856340#41856340

        point = [point.x, point.y]
        origin = [self.curr_node_coord.x, self.curr_node_coord.y]
        # refvec = [0, 1] # noon 
        refvec = [-1, 0] #9pm 
        refvec = [1, 0] #3pm  for ccw

        # Vector between point and the origin: v = p - o
        vector = [point[0]-origin[0], point[1]-origin[1]]
        # Length of vector: ||v||
        lenvector = math.hypot(vector[0], vector[1])
        # If length is zero there is no angle
        if lenvector == 0:
            return -math.pi, 0
        # Normalize vector: v/||v||
        normalized = [vector[0]/lenvector, vector[1]/lenvector]
        dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]     # x1*x2 + y1*y2
        diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]     # x1*y2 - y1*x2
        angle = math.atan2(diffprod, dotprod)
        # Negative angles represent counter-clockwise angles so we need to subtract them from 2*pi (360 degrees)

        if angle < 0:
            return 2*math.pi+angle
        # I return first the angle because that's the primary sorting criterium
        # but if two vectors have the same angle then the shorter distance should come first.
        return angle
        



