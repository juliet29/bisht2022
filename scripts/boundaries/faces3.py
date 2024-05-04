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


    