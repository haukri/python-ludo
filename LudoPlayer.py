import random


class LudoPlayer:

    def __init__(self, playerId):
        self.playerId = playerId
        pass

    def makeDecision(self):
        if self.diceRoll == 6:
            pass
        return 1

    def play(self, diceRoll, playerPositions):
        for i, position in enumerate(playerPositions[self.playerId]):
            if position == 1:
                return i
            if position == -1 and diceRoll == 6 and not any(x == 1 for x in playerPositions[self.playerId]):
                return i
            elif position != -1 and position != 99 and not (diceRoll == 6 and any(x == -1 for x in playerPositions[self.playerId])):
                return i
        return -1
