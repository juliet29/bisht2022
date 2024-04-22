from helpers import *


class RegularEdgeLabeling:
    def __init__(self, GraphData: GraphData) -> None:
        self.G = GraphData.G
        self.embed = GraphData.embed
        self.corner_node_data = GraphData.corner_node_dict

    def run(self):
        self.orient_corner_edges()
        self.rel = nx.DiGraph()
        self.rel.add_edges_from(self.corner_edges)
        self.color_corner_nodes()
        
    def orient_corner_edges(self):
        all_correct = []
        for node in self.corner_node_data.values():
            current = self.get_node_edges(node.index)
            correct = self.process_edges(node, current)
            all_correct.extend(correct)
        self.corner_edges = all_correct

    def color_corner_nodes(self):
        for v in self.corner_node_data.values():
            if v.name in [CardinalDirections.SOUTH, CardinalDirections.NORTH]:
                self.rel.nodes[v.index]["node"] = "T_blue"
            else:
                self.rel.nodes[v.index]["node"] = "T_red"


    def get_node_edges(self, node_to_find):
        # Find edges connected to the specified node
        original = [
            (u, v) for u, v in self.G.edges() if u == node_to_find or v == node_to_find
        ]
        filtered = self.filter_corner_connections(original)
        return filtered
    
    def filter_corner_connections(self, original ):
        corner_indices = [ix.index for ix in self.corner_node_data.values()]
        filtered = []
        for e in original:
            conencting_corner_nodes = e[0] in corner_indices and e[1] in corner_indices
            if not conencting_corner_nodes:
                filtered.append(e)
        return filtered


    def process_edges(self, node:CornerNode, edges):
        if node.name in [CardinalDirections.SOUTH, CardinalDirections.WEST]:
            DIR = "out"
        elif node.name in [CardinalDirections.EAST, CardinalDirections.NORTH]:
            DIR = "in"
        else:
            raise ValueError("Invalid direction name")

        correct_edges = self.rearrange_edges(edges, node.index, DIR)
        # ic((node.index, node.name, correct_edges, DIR, "\n"))
        return correct_edges


    def rearrange_edges(self, edges, node, DIR="out"):
        if DIR == "in":
            return [(v, u) if u == node else (u, v) for u, v in edges]
        elif DIR == "out":
            return [(v, u) if v == node else (u, v) for u, v in edges]

