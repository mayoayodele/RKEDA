
from numba import njit
import numpy as np

class Problem_QAP:
    def __init__(self, path):
        f = open(path, "r")
        file_content = f.read().splitlines()
        file_reader_counter = 0
        problem_properties = file_content[file_reader_counter].split()
        file_reader_counter+=2

        self.problem_size = int(problem_properties[0])
        try:
            self.best_known = int(problem_properties[1])
        except:
            self.best_known = None

        self.flow_matrix = np.array([np.array(file_content[file_reader_counter +i].split()) for i in range(self.problem_size)], dtype = 'int64')

        try:
            self.distance_matrix = np.array([np.array(file_content[file_reader_counter + self.problem_size + i + 1].split()) for i in range(self.problem_size)], dtype = 'int64')
        except:
            self.distance_matrix = np.array([np.array(file_content[file_reader_counter + self.problem_size + i ].split()) for i in range(self.problem_size)], dtype = 'int64')



    def get_objective_function_slower( self, solution):
        return sum([int(self.flow_matrix[i][j]) *int(self.distance_matrix[solution[i]][solution[j]]) for j in range(self.problem_size) for i in range(self.problem_size) ])

   
    def get_objective_function( flow_matrix, distance_matrix):
        @njit
        def inner(solution):
            fitness = 0
            for i in range(len(solution)):
                for j in range(len(solution)):
                    fitness+=flow_matrix[i][j] *distance_matrix[solution[i]][solution[j]]
            return fitness
        return inner