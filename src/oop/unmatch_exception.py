class UnmatchError(BaseException): 
    def __init__(self, info):
        self.info = info
