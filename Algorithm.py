import numpy as np
from Model import *
from RK import *



class Algorithm:
    def __init__(self,
                problem_size,
                population_size,
                truncation_size,
                number_of_generations,
                initial_sigma = 0.3, 
                end_sigma = 0.1, 
                cooling_factor= None
                ):
        self.problem_size = problem_size
        self.population_size = population_size
        self.truncation_size = truncation_size
        self.number_of_generations = number_of_generations
        if (cooling_factor is None):
            cooling_factor = 1/number_of_generations
        if(end_sigma is None):
            self.cooling_rates = [((1-(cooling_factor*i)) * initial_sigma) for i in range(number_of_generations)]
        else:
            self.cooling_rates = [((1-(cooling_factor*i)) * initial_sigma) if (((1-(cooling_factor*i)) * initial_sigma) > end_sigma) else end_sigma for i in range(number_of_generations)]


            
    def run_algorithm(self, objective_function):
        model = None
        for j in range(self.number_of_generations):
            sigma = self.cooling_rates[j]
            population = []
            for k in range(self.population_size):
                if(j > 0):
                    solution = Model.get_child(model, sigma)
                else:
                    solution = [np.random.random() for i in range(self.problem_size)]
                rk = RK(solution)
                rk.fitness = objective_function(rk.permutation)
                population.append(rk)
            model = Model.get_model(population, self.truncation_size)
        
        self.best_solution = min(population)
        