from helpers import sp, nx, ic
from copy import deepcopy

class Faces:
    def __init__(self, GraphData, embedding) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embedding = embedding
        self.starting_index = 0
        self.node_order = [g for g in nx.dfs_preorder_nodes(self.G)]
        

        self.source_vertex = 0
        self.target_vertex = 2
        self.focus_vertex = 0

        self.counter = 0

        self.faces = []
        self.face = []

    def create_edge_list(self):
        self.all_edges = []
        for v in self.embedding.values():
            for iv in v:
                    self.all_edges.append(iv)

        self.available_edges = deepcopy(self.all_edges)
        self.available_embedding = deepcopy(self.embedding)
        self.remove_source_target_edges()


    def start_face(self):
        self.face_start = self.get_edge(edge_index=0)
        self.add_edge_to_current_face(self.face_start)
        self.curr_edge = self.face_start

        self.face_end = self.get_edge(edge_index=1)
        self.face_end_nb = self.face_end[1]

        ic(self.face_start, self.face_end, self.face_end_nb)

    def finish_face(self):
        while True:
            if self.check_face_complete():
                self.handle_face_complete()
                break
            else: 
                self.find_next_edge()

            self.counter+=1
            if self.counter > 8:
                break 

    def find_next_edge(self):
        self.start_node, self.end_node = self.curr_edge
        self.end_node_nbs = self.get_nbs(self.end_node)

        if self.face_end_nb in self.end_node_nbs:
            self.find_next_edge_based_on_end_nb()
        else:
            self.find_next_edge_based_on_index()

        self.next_edge = self.get_edge(edge_index=self.ix_next, node=self.end_node)

        ic(self.counter)
        ic(self.curr_edge, self.end_node_nbs, self.ix_next, self.end_node, self.next_edge, "\n")
        
        self.curr_edge = self.next_edge
        self.add_edge_to_current_face(self.curr_edge)


    def check_face_complete(self):
        if self.face[0][0] == self.face[-1][1]:
            ic("completed face")
            return True 
        
    def handle_face_complete(self):
        self.faces.append(self.face)
        ic(self.faces)
        for e in self.face:
            self.available_edges.remove(e)
            self.available_embedding[e[0]].remove(e)

        self.face = []


    def find_next_edge_based_on_end_nb(self):
        ic("the end is near!")
        self.ix_next = self.end_node_nbs.index(self.face_end_nb)


    def find_next_edge_based_on_index(self):
        #  TODO check if  nbs contain self.face_end_nb
        ix_curr = self.end_node_nbs.index(self.start_node)

        if ix_curr != 0:
            self.ix_next = ix_curr  - 1
        else:
            self.ix_next = len(self.end_node_nbs) - 1
        

        
    
        
    def add_edge_to_current_face(self, edge):
        self.face.append(edge)
        

    def remove_source_target_edges(self):
        st = (self.source_vertex, self.target_vertex)
        ts = (self.target_vertex, self.source_vertex)
        self.available_edges.remove(st)
        self.available_edges.remove(ts)
        self.available_embedding[self.source_vertex].remove(st)
        self.available_embedding[self.target_vertex].remove(ts)

    def get_edge(self, edge_index, node=None):
        if node:
            return self.available_embedding[node][edge_index]
        else:
            return self.available_embedding[self.focus_vertex][edge_index]

    def get_nbs(self, node=None):
        if node: 
            return [v[1] for v in self.available_embedding[node]]
        else:
            return [v[1] for v in self.available_embedding[self.focus_vertex]]




    def check_euler(self):
        self.n_nodes = len(self.G.nodes)
        self.n_edges = len(self.G.edges)
        self.n_faces = len(self.faces)
        
        self.correct_balance = self.n_edges - self.n_nodes  + 2 == self.n_faces
        if self.correct_balance: 
            return True
        else:
            return False


    