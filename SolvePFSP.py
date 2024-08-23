from Algorithm import *
from Problem_PFSP import *

path = 'PFSP/tai20_5_0.fsp'
p = Problem_PFSP(path)


stopping_criteria = p.problem_size**4 

algorithm = Algorithm(
            problem_size=p.problem_size,
            population_size=50,
            truncation_size=5,
            termination= ("number_of_generations", int(stopping_criteria/50)),
            initial_sigma = 0.3)



algorithm.run_algorithm(p.objective_function_tft)


print(algorithm.best_solution.permutation)
print(algorithm.best_solution.fitness)