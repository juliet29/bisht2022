from helpers_classes import GraphData
from canonical_order_base import CanonicalOrderBaseClass



class KantCanonicalOrder(CanonicalOrderBaseClass):
    def __init__(self, GraphData:GraphData) -> None:
        super(KantCanonicalOrder, self).__init__(GraphData)

    def run(self):
        self.initialize_order()
        self.finish_order()


    def initialize_order(self):
        self.initialize_all_nodes()
        self.update_starting_nodes()


    def finish_order(self):
        for i in range(len(self.G.nodes)):
            self.order_next_node()
            if self.vk ==  1:
                print(f"completed order - vk == {self.vk}")
                break

    def order_next_node(self):
        self.get_nbs_of_last_2_ordered_nodes()
        self.rearrange_unordered_nodes()
        for node_index in self.unordered_nodes: # TODO could search only in unordered nodes 
            if self.check_vertex_criteria(node_index): #3.1
                self.current_node_index = node_index
                self.update_node(self.current_node_index)
                
                self.update_tracker()
                self.update_neighbors(self.current_node_index)
                self.update_rel_helper()

                if self.G_unmarked_ext:
                    self.check_conditions()
            
                self.update_vk()

                # operate on only one node each round
                break


    def check_vertex_criteria(self, node_index):
        data = self.get_node_data(node_index)
        if data.mark == False:
            if data.visited >= 2:
                if data.chords == 0:
                    if data.order != 0 and data.order != 1:
                        return True
                    



