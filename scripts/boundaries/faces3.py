from faces_base import FacesBaseClass, ic


class Faces(FacesBaseClass):
    def __init__(self, STGraphData) -> None:
        super(Faces, self).__init__(STGraphData)

    def find_faces(self):
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
                self.update_focus_vertex()
                self.outer_face = self.faces[-1]
                break

            self.faces_counter += 1
            self.check_faces_counter()

    def finish_face(self):
        self.counter = 0
        while True:
            if self.check_face_complete():
                self.handle_face_complete()
                break
            else:
                if self.outer_face_bool:
                    self.find_next_edge_outer_face()
                else:
                    self.find_next_edge()
            self.counter += 1
            self.check_counter()

    def start_face(self):
        self.inititialize_face()
        self.face_end = self.get_edge(embed=self.mutated_embedding, edge_index=1) # TODO why is this 1, maybe it should be next or neg 1? 
        ic(self.face_end)
        self.face_end_nb = self.face_end[1]

    def start_outer_face(self):
        self.inititialize_face()
        self.outer_face_bool = True

    def find_next_edge(self):
        self.start_node, self.end_node = self.curr_edge
        self.end_node_nbs = self.get_nbs(
            embed=self.preserved_embedding, node=self.end_node
        )
        ic(self.curr_edge, self.end_node_nbs)

        if self.face_end_nb in self.end_node_nbs:
            self.find_next_edge_based_on_end_nb()
        else:
            self.find_next_edge_based_on_index()

        self.next_edge = self.get_edge(
            embed=self.preserved_embedding, edge_index=self.ix_next, node=self.end_node
        )
        self.update_face()


    def find_next_edge_based_on_end_nb(self):
        self.ix_next = self.end_node_nbs.index(self.face_end_nb)

    def find_next_edge_based_on_index(self):
        if len(self.end_node_nbs) == 1:
            self.ix_next = 0
            return

        
        ix_curr = self.end_node_nbs.index(self.start_node)
        # if ix_curr != 0:
        #     self.ix_next = ix_curr - 1
        # else:
        #     self.ix_next = len(self.end_node_nbs) - 1

        if ix_curr != len(self.end_node_nbs) - 1:
            self.ix_next = ix_curr + 1
        else:
            self.ix_next = 0

        ic(ix_curr, self.ix_next)

    def find_next_edge_outer_face(self):
        self.start_node, self.end_node = self.curr_edge
        nbs = self.get_nbs(embed=self.mutated_embedding, node=self.end_node)
        assert len(nbs) == 1, "Too many remaining nbs vertex on outer face"
        self.next_edge = self.get_edge(
            embed=self.mutated_embedding, edge_index=0, node=self.end_node
        )
        self.update_face()