from helpers import *

import shapely as sp
import copy 

import traceback


class BoundaryCycle:
    """Gives cycle of a given boundary in clockwise order"""

    def __init__(self, GraphData: GraphData, CONVEX_APPROACH=False) -> None:
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.boundary_line_string = None
        self.convex_approach = CONVEX_APPROACH

        self.run()

    def run(self, ):
        if not self.convex_approach:
            try:
                self.generate_geometry_from_graph()
                self.get_geometry_boundary()
                self.get_cycle()
            except Exception as e: 
                ic("issue when running b cycle")
                traceback.print_exc(e)
        else:
            self.get_convex_hull_boundary()
            self.get_cycle()
            pass
    

    def get_cycle(self):
        assert self.boundary_line_string
        self.get_graph_boundary_cycle()
        self.get_ccw_cycle()

    def generate_geometry_from_graph(self):
        self.inner_faces = {}
        for ix, c in enumerate(nx.simple_cycles(G=self.G, length_bound=3)):
            self.inner_faces[ix] = {
                "cycle": c,
                "shape": sp.LinearRing(get_emedding_coords(self.embed, c)),
            }

    def get_geometry_boundary(self):
        complete_faces = sp.MultiPolygon(
            [sp.Polygon(i["shape"]) for i in self.inner_faces.values()]
        )
        self.boundary_line_string = sp.unary_union(complete_faces).boundary

    def get_convex_hull_boundary(self):
        points = sp.MultiPoint([sp.Point(i) for i in get_emedding_coords(self.embed, self.G.nodes)])
        self.boundary_line_string = points.convex_hull.boundary
        

    def get_graph_boundary_cycle(self):
        coords = [i for i in self.boundary_line_string.coords]

        self.boundary_cycle = []
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
