from undefined_exception import UndefinedError


class Strategy:
    def __init__(self):
        pass

    def execute(self, problem):
        raise UndefinedError("A strategy has not been defined!")
