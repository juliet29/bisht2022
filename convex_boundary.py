from helpers import *


class BoundaryCycle:
    """Gives cycle of a given boundary in clockwise order"""

    def __init__(self, GraphData: GraphData) -> None:
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.boundary_line_string = None

        self.run()

    def run(self):
        self.get_convex_boundary()
        self.get_exterior_nodes()
        self.get_exterior_cycle()


    def get_convex_boundary(self):
        # TODO assert that the graph is convex => either bi-connected or something else.. 
        points = sp.MultiPoint([sp.Point(i) for i in get_emedding_coords(self.embed, self.G.nodes)])
        self.points_list = [g for g in points.geoms]
        self.boundary_shape = sp.Polygon(points.convex_hull.boundary)
        
    
    def get_exterior_nodes(self):
        self.ext_nodes = []
        for ix, point in enumerate(self.points_list):
            if not self.boundary_shape.contains(point):
                self.check_node_point_match()
                self.ext_nodes.append(ix)

    def get_exterior_cycle(self):
        G_ext = nx.subgraph(self.G, self.ext_nodes)
        self.cycle_edges = nx.find_cycle(G_ext, self.ext_nodes[0])
        self.cycle = [i[0] for i in self.cycle]


    def check_node_point_match(self):
        assert self.embed[0][0] == self.points_list[0].x and self.embed[0][1] == self.points_list[0].y