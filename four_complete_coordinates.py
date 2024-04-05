from helpers import *

from shapely import LineString, Point, Polygon


class FourCompleteCoordinates:
    def __init__(self, GraphData: GraphData, path: list, boundary_shape, distance:float = 0.5) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed

        self.path = path
        self.boundary_shape = Polygon(boundary_shape)

        self.distance = distance

        self.create_corner_node_location()

    # MARK: action begins
    def create_corner_node_location(self):
        self.get_slopes()
        self.choose_best_slope()
        self.choose_best_midpoint()
        self.define_corner_node_axis()
        


    def get_slopes(self):
        self.boundary_embed = get_dict_subset(self.data.embed, self.path)
        embed_vals = [tuple(v) for v in self.boundary_embed.values()]
        embed_keys = [k for k in self.boundary_embed.keys()]

        self.slopes = []
        self.nodes = []

        for val, key in zip(embed_vals[1:], embed_keys[1:]):
            slope, b = find_line_through_points((embed_vals[0], val))
            self.slopes.append(np.round(slope, decimals=9))
            self.nodes.append((embed_keys[0], key))
        self.slopes = np.array(self.slopes)


    def choose_best_slope(self):
        # if no slopes are most freq, just get the first
        if len(np.unique(self.slopes)) == 1:
            self.most_freq_slope = self.slopes[0]
        else:
            _, frequencies = np.unique(self.slopes, return_counts=True)

            most_freq_index = np.argmax(frequencies)
            self.most_freq_slope = self.slopes[most_freq_index]

            assert(self.most_freq_slope), f"most freq index was {most_freq_index}"

        
    def choose_best_midpoint(self):
        # may have multiple lines with same slope, get midpoint of longest
        valid_slope_ix = np.where(self.slopes == self.most_freq_slope)[0]

        line = LineString(((0, 0), (0, 0)))

        for ix in valid_slope_ix:
            u, v = self.nodes[ix]
            u_coord = self.boundary_embed[u]
            v_coord = self.boundary_embed[v]

            l = LineString((u_coord, v_coord))
            if l.length > line.length:
                line = l

        self.midpoint = line.centroid

    def define_corner_node_axis(self):
        self.orthog_line = self.create_axis()

        # if end point is in line.. 
        if self.boundary_shape.contains(self.orthog_line.centroid):
            ic("flipped")
            self.orthog_line = self.create_axis(dir=-1)

        # if slope is 0, and the line is crossing, there could be a more optimal pairing 
        if self.boundary_shape.crosses(self.orthog_line) and self.most_freq_slope == 0:
            self.orthog_line = self.create_axis(dir=-1)



        self.corner_node_location = (self.orthog_line.centroid.x, self.orthog_line.centroid.y)
        

    def create_axis(self, dir=1):
        line = line_from_point_and_slope(
            self.midpoint, orthogonal_slope(self.most_freq_slope), dir*self.distance
        )
        return line



# MARK: helpers
def line_from_point_and_slope(point, slope, length=10):
    # Calculate the second point using the given point and slope
    x2 = point.x + length
    y2 = point.y + length * slope
    if slope != 0:
        second_point = Point(x2, y2)
    elif slope==0:
        ic("slope is 0")
        second_point = Point(x2, y2+length)
    else:
        raise Exception("vertical slope not implmented for four completion location")

    # Create a LineString from the two points
    line = LineString([point, second_point])
    return line


def orthogonal_slope(slope):
    if slope != 0:
        return -1 / slope
    elif slope == 0:
        return 0
    else:
        raise Exception("vertical slope not implmented for four completion location")
