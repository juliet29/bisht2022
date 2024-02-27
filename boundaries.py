from helpers import *

## NOTE: keeping this seperate from augment.py class, bc could possibly want to get boundary at anyy stage of the augmentation, but could put togetehr later ..


class Boundaries:
    def __init__(self, G) -> None:
        self.G = G
        self.embed = nx.planar_layout(self.G) # dictionary with node locations 
        pass

    def find_boundary_points(self):
        # todo split this up 
        # find planar embedding -> for network x, this will arrange points in triangular fashion
        
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
                    known_boundary_ix = np.append(known_boundary_ix, ix)
                    test_ix = set(indices) - set(known_boundary_ix)

        # nodes are named  1, 2, ...
        self.boundary_nodes = [i + 1 for i in known_boundary_ix]  
        return self.boundary_nodes

    def find_boundary_edges(self):
        potential_b_edge = []
        true_b_edge = []
        for pair in self.G.edges:
            u, v = pair
            if u in self.boundary_nodes and v in self.boundary_nodes:
                potential_b_edge.append(pair)
                # check which edges align w convex hull 
                slope, _ = find_line_through_points((self.embed[u], self.embed[v]))
                for hull_line in self.hull_lines:
                    if check_parallel(hull_line[0], slope):
                        true_b_edge.append(pair)
                        break
        self.shortcuts = list(set(potential_b_edge) - set(true_b_edge))

    def find_seperating_triangles(self):
        three_cyles = sorted(nx.simple_cycles(self.G, 3))
        sep_triangles = []
        for cycle in three_cyles:
            other_nodes = list(set(self.G.nodes) - set(cycle))
            coords = [self.embed[k] for k in cycle]
            domain = find_min_max_coordinates(coords)

            for node in other_nodes:
                if check_point_in_hull(domain, self.embed[node]):
                    sep_triangles.append(cycle)

        return sep_triangles
