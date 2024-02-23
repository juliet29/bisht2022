import networkx as nx
from icecream import ic
from helpers import *
from augment import *

class REL:
    def __init__(self, G) -> None:
        self.G_start = G

    def augment(self):
        a = Augment(self.G_start)
        a.run_augment(DEBUG=True)
        self.G = a.G_final
        return self.G




