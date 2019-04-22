# pyludo
A python3 ludo simulator. Forked from haukuri.
### install

```
$ git clone https://github.com/RasmusHaugaard/pyludo.git
```
```
$ cd pyludo
```
```
$ pip3 install -e .
```

### examples
Visualize a game with random players
```python
import pyglet
from pyludo import LudoGame, LudoPlayerRandom, LudoVisualizerStep

game = LudoGame([LudoPlayerRandom() for _ in range(4)], info=True)
window = LudoVisualizerStep(game)
pyglet.app.run()
# use left and right arrow to progress game
```

See LudoPlayerRandom.py for instructions of how to write a player.

### implemented rules
* Always four players.
* A player must roll a 6 to enter the board.
* Rolling a 6 does not grant a new dice roll.
* Globe positions are safe positions.
* The start position outside each home is considered a globe position
* A player token landing on a single opponent token sends the opponent token home if it is not on a globe position. If the opponent token is on a globe position the player token itself is sent home.
* A player token landing on two or more opponent tokens sends the player token itself home.
* If a player token lands on one or more opponent tokens when entering the board, all opponent tokens are sent home.
* A player landing on a star is moved to the next star or directly to goal if landing on the last star.
* A player in goal cannot be moved.

