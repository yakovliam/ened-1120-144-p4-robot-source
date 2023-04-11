class StateToken:

    def __init__(self, state=False):
        self.state = state

    def flag(self):
        self.state = True

    def unflag(self):
        self.state = False

    def is_flagged(self):
        return self.state