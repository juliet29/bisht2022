from helpers import *


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
        coords = [i.location for i in self.corner_node_list]
        directions = assign_directions(coords)
        for k, v in directions.items():
            ix = coords.index(v)
            self.corner_node_list[ix].name = k

    def embed_corner_nodes(self):
        for v in self.corner_node_list:
            # update graph edges
            new_edges = []
            for node in v.neighbour_indices:
                new_edges.append((v.index, node))
                self.G.add_edges_from(new_edges)

            # update the embedding
            self.embed[v.index] = np.array(v.location)

    def connect_outer_nodes(self):
        self.corner_node_dict = {
            k: v for k, v in zip(list(range(4)), self.corner_node_list)
        }
        self.data.corner_node_dict = self.corner_node_dict
        # TODO move to own four connect class?
        ix = self.get_node_index  # create alias
        edges = [
            (ix("south"), ix("east")),
            (ix("east"), ix("north")),
            (ix("north"), ix("west")),
            (ix("west"), ix("south")),
            (ix("south"), ix("north")),
        ]
        self.G.add_edges_from(edges)

    def get_node_index(self, key):
        dict_key = get_key_by_value(self.corner_node_dict, key, object=True)
        return self.corner_node_dict[dict_key].index
