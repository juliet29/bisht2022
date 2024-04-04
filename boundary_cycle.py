from helpers import *

import shapely as sp
import copy 


class BoundaryCycle:
    """Gives cycle of a given boundary in clockwise order"""

    def __init__(self, GraphData: GraphData) -> None:
        self.G = GraphData.G
        self.embed = GraphData.embed

        self.run()

    def run(self):
        self.generate_geometry_from_graph()
        self.get_geometry_boundary()
        self.get_graph_boundary_cycle()
        self.get_ccw_cycle()

    def get_emedding_coords(self, embed, arr):
        return [embed[i] for i in arr]

    def generate_geometry_from_graph(self):
        self.inner_faces = {}
        for ix, c in enumerate(nx.simple_cycles(G=self.G, length_bound=3)):
            self.inner_faces[ix] = {
                "cycle": c,
                "shape": sp.LinearRing(self.get_emedding_coords(self.embed, c)),
            }

    def get_geometry_boundary(self):
        complete_faces = sp.MultiPolygon(
            [sp.Polygon(i["shape"]) for i in self.inner_faces.values()]
        )
        self.boundary_line_string = sp.unary_union(complete_faces).boundary

    def get_graph_boundary_cycle(self):
        self.boundary_cycle = []
        coords = [i for i in self.boundary_line_string.coords]
        for coord in coords:
            distances = [
                euclidean_distance(coord, self.embed[key]) for key in self.embed
            ]
            closest_key = np.argmin(distances)
            self.boundary_cycle.append(closest_key)

    def get_ccw_cycle(self):
        temp = copy.copy(self.boundary_cycle)
        temp.reverse()

        self.ccw_boundary_cycle = temp[:-1]
