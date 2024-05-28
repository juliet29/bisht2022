from stgraph_data import STGraphData
import shapely as sp
from angles import angle_from_dot_product, calc_tangent_angle_between_two_points
from icecream import ic

class Faces:
    def __init__(self, STGraphData) -> None:
        self.data = STGraphData
        self.embed = self.data.embed
        self.G = self.data.G
        self.curr_node = None
        self.prev_node = None
        self.start_node = None
        self.face = []
        self.faces = []

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
        if self.check_complete_face():
            self.handle_complete_face()
            ic(self.faces)

    def check_complete_face(self):
        if len(self.face) > 1:
            if self.face[0] == self.face[-1]:
                ic("complete face")
                return True
        
    def handle_complete_face(self):
        self.faces.append(self.face)
        self.face = []
        self.curr_node = None
        self.prev_node = None



    def get_curr_nbs(self):
        self.curr_nbs = [n for n in self.G.neighbors(self.curr_node) if n != self.prev_node]

    
    def find_smallest_angle(self, ref_pt=None):
        angles = []
        for nb in self.curr_nbs:
            angle = self.calc_angle_between_points(nb, ref_pt)
            angles.append((angle, nb))

        self.smallest_angle_node = sorted(angles)[0][1]

    
    def calc_angle_between_points(self, test_node, ref_pt=None):
        origin = self.embed_points[self.curr_node]
        prev_pt = ref_pt if ref_pt else self.embed_points[self.prev_node]
        test_pt = self.embed_points[test_node]
        angle = angle_from_dot_product(origin=origin, a=prev_pt, b=test_pt)
        return angle  
    

    def find_smallest_tangent_angle(self):
        angles = []
        for nb in self.curr_nbs:
            angle = self.calc_tangent_angle_for_point(nb)
            angles.append((angle, nb))

        self.smallest_tangent_angle_node = sorted(angles, reverse=True)[0][1]
    
    def calc_tangent_angle_for_point(self, test_node):
        origin = self.embed_points[self.curr_node]
        test_pt = self.embed_points[test_node]
        angle = calc_tangent_angle_between_two_points(origin, test_pt)
        ic(angle, test_node)
        return angle
    
    
    def find_start_edge(self):
        self.curr_node = self.start_node
        self.get_curr_nbs()
        self.find_smallest_tangent_angle()
        self.prev_node = self.curr_node
        self.curr_node = self.smallest_tangent_angle_node
        ic(self.prev_node, self.curr_node)


        

