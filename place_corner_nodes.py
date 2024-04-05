from helpers import *

from shapely import LineString, Point


class LocateCornerNodes:
    def __init__(self, GraphData: GraphData, path:list) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.path = path