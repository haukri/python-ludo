from collections import defaultdict
import numpy as np
import random
import logging


class LudoGame:

    def __init__(self, players, info=False):
        self.players = players
        self.states = []
        self.actions = defaultdict(list)
        self.boardPositions = np.full((72, 1), -1)
        self.greenBoardOffset = np.array(list(range(72)))
        self.playerPositions = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
        self.relativePlayerPositions = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
        self.gameDone = False
        self.winner = -1
        # beginner = random.randint(0, 3)
        # playerOrder = list(range(beginner, 4)) + list(range(0, beginner))
        # for index, order in enumerate(playerOrder):
        #     self.players[order] = players[index]
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
                if self.checkForWinner():
                    return False
                else:
                    return self.playerPositions

    def playFullGame(self):
        while not self.gameDone:
            for playerId, player in enumerate(self.players):
                self.getRelativePlayerPositions(playerId)
                diceRoll = random.randint(1, 6)
                token = player.play(diceRoll, self.relativePlayerPositions)
                if token != -1 and self.validateMove(playerId, token, diceRoll):
                    self.moveToken(playerId, token, diceRoll)
                if self.checkForWinner():
                    return self.winner

    def checkForWinner(self):
        for playerId in range(4):
            if all(x == 99 for x in self.playerPositions[playerId]):
                self.gameDone = True
                self.winner = playerId
                return True
        return False

    def moveToken(self, playerId, tokenId, moves):
        if moves == 6 and self.relativePlayerPositions[playerId][tokenId] == -1:
            self.playerPositions[playerId][tokenId] = 1 + (playerId * 13)
            # Move opponent token home
            if self.boardPositions[self.playerPositions[playerId][tokenId]] / 4 != playerId and self.boardPositions[self.playerPositions[playerId][tokenId]] > 0:
                opponentId, opponentTokenId = self.positionToPlayerToken(self.boardPositions[self.playerPositions[playerId][tokenId]])
                self.playerPositions[opponentId][opponentTokenId] = -1
            self.boardPositions[1 + (playerId * 13)] = playerId * 4 + tokenId
        else:
            targetPos = self.playerPositions[playerId][tokenId] + moves
            relativeTargetPos = self.relativePlayerPositions[playerId][tokenId] + moves
            # If the token will be in the final zone
            if relativeTargetPos >= 52 and relativeTargetPos < 57:
                self.boardPositions[self.playerPositions[playerId][tokenId]] = -1
                self.playerPositions[playerId][tokenId] = relativeTargetPos + playerId * 5
                self.boardPositions[self.playerPositions[playerId][tokenId]] = playerId * 4 + tokenId
            # If the token has reached the goal
            elif relativeTargetPos == 58:
                self.boardPositions[self.playerPositions[playerId][tokenId]] = -1
                self.playerPositions[playerId][tokenId] = 99
            # If the token should continue over the wrap around
            elif targetPos >= 52 and relativeTargetPos < 52:
                self.boardPositions[self.playerPositions[playerId][tokenId]] = -1
                self.playerPositions[playerId][tokenId] += moves
                self.playerPositions[playerId][tokenId] %= 52
                # Move opponent token home
                if self.boardPositions[self.playerPositions[playerId][tokenId]] / 4 != playerId and self.boardPositions[self.playerPositions[playerId][tokenId]] > 0:
                    opponentId, opponentTokenId = self.positionToPlayerToken(self.boardPositions[self.playerPositions[playerId][tokenId]])
                    self.playerPositions[opponentId][opponentTokenId] = -1
                self.boardPositions[self.playerPositions[playerId][tokenId]] = playerId * 4 + tokenId
            elif relativeTargetPos < 52:
                self.boardPositions[self.playerPositions[playerId][tokenId]] = -1
                self.playerPositions[playerId][tokenId] += moves
                # Move opponent token home
                if self.boardPositions[self.playerPositions[playerId][tokenId]] / 4 != playerId and self.boardPositions[self.playerPositions[playerId][tokenId]] > 0:
                    opponentId, opponentTokenId = self.positionToPlayerToken(self.boardPositions[self.playerPositions[playerId][tokenId]])
                    self.playerPositions[opponentId][opponentTokenId] = -1
                self.boardPositions[self.playerPositions[playerId][tokenId]] = playerId * 4 + tokenId
                self.correctTokenPositions(playerId, tokenId)
            else:
                logging.info('Cant move the token you have to roll exact to the goal field!')

    def correctTokenPositions(self, playerId, tokenId):
        self.getRelativePlayerPositions(playerId)
        if self.relativePlayerPositions[playerId][tokenId] < 52 and self.playerPositions[playerId][tokenId] >= 52 and self.playerPositions[playerId][tokenId] < 99:
            self.playerPositions[playerId][tokenId] %= 52

    def positionToPlayerToken(self, position):
        return (int(position / 4), int(position % 4))

    def validateMove(self, player, token, diceRoll):
        playerPos = self.relativePlayerPositions[player][token]
        if playerPos == -1:
            if diceRoll != 6:
                logging.info('You have to roll a six to get out!')
                return False
            elif self.boardPositions[1 + (player * 13)] / 4 == player:
                logging.info('Your token is already on the start field!')
                return False
        elif playerPos == 99:
            logging.info('Trying to move a token that is already reached the goal!')
            return False
        else:
            for token in self.relativePlayerPositions[player]:
                if playerPos + diceRoll == token:
                    logging.info("Your token is already on this field!")
                    return False
        return True

    def getRelativePlayerPositions(self, playerId):
        for teamId, team in enumerate(self.playerPositions):
            for tokenId, token in enumerate(team):
                pos = self.playerPositions[teamId][tokenId]
                if pos == -1:
                    self.relativePlayerPositions[teamId][tokenId] = -1
                elif pos != -1 and pos < 52:
                    self.relativePlayerPositions[teamId][tokenId] = (pos - playerId * 13) % 52
                elif pos != -1 and pos >= 52 and pos < 99:
                    self.relativePlayerPositions[teamId][tokenId] = ((pos - 52 - playerId * 5) % 20) + 52
                elif pos == 99:
                    self.relativePlayerPositions[teamId][tokenId] = 99

    def rollDice(self):
        pass
