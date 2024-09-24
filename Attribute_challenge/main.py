import sys

from constraint import *
from lxml import etree as ET



class Cache:
    def __init__(self, gcode, d, t, attributes):
        self.gcode = gcode
        self.d = d
        self.t = t
        self.attributes = attributes

    def __str__(self):
        return self.gcode

    def __repr__(self):
        return self.gcode



def get_index(row, column):
    return row * matrix_size + column

def get_row_column(index):
    return index // matrix_size, index % matrix_size

def print_matrix(matrix):
    for row in matrix:
        print(row)

def get_cache_from_attribute(attribute, d, t):
    for cache in caches:
        if attribute in cache.attributes and cache.d == d and cache.t == t:
            return cache
    return None

def map_float_to_int(value):
    return int(value * 2) - 1

def get_caches_from_gpx(filename):
    namespace = {
        'gpx': 'http://www.topografix.com/GPX/1/0',
        'groundspeak': 'http://www.groundspeak.com/cache/1/0/1' #todo: forse bisogna eliminare l'ultimo 1
    }
    tree = ET.parse(filename)
    root = tree.getroot()
    children = root.findall('gpx:wpt',namespace)

    caches = []
    for child in children:
        cache = child.find('groundspeak:cache', namespace)
        if cache is not None:
            name = child.find('gpx:name', namespace).text
            d = map_float_to_int(float(cache.find('groundspeak:difficulty', namespace).text))
            t = map_float_to_int(float(cache.find('groundspeak:terrain', namespace).text))
            attribute_list = cache.find('groundspeak:attributes', namespace).findall('groundspeak:attribute', namespace)
            attribute_list = [attribute.text for attribute in attribute_list if attribute.attrib['inc'] == '1']

            if len(attribute_list) == 0:
                continue
        print(name, d, t, attribute_list)
        caches.append(Cache(name, d, t, attribute_list))

    return caches

if __name__ == '__main__':

    caches = get_caches_from_gpx(sys.argv[1])
    problem = Problem()
    problem.addConstraint(AllDifferentConstraint())
    matrix_size = 10
    possibilities_matrix = [[set() for column in range(matrix_size)] for row in range(matrix_size)]
    for cache in caches:
        if cache.d <= matrix_size and cache.t <= matrix_size:
            for attribute in cache.attributes:
                possibilities_matrix[cache.d - 1][cache.t - 1].add(attribute)

    for row in range(matrix_size):
        for column in range(matrix_size):
            if len(possibilities_matrix[row][column]) == 0:
                print(f"No cache with difficulty {(row + 1)} and terrain {(column + 1)}")
                exit()
            problem.addVariable(get_index(row, column), list(possibilities_matrix[row][column]))

    solution = problem.getSolution()

    if solution is None:
        print("No solution found")
        exit()

    caches_solution = {}
    for key in solution:
        caches_solution[key] = get_cache_from_attribute(solution[key], get_row_column(key)[0] + 1, get_row_column(key)[1] + 1)
    caches_solution= caches_solution

    # Sort the solution dictionary by keys
    sorted_solution = dict(sorted(solution.items()))

    # Sort the caches_solution dictionary by keys
    sorted_caches_solution = dict(sorted(caches_solution.items()))

    complete_matrix = [[None for column in range(matrix_size)] for row in range(matrix_size)]
    for key in sorted_caches_solution:
        row, column = get_row_column(key)
        complete_matrix[row][column] =f"{sorted_caches_solution[key]} : {sorted_solution[key]}"

    print_matrix(complete_matrix)