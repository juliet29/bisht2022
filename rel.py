from helpers import *

class RegularEdgeLabeling:
    def __init__(self, GraphData:GraphData) -> None:
        self.G = GraphData.graph
        self.embed = GraphData.embed
        self.corner_node_data = GraphData.corner_node_data