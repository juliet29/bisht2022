import inspect
from list_and_dict_utils import get_key_by_value

import math 

from icecream import ic
import networkx as nx
import numpy as np
import shapely as sp

from helpers_classes import Domain



def vector_between_points(pt1:sp.Point, pt2:sp.Point):
    x, y = (pt1.x - pt2.x, pt1.y - pt2.y)
    magnitude = math.sqrt(x**2 + y**2)
    # return (x/magnitude, y/magnitude)
    return (x,y)


def angle_between_vectors(v, w):
    dot_product = np.dot(v, w)
    v_magnitude = np.linalg.norm(v)
    w_magnitude = np.linalg.norm(w)
    cos_theta = dot_product / (v_magnitude * w_magnitude)
    angle_radians = np.arccos(np.clip(cos_theta, -1.0, 1.0))
    angle_degrees = np.degrees(angle_radians)
    return angle_degrees, angle_radians



def get_index_by_cardinal_direction(key, corner_node_dict):
    dict_key = get_key_by_value(corner_node_dict, key, object=True)
    return corner_node_dict[dict_key].index

# self- knowlegde
def get_calling_function_name():
    # Get the frame of the calling function-> 2 levels up
    frame = inspect.currentframe().f_back.f_back
    # Get the name of the calling function
    calling_function_name = frame.f_code.co_name
    return calling_function_name


#MARK: utilities

def find_westernmost_point(coordinates):
    # Initialize variables to store the westernmost point
    westernmost_point = None
    min_longitude = float('inf')

    # Iterate through the coordinates
    for coordinate in coordinates:
        longitude = coordinate[0]  # Get the longitude (x-coordinate)
        if longitude < min_longitude:
            min_longitude = longitude
            westernmost_point = coordinate

    return westernmost_point





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


# geometry
def euclidean_distance(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)


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
    d = Domain(
        x_min=np.min(x_coords),
        x_max=np.max(x_coords),
        y_min=np.min(y_coords),
        y_max=np.max(y_coords),
    )

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


def furthest_coordinate(coord1, coord2, direction):
    # Define a dictionary mapping directions to coordinate components
    direction_mapping = {
        "north": lambda coord: coord[1],
        "south": lambda coord: -coord[1],
        "east": lambda coord: coord[0],
        "west": lambda coord: -coord[0],
    }

    # Check if the provided direction is valid
    if direction.lower() in direction_mapping:
        # Get the coordinate components for the specified direction
        comp1 = direction_mapping[direction.lower()](coord1)
        comp2 = direction_mapping[direction.lower()](coord2)

        # Determine the furthest coordinate in the specified direction
        if comp1 > comp2:
            return coord1
        elif comp1 < comp2:
            return coord2
        elif comp1 == comp2:
            ic("Both coordinates are equidistant in the specified direction")
            return coord2
        else:
            return "Error when getting furthes coord"
    else:
        return "Invalid direction"


def assign_directions(coords):
    north = south = east = west = None

    for coord in coords:
        # ic(f"NEW COORD {coord}")
        x, y = coord
        if north is None or y > north[1]:
            # ic(coord, "north")
            north = coord
        if south is None or y < south[1]:
            # ic(coord, "south")
            south = coord
        if east is None or x > east[0]:
            # ic(coord, "east")
            east = coord
        if west is None or x < west[0]:
            # ic(coord, "west")
            west = coord

    directions = {"north": north, "south": south, "east": east, "west": west}

    # edge case
    if find_keys_with_same_value(directions):
        # ic(directions)
        missing_coord = list(set(coords) - set([v for v in directions.values()]))[0]
        double_count_coord = list(find_keys_with_same_value(directions).keys())[0]

        dir1, dir2 = list(find_keys_with_same_value(directions).values())[0]

        res = furthest_coordinate(missing_coord, double_count_coord, dir1)
        directions[dir1] = res

        leftover = set([missing_coord, double_count_coord]) - set([res])
        directions[dir2] = list(leftover)[0]

        ic("When assigning corner node directions, had to reshuffle")

        return directions
    else:
        return directions


def find_point_along_vector(coord, direction_str, distance):
    # Define direction vectors for cardinal directions
    direction_vectors = {
        "north": np.array([0, 1]),
        "south": np.array([0, -1]),
        "east": np.array([1, 0]),
        "west": np.array([-1, 0]),
    }

    # Check if direction string is valid
    if direction_str not in direction_vectors:
        raise ValueError(
            "Invalid direction string. Please use 'north', 'south', 'east', or 'west'."
        )

    # Get direction vector based on the input string
    direction = direction_vectors[direction_str]

    # Calculate new point coordinates
    new_point = tuple(coord + direction * distance)

    return new_point
