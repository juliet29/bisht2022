from helpers import *
from augment import *

from helpers_classes import *

from four_complete_locations import *
from canonical_order_node import *

from convex_boundary import *

# NOTE: canonical order is indexed 1,2,... while nodes are indexed 0,1,2, ... 

class CanonicalOrderChecks:
    def __init__(self, co) -> None:
        self.co = co

    def check_conditions(self):
        self.check_biconnected()
        self.check_nb_conditions()


    def check_biconnected(self):
        test_biconnect(self.co.G_unmarked)

    
    def check_nb_conditions(self):
        self.organize_nbs()
        self.check_sufficient_ordered_nbs()
        self.check_sufficient_unordered_nbs()
    
    def organize_nbs(self):
        nbs = [n for n in nx.neighbors(self.co.G, self.co.current_node_index)]

        self.ordered_nbs = []
        unordered_nbs = []
        for node in nbs:
            if node in self.co.ordered_nodes:
                self.ordered_nbs.append(node)
            else: 
                unordered_nbs.append(node)

        self.G_unordered_nb = nx.Graph(nx.subgraph(self.co.G, unordered_nbs))
    

    def check_sufficient_ordered_nbs(self):
        if self.co.vk < len(self.co.G.nodes) - 2:
            assert len(self.ordered_nbs) >= 2, "Not enough ordered nbs"

    def check_sufficient_unordered_nbs(self):
        # check nbs are in boundary of Gk_minus
        a, b = freeze_list_of_tuples(self.G_unordered_nb.edges, self.co.boundary_unmarked.cycle_edges)
        overlapping_edges = a.intersection(b)
        assert len(list(overlapping_edges)) == len(self.G_unordered_nb.edges), "Neighbours not in outer boundary"



    
    def get_order_of_nodes(self, node_list):
        labels = {}
        for node_index in node_list:
            labels[node_index] = [self.get_node_data(node_index).order]
        return labels
