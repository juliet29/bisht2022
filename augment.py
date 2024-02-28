from helpers import *

## graph augmentation algorithms 
## Bisht 2022

class Augment:
    def __init__(self, G) -> None:
        self.G = G
        self.G_tri = None
        self.DEBUG = None

    def run_augment(self, DEBUG=False):
        self.DEBUG = DEBUG
        self.biconnect()
        self.test_biconnect()

        self.triangulate()
        self.test_triangulate()

        self.seperating_triangle_check()

        self.G_final = self.G_tri

        return self.G_final
        

    def check_block(self, node, blocks):
        # see what blocks a node belongs to
        indices = []
        set_members = []
        for index, my_set in enumerate(blocks):
            if node in my_set:
                indices.append(index)
                set_members.append(my_set)

        return indices, set_members


    def biconnect(self, DEBUG=False):
        LOCAL_DEBUG = self.DEBUG or DEBUG
        self.G_biconnect = self.G.copy()
        cut_vertices = list(nx.articulation_points(self.G_biconnect))
        ic(cut_vertices)

        for v in cut_vertices:
            # find vertices adjacent to x (ie neighbours of x?)
            neighbors = list(self.G_biconnect.neighbors(v))
            blocks = list(nx.biconnected_components(self.G_biconnect))
            if LOCAL_DEBUG:
                ic(f"START WORK FOR V={v} ");
                ic(v, neighbors)
            for curr_item, next_item in zip(neighbors, neighbors[1:]):
                curr_block, curr_block_members = self.check_block(curr_item, blocks)
                next_block, next_block_members = self.check_block(next_item, blocks)
                if LOCAL_DEBUG:
                    ic(curr_item, curr_block_members)
                    ic(next_item, next_block_members)
                if not set(curr_block) & set(next_block):
                    edge = (curr_item, next_item)
                    if LOCAL_DEBUG:
                        ic(f"No overlap between {edge}. Adding edge")
                    # add edges between vertices 
                    self.G_biconnect.add_edge(curr_item, next_item)
            # TODO add the part to make minimal additions.. 

        return self.G_biconnect

    def test_biconnect(self):
        # check that graph is biconnected => no articulation points
        assert len(list(nx.articulation_points(self.G_biconnect))) == 0


    def triangulate(self):
        self.G_tri, alpha = nx.complete_to_chordal_graph(self.G_biconnect.copy()) 
        return self.G_tri

    def test_triangulate(self):
        assert nx.is_chordal(self.G_tri)
        
    def seperating_triangle_check(self, G=None):
        local_G = G if G else self.G_tri
        l3_cycles = sorted(nx.simple_cycles(local_G, 3))
        m = len(list(local_G.edges))
        n = len(list(local_G.nodes))
        if self.DEBUG:
            ic(len(l3_cycles), m, n, m-n+1);
        assert len(l3_cycles) == m-n+1    


    