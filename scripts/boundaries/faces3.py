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

        self.faces = []
        self.face = []
        self.outer_face_bool = False

        self.establish_euler_targets()

    def create_edge_list(self):
        self.mutated_embedding = deepcopy(self.embedding)
        self.preserved_embedding = deepcopy(self.embedding)
        self.remove_source_target_edges()

    def finish_faces(self):
        self.faces_counter = 0
        while True:
            self.update_focus_vertex()
            self.start_face()
            self.finish_face()

            if self.check_near_interior_goal():
                self.add_source_target_edges()

            if self.check_interior_goal():
                self.start_outer_face()
                self.finish_face()

            if self.check_total_goal():
                break


            self.faces_counter+=1
            self.check_faces_counter()

    def start_outer_face(self):
        self.face  = []
        self.update_focus_vertex()
        self.face_start = self.get_edge(embed=self.mutated_embedding, edge_index=0)
        self.curr_edge = self.face_start
        self.outer_face_bool = True
        self.face.append(self.face_start)
        
        ic("starting outer face")
     

    def find_next_edge_outer_face(self):
        self.start_node, self.end_node = self.curr_edge

        nbs = self.get_nbs(embed=self.mutated_embedding, node=self.end_node)

        assert len(nbs) == 1, "Too many remaining nbs vertex on outer face"
        
        self.next_edge = self.get_edge(embed=self.mutated_embedding, edge_index=0, node=self.end_node)

        self.curr_edge = self.next_edge
        self.add_edge_to_current_face(self.curr_edge)



    def check_faces_counter(self):
        ic(self.faces_counter)
        if self.faces_counter > self.total_faces_goal:
            if not self.check_interior_goal():
                raise Exception("Too many iterations, too few completed faces")


    def update_focus_vertex(self):
        if len(self.mutated_embedding[self.focus_vertex]) == 0:
            self.focus_vertex+=1

    def start_face(self):
        self.face_start = self.get_edge(embed=self.mutated_embedding, edge_index=0)
        self.add_edge_to_current_face(self.face_start)
        self.curr_edge = self.face_start

        self.face_end = self.get_edge(embed=self.mutated_embedding, edge_index=1)
        self.face_end_nb = self.face_end[1]

        ic(self.face_start, self.face_end, self.face_end_nb)

    def finish_face(self):
        self.counter = 0
        while True:
            if self.check_face_complete():
                self.handle_face_complete()
                break
            else: 
                if self.outer_face_bool:
                    ic("working on outer face")
                    self.find_next_edge_outer_face()
                else:
                    self.find_next_edge()

            self.counter+=1
            if self.counter > 8: # TODO max edges of a face? 
                break 

    def find_next_edge(self):
        # print(f"looking for edge #{self.counter} that will chain to {self.curr_edge}")
        self.start_node, self.end_node = self.curr_edge
        self.end_node_nbs = self.get_nbs(embed=self.preserved_embedding, node=self.end_node)

        if self.face_end_nb in self.end_node_nbs:
            self.find_next_edge_based_on_end_nb()
        else:
            self.find_next_edge_based_on_index()

        self.next_edge = self.get_edge(embed=self.preserved_embedding, edge_index=self.ix_next, node=self.end_node)

        
        self.curr_edge = self.next_edge
        self.add_edge_to_current_face(self.curr_edge)


    def find_next_edge_based_on_end_nb(self):
        # print("the end is near!")
        self.ix_next = self.end_node_nbs.index(self.face_end_nb)


    def find_next_edge_based_on_index(self):
        if len(self.end_node_nbs) == 1:
            self.ix_next = 0
            return

        ix_curr = self.end_node_nbs.index(self.start_node)

        if ix_curr != 0:
            self.ix_next = ix_curr  - 1
        else:
            self.ix_next = len(self.end_node_nbs) - 1
        
        
    def add_edge_to_current_face(self, edge):
        self.face.append(edge)


    def check_face_complete(self):
        if self.face[0][0] == self.face[-1][1]:
            print("completed face")
            return True 
        
    def handle_face_complete(self):
        self.faces.append(self.face)
        ic(f"faces = {self.faces} \n")
        for e in self.face:
            self.mutated_embedding[e[0]].remove(e)

        self.face = []
        

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



    def get_edge(self, embed, edge_index, node=None):
        if node:
            return embed[node][edge_index]
        else:
            return embed[self.focus_vertex][edge_index]

    def get_nbs(self, embed, node=None):
        if node: 
            return [v[1] for v in embed[node]]
        else:
            return [v[1] for v in embed[self.focus_vertex]]
        

    def establish_euler_targets(self):
        self.n_nodes = len(self.G.nodes)
        self.n_edges = len(self.G.edges)
        
        self.total_faces_goal = self.n_edges - self.n_nodes  + 2
        self.interor_faces_goal = self.total_faces_goal -1 


    def check_near_interior_goal(self):
        if self.interor_faces_goal-1 == len(self.faces):
            ic("almost at interior goal !") 
            return True

    def check_interior_goal(self):
        if self.interor_faces_goal == len(self.faces):
            ic("met interior goal !") 
            return True
        
    def check_total_goal(self):
        if self.total_faces_goal == len(self.faces):
            ic("met total goal !") 
            return True
   


    