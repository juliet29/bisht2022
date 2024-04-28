from enum import Enum


class EdgeColorings(Enum):
    LEFT_BLUE = 0 # Blue 
    RIGHT_RED = 1 # Red


class EdgeLabeling:
    def __init__(self, color) -> None:
        self.color = EdgeColorings(color)

        # print(self.corner_node_dict)

    def __repr__(self):
        return f"EdgeLabeling{self.__dict__})"
    
    def set_edge_color(self, index):
        self.color = EdgeColorings(index)
