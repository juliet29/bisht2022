from helpers import copy, nx
from edge_label import EdgeLabeling, EdgeColorings
from helpers_classes import CardinalDirections


class RELCorners:
    def __init__(self, REL) -> None:
        self.REL = REL
        self.corner_node_directions = {v.index: v.name for v in self.REL.co.corner_node_dict.values()}
    

    def order_all_corners(self):
        for self.curr_node, self.direction in self.corner_node_directions.items():
            self.order_corner()


    def order_corner(self):
        self.nbs = self.REL.get_node_nbs(self.curr_node)
        self.get_corner_attributes()
        self.update_graph()


    def update_graph(self):
        self.REL.G_rel.add_edges_from(self.edges)
        nx.set_edge_attributes(self.REL.G_rel, self.attrs)


    def get_corner_attributes(self):
        if self.direction == CardinalDirections.WEST:
            self.create_outgoing_edges()
            self.create_attrs(EdgeColorings.RIGHT_RED)
            

        elif self.direction == CardinalDirections.NORTH:
            self.create_incoming_edges()
            self.create_attrs(EdgeColorings.LEFT_BLUE)

        elif self.direction == CardinalDirections.EAST:
            self.create_incoming_edges()
            self.create_attrs(EdgeColorings.RIGHT_RED)

        elif self.direction == CardinalDirections.SOUTH:
            self.create_outgoing_edges()
            self.create_attrs(EdgeColorings.LEFT_BLUE)
        else:
            raise Exception("Undefined direction")
        
    
    def create_outgoing_edges(self, ):
        self.edges = [(self.curr_node, nb) for nb in self.nbs]

    def create_incoming_edges(self, ):
        self.edges = [(nb, self.curr_node) for nb in self.nbs]

    def create_attrs(self, color:EdgeColorings):
        self.attrs =  {e: {"data": EdgeLabeling(color)} for e in self.edges}
        self.REL.edge_split[color].extend(self.edges)
