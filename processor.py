from helpers import *
from augment import *
from separating_tri import *
from boundaries import *


class Processor:
    def __init__(self, G) -> None:
        self.G_init = G
        self.G = self.G_init.copy()
        pass

    def augment(self):
        self.a = Augment(self.G)
        self.G = self.a.run_augment()
        self.embed = nx.planar_layout(self.G)

    def fix_separating_triangles(self):
        self.b = Boundaries(self.G, self.embed)
        self.s = FixSeparatingTriangles(self.G, self.embed, self.b.boundary_edges)
        
        G = self.s.run_st()
        
        self.G = G
        self.embed = self.s.embed

        # TODO put back on top .. 
        self.s.seperating_triangle_check()


    
