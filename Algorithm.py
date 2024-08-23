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
        self.initial_sigma = initial_sigma
        self.end_sigma = end_sigma
        
        if(cooling_factor is None):
            self.cooling_factor = 1/number_of_generations
        else:
            self.cooling_factor = cooling_factor
            


            
    def run_algorithm(self, objective_function):
        model = None
        sigma = self.initial_sigma
        for j in range(self.number_of_generations):
            temp_sigma = (1-(self.cooling_factor*j)) * self.initial_sigma
            if(temp_sigma > self.end_sigma):
                sigma = temp_sigma
            population = []
            for k in range(self.population_size):
                if(j > 0):
                    solution = Model.get_child(model, sigma)
                else:
                    solution = [np.random.random() for i in range(self.problem_size)]
                rk = RK(solution)
                rk.fitness = objective_function(rk.permutation)
                population.append(rk)
            best_solution = min(population)
            if(j==0):
                self.best_solution = best_solution
            else:
                if (best_solution < self.best_solution):
                    self.best_solution= best_solution
            model = Model.get_model(population, self.truncation_size)
        