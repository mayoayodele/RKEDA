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
            cooling_scheme = 'sigmoid'
            )


h = np.array(p.flow_matrix, dtype = 'int64')
d = np.array(p.distance_matrix, dtype = 'int64')




algorithm.run_algorithm(Problem_QAP.get_objective_function(h, d ))


print(algorithm.best_solution.permutation)
print(algorithm.best_solution.fitness)


