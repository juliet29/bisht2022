from helpers import sp, nx, ic
from copy import deepcopy

class Faces:
    def __init__(self, GraphData, embedding) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embedding = embedding


        self.source_vertex = 0
        self.target_vertex = 2
        self.focus_vertex = 1

    def create_edge_list(self):
        self.all_edges = []
        for v in self.embedding.values():
            for iv in v:
                    self.all_edges.append(iv)

        self.available_edges = deepcopy(self.all_edges)


    def create_simple_face(self):
        # init edge
        self.face = []
        self.face.append(self.get_edge(self.focus_vertex, 0))
        # next edges
        nbs = self.get_nbs(self.focus_vertex)
        for ix, _ in enumerate(nbs):
            try:
                self.face.append((nbs[ix], nbs[ix+1]))
            except:
                # last edge 
                self.face.append((nbs[ix], self.focus_vertex))
                break

    def identify_invalid_edge(self):
        self.invalid_edges = []
        for e in self.face: 
            if e not in self.available_edges:
                self.invalid_edges.append(e)
        assert len(self.invalid_edges) == 1, "More than 1 invalid edge"
        self.start_vertex, self.end_vertex = self.invalid_edges[0]
        

    def get_correct_path(self):
        self.potential_paths = []
        self.paths = [m for m in nx.all_shortest_paths(self.G, self.start_vertex, self.end_vertex)]

        for path in self.paths: 
            path_center = path[1:-1]
            if self.check_path_validity(path_center):
                self.potential_paths.append(path_center)
        assert len(self.potential_paths) == 1, "More than 1 potential path"
        self.path_edges = list(nx.path_graph(self.potential_paths[0]).edges)

    def update_face(self):
        pass
            
            
                    
    def check_path_validity(self, path):
        if self.source_vertex not in path:
                if self.target_vertex not in path:
                    if self.focus_vertex not in path:
                        return True



    def get_edge(self, edge_index):
        return self.embedding[self.focus_vertex][edge_index]

    def get_nbs(self):
        return [v[1] for v in self.embedding[self.focus_vertex]]

    def check_euler(self):
        self.n_nodes = len(self.G.nodes)
        self.n_edges = len(self.G.edges)
        self.n_faces = len(self.faces)
        
        self.correct_balance = self.n_edges - self.n_nodes  + 2 == self.n_faces
        if self.correct_balance: 
            return True
        else:
            return False


    