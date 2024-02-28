from helpers import *
import random

## NOTE: keeping this seperate from augment.py class, bc could possibly want to get boundary at anyy stage of the augmentation, but could put togetehr later ..


class Boundaries:
    def __init__(self, G) -> None:
        self.G = G
        self.embed = nx.planar_layout(self.G)  # dictionary with node locations
        pass

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

    # TODO this may be its own class..

    def find_seperating_triangles(self):
        three_cyles = sorted(nx.simple_cycles(self.G, 3))
        self.sep_triangles = []
        for ix, cycle in enumerate(three_cyles):
            other_nodes = list(set(self.G.nodes) - set(cycle))
            coords = [self.embed[k] for k in cycle]
            domain = find_min_max_coordinates(coords)

            for node in other_nodes:
                # TODO double check for nested triangles..
                if (
                    check_point_in_hull(domain, self.embed[node])
                    and cycle not in self.sep_triangles
                ):
                    self.sep_triangles.append(SeperatingTriangle(cycle, node))

        return self.sep_triangles

    def find_sep_triangle_targets(self):
        # [[ei1, ei2, ei3], ... , [ep1, ep2, ep3]], p = num of sep triangles
        st_edges = [
            list(self.G.subgraph(tri.cycle).edges) for tri in self.sep_triangles
        ]

        # will find a set of less than k edges that are needed to solve st problem  => here setting to n
        edges = list(self.G.edges())
        k = len(edges)
        random.shuffle(edges)
        random_graph_edges = edges[:k]

        covered_bools = []
        # self.target_edges = []

        for ix, tri in enumerate(self.sep_triangles):
            covered_bools.append(False)
            for edge in random_graph_edges:
                if edge in st_edges[ix]:
                    tri.target_edge = edge
                    covered_bools[ix] = True
                    break
            # check that each st was covered
            assert covered_bools[ix] == True

        return self.sep_triangles

    def clean_up_sep_triangle(self, pos):
        self.G_no_st = self.G.copy()  # no sep triangle
        for ix, tri in enumerate(self.sep_triangles):
            new_node = len(self.G.nodes) + ix
            ic(ix, new_node, len(self.G.nodes))
            n1, n2 = tri.target_edge
            ic(tri.target_edge)
            new_edges = [(n1, new_node), (n2, new_node), (tri.inner_node, new_node)]

            # update graph .. 
            self.G_no_st.remove_edge(n1, n2)
            self.G_no_st.add_edges_from(new_edges)

            # update positions in embedding 
            new_pos = new_node_pos(pos, pos[n1], pos[n2])
            pos[new_node] = np.array(new_pos)
            

        return self.G_no_st, pos
    


