from LudoGame import LudoGame
from LudoPlayer import LudoPlayer
import random


ludoPlayer0 = LudoPlayer(0)
ludoPlayer1 = LudoPlayer(1)
ludoPlayer2 = LudoPlayer(2)
ludoPlayer3 = LudoPlayer(3)
players = [ludoPlayer0, ludoPlayer1, ludoPlayer2, ludoPlayer3]

score = [0, 0, 0, 0]

for i in range(1000):
    random.shuffle(players)
    ludo = LudoGame(players)
    winner = ludo.playFullGame()
    score[winner] += 1

print(score)
