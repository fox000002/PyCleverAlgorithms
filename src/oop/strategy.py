from undefined_exception import UndefinedError

class Strategy:
    def execute(self, problem):
        raise UndefinedError("A strategy has not been defined!")
