import shapely as sp

def get_centroid(shape:sp.Polygon):
    return (shape.centroid.xy[0][0], shape.centroid.xy[1][0])
