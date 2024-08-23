import numpy as np
from Model import *
from RK import *
import math
import time


class Algorithm:
    def __init__(self,
                problem_size,
                population_size,
                truncation_size,
                number_of_generations=100,
                time_limit = None,
                initial_sigma = 0.3, 
                end_sigma = 0.1, 
                cooling_factor= None,
                cooling_scheme = 'linear' #options 'linear', 'sigmoid'
                ):
        self.problem_size = problem_size
        self.population_size = population_size
        self.truncation_size = truncation_size
        self.number_of_generations = number_of_generations
        self.initial_sigma = initial_sigma
        self.end_sigma = end_sigma
        self.cooling_scheme = cooling_scheme
        self.time_limit = time_limit
        self.cooling_factor = cooling_factor



           
    def run_algorithm(self, objective_function):
        
        #run first iteration
        start_time = time.time()
        sigma = self.initial_sigma
        population = []
        for _ in range(self.population_size):
            solution = [np.random.random() for i in range(self.problem_size)]
            rk = RK(solution)
            rk.fitness = objective_function(rk.permutation)
            population.append(rk)
        best_solution = min(population)
        self.best_solution = best_solution
        model = Model.get_model(population, self.truncation_size)
        end_time = time.time()
        duration = end_time - start_time 
        
        if(self.time_limit is not None):
            number_of_generations = round(self.time_limit/duration)
        else: 
            number_of_generations = self.number_of_generations-1  
            
        if(self.cooling_factor is None):
            cooling_factor = 1/number_of_generations
        else:
            cooling_factor = self.cooling_factor
               
        for j in range(number_of_generations):
            if(self.cooling_scheme.lower() == 'linear'):
                temp_sigma = (1-(cooling_factor*j)) * self.initial_sigma
            elif(self.cooling_scheme.lower() == 'sigmoid'):
                temp_sigma = ((1/(1+math.exp((10*j)/number_of_generations))) * self.initial_sigma * 2) 
            else:
                raise NotImplementedError('Please set cooling scheme to "linear" or "sigmoid"')
            if(temp_sigma > self.end_sigma):
                sigma = temp_sigma
            population = []
            for k in range(self.population_size):
                solution = Model.get_child(model, sigma)
                rk = RK(solution)
                rk.fitness = objective_function(rk.permutation)
                population.append(rk)
            best_solution = min(population)
            if (best_solution < self.best_solution):
                self.best_solution= best_solution
            model = Model.get_model(population, self.truncation_size)
        end_time = time.time()
        duration = end_time - start_time 
        self.total_duration = duration