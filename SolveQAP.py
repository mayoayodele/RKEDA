from Algorithm import *
from Problem_QAP import *

path = 'QAP/had12.dat'
p = Problem_QAP(path)


stopping_criteria = p.problem_size**4

algorithm = Algorithm(
            problem_size=p.problem_size,
            population_size=50,
            truncation_size=5,
            #termination= ("number_of_generations", int(stopping_criteria/50)),
            termination= ("time_limit", 1),
            #initial_sigma=0.15,
            #cooling_scheme = 'sigmoid',
            cooling_scheme = 'linear',
            )


h = np.array(p.flow_matrix, dtype = 'int64')
d = np.array(p.distance_matrix, dtype = 'int64')



for i in range(10):
    algorithm.run_algorithm(Problem_QAP.get_objective_function(h, d ))


    print(algorithm.best_solution.permutation)
    print(algorithm.best_solution.fitness)
    print(algorithm.total_duration)


