from helpers import nx, sp, ic
from helpers_classes import get_emedding_coords_as_point, GraphData
from shapely_helpers import get_centroid
from list_and_dict_utils import get_key_by_value

from embedding import Embedding
from faces3 import Faces

from edge_face_match import EdgeFaceMatch
from vertex_face_match import VertexFaceMatch


class Dual:
    "takes in data for 1 st graph"
    # todo break into => embed, edges, coordinates from dual 
    def __init__(self, DiGraphData, GraphData) -> None:
        self.digraph_data = DiGraphData
        self.graph_data = GraphData

    def create_dual(self):
        self.find_and_match_faces()
        self.create_dual_embed()
        self.create_dual_edges()
        self.create_dual_graph()

    def find_and_match_faces(self):
        em = Embedding(self.graph_data)
        em.get_graph_embedding()

        fa = Faces(self.graph_data, em.half_edges)
        fa.find_faces()

        vf = VertexFaceMatch(self.digraph_data, fa.faces)
        vf.run()

        ef = EdgeFaceMatch(self.digraph_data, fa.faces)
        ef.run()

        self.faces = fa.faces
        self.face_dict = {k:v for k,v in enumerate(self.faces)}
        
        self.vertex_faces = vf.vertex_faces
        self.edge_faces = ef.edge_faces

    def create_dual_embed(self):
        self.face_locs = {ix:self.get_center(f) for ix, f in enumerate(self.faces)}
        unit = 0.5
        # convention 4 is left most face created by st connection, 
        # 5 is the outer face and will be on the right 
        self.face_locs[4] = (self.face_locs[3][0] - unit, self.face_locs[4][1] - unit)
        self.face_locs[5] = (self.face_locs[0][0] + unit, self.face_locs[0][1] - unit)

    def get_center(self, face):
        shape = self.create_shape(face)
        xy = get_centroid(shape)
        return xy

    def create_shape(self, face):
        nodes = [e[1] for e in face]
        face_coords = get_emedding_coords_as_point(self.digraph_data.embed, nodes)
        shape = sp.Polygon(sp.LinearRing(face_coords))
        return shape
    

    def create_dual_edges(self):
        self.simplify_edge_faces()
        self.edges = list(self.tuple_edge_faces.values())
        # 4 is technically west, anf 5 is east 
        for ix, e in enumerate(self.edges):
            if e == (5,4):
                self.edges[ix] = (4,5)

    def simplify_edge_faces(self):
        self.tuple_edge_faces = {}
        for k,v in self.edge_faces.items():
            l = self.get_face_ix(v.left_face)
            r = self.get_face_ix(v.right_face)
            self.tuple_edge_faces[k] = (l, r)


    def get_face_ix(self, face):
        return get_key_by_value(self.face_dict, face)


    def create_dual_graph(self):
        G = nx.DiGraph()
        G.add_edges_from(self.edges)
        self.DualGraphData = GraphData(G,embed=self.face_locs)
        


    def simplify_vertex_faces(self):
        self.tuple_vertex_faces = {}
        for k,v in self.vertex_faces.items():
            if v.left_face and v.right_face:
                l = self.get_face_ix(v.left_face)
                r = self.get_face_ix(v.right_face)
                self.tuple_vertex_faces[k] = (l, r)