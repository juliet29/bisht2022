from helpers import *
from boundary_cycle import *
from corner_implying_paths import *

from itertools import cycle
import random 

def contains_sublist(larger_list, smaller_list):
    n = len(smaller_list)
    for i in range(len(larger_list) - n + 1):
        if larger_list[i:i+n] == smaller_list:
            return True
    return False


class FourComplete:
    """ Approach here is loosely taken from Kant and He '97 and '93 """
    def __init__(self, GraphData: GraphData) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed

    def run(self):
        self.get_boundary_cyle()
        self.generate_dividing_indices()
        self.divide_boundary_cycle()
        self.assign_corner_nodes()
        self.connect_corner_nodes()
        
        self.locate_corner_nodes()
        # self.connect_outer_nodes()

        self.assert_planarity()
        # self.assert_triangulated()
    
    def run_to_division(self):
        self.get_boundary_cyle()
        self.generate_dividing_indices()
        self.divide_boundary_cycle()
        self.ensure_no_cips()
    
    def run_to_completion(self):
        self.assign_corner_nodes()
        self.connect_corner_nodes()
        
        self.locate_corner_nodes()
        # self.connect_outer_nodes()

        self.assert_planarity()


    # TODO helpers? 

    # checks
    def assert_correct_division(self):
        assert set(flatten_list(self.paths)) == set(self.boundary), "Four completion incorrect - not all boundary nodes were accounted for"

    def assert_planarity(self):
        planar_check, self.alt_planar_G = nx.check_planarity(self.G)
        assert planar_check, "Four completed graph is not planar "

    def assert_triangulated(self):
         assert nx.is_chordal(self.G), "Four completed graph ia not triangulated "


    def check_for_cips(self):  # helper function 
        c = CornerImplyingPaths(self.data)
        assert c.boundary == self.boundary # TODO actually fix in data object 

        for path in self.paths:
            for cip in c.arranged_cips:
                try:
                    overlap = contains_sublist(path, cip)
                    if overlap:
                        ic(cip, path, "NEED to adjust division")
                        return True
                except:
                    pass
        return False
    

    # action begins 
    def get_boundary_cyle(self):
        g = BoundaryCycle(self.data)
        self.boundary = g.ccw_boundary_cycle
        

    def generate_dividing_indices(self):
        assert len(self.G.nodes) > 4, "TODO Less than 4 nodes"
        self.num_corner_points = 4

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
                path = self.boundary[i:] + self.boundary[:j+1]
            else: 
                path = self.boundary[i:j+1]

            self.paths.append(path)

            if ix >= (self.num_corner_points - 1):
                break
        
        self.assert_correct_division()

    
    def ensure_no_cips(self):
        n = len(self.boundary)
        cntr = 1

        for i in range(10):
            if self.check_for_cips():
                cntr+=1
                ic(i, self.paths, "found cips")
                # update dividing indices, divide boundary cycle and continue checking until passes
                self.dividing_indices = [(i+cntr)%n for i in self.dividing_indices]
                self.divide_boundary_cycle()
            else:
                return


    def assign_corner_nodes(self):
        self.corner_node_data = {k: CornerNode() for k in range(4)}

        for ix, path in enumerate(self.paths):
            self.corner_node_data[ix].index = len(self.G.nodes) + ix
            self.corner_node_data[ix].neighbour_indices = path 


    def connect_corner_nodes(self):
        for v in self.corner_node_data.values():
            # update graph edges
            new_edges = []
            for node in v.neighbour_indices:
                new_edges.append((v.index, node))
                self.G.add_edges_from(new_edges)

    def get_node_index(self, key):
        dict_key = get_key_by_value(self.corner_node_data, key, object=True)
        return self.corner_node_data[dict_key].index

    def connect_outer_nodes(self):
        # TODO move to own four connect class?
        ix = self.get_node_index  # create alias
        edges = [
            (ix("south"), ix("east")),
            (ix("east"), ix("north")),
            (ix("north"), ix("west")),
            (ix("west"), ix("south")),
            (ix("south"), ix("north")),
        ]
        self.G.add_edges_from(edges)
        
    

    def locate_corner_nodes(self, buffer=0.5):
        # TODO split this up .. 
        # get the central location of interior nodes for a given corner node
        for v in self.corner_node_data.values():
            arr = np.array([self.embed[i] for i in v.neighbour_indices])
            v.mean_location = (np.mean(arr[:, 0]), np.mean(arr[:, 1]))

        # determine whicch of these locations are most north, east etc
        coords = [v.mean_location for v in self.corner_node_data.values()]
        self.direction_dict = assign_directions(coords)

        for k, v in self.direction_dict.items():
            # match items in four_con dictionary to the direction dict
            item = self.corner_node_data[get_key_by_value(self.corner_node_data, self.direction_dict[k], object=True)]
            item.name = k
            # assign location with approp direction
            item.location = find_point_along_vector(item.mean_location, k, buffer)

        for v in self.corner_node_data.values():
            self.embed[v.index] = np.array(v.location)


    def show_updated_graph(self):
        plot_planar(self.G, self.embed)
    


        


    
 
