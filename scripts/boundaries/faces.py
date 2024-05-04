from helpers import sp, nx, ic
from copy import deepcopy

class Faces:
    def __init__(self, GraphData, embedding) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embedding = embedding
        self.starting_index = 0
        self.node_order = [g for g in nx.dfs_preorder_nodes(self.G)]

    def create_edge_list(self):
        self.all_edges = []
        for v in self.embedding.values():
            for iv in v:
                    self.all_edges.append(iv)

        self.available_edges = deepcopy(self.all_edges)

    def check_euler(self):
        self.n_nodes = len(self.G.nodes)
        self.n_edges = len(self.G.edges)
        self.n_faces = len(self.faces)
        
        self.correct_balance = self.n_edges - self.n_nodes  + 2 == self.n_faces
        if self.correct_balance: 
            return True
        else:
            return False


    def make_faces(self, ):
        self.faces = []
        cntr = 0 

        while True:
            self.make_face()

            overlap = set(self.available_edges).intersection(set(self.face))
            assert len(overlap) == 0, f"overlap in face and available edges {overlap}"

            self.faces.append(self.face)
            self.check_face_edges(self.faces)

            if self.check_euler():
                ic("correct balance")
                break


            cntr+=1
            if cntr == 7:
                break

    def get_starting_edge(self):
        self.starting_node = self.node_order[self.starting_index]
        for e in self.embedding[self.starting_node]:
            if e in self.available_edges:
                ic("starting edge", e)
                return e


    def make_face(self):
        assert self.available_edges, f"No avail edges: {self.available_edges}"

        curr_edge = self.get_starting_edge()
        face = [curr_edge]
        self.available_edges.remove(curr_edge)

        cntr = 0 
        while True:
            next_edge = self.get_next_edge(curr_edge)
            if not next_edge:
                raise Exception(f"no next edge {face, self.available_edges}", )

            self.available_edges.remove(next_edge)

            if next_edge[1] == face[0][0]:
                face.append(next_edge)
                self.face = face
                self.starting_index+=1
                return
   
            else:
                face.append(next_edge)
                curr_edge = next_edge

            cntr+=1
            if cntr == 9:
                raise Exception(f"too many iterations {face, self.available_edges}", )
            



    def get_next_edge(self, curr_edge):
        assert self.available_edges, f"No avail edges: {self.available_edges}"
        self.cw_edges = self.embedding[curr_edge[1]]
        
        self.potential_edges = []
        for e in self.cw_edges:
            if e in self.available_edges:
                self.potential_edges.append(e)

        for potential_edge in self.potential_edges:
            if potential_edge[0] == curr_edge[1]:
                    if potential_edge[1] != curr_edge[0]:
                        return potential_edge
                    

    def check_face_edges(self, faces):
        if len(faces) < 2:
            return
        for ix in range(len(faces)-1):
            assert len(set(faces[ix]).intersection(set(faces[ix+1]))) == 0, "Overlap in edges"