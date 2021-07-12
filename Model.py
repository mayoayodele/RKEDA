import numpy as np

class Model:
    
    @staticmethod
    def get_model(current_population, truncation_size):
        current_population.sort()
        problem_size = len(current_population[0].normalised_solution)
        model = [np.mean([current_population[i].normalised_solution[j] for i in range(truncation_size)]) for j in range(problem_size)]
        return tuple(model)

    @staticmethod
    def get_child(current_model, sigma):
        return [np.random.normal(mean, sigma) for mean in current_model]