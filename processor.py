from helpers import *
from augment import *
from separating_tri import *
from boundaries import *


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

    def fix_cips(self):
        self.b = Boundaries(self.G, self.embed)
        self.b.find_cips()
        # right now does not modify the graph 
        # TODO fix if > than 4 cips

    def add_corner_nodes(self):
        
        self.b.organize_cips()
        self.b.distribute_corner_nodes()
        self.b.locate_corner_nodes()
        self.b.connect_corner_nodes()
        self.b.distinguish_corner_nodes()
        # TODO => should have clean thing that is like run_corner_nodes 
        

        # self.b.assign_corner_node_pos()
        # self.b.four_connect()
