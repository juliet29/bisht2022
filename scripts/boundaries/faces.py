from helpers import sp, nx, ic
from helpers_classes import get_emedding_coords_as_point
from copy import deepcopy

class Faces:
    def __init__(self, GraphData, embedding) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.embedding = embedding
        self.starting_index = 0
        self.all_coords = get_emedding_coords_as_point(self.embed, self.G.nodes)
        self.starting_index = 0
        # self.node_order = [g for g in nx.dfs_preorder_nodes(self.G)]

    def create_edge_list(self):
        self.all_edges = []
        for v in self.embedding.values():
            for iv in v:
                    self.all_edges.append(iv)

        self.available_edges = deepcopy(self.all_edges)



    def make_faces(self):
        self.faces = []
        cntr = 0 

        while True:
            # self.get_starting_edge()
            self.make_face()

            if self.check_shape_overlap():
                self.handle_shape_overlap()
                # TODO 
            
            self.check_edge_overlap()
            self.faces.append(self.face)
            self.check_face_edges(self.faces)

            if self.check_euler():
                ic("correct balance")
                break


            cntr+=1
            if cntr == 7:
                break

    def check_edge_overlap(self):
        overlap = set(self.available_edges).intersection(set(self.face))
        assert len(overlap) == 0, f"overlap in face and available edges {overlap}"



    def make_face(self):
        assert self.available_edges, f"No avail edges: {self.available_edges}"

        self.get_starting_edge()
        
        curr_edge = self.starting_edge
        face = [curr_edge]
        self.available_edges.remove(curr_edge)

        cntr = 0 
        while True:
            next_edge = self.get_next_edge(curr_edge)
            if not next_edge:
                ic(self.faces)
                raise Exception(f"no next edge {face}", )

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
                raise Exception(f"too many iterations {face}", )
            


    def get_next_edge(self, curr_edge):
        assert self.available_edges, f"No avail edges: {self.available_edges}"
        self.cw_edges = self.embedding[curr_edge[1]]
        
        self.potential_edges = []
        for e in self.cw_edges:
            if e in self.available_edges:
                self.potential_edges.append(e)
        
        if curr_edge == (6,2):
            ic(self.potential_edges)

        for potential_edge in self.potential_edges:
            if potential_edge[0] == curr_edge[1]:
                    if potential_edge[1] != curr_edge[0]:
                        return potential_edge
                    
    def handle_shape_overlap(self):
        # put back edges and choose a new starting edge index 
        rev_face = sorted(self.face, reverse=True)
        for e in rev_face:
            self.available_edges.insert(rev_face)
        self.starting_index = 1


    def check_shape_overlap(self):
        self.create_shape()
        diff = set(self.all_coords).difference(set(self.face_coords))
        for p in diff:
            if self.shape.intersects(p):
                ic(p)
                raise Exception("overlapping shape!")
                return True
            


    def create_shape(self):
        nodes = [e[1] for e in self.face]
        self.face_coords = get_emedding_coords_as_point(self.embed, nodes)
        self.shape = sp.Polygon(sp.LinearRing(self.face_coords))


    def get_starting_edge(self):
        self.starting_edge = self.available_edges[self.starting_index]
        ic(self.starting_edge)

    def check_face_edges(self, faces):
        if len(faces) < 2:
            return
        for ix in range(len(faces)-1):
            assert len(set(faces[ix]).intersection(set(faces[ix+1]))) == 0, "Overlap in edges"


    def check_euler(self):
        self.n_nodes = len(self.G.nodes)
        self.n_edges = len(self.G.edges)
        self.n_faces = len(self.faces)
        
        self.correct_balance = self.n_edges - self.n_nodes  + 2 == self.n_faces
        if self.correct_balance: 
            return True
        else:
            return False