from helpers import *


## NOTE: keeping this seperate from augment.py class, bc could possibly want to get boundary at anyy stage of the augmentation, but could put togetehr later ..


class Boundaries:
    def __init__(self, G, embed) -> None:
        self.G = G
        self.embed = embed
        self.find_boundary_points()
        self.find_boundary_edges()
        # self.embed = nx.planar_layout(self.G)  # dictionary with node locations

    def find_boundary_points(self):
        embed_arr = np.array([self.embed[key] for key in sorted(self.embed.keys())])
        indices = np.arange(len(embed_arr))

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
        self.boundary_nodes = known_boundary_ix 
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

        self.boundary_edges = true_b_edge
        self.shortcuts = list(set(potential_b_edge) - set(true_b_edge))


    def find_cips(self):
        # corner implying paths: len > 3, 
        self.cips = []
        self.boundary_graph = nx.subgraph(self.G, self.boundary_nodes)
        shortcut_ends = np.unique(self.shortcuts)

        for shortcut in self.shortcuts:
            for path in nx.all_simple_paths(self.boundary_graph, shortcut[0], shortcut[1]):
                if not set(shortcut_ends).intersection(path[1:-1]) and len(path) >=3:
                    self.cips.append(path)

        assert len(self.cips) <= 4, "More than 4 corner implying paths"


    def organize_cips(self):
        n_cips = total_length(self.cips)
        self.boundary_cycles = []
        for c in nx.simple_cycles(G=self.boundary_graph, length_bound=n_cips+1):
            if len(c) >= n_cips+1:
                self.boundary_cycles.append(c)

        # TODO there should only be one cycle that is as long is the length of the cips but havent verified this ...
        self.boundary_cycles = self.boundary_cycles[0]

        # leave only the bounary items that match up with the cips 
        cip_nodes = [item for sublist in self.cips for item in sublist]
        diff = (list(set(self.boundary_cycles).difference(set(cip_nodes))))
        for d in diff:
            self.boundary_cycles.remove(d)



    def distribute_boundary_nodes(self):
        wrap_list = self.boundary_cycles #+ [self.boundary_cycles[0]]
        num_connect = 4 #ewsn
        j = (len(self.boundary_cycles) // (num_connect -1)) + 1
        
        end_indices = [j*(i+1) - i for i in range(num_connect )]
        ic(end_indices)
        self.four_con = {}
        for ix, end_index in enumerate(end_indices):
            self.four_con[ix] = wrap_list[end_index-j:end_index]
            
        if len(self.four_con[3]) < 2: # TODO change to be in terms of num_connect 
            self.four_con[3] = [self.boundary_cycles[-1], self.boundary_cycles[0]]

        return self.four_con
    
    def four_connect(self):
        # TODO treatment for when n verts < 4 
        pass
        # create nodes and position them 
        # s < y_min, and centered in x (need hull points)
        # n > y_max 
        # e < x_min and centered in y 
        # w > x_max 
        




