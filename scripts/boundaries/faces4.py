from stgraph_data import STGraphData
import shapely as sp
from angles import angle_from_dot_product
from icecream import ic

class Faces:
    def __init__(self, STGraphData) -> None:
        self.data = STGraphData
        self.embed = self.data.embed
        self.G = self.data.G
        self.curr_node = None
        self.prev_node = None
        self.face = []

        self.create_embed_points()
        self.get_starting_edge()


    def get_starting_edge(self):
        # TODO make dynamic 
        self.prev_node = 0
        self.curr_node = 1


    def create_embed_points(self):
        self.embed_points = {key:sp.Point(val) for key, val in self.embed.items()}

    def get_next_edge(self):
        self.get_curr_nbs()
        self.find_smallest_angle()
        self.face.append(self.prev_node)
        self.prev_node = self.curr_node
        self.curr_node = self.smallest_angle_node
        ic(self.face)


    def get_curr_nbs(self):
        self.curr_nbs = [n for n in self.G.neighbors(self.curr_node) if n != self.prev_node]

    
    def find_smallest_angle(self):
        angles = []
        for nb in self.curr_nbs:
            angle = self.calc_angle_between_points(nb)
            angles.append((angle, nb))
        self.smallest_angle_node = sorted(angles)[0][1]

    
    def calc_angle_between_points(self, test_node):
        origin = self.embed_points[self.curr_node]
        prev_pt = self.embed_points[self.prev_node]
        test_pt = self.embed_points[test_node]
        angle = angle_from_dot_product(origin=origin, a=prev_pt, b=test_pt)
        return angle


        

