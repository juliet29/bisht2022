import networkx as nx

class STGraphData:
    def __init__(
        self,
        DG: nx.DiGraph,
        embed: dict,
        source: int, 
        target: int
    ) -> None:
        self.DG = DG
        self.embed = embed
        self.source = source
        self.target = target
        self.embedding = None
        self.create_source_taget_edge()
        self.create_undirected_graph()

    def create_source_taget_edge(self):
        self.DG.add_edge(self.source, self.target)


    def create_undirected_graph(self):
        self.G = self.DG.to_undirected()

    def update_embedding(self, embedding):
        self.embedding = embedding
        
    def plot_graph(self):
        nx.draw_networkx(self.DG, self.embed)
        

    def update_faces(self, faces):
        self.faces = faces


    def __repr__(self):
        return f"STGraphData{self.__dict__})"