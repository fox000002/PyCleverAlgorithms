from undefined_exception import UndefinedError

class Problem:
    def assess(self, candidate_solution):
        raise UndefinedError("A problem has not been defined")
  
    def is_optimal(self, candidate_solution):
        raise UndefinedError("A problem has not been defined")
