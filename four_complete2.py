from helpers import *
from boundary_cycle import *

from itertools import cycle
import random 


class FourComplete2:
    """ Approach here is loosely taken from Kant and He '97 and '93 """
    def __init__(self, GraphData: GraphData) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed

        # action begins 
    def get_boundary_cyle(self):
        b = BoundaryCycle(self.data)
        b.run()
        self.boundary = b.ccw_boundary_cycle
        