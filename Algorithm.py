import numpy as np
from Model import *
from RK import *
import math
import datetime


class Algorithm:
    def __init__(self,
                problem_size,
                population_size,
                truncation_size,
                termination = ('time_limit', 1),
                initial_sigma = 0.3, 
                end_sigma = 0.1, 
                cooling_factor= None,
                cooling_scheme = 'linear' #options 'linear', 'sigmoid'
                ):
        if termination[0].lower() == 'time_limit':
            self.time_limit = termination[1]
            self.number_of_generations = None
        elif termination[0].lower() == 'number_of_generations':
            self.number_of_generations = termination[1]
            self.time_limit = None
        else:
            raise NotImplementedError('Please set termination as a tuple ("number_of_generations", 100) or ("time_limit": 1), number of generations or time limit must be a positive integer')
        self.problem_size = problem_size
        self.population_size = population_size
        self.truncation_size = truncation_size
        self.initial_sigma = initial_sigma
        self.end_sigma = end_sigma
        self.cooling_scheme = cooling_scheme
        self.cooling_factor = cooling_factor


    def run_algorithm(self, objective_function):
        if(self.number_of_generations is None):
            self.run_algorithm_time_limit(objective_function)
        else:
            self.run_algorithm_generations(objective_function)
    
    def run_algorithm_generations(self, objective_function):
        #run first iteration
        overall_start_time = datetime.datetime.now()
        sigma = self.initial_sigma
        
        number_of_generations = self.number_of_generations
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
                if(j > 0):
                    solution = Model.get_child(model, sigma)
                else:
                    solution = [np.random.random() for _ in range(self.problem_size)]
                rk = RK(solution)
                rk.fitness = objective_function(rk.permutation)
                population.append(rk)
            best_solution = min(population)
            if(j > 0):
                if (best_solution < self.best_solution):
                    self.best_solution= best_solution
            else:
                self.best_solution= best_solution
            model = Model.get_model(population, self.truncation_size)
            j+=1
        
        overall_end_time = datetime.datetime.now()
        overall_duration = (overall_end_time - overall_start_time).total_seconds()
        self.total_duration = overall_duration

           
    
    
    def run_algorithm_time_limit(self, objective_function):   
        #run first iteration
        overall_start_time = datetime.datetime.now()
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
        end_time = datetime.datetime.now()
        duration = (end_time - overall_start_time).total_seconds()
        overall_duration = duration

        
        
        j = 1
        stopping_criteria = False
        while (stopping_criteria == False):
            start_time = datetime.datetime.now()
            duration_avoid_divisition_by_zero = max(duration, 10**-3)
            number_of_generations = round((self.time_limit - overall_duration) /duration_avoid_divisition_by_zero)
            all_generations = number_of_generations + j 
            if(self.cooling_factor is None):
                cooling_factor = 1/all_generations
            else:
                cooling_factor = self.cooling_factor

            if(self.cooling_scheme.lower() == 'linear'):
                temp_sigma = (1-(cooling_factor*j)) * self.initial_sigma
            elif(self.cooling_scheme.lower() == 'sigmoid'):
                temp_sigma = ((1/(1+math.exp((10*j)/all_generations))) * self.initial_sigma * 2) 
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
            j+=1
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()
            overall_duration = (end_time - overall_start_time).total_seconds()
            #print(j, overall_duration, duration)
            if((overall_duration+ duration) > self.time_limit):
                stopping_criteria = True
        self.evaluations = (j-1) * self.population_size
        self.total_duration = overall_duration