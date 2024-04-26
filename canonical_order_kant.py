from helpers import *
from augment import *

from helpers_classes import *

from four_complete_locations import *
from canonical_order_node import *

from boundary_cycle import *
from convex_boundary import *

# NOTE: canonical order is indexed 1,2,... while nodes are indexed 0,1,2, ... 

class KantCanonicalOrder:
    def __init__(self, GraphData:GraphData) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.corner_node_dict = GraphData.corner_node_dict
        self.order = None
        self.diff_graph_state = {}
        self.ordered_nodes = []

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

    def order_next_node(self):
        for node_index in self.G.nodes:
            if self.check_vertex_criteria(node_index): #3.1
                self.current_node_index = node_index
                
                self.update_node(self.current_node_index)
                self.ordered_nodes.append(self.current_node_index)

                self.update_vk()
                
                if self.vk < 2:
                    ic(f"finished running - vk in loop {self.vk}")
                    return
                self.update_neighbors(self.current_node_index)
                break

    def check_vertex_criteria(self, node_index):
        data = self.get_node_data(node_index)
        if data.mark == False:
            if data.visited >= 2:
                # ic(f"{node_index} has >= 2 visited")
                if data.chords == 0:
                    if data.order != 0 and data.order != 1:
                        return True
                    
    def update_node(self, node_index):
        # TODO clean this up so that not holding on to data at this point // 
        # ic(node_index)
        data = self.get_node_data(node_index)
        data.update_mark()
        data.add_node_to_order(self.vk)

    def update_vk(self):
        # ic(f"updated vk: {self.vk}")
        self.vk-=1

    def update_neighbors(self, node_index):
        valid_nbs = [nb for nb in self.G.neighbors(self.vk) if self.get_node_data(nb).mark == False]
        # ic(valid_nbs)
        for nb in valid_nbs: #3.2
            data = self.get_node_data(nb)
            data.update_visited()
        
        self.G_chord_analysis = self.get_chord_analysis_graph()
        for node in valid_nbs + [node_index]: # 3.3
            self.check_and_update_chords(self.G_chord_analysis, node)
    
    
    def check_and_update_chords(self, G_chord_analysis, node_index):
        if node_index in G_chord_analysis.nodes:
            nbs = [nb for nb in G_chord_analysis.neighbors(node_index)]
            if len(nbs) > 2:
                num_chords = len(nbs) - 2
                ic(f"updating chords for {node_index} to {num_chords}")
                self.get_node_data(node_index).update_chords(num_chords)

    def get_chord_analysis_graph(self, ):
        G_diff = self.get_unmarked_graph()
        self.G_ext = self.get_exterior_graph(G_diff)
        return self.G_ext

    def get_unmarked_graph(self, ):
        marked_nodes = []
        for node_index in self.G.nodes:
            data = self.get_node_data(node_index)
            if data.mark == True:
                marked_nodes.append(node_index)

        unmarked_nodes = set(self.G.nodes).difference(set(marked_nodes))
        G_diff = nx.subgraph(self.G, unmarked_nodes)
        return G_diff

    def get_exterior_graph(self, G_diff):
        temp_graph_data  = GraphData(G_diff, self.embed)
        b = ConvexBoundary(temp_graph_data)
        # b = BoundaryCycle(temp_graph_data, CONVEX_APPROACH=True)
        # exterior_nodes = b.ccw_boundary_cycle
        G_ext = nx.subgraph(self.G, b.cycle)        
        return G_ext
       

    def get_node_data(self, node_index):
        data:NodeCanonicalOrder = self.G.nodes[node_index]["data"]
        return data
    

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


    