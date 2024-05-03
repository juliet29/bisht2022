from itertools import tee

# list utilities
def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def flatten_list(input_list):
    return [item for sublist in input_list for item in sublist]


# set utilities
def freeze_list_of_tuples(set1, set2):
    a = {frozenset(t) for t in set1}
    b = {frozenset(t) for t in set2}

    return a, b


# dictionary utilities
def get_dict_subset(dict, keys_to_select):
    return {key: dict[key] for key in keys_to_select}


def any_attribute_matches_value(obj, value):
    for attr_name in vars(obj):  # Get all attributes of the object
        if getattr(obj, attr_name) == value:
            return True
    return False


def get_key_by_value(dictionary, value, object=False):
    for key, val in dictionary.items():
        if val == value:
            return key
        # if the dictionary has objects as its values in each key value pair, set object=True
        if object:
            if any_attribute_matches_value(val, value):
                return key
    return None


def find_keys_with_same_value(dictionary):
    keys_by_value = {}

    for key, value in dictionary.items():
        if value in keys_by_value:
            keys_by_value[value].append(key)
        else:
            keys_by_value[value] = [key]

    keys_with_same_value = {
        value: keys for value, keys in keys_by_value.items() if len(keys) > 1
    }

    return keys_with_same_value
