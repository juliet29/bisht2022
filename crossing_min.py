from helpers import *
from boundary_cycle import BoundaryCycle
# from matplotlib.patches import FancyArrowPatch, ConnectionStyle

class CrossingMin:
    def __init__(self, GraphData: GraphData, pre_four_complete_shape:sp.LineString, buffer_size:float = 0.5) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.buffer_size = buffer_size

        self.pre_four_complete_shape = sp.Polygon(pre_four_complete_shape)

        self.index = 0

    def run(self):
        self.find_crossing_edges()

         # TODO will need to loop through.. 
        
        for i in range(len(self.crossing_edges)):
            self.find_extrema_near_crossinge_edge()
            self.create_guiding_circle()
            self.create_new_boundary()
            self.update_graph_edge()
            self.index+=1
        

    def find_crossing_edges(self):
        self.crossing_edges = [] 
        self.crossing_lines = []
        for e in list(self.G.edges):
            u, v = get_emedding_coords(self.embed, e)
            line = sp.LineString((list(u), list(v)))
            if line.crosses(self.pre_four_complete_shape):
                self.crossing_edges.append(e)
                self.crossing_lines.append(line)


    def find_extrema_near_crossinge_edge(self):
        self.curr_line = self.crossing_lines[self.index]

        extrema = [sp.Point(c) for c in self.pre_four_complete_shape.convex_hull.boundary.coords] #

        # TODO could make this simpler with argmin 
        min_distance = 1000
        self.guiding_circle_center  = sp.Point()
        for e in extrema:
            if e.dwithin(self.curr_line.centroid, min_distance):
                min_distance = e.distance(self.curr_line.centroid)
                self.guiding_circle_center = e


    def create_guiding_circle(self):
        distances = [sp.Point(p).distance(self.guiding_circle_center) for p in self.curr_line.coords]
        self.radius = min(distances)
        self.guiding_circle = create_circle(self.guiding_circle_center.x, self.guiding_circle_center.y, self.radius)

    def create_new_boundary(self):
        _, _, rad0 = self.calculate_node_radians(0)
        _, _, rad1 = self.calculate_node_radians(1)
        ic(self.guiding_circle_center)

        self.new_boundary = create_circle(self.guiding_circle_center.x, self.guiding_circle_center.y, self.radius, theta_start=rad0, theta_end=rad1, closed=False)

    def update_graph_edge(self):
        curr_edge = self.crossing_edges[self.index]
        self.G.edges[curr_edge]["curved_edge_data"] = self.new_boundary


    def calculate_node_radians(self, edge_node_ix):
        # each edge has two things.. 
        pt = sp.get_geometry(self.curr_line.boundary, edge_node_ix)
        dist_along = self.guiding_circle.line_locate_point(pt)
        pt_on_circle = self.guiding_circle.line_interpolate_point(dist_along) # TODO this is a behavior that is repeated with buffer, so should make a function .. 

        # adjust poistion in graph embedding 
        curr_node = self.crossing_edges[self.index][edge_node_ix]
        self.embed[curr_node] = np.array((pt_on_circle.x, pt_on_circle.y))

        x, y = self.adjust_point_relative_to_origin(pt_on_circle)

        radians = math.atan((y/x))
        # ic(radians)
        # ic(math.degrees(radians))

        # Ensure the angle is in [0, 2π]
        if radians < 0:
                radians += 2 * math.pi  

        ic(math.degrees(radians))

        return pt, pt_on_circle, radians
    


    def adjust_point_relative_to_origin(self, point):
        x1,y1 = self.move_guiding_circle_to_origin()
        ls = sp.LineString((self.guiding_circle_center, point))
        ls2 = sp.transform(ls, lambda x: x + [x1, y1] )
        new_pt = None
        for c in ls2.coords:
            if c[0] != 0 and c[1] != 0:
                new_pt = c

        assert new_pt
        d1 = euclidean_distance(new_pt, (0,0))
        d2 = euclidean_distance((self.guiding_circle_center.x, self.guiding_circle_center.y), (point.x, point.y))

        assert d1 == d2

        return new_pt
    

    def move_guiding_circle_to_origin(self):
        x = self.guiding_circle_center.x * -1
        y =  self.guiding_circle_center.y * -1
        return x, y

                

def create_circle(h, k, r, num_points=10, theta_start=0.0, theta_end=2*math.pi, closed=True):
    # TODO => can put (h,k,r) into own class.. 

    # Generate values for theta within the specified range
    theta = np.linspace(theta_start, theta_end, num_points)

    # Calculate corresponding x and y values using parametric equations
    x_coords = h + r * np.cos(theta)
    y_coords = k + r * np.sin(theta)

    coords = [(x,y) for x,y in zip(x_coords, y_coords) ]

    if closed:
        circle = sp.LinearRing(coords)
    else:
        circle = sp.LineString(coords)

    return circle
    



        
        