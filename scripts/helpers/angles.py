import numpy as np
import shapely.geometry as sg
from shapely import Point
import math


# attributes to https://github.com/shapely/shapely/issues/1046

def get_angles(vec_1,vec_2):
    """
    return the angle, in degrees, between two vectors
    """
    
    dot = np.dot(vec_1, vec_2)
    det = np.cross(vec_1,vec_2)
    angle_in_rad = np.arctan2(det,dot)
    return np.degrees(angle_in_rad)


def simplify_by_angle(poly_in, deg_tol = 1):
    """
    try to remove persistent coordinate points that remain after
    simplify, convex hull, or something, etc. with some trig instead
    params:
    poly_in: shapely Polygon 
    deg_tol: degree tolerance for comparison between successive vectors
    return: 'simplified' polygon
    
    """
    
    ext_poly_coords = poly_in.exterior.coords[:]
    vector_rep = np.diff(ext_poly_coords,axis = 0)
    angles_list = []
    for i in range(0,len(vector_rep) -1 ):
        angles_list.append(np.abs(get_angles(vector_rep[i],vector_rep[i+1])))
    
#   get mask satisfying tolerance
    thresh_vals_by_deg = np.where(np.array(angles_list) > deg_tol)
    
#   gotta be a better way to do this next part
#   sandwich betweens first and last points
    new_idx = [0] + (thresh_vals_by_deg[0] + 1).tolist() + [0]
    new_vertices = [ext_poly_coords[idx] for idx in new_idx]
    

    return sg.Polygon(new_vertices)


def calc_angles_complex(origin:Point, point:Point):
        # ref: https://stackoverflow.com/questions/41855695/sorting-list-of-two-dimensional-coordinates-by-clockwise-angle-using-python/41856340#41856340

        point = [point.x, point.y]
        origin = [origin.x, origin.y]
        # refvec = [0, 1] # noon 
        refvec = [-1, 0] #9pm 
        refvec = [1, 0] #3pm  for ccw

        # Vector between point and the origin: v = p - o
        vector = [point[0]-origin[0], point[1]-origin[1]]
        # Length of vector: ||v||
        lenvector = math.hypot(vector[0], vector[1])
        # If length is zero there is no angle
        if lenvector == 0:
            return -math.pi, 0
        # Normalize vector: v/||v||
        normalized = [vector[0]/lenvector, vector[1]/lenvector]
        dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]     # x1*x2 + y1*y2
        diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]     # x1*y2 - y1*x2
        angle = math.atan2(diffprod, dotprod)
        # Negative angles represent counter-clockwise angles so we need to subtract them from 2*pi (360 degrees)

        if angle < 0:
            return 2*math.pi+angle
        # I return first the angle because that's the primary sorting criterium
        # but if two vectors have the same angle then the shorter distance should come first.
        return angle