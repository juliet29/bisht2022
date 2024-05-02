from helpers import nx, np
from helpers_classes import GraphData

edges = [(0,2), (0,1), (1,2), (2,3), (3,0),
         (0,4), (0,7), (0,6),
         (4,5), (5,2),
         (7,5),
         (6,2)]

pos = [(1.5,0), (0,1), (2,3), (4,1), (1,1), (1.5,2), (3,1), (2,1)]

def create_graph(edges, pos):
    G = nx.Graph()
    G.add_edges_from(edges)
    embed = {k:np.array(v) for (k,v) in enumerate(pos)}
    return GraphData(G, embed)



graph_data = create_graph(edges, pos)
