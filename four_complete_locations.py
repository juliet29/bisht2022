from helpers import *

from four_complete_coordinates import *


class FourCompleteLocations:
    def __init__(self, GraphData: GraphData, boundary:list, paths:list, boundary_shape) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.boundary = boundary
        self.boundary_shape = boundary_shape
        self.paths  = paths

        self.corner_node_data = []

    def run(self):
        self.get_corner_node_coordinates()
        self.assign_cardinal_directions()
        self.embed_corner_nodes()


    def get_corner_node_coordinates(self):
        for ix, p in enumerate(self.paths):
            l = FourCompleteCoordinates(self.data, p, self.boundary_shape)
            self.corner_node_data.append(CornerNode(
                location=l.corner_node_location,
                index = len(self.G.nodes) + ix,
                neighbour_indices = p 
                ))

    def assign_cardinal_directions(self):
        coords = [i.location for i in self.corner_node_data]
        directions = assign_directions(coords)
        for k,v in directions.items():
            ix = coords.index(v)
            self.corner_node_data[ix].name = k


    def embed_corner_nodes(self):
        for v in self.corner_node_data:
            # update graph edges
            new_edges = []
            for node in v.neighbour_indices:
                new_edges.append((v.index, node))
                self.G.add_edges_from(new_edges)
        
            # update the embedding 
            self.embed[v.index] = np.array(v.location)


    def connect_outer_nodes(self):
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
        dict_key = get_key_by_value(self.corner_node_data, key, object=True)
        return self.corner_node_data[dict_key].index