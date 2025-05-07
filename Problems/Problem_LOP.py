import random as rd

class Problem_LOP:
    def __init__(self, size, cost_matrix):
        self.problem_size = size
        self.matrix = cost_matrix
        self.best_known = None
   
    def get_objective_function(self, solution):
        if len(solution) != self.problem_size: return False
        cumsum = 0
        for i in range(0, len(solution) - 1):
            for j in range(i + 1, len(solution)):
                cumsum += self.matrix[solution[i], solution[j]]
        return cumsum

    @staticmethod
    def compare_solutions(self, solution1_fitness, solution2_fitness):
        if solution1_fitness > solution2_fitness:
            return solution1_fitness
        else:
            return solution2_fitness

    def is_symmetric(self):
        for i in range(self.problem_size):
            for j in range(i+1, self.problem_size):
                if self.matrix[i, j] != self.matrix[j, i]:
                    return False
        return True


def read_lolib_instance(filename):
    """Read data for a LOP problem from file in LOLIB format."""
    try:
        if len(filename) > 3 and filename[-3:] == ".gz":  # file compressed with gzip
            import gzip
            f = gzip.open(filename, "rb")
        else:  # usual, uncompressed file
            f = open(filename)
    except IOError:
        print("could not open file", filename)
        exit(-1)

    data = f.read()
    f.close()

    try:
        pass
        data = data.split()
        n = int(data.pop(0))
        matrix = {}  # for n times n flow matrix
        for i in range(n):
            for j in range(n):
                matrix[i, j] = int(data.pop(0))

    except IndexError:
        print("inconsistent data on QAP file", filename)
        exit(-1)
    return Problem_LOP(size=n, cost_matrix=matrix)


if __name__ == "__main__":
    rd.seed(1)
    problem = read_lolib_instance("../Instances/LOP/LOP10instance1.lop")
    permutation = list(range(problem.problem_size))
    rd.shuffle(permutation)
    print(problem.get_objective_function(permutation))
    print("Symmetric matrix: " + str(problem.is_symmetric()))