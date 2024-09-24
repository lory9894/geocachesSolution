from constraint import *


class Cache:
    def __init__(self, name, d, t, attributes):
        self.name = name
        self.d = d
        self.t = t
        self.attributes = attributes

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name



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



if __name__ == '__main__':
    caches = [Cache("A", 1, 1, ["a", "c"]),Cache("E", 1, 1, ["a", "b"]), Cache("B", 1, 2, ["a"]), Cache("C", 2, 2, ["h"]), Cache("D", 2, 1, ["j", "k", "l"])]

    problem = Problem()
    problem.addConstraint(AllDifferentConstraint())
    matrix_size = 2
    possibilities_matrix = [[set() for column in range(matrix_size)] for row in range(matrix_size)]
    for cache in caches:
        if cache.d <= matrix_size and cache.t <= matrix_size:
            for attribute in cache.attributes:
                possibilities_matrix[cache.d - 1][cache.t - 1].add(attribute)

    for row in range(matrix_size):
        for column in range(matrix_size):
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