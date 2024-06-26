from helpers import np, get_index_by_cardinal_direction
import copy
from helpers_classes import CornerNode, CardinalDirections, GraphData
import math


# from four_complete_coordinates import *
from four_complete_buffer import *


class FourCompleteLocations:
    def __init__(
        self, GraphData: GraphData, boundary: list, paths: list, boundary_shape
    ) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.boundary = boundary
        self.boundary_shape = boundary_shape
        self.paths = paths

        self.corner_node_list = []

    def run(self):
        self.get_corner_node_coordinates()
        self.assign_cardinal_directions()
        self.embed_corner_nodes()

    def get_corner_node_coordinates(self):
        for ix, p in enumerate(self.paths):
            l = FourCompleteBuffer(self.data, p, self.boundary_shape)
            self.corner_node_list.append(
                CornerNode(
                    location=l.corner_node_location,
                    index=len(self.G.nodes) + ix,
                    neighbour_indices=p,
                )
            )

    def assign_cardinal_directions(self):
        coords = [c.location for c in self.corner_node_list]
        cw = clockwise_order(coords)
        order = [coords.index(i) for i in cw]
        for o, direction in zip(order, CardinalDirections):
            ix = self.corner_node_list[o].index
            ic(o, direction, ix)
            self.corner_node_list[o].name = direction

    def embed_corner_nodes(self):
        for v in self.corner_node_list:
            # update graph edges
            new_edges = []
            for node in v.neighbour_indices:
                new_edges.append((v.index, node))
                self.G.add_edges_from(new_edges)

            # update the embedding
            self.embed[v.index] = np.array(v.location)
        self.G_unconnected_corner_nodes = copy.deepcopy(self.G)

    def connect_outer_nodes(self):
        self.corner_node_dict = {
            k: v for k, v in zip(list(range(4)), self.corner_node_list)
        }
        self.data.corner_node_dict = self.corner_node_dict
        # TODO move to own four connect class?
        ix = self.local_get_index_by_cardinal_direction  # create alias
        edges = [
            (ix(CardinalDirections.SOUTH), ix(CardinalDirections.EAST)),
            (ix(CardinalDirections.EAST), ix(CardinalDirections.NORTH)),
            (ix(CardinalDirections.NORTH), ix(CardinalDirections.WEST)),
            (ix(CardinalDirections.WEST), ix(CardinalDirections.SOUTH)),
            (ix(CardinalDirections.SOUTH), ix(CardinalDirections.NORTH)),
        ]
        self.G.add_edges_from(edges)


    def remove_south_north_connection(self):
        n1 = self.local_get_index_by_cardinal_direction(CardinalDirections.SOUTH)
        n2 = self.local_get_index_by_cardinal_direction(CardinalDirections.NORTH)
        self.G.remove_edge(n1, n2)

    def add_south_north_connection(self):
        n1 = self.local_get_index_by_cardinal_direction(CardinalDirections.SOUTH)
        n2 = self.local_get_index_by_cardinal_direction(CardinalDirections.NORTH)
        self.G.add_edge(n1, n2)

    def local_get_index_by_cardinal_direction(self, key):
        return get_index_by_cardinal_direction(key, self.corner_node_dict)
            



#MARK: helpers
def clockwise_order(coordinates):
    # Calculate the centroid of the coordinates
    centroid_x = sum(x for x, y in coordinates) / len(coordinates)
    centroid_y = sum(y for x, y in coordinates) / len(coordinates)
    centroid = Point(centroid_x, centroid_y)

    # Calculate the angle between each coordinate and the centroid
    angles = [
        (math.atan2(y - centroid.y, x - centroid.x), x, y) for x, y in coordinates
    ]

    # Sort the coordinates based on the angles
    sorted_coordinates = sorted(angles)

    # Extract the sorted coordinates without the angles
    clockwise_ordered_coordinates = [(x, y) for angle, x, y in sorted_coordinates]

    return clockwise_ordered_coordinates
