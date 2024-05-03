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
        self.run()

    def run(self):
        self.get_shortcuts()
        self.get_cips()
        self.arrange_cips()

    # helpers

    def get_boundary(self):
        if not self.boundary:
            g = BoundaryCycle(self.data)
            self.boundary = g.ccw_boundary_cycle

    def path_in_boundary_cylce(self, path):
        path_edges = {(path[i], path[i + 1]) for i in range(len(path) - 1)}

        froze_path, froze_cycle = freeze_list_of_tuples(
            path_edges, self.boundary_cycle_edges
        )

        return froze_path.issubset(froze_cycle)

    def path_interior_is_not_shortcut(self, path):
        shortcut_nodes = {number for tuple in self.shortcuts for number in tuple}
        path_interior = path[1:-1]
        for p in path_interior:
            if p in shortcut_nodes:
                return False
        return True

    # action

    def get_shortcuts(self):
        if not self.boundary:
            self.get_boundary()

        # get all edges involving 2 nodes on the boundary
        self.subgraph = self.G.subgraph(self.boundary)

        # get edges in boundary cycle..
        boundary_cycle_graph = nx.cycle_graph(self.boundary)
        self.boundary_cycle_edges = boundary_cycle_graph.edges()

        # compare to find shortcuts
        a, b = freeze_list_of_tuples(self.boundary_cycle_edges, self.subgraph.edges)
        difference = b - a

        self.shortcuts = [tuple(i) for i in difference]

    def get_cips(self):
        # bisht -> reqs for corner implying path
        self.cips = []

        for shortcut in self.shortcuts:
            # u1, un must be a shortcut
            for path in nx.all_simple_paths(self.subgraph, shortcut[0], shortcut[1]):
                # has to be on outer boundary
                if self.path_in_boundary_cylce(path):
                    # intervening nodes must not be endpoints in any shortcut
                    if self.path_interior_is_not_shortcut(path):
                        self.cips.append(path)

    def arrange_cips(self):
        comp = [self.boundary[-1]] + self.boundary # TODO this is a hack!! ideally would have something fully circular 
        self.arranged_cips = []
        for cip in self.cips:
            self.arranged_cips.append(sorted(cip, key=lambda x: comp.index(x)))
