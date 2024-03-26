from helpers import *
from scipy.spatial import ConvexHull


## NOTE: keeping this seperate from augment.py class, bc could possibly want to get boundary at anyy stage of the augmentation, but could put togetehr later ..
# yes, earlier functions are more of a general graph utility class, while the later functions will only be used at one stage ... 03/04/24


class Boundaries:
    def __init__(self, G: nx.Graph, embed: dict) -> None:
        # TODO make this and FixSepTris extend a base class with these type hint
        self.G = G.copy()
        self.embed = embed.copy()
        self.find_boundary_points()
        self.find_boundary_edges()

    def fix_cips_and_add_corner_nodes(self):
        self.find_cips()  # right now does not modify the graph 
        # TODO fix if > than 4 cips
        # self.fix_cips()
        self.add_corner_nodes()
        

    def add_corner_nodes(self):
        self.organize_cips()
        self.distribute_corner_nodes()
        self.locate_corner_nodes()
        self.connect_corner_nodes()
        self.distinguish_corner_nodes()

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
    
    def find_boundary_cycle(self):
        n_cips = total_length(self.cips)
        self.boundary_cycles = []
        for c in nx.simple_cycles(G=self.boundary_graph, length_bound=n_cips + 1):
            if len(c) >= n_cips + 1:
                self.boundary_cycles.append(c)

        # TODO there should only be one cycle that is as long is the length of the cips but havent verified this ...
        self.boundary_cycles = self.boundary_cycles[0]

    def organize_cips(self):
        self.find_boundary_cycle()
        # leave only the bounary items that match up with the cips
        cip_nodes = [item for sublist in self.cips for item in sublist]
        diff = list(set(self.boundary_cycles).difference(set(cip_nodes)))
        for d in diff:
            self.boundary_cycles.remove(d)

    def distribute_corner_nodes(self):
        self.corner_node_data = {k: CornerNode() for k in range(4)}

        # east, west, south, north
        num_connect = 4  #
        j = (len(self.boundary_cycles) // (num_connect - 1)) + 1
        end_indices = [j * (i + 1) - i for i in range(num_connect)]

        for ix, end_index in enumerate(end_indices):
            self.corner_node_data[ix].interior_nodes = self.boundary_cycles[
                end_index - j : end_index
            ]
            self.corner_node_data[ix].node = len(self.G.nodes) + ix

        if len(self.corner_node_data[num_connect - 1].interior_nodes) < 2:
            self.corner_node_data[3].interior_nodes = [
                self.boundary_cycles[-1],
                self.boundary_cycles[0],
            ]

        return self.corner_node_data

    def locate_corner_nodes(self, buffer=0.5):
        # get the central location of interior nodes for a given corner node
        for v in self.corner_node_data.values():
            arr = np.array([self.embed[i] for i in v.interior_nodes])
            v.mean_location = (np.mean(arr[:, 0]), np.mean(arr[:, 1]))

        # determine whicch of these locations are most north, east etc
        coords = [v.mean_location for v in self.corner_node_data.values()]
        self.direction_dict = assign_directions(coords)

        for k, v in self.direction_dict.items():
            # match items in four_con dictionary to the direction dict
            item = self.corner_node_data[
                get_key_by_value(self.corner_node_data, self.direction_dict[k], object=True)
            ]
            item.name = k
            # assign location with approp direction
            item.location = find_point_along_vector(item.mean_location, k, buffer)

    def connect_corner_nodes(self):
        # TODO treatment for when n verts < 4

        for ix, (k, v) in enumerate(self.corner_node_data.items()):
            # update graph edges
            new_edges = []
            for node in v.interior_nodes:
                new_edges.append((v.node, node))
                self.G.add_edges_from(new_edges)

            # update embedding
            self.embed[v.node] = np.array(v.location)


        planar_check, self.alt_planar_G = nx.check_planarity(self.G)
        if planar_check:
            ic("Passes planarity check")
        else:
            ic("FAILS PLANAR CHECK!!!!")

    def distinguish_corner_nodes(self):
        corner_node_ix = [v.node for v in self.corner_node_data.values()]
        for ix in self.G.nodes:
            if ix in corner_node_ix:
                self.G.nodes[ix]["corner_or_interior"] = "corner"
            else: 
                self.G.nodes[ix]["corner_or_interior"] = "interior"
