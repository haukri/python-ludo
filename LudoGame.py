from collections import defaultdict
import numpy as np
import random
import logging


class LudoGame:

    def __init__(self, players, info=False):
        self.players = players
        self.states = []
        self.actions = defaultdict(list)
        self.playerPositions = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
        self.relativePlayerPositions = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
        self.gameDone = False
        self.winner = -1
        if info:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.WARNING)

    def playStep(self, steps=1):
        for a in range(steps):
            logging.info(str(self.playerPositions))
            for playerId, player in enumerate(self.players):
                self.getRelativePlayerPositions(playerId)
                diceRoll = random.randint(1, 6)
                token = player.play(diceRoll, self.relativePlayerPositions)
                if token != -1 and self.validateMove(playerId, token, diceRoll):
                    self.moveToken(playerId, token, diceRoll)
                if self.checkForWinner(playerId):
                    return False
        return self.playerPositions

    def playFullGame(self):
        while not self.gameDone:
            for playerId, player in enumerate(self.players):
                self.getRelativePlayerPositions(playerId)
                diceRoll = random.randint(1, 6)
                token = player.play(diceRoll, self.relativePlayerPositions)
                if token != -1 and self.validateMove(playerId, token, diceRoll):
                    self.moveToken(playerId, token, diceRoll)
                    if self.checkForWinner(playerId):
                        return self.winner

    def checkForWinner(self, playerId):
        if all(x == 99 for x in self.playerPositions[playerId]):
            self.gameDone = True
            self.winner = playerId
            return True
        return False

    def moveToken(self, playerId, tokenId, moves):
        if moves == 6 and self.playerPositions[playerId][tokenId] == -1:
            self.moveOpponentHome(1 + (playerId * 13))
            self.playerPositions[playerId][tokenId] = 1 + (playerId * 13)
        else:
            targetPos = self.playerPositions[playerId][tokenId] + moves
            relativeTargetPos = self.relativePlayerPositions[playerId][tokenId] + moves
            # If the token will be in the final zone
            if relativeTargetPos >= 52 and relativeTargetPos < 57:
                self.playerPositions[playerId][tokenId] = relativeTargetPos + playerId * 5
            # If the token has reached the goal
            elif relativeTargetPos == 58:
                self.playerPositions[playerId][tokenId] = 99
            # If the token should continue over the wrap around
            elif targetPos >= 52 and relativeTargetPos < 52:
                self.moveOpponentHome(targetPos % 52)
                self.playerPositions[playerId][tokenId] = targetPos % 52
            elif relativeTargetPos < 52:
                self.moveOpponentHome(targetPos)
                self.playerPositions[playerId][tokenId] = targetPos
            else:
                logging.info('Cant move the token you have to roll exact to the goal field!')

    def moveOpponentHome(self, position):
        if self.isOccupied(position):
            self.moveHome(position)

    def isOccupied(self, position):
        for teamId, team in enumerate(self.playerPositions):
            for tokenId, token in enumerate(team):
                if token == position:
                    return True
        return False

    def occupant(self, position):
        for teamId, team in enumerate(self.playerPositions):
            for tokenId, token in enumerate(team):
                if token == position:
                    return (teamId, tokenId)

    def moveHome(self, position):
        for teamId, team in enumerate(self.playerPositions):
            for tokenId, token in enumerate(team):
                if token == position:
                    self.playerPositions[teamId][tokenId] = -1

    def positionToPlayerToken(self, position):
        return (int(position / 4), int(position % 4))

    def validateMove(self, player, token, diceRoll):
        playerPos = self.relativePlayerPositions[player][token]
        if playerPos == -1:
            if diceRoll != 6:
                logging.info('You have to roll a six to get out!')
                return False
            elif self.isOccupied(1 + (player * 13)):
                teamId, tokenId = self.occupant(1 + (player * 13))
                if teamId == player:
                    logging.info('Your token is already on the start field!')
                    return False
        elif playerPos == 99:
            logging.info('Trying to move a token that is already reached the goal!')
            return False
        else:
            for tokenPos in self.relativePlayerPositions[player]:
                if playerPos + diceRoll == tokenPos:
                    logging.info("Your token is already on this field!")
                    return False
        return True

    def getRelativePlayerPositions(self, playerId):
        for teamId, team in enumerate(self.playerPositions):
            for tokenId, tokenPos in enumerate(team):
                if tokenPos == -1:
                    self.relativePlayerPositions[teamId][tokenId] = -1
                elif tokenPos != -1 and tokenPos < 52:
                    self.relativePlayerPositions[teamId][tokenId] = (tokenPos - playerId * 13) % 52
                elif tokenPos != -1 and tokenPos >= 52 and tokenPos < 99:
                    self.relativePlayerPositions[teamId][tokenId] = ((tokenPos - 52 - playerId * 5) % 20) + 52
                elif tokenPos == 99:
                    self.relativePlayerPositions[teamId][tokenId] = 99
