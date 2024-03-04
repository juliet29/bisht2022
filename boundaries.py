from helpers import *


## NOTE: keeping this seperate from augment.py class, bc could possibly want to get boundary at anyy stage of the augmentation, but could put togetehr later ..
# yes, earlier functions are more of a general graph utility class, while the later functions will only be used at one stage ... 03/04/24


class Boundaries:
    def __init__(self, G: nx.Graph, embed: dict) -> None:
        # TODO make this and FixSepTris extend a base class with these type hint
        self.G = G.copy()
        self.embed = embed.copy()
        self.find_boundary_points()
        self.find_boundary_edges()

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
            for path in nx.all_simple_paths(
                self.boundary_graph, shortcut[0], shortcut[1]
            ):
                if not set(shortcut_ends).intersection(path[1:-1]) and len(path) >= 3:
                    self.cips.append(path)

        assert len(self.cips) <= 4, "More than 4 corner implying paths"

    def organize_cips(self):
        n_cips = total_length(self.cips)
        self.boundary_cycles = []
        for c in nx.simple_cycles(G=self.boundary_graph, length_bound=n_cips + 1):
            if len(c) >= n_cips + 1:
                self.boundary_cycles.append(c)

        # TODO there should only be one cycle that is as long is the length of the cips but havent verified this ...
        self.boundary_cycles = self.boundary_cycles[0]

        # leave only the bounary items that match up with the cips
        cip_nodes = [item for sublist in self.cips for item in sublist]
        diff = list(set(self.boundary_cycles).difference(set(cip_nodes)))
        for d in diff:
            self.boundary_cycles.remove(d)
        # TODO need to make sure this is going one direction (CCW or CW)

    def distribute_corner_nodes(self):
        self.four_con = {k: CornerNode() for k in range(4)}

        # TODO clean up .. wrap list once verify that its working ..
        wrap_list = self.boundary_cycles  # + [self.boundary_cycles[0]]
        num_connect = 4  # east, west, south, north
        j = (len(self.boundary_cycles) // (num_connect - 1)) + 1

        end_indices = [j * (i + 1) - i for i in range(num_connect)]

        for ix, end_index in enumerate(end_indices):
            self.four_con[ix].interior_nodes = wrap_list[end_index - j : end_index]
            self.four_con[ix].node = len(self.G.nodes) + ix

        if len(self.four_con[num_connect - 1].interior_nodes) < 2:
            self.four_con[3].interior_nodes = [
                self.boundary_cycles[-1],
                self.boundary_cycles[0],
            ]

        return self.four_con
    

    # def assign_location(self, key):
    #     buffer = 1
    #     item = self.four_con[get_key_by_value(self.four_con, self.dir_data[key], object=True)]
    #     item.name = key
    #     item.location = find_point_along_vector(item.mean_location, key, buffer)

    #     return

    def locate_corner_nodes(self, buffer = 1):
        # get the central location of interior nodes for a given corner node
        for v in self.four_con.values():
            arr = np.array([self.embed[i] for i in v.interior_nodes])
            v.mean_location = (np.mean(arr[:, 0]), np.mean(arr[:, 1]))
    
        # determine whicch of these locations are most north, east etc
        coords = [v.mean_location for v in self.four_con.values()]
        self.direction_dict = assign_directions(coords)
         
        for k, v in self.direction_dict.items():
            # match items in four_con dictionary to the direction dict
            item = self.four_con[get_key_by_value(self.four_con, self.direction_dict[k], object=True)]
            item.name = k
            # assign location with approp direction 
            item.location = find_point_along_vector(item.mean_location, k, buffer)
            # self.assign_location(k)


    # def assign_corner_node_pos(self):
    #     buffer = 0.5
    #     d = find_min_max_coordinates(list(self.embed.values()))

    #     x_mid = np.mean([d.x_max, d.x_min])
    #     y_mid = np.mean([d.y_max, d.y_min])

    #     # TODO make custom method ...for this class... ie, make four_con a class instead of dictionary to clean this up..or just fx..
    #     self.four_con[get_key_by_value(self.four_con, "SOUTH", object=True)].coords = (
    #         x_mid,
    #         d.y_min - buffer,
    #     )
    #     self.four_con[get_key_by_value(self.four_con, "NORTH", object=True)].coords = (
    #         x_mid,
    #         d.y_max + buffer,
    #     )

    #     self.four_con[get_key_by_value(self.four_con, "WEST", object=True)].coords = (
    #         d.x_min - buffer,
    #         y_mid,
    #     )
    #     self.four_con[get_key_by_value(self.four_con, "EAST", object=True)].coords = (
    #         d.x_max + buffer,
    #         y_mid,
    #     )

    def four_connect(self):
        # TODO treatment for when n verts < 4

        for ix, (k, v) in enumerate(self.four_con.items()):
            # update graph edges
            new_edges = []
            for node in v.interior_nodes:
                new_edges.append((v.node, node))
                self.G.add_edges_from(new_edges)

            # update embedding
            self.embed[v.node] = np.array(v.location)

        planar_check, self.planarG = nx.check_planarity(self.G)
        if planar_check:
            ic("Passes planarity check")
        else:
            ic("FAILS PLANAR CHECK!!!!")
