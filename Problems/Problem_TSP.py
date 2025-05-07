import math
import random as rd

class Problem_TSP:
    def __init__(self, size, distance_matrix):
        self.problem_size = size
        self.matrix = distance_matrix
        self.best_known = None

    def get_objective_function(self, solution):
        fitness = self.matrix[solution[-1], solution[0]]
        for i in range(0, len(solution) - 1):
            fitness += self.matrix[solution[i], solution[i + 1]]

        return fitness

    @staticmethod
    def compare_solutions(solution1_fitness, solution2_fitness):
        if solution1_fitness < solution2_fitness:
            return solution1_fitness
        else:
            return solution2_fitness

    def is_symmetric(self):
        for i in range(self.problem_size):
            for j in range(i+1, self.problem_size):
                if self.matrix[i, j] != self.matrix[j, i]:
                    return False
        return True


def read_tsplib(filename):
    "basic function for reading a TSP problem on the TSPLIB format"
    "NOTE: only works for 2D euclidean or manhattan distances"
    f = open(filename, 'r');

    line = f.readline()
    while line.find("EDGE_WEIGHT_TYPE") == -1:
        line = f.readline()

    if line.find("EUC_2D") != -1:
        dist = distL2
    elif line.find("MAN_2D") != -1:
        dist = distL1
    else:
        print("cannot deal with non-euclidean or non-manhattan distances")
        raise Exception

    while line.find("NODE_COORD_SECTION") == -1:
        line = f.readline()

    xy_positions = []
    while 1:
        line = f.readline()
        if line.find("EOF") != -1: break
        (i, x, y) = line.split()
        x = float(x)
        y = float(y)
        xy_positions.append((x, y))

    n, D = mk_matrix(xy_positions, dist)
    return Problem_TSP(size=n, distance_matrix=D)

def distL2(v1,v2):
    """Compute the L2-norm (Euclidean) distance between two points.

    The distance is rounded to the closest integer, for compatibility
    with the TSPLIB convention.

    The two points are located on coordinates (x1,y1) and (x2,y2),
    sent as parameters"""
    x1, y1 = v1
    x2, y2 = v2
    xdiff = x2 - x1
    ydiff = y2 - y1
    return int(math.sqrt(xdiff * xdiff + ydiff * ydiff) + .5)


def distL1(v1, v2):
    """Compute the L1-norm (Manhattan) distance between two points.

    The distance is rounded to the closest integer, for compatibility
    with the TSPLIB convention.

    The two points are located on coordinates (x1,y1) and (x2,y2),
    sent as parameters"""
    x1, y1 = v1
    x2, y2 = v2
    return int(abs(x2 - x1) + abs(y2 - y1) + .5)

def mk_matrix(coord, dist):
    """Compute a distance matrix for a set of points.

    Uses function 'dist' to calculate distance between
    any two points.  Parameters:
    -coord -- list of tuples with coordinates of all points, [(x1,y1),...,(xn,yn)]
    -dist -- distance function
    """
    n = len(coord)
    D = {}  # dictionary to hold n times n matrix
    for i in range(n - 1):
        for j in range(i + 1, n):
            (x1, y1) = coord[i]
            (x2, y2) = coord[j]
            D[i, j] = dist((x1, y1), (x2, y2))
            D[j, i] = D[i, j]
    return n, D


if __name__ == "__main__":
    rd.seed(1)
    problem = read_tsplib("../Instances/TSP/kroA100.tsp")
    permutation = list(range(problem.problem_size))
    rd.shuffle(permutation)
    print(problem.get_objective_function(permutation))
    print("Symmetric matrix: " + str(problem.is_symmetric()))