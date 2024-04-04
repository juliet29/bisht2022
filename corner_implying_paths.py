from helpers import *
from boundary_cycle import *

from itertools import cycle
import random 


class CornerImplyingPaths:
    "discussed in Bisht, also Sahner and Bhaski?"
    def __init__(self, GraphData: GraphData) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.boundary = None
        

    def get_boundary(self):
        if not self.boundary:
            g = BoundaryCycle(self.data)
            self.boundary = g.ccw_boundary_cycle


    def get_shortcuts(self):
        if not self.boundary:
            self.get_boundary()
        ic(self.boundary)
        
        # get all edges involving 2 nodes on the boundary 
        subgraph = self.G.subgraph(self.boundary)

        # get edges in boundary cycle.. 
        boundary_cycle_graph = nx.cycle_graph(self.boundary)
        boundary_cycle_edges = boundary_cycle_graph.edges()

        # compare to find shortcuts 
        cycle_edges_frozen = {frozenset(t) for t in boundary_cycle_edges}
        subgraph_edges_frozen = {frozenset(t) for t in subgraph.edges}

        difference = subgraph_edges_frozen - cycle_edges_frozen

        self.shortcuts = {tuple(fs) for fs in difference}

        