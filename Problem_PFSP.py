

import numpy as np

class Problem_PFSP:
    def __init__(self, path):
        f = open(path, "r")
        file_content = f.read().splitlines()
        file_reader_counter = 1
        problem_properties = file_content[file_reader_counter].split()

        self.number_of_jobs = int(problem_properties[0])
        self.number_of_machines = int(problem_properties[1])
        self.problem_size = self.number_of_jobs
        file_reader_counter = 3
        self.processing_times = [file_content[file_reader_counter+i].split() for i in range(self.number_of_machines)]
        self.processing_times = [[int(i) for i in self.processing_times[j]] for j in range(self.number_of_machines)]


    
    def objective_function_tft(self, solution):
        fitness = 0
        time_table = np.zeros(shape = self.number_of_jobs, dtype = int)
        for y in range(self.number_of_jobs):
            for m in range(self.number_of_machines):
                if (m==0):
                    time_table[m]+=self.processing_times[m][solution[y]]
                else:
                    time_table[m] = max(prev_machine, time_table[m]) + self.processing_times[m][solution[y]]
                prev_machine = time_table[m]
            fitness += time_table[self.number_of_machines-1]
        return fitness