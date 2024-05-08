from helpers import ic, nx
from face_data import FaceData
from enum import Enum


# TODO, why all of a sudden callinf vertices when use nodes elsewhere?


class EdgeDirection(Enum):
    IN = 0
    OUT = 1


class VertexFaceMatch:
    def __init__(self, GraphData, faces) -> None:
        assert type(GraphData.G) == nx.DiGraph, "Not a directed graph!"
        self.G = GraphData.G
        self.faces = faces
        self.curr_vertex = None
        self.order = {}
        self.completed_order = False

        # TODO these should be gotten automatically
        # TODO update for graphs that are not st..
        self.source_vertex = 0
        self.target_vertex = 2

        self.correct_faces()
        self.prepare_vertex_faces()

    def run(self):
        self.match_vertices()

    def prepare_vertex_faces(self):
        self.vertex_faces = {k: FaceData() for k in self.G.nodes}

    def match_vertices(self):
        for vertex in self.G.nodes:
            if vertex != self.source_vertex and vertex != self.target_vertex:
                
                self.curr_vertex = vertex
                self.match_curr_vertex()

    def match_curr_vertex(self):
        for ix, face in enumerate(self.new_faces):
            self.order[ix] = []
            for edge in face:
                self.handle_edge(ix, edge)

                self.check_full_order()
                if self.completed_order:
                    self.assign_vertex_faces()
                    break

            if self.completed_order:
                self.reset_order()
                break

    def handle_edge(self, ix, edge):
        if self.incoming_edge(edge, self.curr_vertex):
            self.order[ix].append(EdgeDirection.IN)
        if self.outgoing_edge(edge, self.curr_vertex):
            self.order[ix].append(EdgeDirection.OUT)

    def check_full_order(self):
        # need two faces, with and in and out label for each 
        self.valid_order = {k: v for k, v in self.order.items() if len(v) == 2}

        if len(self.valid_order.keys()) == 2:
            self.completed_order = True

    def reset_order(self):
        self.valid_order = {}
        self.order = {}
        self.completed_order = False

    def assign_vertex_faces(self):
        for k, v in self.valid_order.items():
            if v[0] == EdgeDirection.OUT:
                self.vertex_faces[self.curr_vertex].update_right_face(self.faces[k])
            elif v[0] == EdgeDirection.IN:
                self.vertex_faces[self.curr_vertex].update_left_face(self.faces[k])

    def incoming_edge(self, edge, v):
        if edge[1] == v:
            return True

    def outgoing_edge(self, edge, v):
        if edge[0] == v:
            return True

    def correct_faces(self):
        edges = list(self.G.edges)
        self.new_faces = []
        for face in self.faces:
            new_face = []
            for e in face:
                if e not in edges:
                    new_face.append((e[1], e[0]))
                else:
                    new_face.append(e)
            self.new_faces.append(new_face)

    
