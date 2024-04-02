from helpers import *
from augment import *
from separating_tri import *
from boundaries import *
from canonical_order import *
from rel import *

from collections import OrderedDict
import copy


class Processor:
    def __init__(self, G) -> None:
        self.data = GraphData(G, nx.planar_layout(G))
        self.history = OrderedDict()
        self.history["init"] = copy.copy(self.data)

    def update_history(self):
        hist_name = get_calling_function_name()
        self.history[hist_name] = copy.deepcopy(self.data)

    def augment(self):
        self.a = Augment(self.data.G)
        self.data.G = self.a.run_augment()
        self.data.embed = nx.planar_layout(self.data.G) #TODO let the class handle this.. 
        self.update_history()


    def fix_separating_triangles(self):
        self.b_st = Boundaries(self.data.G, self.data.embed)
        # TODO clean this up ^ and below 
        self.s = SeparatingTriangles(self.data.G, self.data.embed, self.b_st.boundary_edges)

        self.data.G = self.s.run_st()
        self.data.embed = self.s.embed
        self.update_history()

    def fix_cips_and_add_corner_nodes(self):
        self.b = Boundaries(self.data.G, self.data.embed)
        self.b.fix_cips_and_add_corner_nodes()
        self.data.G = self.b.G
        self.data.embed = self.b.embed
        self.update_history()

        self.data = GraphData(self.b.G, self.b.embed, self.b.corner_node_data)

    def set_canonical_order(self):
        self.c = CanonicalOrder(self.data)
        self.c.run()
        self.data.G = self.c.G
        self.data.embed = self.c.embed
        self.update_history()

    def create_rel(self):
        self.r = RegularEdgeLabeling(self.data)
        self.r.run()
        self.data.rel = self.r.rel
        self.update_history()

    def run(self):
        self.augment()
        self.fix_separating_triangles()
        self.fix_cips_and_add_corner_nodes()
        # self.set_canonical_order()
        # self.create_rel()
