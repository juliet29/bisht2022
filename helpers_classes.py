import networkx as nx


# simple classes
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
        self, G:nx.Graph, embed:dict, corner_node_data:dict = None, rel:nx.Graph = None
    ) -> None:
        self.G = G
        self.embed = embed
        self.corner_node_data = corner_node_data
        self.rel = rel

    def __repr__(self):
        return f"GraphData{self.__dict__})"
