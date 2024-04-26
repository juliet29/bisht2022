from helpers import *
from graph_checks import *
from itertools import cycle


class ConvexBoundary:
    """Gives cycle of a given boundary in clockwise order"""
    def __init__(self, GraphData: GraphData) -> None:
        self.G = GraphData.G
        self.embed = GraphData.embed

        self.run()

    def run(self):
        check_triangulated_interior(self.G)
        
        self.generate_triangulated_shapes()
        self.get_triangulation_boundary()
        self.get_points()
        self.get_exterior_nodes()
        self.get_exterior_cycle()
        self.get_exterior_cycle_edges()



    def generate_triangulated_shapes(self):
        self.inner_faces = {}
        for ix, c in enumerate(nx.simple_cycles(G=self.G, length_bound=3)):
            self.inner_faces[ix] = {
                "cycle": c,
                "shape": sp.LinearRing(get_emedding_coords(self.embed, c)),
            }

    def get_triangulation_boundary(self):
        complete_faces = sp.MultiPolygon(
            [sp.Polygon(i["shape"]) for i in self.inner_faces.values()]
        )
        self.boundary_shape = sp.Polygon(sp.unary_union(complete_faces).boundary)


    def get_points(self):
        self.points = sp.MultiPoint([sp.Point(i) for i in get_emedding_coords(self.embed, self.G.nodes)])
        self.points_list = [g for g in self.points.geoms]
        # self.boundary_shape = sp.Polygon(self.points.convex_hull.boundary)
        
    
    def get_exterior_nodes(self):
        self.ext_nodes = []
        for node_index, point in zip(self.G.nodes, self.points_list):
            if not self.boundary_shape.contains(point):
                self.ext_nodes.append(node_index)

    def get_exterior_cycle(self):
        self.G_ext = nx.subgraph(self.G, self.ext_nodes)
        cycles = [g for g in nx.simple_cycles(self.G_ext._graph) if len(g) == len(self.ext_nodes)]

        assert len(cycles) >= 1, "No cycles found with the correct length"

        self.cycle  = None
        for c in cycles:
            if self.check_ext_nodes_in_cycle(c):
                self.cycle = c
                break

        assert self.cycle, "True cycle was not found"

    def get_exterior_cycle_edges(self):
        cycled_cycle = cycle(self.cycle)
        self.cycle_edges = []
        for ix, pair in enumerate(pairwise(cycled_cycle)):
            self.cycle_edges.append(pair)
            if ix >= len(self.cycle) -1:
                break


    def check_ext_nodes_in_cycle(self, cycle):
        for n in self.ext_nodes:
            if n not in cycle:
                return
            # ic(cycles[2])
        return True

        # try:
        #     self.cycle_edges = nx.find_cycle(self.G_ext, self.ext_nodes[0])
        # except nx.NetworkXNoCycle:
        #     print (f"No cycle found from exterior nodes {self.ext_nodes}")
        #     return

        # self.cycle = [i[0] for i in self.cycle_edges]


    # def check_node_point_match(self):
    #     assert self.embed[0][0] == self.points_list[0].x and self.embed[0][1] == self.points_list[0].y