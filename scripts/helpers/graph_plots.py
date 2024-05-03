import os 
import pickle

import networkx as nx
import numpy as np




#MARK: plotting graphs 
def plot_planar(G, old_pos=None, hide_ticks=True):
    # ic(old_pos)
    pos = old_pos if old_pos else nx.planar_layout(G)
    pos = nx.draw_networkx(G, pos, hide_ticks)
    return pos

def plot_planar_embed(embed: nx.PlanarEmbedding):
    pos = nx.combinatorial_embedding_to_pos(embed)
    nx.draw_networkx(nx.Graph(embed), pos)

def plot_just_planar(G: nx.Graph, pos=None):
    try:
        if not pos:
            pos = nx.planar_layout(G)
        nx.draw_networkx(G, pos)
        return pos
    except:
        print("not planar")
        nx.draw_networkx(G)





