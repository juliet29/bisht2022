import networkx as nx
from enum import Enum
from pprint import pprint
from shapely import Point

#MARK: getting graph info 
#TODO make augmented networkx classes.. 
def get_emedding_coords(embed, arr):
        return [embed[i] for i in arr]

def get_emedding_coords_as_tuple(embed, arr):
        return [tuple(embed[i]) for i in arr]


def get_emedding_coords_as_point(embed, arr):
        return [Point(tuple(embed[i])) for i in arr]


def show_graph_attributes(G:nx.Graph):
    for node, data in G.nodes.data():
        if data:
            pprint(f"Node {node}: {data}")

    for e1, e2, data in G.edges.data():
        if data:
            pprint(f"Edge {e1, e2}: {data}")
        

# --- 
class PointsList:
    def __init__(self, pair:tuple):
        self.x = pair[0]
        self.y = pair[1]
    
    def __repr__(self):
        return f"PointsList({self.__dict__})"


class CardinalDirections(Enum):
    SOUTH = 0
    WEST = 1
    NORTH = 2
    EAST = 3


class SeperatingTriangleData:
    def __init__(self, cycle: list, inner_node: int) -> None:
        self.cycle = cycle
        self.inner_node = inner_node
        self.target_edge: tuple = None

    # TODO RENAME THIS!!

    def __repr__(self):
        return f"SeperatingTriangle({self.__dict__})"


class Domain:
    def __init__(self, x_min: float, x_max: float, y_min: float, y_max: float) -> None:
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    # TODO break down futher into a coordinate class..

    def __repr__(self):
        return f"Domain({self.__dict__})"


class CornerNode:
    def __init__(
        self,
        neighbour_indices: list[int] = None,  # nodes that this is connected to
        name: str = None,
        index: int = None,
        location: tuple = None,
        mean_location: tuple = None,
    ) -> None:
        self.neighbour_indices = neighbour_indices
        self.name = name
        self.index = index
        self.location = location
        self.mean_location = mean_location

    def __repr__(self):
        return f"CornerNode({self.__dict__})"


class GraphData:
    def __init__(
        self,
        G: nx.Graph,
        embed: dict,
        corner_node_dict:dict = None,
        rel: nx.Graph = None,
        boundary: list = None,
    ) -> None:
        self.G = G
        self.embed = embed
        self.corner_node_dict = corner_node_dict
        self.rel = rel

        self.boundary: list = boundary

        # print(self.corner_node_dict)

    def __repr__(self):
        return f"GraphData{self.__dict__})"
    
    
    



