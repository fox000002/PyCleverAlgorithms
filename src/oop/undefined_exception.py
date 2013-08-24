class UndefinedError(BaseException): 
    def __init__(self, info):
        self.info = info
