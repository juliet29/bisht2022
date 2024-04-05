from helpers import *
from boundary_cycle import *
from corner_implying_paths import *

from itertools import cycle
import random 


class FourComplete:
    """ Approach here is loosely taken from Kant and He '97 and '93 """
    def __init__(self, GraphData: GraphData) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed

        self.num_corner_points = 4

    def run(self):
        self.run_to_division()
        self.run_to_completion()
    
    def run_to_division(self):
        self.get_boundary_cyle()
        self.generate_dividing_indices()
        self.divide_boundary_cycle()
        self.ensure_no_cips()
    
    def run_to_completion(self):

        self.assert_planarity()


    # action begins 
    def get_boundary_cyle(self):
        g = BoundaryCycle(self.data)
        self.boundary = g.ccw_boundary_cycle
        

    def generate_dividing_indices(self):
        assert len(self.G.nodes) > self.num_corner_points, "TODO Less than 4 nodes"
       
        self.seed = 0
        random.seed(self.seed)
        random_boundary_nodes = random.sample(self.boundary, self.num_corner_points)
        self.dividing_indices = [self.boundary.index(num) for num in random_boundary_nodes]

        self.dividing_indices.sort()


    def divide_boundary_cycle(self):
        cycled_dividing_indices = cycle(self.dividing_indices)
        self.paths = []

        for ix, (i,j) in enumerate(pairwise(cycled_dividing_indices)):
            if i > j:
                # wrap around the boundary 
                path = self.boundary[i:] + self.boundary[:j+1]
            else: 
                path = self.boundary[i:j+1]

            self.paths.append(path)
            
            # IMPORTANT -> otherwise will loop for ever 
            if ix >= (self.num_corner_points - 1):
                break
        
        self.assert_correct_division()
    
    def ensure_no_cips(self):
        n = len(self.boundary)
        cntr = 1

        for i in range(n):
            if self.check_for_cips():
                cntr+=1
                # ic(i, self.paths, "found cips")
                self.dividing_indices = [(i+cntr)%n for i in self.dividing_indices]
                self.divide_boundary_cycle()
            else:
                return
        raise Exception("Did not find four completion without separating triangles!")
    
    
    def check_for_cips(self):  # helper function 
        c = CornerImplyingPaths(self.data)
        assert c.boundary == self.boundary # TODO actually fix in data object 
        self.cips = c.cips
        # ic(self.cips)

        for p in self.paths:
            for cip in c.cips:
                if len(cip) > len(p):
                    # ic("skipping", p, cip)
                    pass
                else:
                    # ic("evaluating", p, cip)
                    if contains_sublist(p, cip):
                        ic('found cips - contains')
                        return True
                    elif contains_sublist(p, cip[::-1]):
                        ic('found cips - contains reverse')
                        return True

        return False
        

    def show_updated_graph(self):
        plot_planar(self.G, self.embed)
    


    # checks
    def assert_correct_division(self):
        assert set(flatten_list(self.paths)) == set(self.boundary), "Four completion incorrect - not all boundary nodes were accounted for"

    def assert_planarity(self):
        planar_check, self.alt_planar_G = nx.check_planarity(self.G)
        assert planar_check, "Four completed graph is not planar "

    def assert_triangulated(self):
         assert nx.is_chordal(self.G), "Four completed graph ia not triangulated "
        

#MARK: helper functions 

def contains_sublist(larger_list, smaller_list):
    # ic(larger_list, smaller_list)
    n = len(smaller_list)
    for i in range(len(larger_list) - n + 1):
        if larger_list[i:i+n] == smaller_list:
            return True
    return False

    
 
