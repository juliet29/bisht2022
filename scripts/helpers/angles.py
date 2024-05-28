import numpy as np
import shapely.geometry as sg
import math
from helpers import ic, sp


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
    # todo => stack overflow..
    
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



def angle_from_dot_product(origin:sp.Point, a:sp.Point, b:sp.Point):
    vec_a, mag_a = calc_vector_and_mag(origin, a)
    vec_b, mag_b = calc_vector_and_mag(origin, b)


    dot_prod = vec_a.x*vec_b.x + vec_a.y*vec_b.y
    scalar_prod = mag_a * mag_b
    quotient = dot_prod/scalar_prod
    angle = math.acos(quotient)

    # diff_prod = refvec.y*unit_vector.x - refvec.x*unit_vector.y
    # cross_prod = vec_b.y*vec_a.x - vec_b.x*vec_a.y

    return angle

def calc_vector_and_mag(origin, pt):
    vec = sp.Point([pt.x - origin.x, pt.y - origin.y])
    mag = math.hypot(vec.x, vec.y)

    return vec, mag



def create_unit_vector(vector):
    # Length of vector: ||v||
    lenvector = math.hypot(vector.x, vector.y)
    # If length is zero there is no angle
    if lenvector == 0:
        raise Exception("vector has length of 0")
    # Normalize vector: v/||v||
    unit_vector = sp.Point([vector.x/lenvector, vector.y/lenvector])

    return unit_vector

def convert_neg_angle(angle):
    return 2*math.pi+angle

def calc_tangent_angle_between_two_points(origin:sp.Point, point:sp.Point):
    # ic(point)
    # refvec = sp.Point([1, 0]) #3pm  for ccw
    vector = sp.Point([point.x - origin.x, point.y - origin.y])
    unit_vector = create_unit_vector(vector)

    # assumption is that refvec is (1,0), so angle represents traversal around unit circle
    simple_angle = math.atan2(unit_vector.y, unit_vector.x)
    if simple_angle < 0:
        ic("negative simple angle")
        simple_angle = convert_neg_angle(simple_angle)

    # dot_prod = unit_vector.x*refvec.x + unit_vector.y*refvec.y
    # diff_prod = refvec.y*unit_vector.x - refvec.x*unit_vector.y
    # complex_angle = math.atan2(diff_prod, dot_prod)
    # ic(complex_angle)

    return simple_angle
    


def calc_angle_between_two_points2(origin:sp.Point, point:sp.Point):
        return
        # ref: https://stackoverflow.com/questions/41855695/sorting-list-of-two-dimensional-coordinates-by-clockwise-angle-using-python/41856340#41856340

        point = [point.x, point.y]
        origin = [origin.x, origin.y]
        ic(point)
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
            ic("angle is neg")
            return 2*math.pi+angle
        # I return first the angle because that's the primary sorting criterium
        # but if two vectors have the same angle then the shorter distance should come first.
        return angle