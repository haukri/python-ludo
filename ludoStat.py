from LudoGame import LudoGame
from LudoPlayer import LudoPlayer
from LudoPlayerRandom import LudoPlayerRandom


ludoPlayer0 = LudoPlayer(0)
ludoPlayer1 = LudoPlayer(1)
ludoPlayer2 = LudoPlayerRandom(2)
ludoPlayer3 = LudoPlayerRandom(3)
players = [ludoPlayer0, ludoPlayer1, ludoPlayer2, ludoPlayer3]

score = [0, 0, 0, 0]

for i in range(1000):
    ludo = LudoGame(players)
    winner = ludo.playFullGame()
    score[winner] += 1
    print('Game ', i, ' done')

print(score)
