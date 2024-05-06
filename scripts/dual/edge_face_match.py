from helpers import nx
from angles import calc_angles_complex
from face_data import FaceData


class EdgeFaceMatch:
    def __init__(self, GraphData, faces) -> None:
        assert type(GraphData.G) == nx.DiGraph, "Not a directed graph!"
        self.G = GraphData.G 
        self.faces = faces
        self.curr_edge = None

    def run(self):
        self.prepare_edge_faces()
        self.match_all_edges()
    
    def prepare_edge_faces(self):
        dir_edges = list(self.G.edges)
        self.edge_faces = {k:FaceData() for k in dir_edges}

    def match_all_edges(self):
        for edge in self.edge_faces.keys():
            self.curr_edge = edge
            self.match_edge()

    def match_edge(self):
        self.match_half_edge(self.curr_edge)
        self.match_half_edge(self.get_opposite_edge(self.curr_edge), REVERSE=True)

    def match_half_edge(self, edge, REVERSE=False):
        for face in self.faces:
            if edge in face:
                if REVERSE:
                    self.edge_faces[self.curr_edge].update_right_face(face)
                else:
                    self.edge_faces[self.curr_edge].update_left_face(face)
                break

    def get_opposite_edge(self, e):
        return (e[1], e[0])


