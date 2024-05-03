from helpers import *
from augment import *

from helpers_classes import *

from four_complete_locations import *
from canonical_order_node import *

from boundary_cycle import *
from convex_boundary import *
from canonical_order_checks import CanonicalOrderChecks

from graph_checks import NotTriangulatedError

# NOTE: canonical order is indexed 1,2,... while nodes are indexed 0,1,2, ... 

class KantCanonicalOrder:
    def __init__(self, GraphData:GraphData) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.corner_node_dict = GraphData.corner_node_dict
        
        self.ordered_nodes = []
        self.unordered_nodes = list(self.G.nodes)
        self.rel_helper = {}

        self.vk = len(self.G.nodes) - 1
        
        # self.run()

    def run(self):
        self.initialize_order()
        self.finish_order()


    def initialize_order(self):
        self.initialize_all_nodes()
        self.update_starting_nodes()

    def initialize_all_nodes(self):
        for node_index in self.G.nodes:
            self.G.nodes[node_index]["data"] = NodeCanonicalOrder(index=node_index)

    def update_starting_nodes(self):
        # cardinal updates - south and east 
        for number in list(range(2)):
            node_index = get_index_by_cardinal_direction(CardinalDirections(number), self.corner_node_dict) 
            self.G.nodes[node_index]["data"].order = number 

        # update north node - 
        node_index = get_index_by_cardinal_direction(CardinalDirections.NORTH, self.corner_node_dict) 
        self.G.nodes[node_index]["data"].visited = 2

    def finish_order(self):
        for i in range(len(self.G.nodes)):
            self.order_next_node()
            if self.vk ==  1:
                ic(f"completed order - vk == {self.vk}")
                break

    def order_next_node(self):
        for node_index in self.G.nodes: # TODO could search only in unordered nodes 
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
                    
    def update_node(self, node_index):
        data = self.get_node_data(node_index)
        data.update_mark()
        data.add_node_to_order(self.vk)

    def update_vk(self):
        self.vk-=1

    def update_neighbors(self, node_index):
        valid_nbs = [nb for nb in self.G.neighbors(self.current_node_index) if self.get_node_data(nb).mark == False]

        for nb in valid_nbs: #3.2
            data = self.get_node_data(nb)
            data.update_visited()
        
        self.get_exterior_graphs()

        if self.G_unmarked_ext:
            for node in valid_nbs: # 3.3
                self.check_and_update_chords(node)


    def update_tracker(self):
        self.ordered_nodes.append(self.current_node_index)
        self.unordered_nodes.remove(self.current_node_index)

    def check_conditions(self):
        self.coc = CanonicalOrderChecks(self)
        self.coc.check_conditions()


    def check_and_update_chords(self, node_index):
        if node_index in self.G_unmarked_ext.nodes:
            nbs = [nb for nb in self.G_unmarked_ext.neighbors( node_index)]
            if len(nbs) > 2:
                num_chords = len(nbs) - 2
                ic(f"updating chords for  {node_index} to {num_chords}")
                self.get_node_data(node_index).update_chords(num_chords)
            
            if len(nbs) == 2 and self.get_node_data(node_index).chords != 0:
                # only want to do this if num_chords was previously not 0 .. 
                ic(f"{node_index} has no more chords")
                self.get_node_data(node_index).update_chords(0)
    

    def get_exterior_graphs(self, ):
        self.differentate_graph()
        self.get_exterior_unmarked_graph()
        self.get_exterior_marked_graph()

    def differentate_graph(self):
        self.G_unmarked = nx.subgraph(self.G, self.unordered_nodes)
        # dont want to include current node 
        self.G_marked = nx.subgraph(self.G, self.ordered_nodes[0:-1])

    def get_exterior_unmarked_graph(self):
        try:
            self.boundary_unmarked = ConvexBoundary(GraphData(self.G_unmarked, self.embed))
            self.unordered_cycle = copy.deepcopy(self.boundary_unmarked.cycle)
            self.G_unmarked_ext = nx.subgraph(self.G, self.boundary_unmarked.cycle)  
            
        except NotTriangulatedError: 
            ic(f"ISSUE  FINDING UNMARKED CYCLE when vk = {self.vk}")
            self.unordered_cycle = []
            self.G_unmarked_ext = None
            

    def get_exterior_marked_graph(self):
        try:
            self.boundary_marked = ConvexBoundary(GraphData(self.G_marked, self.embed))
            self.ordered_cycle = copy.deepcopy(self.boundary_marked.cycle)
        except:
            self.ordered_cycle = []


    def update_rel_helper(self):
        self.rel_helper[self.vk] = {"unordered_boundary": self.unordered_cycle , "ordered_boundary": self.ordered_cycle}


    def get_node_data(self, node_index):
        data:NodeCanonicalOrder = self.G.nodes[node_index]["data"]
        return data
    
    


    # for plotting 
    def split_graph_by_ordered(self, k):
        # for checking while going forward ! 
        ordered_nodes = []
        remaining_nodes = []
        for node_index in self.G.nodes:
            if self.get_node_data(node_index).order < k:
                ordered_nodes.append(node_index)
            elif self.get_node_data(node_index).order > k:
                remaining_nodes.append(node_index)
        
        curr_node = list(set.difference(set(self.G.nodes), set(remaining_nodes+ordered_nodes)))

        assert len(curr_node) == 1, "more than one current node :/"

        curr_node = curr_node[0]
        curr_edges = [e for e in list(self.G.edges) if curr_node in e]

        G_remain = nx.subgraph(self.G, remaining_nodes)
        G_ordered = nx.subgraph(self.G, ordered_nodes)
        # G_curr = nx.subgraph(self.G, list(curr_node))

        return G_remain, G_ordered, curr_node, curr_edges


    