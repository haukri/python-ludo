import random


class LudoPlayerRandom:

    def __init__(self, playerId):
        self.playerId = playerId
        pass

    def play(self, diceRoll, playerPositions):
        return random.randint(0, 3)
