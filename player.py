class Player():
    def __init__(self, name):
        self.name = name
        self.score = 0
        # to validate if player did not answer more then once per round
        self.active = True
