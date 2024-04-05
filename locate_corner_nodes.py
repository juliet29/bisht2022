from helpers import *

from shapely import LineString, Point


class LocateCornerNodes:
    def __init__(self, GraphData: GraphData, path:list) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.path = path

        self.create_corner_node_location()

    #MARK: action begins 
    def create_corner_node_location(self):
        self.get_slopes()
        self.choose_best_slope()
        self.choose_best_midpoint()
        self.define_corner_node_axis()
        self.corner_node_location = self.orthog_line.centroid


    # TODO reverse ordering of subsequent functions since there is only one calling fx
    def define_corner_node_axis(self):
        self.orthog_line = line_from_point_and_slope(self.midpoint, orthogonal_slope(self.most_freq_slope))

    def choose_best_midpoint(self):
        valid_slope_ix = np.where(self.slopes == self.most_freq_slope)[0]
        
        line = LineString(((0,0), (0,0)))

        for ix in valid_slope_ix:
            u, v = self.nodes[ix]
            u_coord = self.boundary_embed[u]
            v_coord = self.boundary_embed[v]
            
            l = LineString((u_coord, v_coord))
            if l.length > line.length:
                line = l

        self.midpoint = line.centroid

        ic(line.length)

    def choose_best_slope(self):
        # if no slopes are most freq, just get the first 
        if len(np.unique(self.slopes)) == 1:
            ic("all same")
        else:
            unique_floats, frequencies = np.unique(self.slopes, return_counts=True)

            most_freq_index = np.argmax(frequencies)
            self.most_freq_slope = self.slopes[most_freq_index]
            # get index of max 
            ic(most_freq_index, self.most_freq_slope)
 

    def get_slopes(self):
        self.boundary_embed = get_dict_subset(self.data.embed, self.path)
        embed_vals = [tuple(v) for v in self.boundary_embed.values()]
        embed_keys = [k for k in self.boundary_embed.keys()]

        self.slopes = []
        self.nodes = []

        for val, key in zip(embed_vals[1:], embed_keys[1:]):
            slope, b = find_line_through_points((embed_vals[0], val))
            ic((embed_keys[0], key), slope)
            self.slopes.append(np.round(slope, decimals=9))
            self.nodes.append((embed_keys[0], key))

        self.slopes = np.array(self.slopes)





#MARK: helpers
def line_from_point_and_slope(point, slope, length=10):
    # Calculate the second point using the given point and slope
    x2 = point.x + length
    y2 = point.y + length * slope
    second_point = Point(x2, y2)
    
    # Create a LineString from the two points
    line = LineString([point, second_point])
    return line

def orthogonal_slope(slope):
    return -1/slope


        