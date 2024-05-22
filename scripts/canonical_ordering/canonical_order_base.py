from helpers import nx, get_index_by_cardinal_direction, ic
from augment import *
import copy

from helpers_classes import GraphData, CardinalDirections

from four_complete_locations import *
from canonical_order_node import *

from boundary_cycle import *
from convex_boundary import ConvexBoundary
from canonical_order_checks import CanonicalOrderChecks

from graph_checks import NotTriangulatedError


class CanonicalOrderBaseClass:
    def __init__(self, GraphData:GraphData) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.corner_node_dict = GraphData.corner_node_dict
        
        self.ordered_nodes = []
        self.unordered_nodes = list(self.G.nodes)
        self.rel_helper = {}
        self.ordered_nbs = {}

        self.vk = len(self.G.nodes) - 1
# 
    
    def initialize_all_nodes(self):
        for node_index in self.G.nodes:
            self.G.nodes[node_index]["data"] = NodeCanonicalOrder(index=node_index)

    

    def update_starting_nodes(self):
        # order nodes south and west 
        self.order_start_node(CardinalDirections.WEST, 0)
        self.order_start_node(CardinalDirections.SOUTH, 1)

        # prepare north node 
        node_index = get_index_by_cardinal_direction(CardinalDirections.NORTH, self.corner_node_dict) 
        self.G.nodes[node_index]["data"].visited = 2

    def order_start_node(self, direction:CardinalDirections, order):
        node_index = get_index_by_cardinal_direction(direction, self.corner_node_dict) 
        self.G.nodes[node_index]["data"].order = order 
        self.update_ordered_nbs(node_index, order)


    def update_node(self, node_index):
        data = self.get_node_data(node_index)
        data.update_mark()
        data.add_node_to_order(self.vk)
        self.update_ordered_nbs(node_index, self.vk)

    def update_ordered_nbs(self, node_index, order):
        nbs = [nb for nb in self.G.neighbors(node_index)]
        self.ordered_nbs[order] = (node_index, nbs)
        pass

    def get_last_2_ordered(self):
        return (list(self.ordered_nbs.keys())[-1], list(self.ordered_nbs.keys())[-2])

    def get_nbs_of_last_2_ordered_nodes(self):
        last_order, second_to_last_order = self.get_last_2_ordered()
        ic(last_order, second_to_last_order)
        self.nbs_of_last_2_ordered = list(set(self.ordered_nbs[last_order][1]).intersection(set(self.ordered_nbs[second_to_last_order][1])))
        ic(self.nbs_of_last_2_ordered)

    


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
        

    def rearrange_unordered_nodes(self):
        for n in self.nbs_of_last_2_ordered:
            if n in self.unordered_nodes:
                self.unordered_nodes.remove(n)
                self.unordered_nodes.insert(0, n)

    def check_conditions(self):
        self.coc = CanonicalOrderChecks(self)
        self.coc.check_conditions()


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



    def update_rel_helper(self):
        self.rel_helper[self.vk] = {"unordered_boundary": self.unordered_cycle , "ordered_boundary": self.ordered_cycle}


    def get_node_data(self, node_index):
        data:NodeCanonicalOrder = self.G.nodes[node_index]["data"]
        return data
    
    