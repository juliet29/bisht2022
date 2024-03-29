from helpers import *
from augment import *
from separating_tri import *
from boundaries import *
from canonical_order import *
from rel import *


class Processor:
    def __init__(self, G) -> None:
        self.G_init = G
        self.G = self.G_init.copy()
        self.embed = nx.planar_layout(self.G)

        pass

    def augment(self):
        self.a = Augment(self.G)
        self.G = self.a.run_augment()
        self.embed = nx.planar_layout(self.G)
        # TODO check if no change to embedding here because just adding edges.. bc doesnt seem to be the case..

    def fix_separating_triangles(self):
        self.b_st = Boundaries(self.G, self.embed)
        self.s = SeparatingTriangles(self.G, self.embed, self.b_st.boundary_edges)

        self.G = self.s.run_st()
        self.embed = self.s.embed

    def fix_cips_and_add_corner_nodes(self):
        self.b = Boundaries(self.G, self.embed)
        self.b.fix_cips_and_add_corner_nodes()
        # TODO clean this up!
        self.G = self.b.G
        self.embed = self.b.embed

        self.GraphData = GraphData(self.b.G, self.b.embed, self.b.corner_node_data)

    def set_canonical_order(self):
        self.c = CanonicalOrder(self.GraphData)
        self.c.run()
        self.GraphData.G = self.c.G
        self.GraphData.embed = self.c.embed

    def create_rel(self):
        self.r = RegularEdgeLabeling(self.GraphData)
        self.r.run()
        self.GraphData.rel = self.r.DG
    

    def run(self):
        self.augment()
        self.fix_separating_triangles()
        self.fix_cips_and_add_corner_nodes()
        self.set_canonical_order()
        self.create_rel()

    # def add_corner_nodes(self):

    #     self.b.organize_cips()
    #     self.b.distribute_corner_nodes()
    #     self.b.locate_corner_nodes()
    #     self.b.connect_corner_nodes()
    #     self.b.distinguish_corner_nodes()
    #     # TODO => should have clean thing that is like run_corner_nodes

    # self.b.assign_corner_node_pos()
    # self.b.four_connect()
