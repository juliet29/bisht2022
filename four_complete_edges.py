from helpers import *
from boundary_cycle import BoundaryCycle
from matplotlib.patches import FancyArrowPatch, ConnectionStyle

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
        ic(edge)

        self.proj_point = self.project_crossing_edge_onto_buffer(line)

        node1, node2 = (sp.Point(t)  for t in get_emedding_coords(self.embed, edge))
        self.vec1 = vector_between_points(node1, self.proj_point)
        self.vec2 = vector_between_points(node2, self.proj_point)
        _, rad = angle_between_vectors(self.vec1, self.vec2)
        ic(rad)

        self.curve = FancyArrowPatch((node1.x, node1.y), (node2.x, node2.y), arrowstyle='fancy', mutation_scale=5, connectionstyle=f"arc3,rad={rad}")

    def create_curved_edge2(self, index):
        edge = self.crossing_edges[index]
        line = self.crossing_lines[index]
        ic(edge)

        self.proj_point = self.project_crossing_edge_onto_buffer(line)

        node1, node2 = (sp.Point(t)  for t in get_emedding_coords(self.embed, edge))
        self.vec1 = vector_between_points(node1, self.proj_point)
        self.vec2 = vector_between_points(node2, self.proj_point)
        _, rad = angle_between_vectors(self.vec1, self.vec2)
        ic(rad)

        self.curve = FancyArrowPatch((node1.x, node1.y), (node2.x, node2.y), arrowstyle='fancy', mutation_scale=5, connectionstyle=f"arc3,rad={rad}")

    

        

    def project_crossing_edge_onto_buffer(self, line):
        self.temp_buffer = self.temp_boundary_shape.buffer(0.5)

        proj = self.temp_buffer.boundary.project(line.centroid)
        proj_point = self.temp_buffer.boundary.line_interpolate_point(proj)

        return proj_point
    

    
    def prepare_to_plot(self):

        buffer = PointsList(points_to_plot(self.temp_buffer.boundary.coords))
        vec1 =  self.join_vector(self.vec1)
        vec2 = self.join_vector(self.vec2)

        self.plotting_data = {"buffer": buffer, "vec1": vec1, "vec2": vec2}

    def join_vector(self, vector):
        x=[self.proj_point.x, vector[0]+self.proj_point.x]
        y=[self.proj_point.y, vector[1]+self.proj_point.y]
        return PointsList((x,y))
        





    






        
        