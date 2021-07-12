import random as r
import copy

class RK:

    def __init__(self, solution):
        self.solution = tuple(solution)
        self.permutation = RK.random_key_to_permutation(solution)
        self.normalised_solution = RK.normalise_ranks(self.permutation)
        self.fitness = None

    
    @staticmethod
    def normalise_ranks(ranks):
        size = len(ranks)
        ranks_temp = copy.deepcopy(ranks)
        AL = [0]*size
        for i in range(size):
            AL[ranks_temp[i]] = float(i/(size-1))
        return AL

    @staticmethod
    def random_key_to_permutation(priorities):
        a = list(range(len(priorities)))
        temp = list(zip(priorities, a))
        temp.sort()
        return ([y for x,y in temp])

    
    def __eq__(self, rk_solution):
        if not isinstance(rk_solution, RK):
            raise ValueError('Check that your solutions are defined and RK')
        else:
            if(len(self.solution) != len(rk_solution.solution)):
                return False
            for i in range(len(self.solution)):
                if(self.solution[i] != rk_solution.solution[i]):
                    return False
            return True

    
    def __lt__(self, rk_solution):
        if not isinstance(rk_solution, RK):
            raise ValueError('Check that your solutions are defined and RK')
        else:
            return self.fitness < rk_solution.fitness


    def __gt__(self, rk_solution):
        if not isinstance(rk_solution, RK):
            raise ValueError('Check that your solutions are defined and RK')
        else:
            return self.fitness > rk_solution.fitness


    def __le__(self, rk_solution):
        if not isinstance(rk_solution, RK):
            raise ValueError('Check that your solutions are defined and RK')
        else:
            return self.fitness <= rk_solution.fitness


    def __ge__(self, rk_solution):
        if not isinstance(rk_solution, RK):
            raise ValueError('Check that your solutions are defined and RK')
        else:
            return self.fitness >=  rk_solution.fitness
