class Value:
    def __init__(self, val=None):
        if val is not None:
            self.amount = val.amount
        else:
            self.amount = 0
