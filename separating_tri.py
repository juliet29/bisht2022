from helpers import *
import random


class SeparatingTriangles:
    def __init__(self, G, embed, boundary_edges) -> None:
        self.G = G.copy()
        self.embed = embed.copy()
        self.boundary_edges = boundary_edges

    def run_st(self):
        self.find_st()
        self.find_targets()
        self.remove_st()

        self.seperating_triangle_check()

        return self.G_no_st

    def find_st(self):
        three_cyles = sorted(nx.simple_cycles(self.G, 3))
        self.sep_triangles = []
        for ix, cycle in enumerate(three_cyles):
            other_nodes = list(set(self.G.nodes) - set(cycle))
            coords = [self.embed[k] for k in cycle]
            domain = find_min_max_coordinates(coords)

            for node in other_nodes:
                # TODO double check if this is correct for nested triangles.. => bc inner node might be different depending on the cycle
                if (
                    check_point_in_hull(domain, self.embed[node])
                    and cycle not in self.sep_triangles
                ):
                    self.sep_triangles.append(SeperatingTriangleData(cycle, node))


        return self.sep_triangles

    def find_targets(self):
        # [[ei1, ei2, ei3], ... , [ep1, ep2, ep3]], p = num of sep triangles
        st_edges = [
            list(self.G.subgraph(tri.cycle).edges) for tri in self.sep_triangles
        ]

        # will find a set of less than k edges that are needed to solve st problem  => here setting to n
        edges = (
            self.boundary_edges
        )  # list(self.G.edges()) # TODO change so only have boundary edges..
        k = len(edges)
        random.shuffle(edges)
        random_graph_edges = edges[:k]

        covering_status = []
        # self.target_edges = []

        for ix, tri in enumerate(self.sep_triangles):
            covering_status.append(False)
            for edge in random_graph_edges:
                if edge in st_edges[ix]:
                    tri.target_edge = edge
                    covering_status[ix] = True
                    break
            # check that each st was covered
            assert covering_status[ix] == True

        return self.sep_triangles

    def remove_st(self):
        self.G_no_st = self.G.copy()  # no sep triangle
        for ix, tri in enumerate(self.sep_triangles):
            new_node = len(self.G.nodes) + ix
            n1, n2 = tri.target_edge
            ic(tri.target_edge)
            new_edges = [(n1, new_node), (n2, new_node), (tri.inner_node, new_node)]

            # update graph edges
            self.G_no_st.remove_edge(n1, n2)
            self.G_no_st.add_edges_from(new_edges)

            # update positions in embedding
            new_pos = new_node_pos(self.embed[n1], self.embed[n2])
            self.embed[new_node] = np.array(new_pos)

        return self.G_no_st

    def seperating_triangle_check(self, G=None):
        local_G = G if G else self.G_no_st
        l3_cycles = sorted(nx.simple_cycles(local_G, 3))
        m = len(list(local_G.edges))
        n = len(list(local_G.nodes))
        # if self.DEBUG:
        ic(len(l3_cycles), m, n, m - n + 1)
        assert len(l3_cycles) == m - n + 1, f"{len(l3_cycles), m, n, m-n+1}"
