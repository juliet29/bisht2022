
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import matplotlib.pyplot as plt
import shapely as sp

def quick_plotly_plot(x,y, label="None", mode="markers"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, name=label, mode=mode, ))
    return fig

def add_geom_to_plotly(geom, fig, label="None", mode="markers"):
    x, y = points_to_plot(geom.coords)
    fig.add_trace(go.Scatter(x=x, y=y, name=label,  mode=mode, ))
    return fig
     
def add_embedding_to_plotly(embed, fig=None):
    if not fig:
        fig = go.Figure()

    x = [v[0] for v in embed.values()]
    y = [v[1] for v in embed.values()]
    keys = [k for k in embed.keys()]

    for ix, k in enumerate(keys):
        fig.add_trace(go.Scatter(
            x=[x[ix]], 
            y=[y[ix]], 
            name=k, mode="markers", 
            hovertext=[f"{k}, ({np.round(x[ix],3), np.round(y[ix],3)})"],
            hoverinfo="text",     
            marker=dict(color="blue", opacity=0.4, size=10)
        ))

    return fig


def points_to_plot(coords):
    x = [c[0] for c in coords]
    y  = [c[1] for c in coords]
    return x, y
