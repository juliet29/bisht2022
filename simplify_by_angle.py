import numpy as np
import shapely.geometry as sg


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