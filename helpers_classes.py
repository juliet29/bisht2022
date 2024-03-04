# simple classes
class SeperatingTriangle:
    def __init__(self, cycle: list, inner_node: int) -> None:
        self.cycle = cycle
        self.inner_node = inner_node
        self.target_edge: tuple = None

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
        interior_nodes: list[int] = None,
        name: str = None,
        node: int = None,
        location: tuple = None,
        mean_location: tuple = None,
    ) -> None:
        self.interior_nodes = interior_nodes
        self.name = name
        self.node = node
        self.location = location
        self.mean_location = mean_location

    def __repr__(self):
        return f"CornerNode({self.__dict__})"
