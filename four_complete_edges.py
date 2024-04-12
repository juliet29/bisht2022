from helpers import *
from boundary_cycle import BoundaryCycle

class FourCompleteEdges:
    def __init__(self, GraphData: GraphData, pre_four_complete_shape:sp.LineString, buffer_size:float = 0.5) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.buffer_size = buffer_size

        self.pre_four_complete_shape = sp.Polygon(pre_four_complete_shape)

    def run(self):
        self.find_crossing_edges()
        self.create_temp_boundary_shape()
        self.create_curved_edge(0)
        

    def find_crossing_edges(self):
        #TODO maybe make an object or dictionary? 
        self.crossing_edges = [] 
        self.crossing_lines = []
        for e in list(self.G.edges):
            u, v = get_emedding_coords(self.embed, e)
            line = sp.LineString((list(u), list(v)))
            if line.crosses(self.pre_four_complete_shape):
                self.crossing_edges.append(e)
                self.crossing_lines.append(line)
        

    def create_temp_boundary_shape(self):
        ## remove edges and create a new shape 
        temp_G = copy.deepcopy(self.G)
        temp_G.remove_edges_from(self.crossing_edges)
        g = GraphData(temp_G, self.embed)
        self.temp_boundary_shape = sp.Polygon(BoundaryCycle(g).boundary_line_string)

    
    def create_curved_edge(self, index):
        edge = self.crossing_edges[index]
        line = self.crossing_lines[index]

        proj_point = self.project_crossing_edge_onto_buffer(line)

        node1, node2 = (sp.Point(t)  for t in get_emedding_coords(self.embed, edge))
        vec1 = vector_between_points(node1, proj_point)
        vec2 = vector_between_points(node2, proj_point)
        _, rad = angle_between_vectors(vec1, vec2)
        ic(rad)

    def project_crossing_edge_onto_buffer(self, line):
        buffer = self.temp_boundary_shape.buffer(0.5)

        proj = buffer.boundary.project(line.centroid)
        proj_point = buffer.boundary.line_interpolate_point(proj)

        return proj_point
    
    #TODO need to visualize!



    






        
        