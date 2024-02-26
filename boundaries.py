from helpers import *

## NOTE: keeping this seperate from augment.py class, bc could possibly want to get boundary at anyy stage of the augmentation, but could put togetehr later ..


class Boundaries:
    def __init__(self, G) -> None:
        self.G = G
        pass

    def find_boundary_points(self):

        # find planar embedding -> for network x, this will arrange points in triangular fashion
        self.embed = nx.planar_layout(self.G) # dictionary with node locations 
        embed_arr = np.array([self.embed[key] for key in sorted(self.embed.keys())])
        indices = np.arange(len(embed_arr))

        # find convex hull
        hull = ConvexHull(embed_arr)

        known_boundary_ix = np.unique(hull.simplices)
        test_ix = set(indices) - set(known_boundary_ix)

        hull_pairs = extract_convex_points(embed_arr, hull)

        self.hull_lines = [] 
        for pair in hull_pairs:
            l = find_line_through_points(pair)
            self.hull_lines.append(l)
            # check if point on line.
            for ix in test_ix:
                if check_point_on_line(l, embed_arr[ix]):
                    # ic("point!", ix)
                    known_boundary_ix = np.append(known_boundary_ix, ix)
                    # ic(known_boundary_ix)
                    test_ix = set(indices) - set(known_boundary_ix)

        self.boundary_locations = embed_arr[known_boundary_ix]
        self.boundary_nodes = [
            i + 1 for i in known_boundary_ix
        ]  # nodes are indexed  1, 2, ...
        return self.boundary_locations, self.boundary_nodes

    def find_boundary_edges(self):
        potential_b_edge = []
        for pair in self.G.edges:
            if pair[0] in self.boundary_nodes and pair[1] in self.boundary_nodes:
                potential_b_edge.append(pair)

        # check which edges are parallel with the lines that define the convex hull => same slope..
