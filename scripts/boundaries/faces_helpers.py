from helpers import ic
from copy import deepcopy


class FacesBaseClass:
    def __init__(self, GraphData, embedding) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embedding = embedding

        # TODO these should be gotten automatically
        # TODO update for graphs that are not st..
        self.source_vertex = 0
        self.target_vertex = 2
        self.focus_vertex = 0

        self.faces = []
        self.face = []
        self.outer_face_bool = False

        self.establish_euler_targets()
        self.create_embedding_versions()

    def get_edge(self, embed, edge_index, node=None):
        focus_node = node if node else self.focus_vertex
        return embed[focus_node][edge_index]

    def get_nbs(self, embed, node=None):
        focus_node = node if node else self.focus_vertex
        return [v[1] for v in embed[focus_node]]

    def update_focus_vertex(self):
        if len(self.mutated_embedding[self.focus_vertex]) == 0:
            self.focus_vertex += 1

    def update_current_edge(self):
        self.curr_edge = self.next_edge
        self.face.append(self.curr_edge)
        # self.add_edge_to_current_face(edge)

    def inititialize_face(self):
        self.face_start = self.get_edge(embed=self.mutated_embedding, edge_index=0)
        self.face.append(self.face_start)
        self.curr_edge = self.face_start


    def check_face_complete(self):
        if self.face[0][0] == self.face[-1][1]:
            return True

    def handle_face_complete(self):
        self.faces.append(self.face)
        for e in self.face:
            self.mutated_embedding[e[0]].remove(e)
        self.face = []

    def check_faces_counter(self):
        if self.faces_counter > self.total_faces_goal:
            if not self.check_interior_goal():
                raise Exception("Too many iterations, too few completed faces")

    def check_counter(self):
        if self.counter > 8:
            raise Exception("Too many iterations, no end to this face in sight")


    def establish_euler_targets(self):
        self.n_nodes = len(self.G.nodes)
        self.n_edges = len(self.G.edges)

        self.total_faces_goal = self.n_edges - self.n_nodes + 2
        self.interor_faces_goal = self.total_faces_goal - 1

    def check_near_interior_goal(self):
        if self.interor_faces_goal - 1 == len(self.faces):
            return True

    def check_interior_goal(self):
        if self.interor_faces_goal == len(self.faces):
            return True

    def check_total_goal(self):
        if self.total_faces_goal == len(self.faces):
            ic(self.faces)
            return True

    def create_embedding_versions(self):
        self.mutated_embedding = deepcopy(self.embedding)
        self.preserved_embedding = deepcopy(self.embedding)
        self.remove_source_target_edges()

    def remove_source_target_edges(self):
        self.st = (self.source_vertex, self.target_vertex)
        self.ts = (self.target_vertex, self.source_vertex)
        for embed in [self.mutated_embedding, self.preserved_embedding]:
            embed[self.source_vertex].remove(self.st)
            embed[self.target_vertex].remove(self.ts)

    def add_source_target_edges(self):
        for embed in [self.mutated_embedding, self.preserved_embedding]:
            embed[self.source_vertex].append(self.st)
            embed[self.target_vertex].append(self.ts)
