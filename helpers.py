from helpers_classes import *
from helpers_plots import *

from icecream import ic

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from scipy.spatial import ConvexHull

# dictionary utilities
def any_attribute_matches_value(obj, value):
    for attr_name in vars(obj):  # Get all attributes of the object
        # ic(attr_name, getattr(obj, attr_name), value)
        if getattr(obj, attr_name) == value:
            return True
    return False


def get_key_by_value(dictionary, value, object=False):
    for key, val in dictionary.items():
        if val == value:
            return key
        if object:
            if any_attribute_matches_value(val, value):
                return key
    return None





# utilities
def total_length(list_of_lists):
    return sum(len(sublist) for sublist in list_of_lists)

def find_difference(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    # Find the elements present in set1 but not in set2
    difference1 = set1 - set2

    # Find the elements present in set2 but not in set1
    difference2 = set2 - set1

    return difference1, difference2


def find_line_through_points(point_pair):
    point1, point2 = point_pair  # tuple of coordinate pts
    x1, y1 = point1
    x2, y2 = point2

    # Calculate slope
    slope = (y2 - y1) / (x2 - x1)

    # Use one of the points to find y-intercept
    b = y1 - slope * x1
    # todo turn output into class
    return slope, b


def check_point_on_line(line_data, test_point):
    # here looking for inbetween points
    slope, y_intercept = line_data
    x, y = test_point

    expected_y = slope * x + y_intercept
    return np.isclose(y, expected_y)


def check_parallel(slope_1, slope_2):
    return np.isclose(slope_1, slope_2)


def extract_convex_points(embed_arr, hull):
    # points that lie on outer most corners of graph embedding
    boundary_points = []
    for simplex in hull.simplices:
        boundary_points.append((embed_arr[simplex[0]], embed_arr[simplex[1]]))
    return boundary_points


def find_min_max_coordinates(coordinates):
    if not coordinates:
        return None

    # Convert the list of arrays into a numpy array for efficient manipulation
    coordinates_array = np.array(coordinates)

    # Extract x and y coordinates into separate arrays
    x_coords = coordinates_array[:, 0]
    y_coords = coordinates_array[:, 1]


    # Find min and max values for x and y coordinates
    d = Domain(x_min=np.min(x_coords), 
               x_max=np.max(x_coords), 
               y_min=np.min(y_coords),
               y_max=np.max(y_coords))

    return d


def check_point_in_hull(domain: Domain, point):
    x, y = point
    
    return domain.x_min < x < domain.x_max and domain.y_min < y < domain.y_max


def new_node_pos(n1, n2):
    # assuming point will be on edge between two nodes
    n1_x = n1[0]
    n2_x = n2[0]

    n1_y = n1[1]
    n2_y = n2[1]

    if np.isclose(n1_x, n2_x):
        ic("same x", n1_x, n2_x)
        n_x = n1_x
        n_y = np.mean([n1_y, n2_y])
    elif np.isclose(n1_y, n2_y):
        ic("same y", n1_y, n2_y)
        n_x = np.mean([n1_x, n2_x])
        n_y = n1_y
    else:
        ic("neither same")
        n_x = np.mean([n1_x, n2_x])
        n_y = np.mean([n1_y, n2_y])

    return (n_x, n_y)





def assign_directions(coords):
    north = south = east = west = None

    for coord in coords:
        x, y = coord
        if north is None or y > north[1]:
            north = coord
        if south is None or y < south[1]:
            south = coord
        if east is None or x > east[0]:
            east = coord
        if west is None or x < west[0]:
            west = coord

    directions = {'north': north, 'south': south, 'east': east, 'west': west}
    return directions


def find_point_along_vector(coord, direction_str, distance):
    # Define direction vectors for cardinal directions
    direction_vectors = {
        'north': np.array([0, 1]),
        'south': np.array([0, -1]),
        'east': np.array([1, 0]),
        'west': np.array([-1, 0])
    }

    # Check if direction string is valid
    if direction_str not in direction_vectors:
        raise ValueError("Invalid direction string. Please use 'north', 'south', 'east', or 'west'.")

    # Get direction vector based on the input string
    direction = direction_vectors[direction_str]

    # Calculate new point coordinates
    new_point = tuple(coord + direction * distance)

    return new_point


