from Algorithm import *
from Problem_QAP import *

path = 'QAP/had12.dat'
p = Problem_QAP(path)


stopping_criteria = p.problem_size**4 

algorithm = Algorithm(
            problem_size=p.problem_size,
            population_size=50,
            truncation_size=5,
            number_of_generations= int(stopping_criteria/50),
            initial_sigma = 0.3,
            end_sigma = 0.01, 
            cooling_factor= 0.02)



algorithm.run_algorithm(p.get_objective_function)


print(algorithm.best_solution.permutation)
print(algorithm.best_solution.fitness)