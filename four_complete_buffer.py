from helpers import *

from shapely import LineString, Point, Polygon


class FourCompleteBuffer:
    def __init__(self, GraphData: GraphData, path: list, boundary_shape, buffer_size:float = 0.5, num:int=0) -> None:
        self.data = GraphData
        self.G = GraphData.G
        self.embed = GraphData.embed

        self.path = path
        self.boundary_shape = boundary_shape

        self.buffer_size = buffer_size
        self.num = num

        self.corner_node_location = None

        self.get_point_on_buffer()
        


    def get_point_on_buffer(self):
        d = get_dict_subset(self.embed, self.path)
        self.l = LineString([Point(i) for i in d.values()])
        self.pt = self.l.centroid

        self.buffer = self.boundary_shape.buffer(self.buffer_size)

        # proj gives the distance along the boundary as a float 
        proj = self.buffer.boundary.project(self.pt)
        proj_point = self.buffer.boundary.line_interpolate_point(proj)

        self.corner_node_location = (proj_point.x, proj_point.y)

    def create_traces_to_plot(self):
        lx, ly = points_to_plot(self.l.coords)
        rx, ry = points_to_plot(self.pt.coords)
        bx, by = points_to_plot(self.buffer.boundary.coords)
        px, py = points_to_plot(self.proj_loc.coords)

        self.traces = []

        if self.num == 0:
            self.traces.append(go.Scatter(x=bx, y=by, mode='markers+lines',))

        self.traces.append(go.Scatter(x=lx, y=ly, mode='markers+lines', name=self.num))

        self.traces.append(go.Scatter(x=rx, y=ry, mode='markers',  marker=dict(color='red'), name=self.num ))

        self.traces.append(go.Scatter(x=px, y=py, mode='markers', marker=dict(color='red'),  name=self.num ))


