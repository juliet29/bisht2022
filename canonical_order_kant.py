from helpers import *
from augment import *

from helpers_classes import *

from four_complete_locations import *
from canonical_order_node import *

from boundary_cycle import *

# NOTE: canonical order is indexed 1,2,... while nodes are indexed 0,1,2, ... 

class KantCanonicalOrder:
    def __init__(self, GraphData:GraphData) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.corner_node_dict = GraphData.corner_node_dict
        self.order = None
        self.diff_graph_state = {}

        self.vn = len(self.G.nodes) - 1
        
        self.run()

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
        # cardinal updates
        for number in list(range(2)):
            node_index = get_index_by_cardinal_direction(CardinalDirections(number), self.corner_node_dict) 
            self.G.nodes[node_index]["data"].order = number 

        # update last node
        self.G.nodes[self.vn]["data"].visited = 2

    def finish_order(self):
        for i in range(len(self.G.nodes)):
            for node_index in self.G.nodes:
                if self.check_vertex_criteria(node_index): #3.1
                    self.update_node(node_index)
                    self.update_vn()
                    
                    if self.vn < 2:
                        ic(f"vn in loop {self.vn}")
                        return
                    self.update_neighbors(node_index)
                    break

    def check_vertex_criteria(self, node_index):
        data = self.get_node_data(node_index)
        if data.mark == False:
            if data.visited >= 2:
                # ic(f"{node_index} has >= 2 visited")
                if data.chords == 0:
                    if data.order != 1 and data.order != 2:
                        return True
                    
    def update_node(self, node_index):
        # ic(node_index)
        data = self.get_node_data(node_index)
        data.update_mark()
        data.add_node_to_order(self.vn)

    def update_vn(self):
        # ic(f"updated vn: {self.vn}")
        self.vn-=1

    def update_neighbors(self, node_index):
        valid_nbs = [nb for nb in self.G.neighbors(self.vn) if self.get_node_data(nb).mark == False]
        # ic(valid_nbs)
        for nb in valid_nbs: #3.2
            data = self.get_node_data(nb)
            data.update_visited()
        
        G_chord_analysis = self.get_chord_analysis_graph()
        for node in valid_nbs + [node_index]: # 3.3
            self.check_and_update_chords(G_chord_analysis, node)
    
    def get_chord_analysis_graph(self, ):
        G_diff = self.get_unmarked_graph()
        G_ext = self.get_exterior_graph(G_diff)
        return G_ext
    
    def check_and_update_chords(self, G_chord_analysis, node_index):
        if node_index in G_chord_analysis.nodes:
            nbs = [nb for nb in G_chord_analysis.neighbors(node_index)]
            if len(nbs) > 2:
                num_chords = len(nbs) - 2
                ic(f"updating chords for {node_index} to {num_chords}")
                self.get_node_data(node_index).update_chords(num_chords)


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
        b = BoundaryCycle(temp_graph_data, CONVEX_APPROACH=True)
        exterior_nodes = b.ccw_boundary_cycle
        G_ext = nx.subgraph(self.G, exterior_nodes)        
        return G_ext
       

    def get_node_data(self, node_index):
        data:NodeCanonicalOrder = self.G.nodes[node_index]["data"]
        return data
    

    def split_graph_by_ordered(k):
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


    