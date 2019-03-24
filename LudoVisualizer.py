import pyglet
from pyglet import clock
import re
from collections import defaultdict
from LudoGame import LudoGame
from LudoPlayer import LudoPlayer


class LudoVisualizer(pyglet.window.Window):

    def __init__(self):
        super(LudoVisualizer, self).__init__()

        self.ludoPlayer0 = LudoPlayer(0)
        self.ludoPlayer1 = LudoPlayer(1)
        self.ludoPlayer2 = LudoPlayer(2)
        self.ludoPlayer3 = LudoPlayer(3)
        self.ludo = LudoGame([self.ludoPlayer0, self.ludoPlayer1, self.ludoPlayer2, self.ludoPlayer3], info=False)
        # Load sprites
        self.width, self.height = 600, 600
        greenPlayerImage = pyglet.resource.image('greenPlayer.png')
        bluePlayerImage = pyglet.resource.image('bluePlayer.png')
        redPlayerImage = pyglet.resource.image('redPlayer.png')
        yellowPlayerImage = pyglet.resource.image('yellowPlayer.png')
        self.playerImages = [greenPlayerImage, bluePlayerImage, redPlayerImage, yellowPlayerImage]
        self.backgroundImage = pyglet.image.load('ludoboard.png')
        self.scaling = min(self.backgroundImage.height, self.height)/max(self.backgroundImage.height, self.height)

        self.playerPositions = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]

        self.states = []
        self.actions = defaultdict(list)
        with open('stateRepresentation.txt') as f:
            lines = f.readlines()
            for line in lines:
                m = re.findall(r'\((\d+), (\d+)\)', line)
                self.states.append((int(m[0][0]), int(m[0][1])))
                for state in m[1:]:
                    self.actions[(int(m[0][0]), int(m[0][1]))].append((int(state[0]), int(state[1])))
        self.sprites = []
        self.initialPlayerPositions = []
        self.initialPlayerPositions.append([(1, 10), (4, 10), (4, 13), (1, 13)])
        self.initialPlayerPositions.append([(10, 10), (13, 10), (13, 13), (10, 13)])
        self.initialPlayerPositions.append([(10, 1), (13, 1), (13, 4), (10, 4)])
        self.initialPlayerPositions.append([(1, 1), (4, 1), (4, 4), (1, 4)])
        for playerId, positions in enumerate(self.playerPositions):
            players = []
            for tokenId, position in enumerate(positions):
                sprite = pyglet.sprite.Sprite(self.playerImages[playerId])
                sprite.scale = self.scaling
                if position == -1:
                    sprite.position = self.indexToPixel(self.initialPlayerPositions[playerId][tokenId])
                else:
                    sprite.position = self.indexToPixel(self.states[position])
                players.append(sprite)
            self.sprites.append(players)
        self.backgroundSprite = pyglet.sprite.Sprite(self.backgroundImage)
        self.backgroundSprite.scale = min(self.backgroundImage.height, self.height)/max(self.backgroundImage.height, self.height)

    def indexToPixel(self, index):
        return (index[0]*self.scaling*50.0, index[1]*self.scaling*50.0)

    def pixelToIndex(self, pixel):
        return (int(pixel[0]/self.scaling/50.0), int(pixel[1]/self.scaling/50.0))

    def on_draw(self):
        self.clear()
        self.backgroundSprite.draw()
        for teamId, team in enumerate(self.playerPositions):
            for tokenId, token in enumerate(team):
                if token == -1:
                    self.sprites[teamId][tokenId].position = self.indexToPixel(self.initialPlayerPositions[teamId][tokenId])
                elif token != 99:
                    self.sprites[teamId][tokenId].position = self.indexToPixel(self.states[token])
                elif token == 99:
                    self.sprites[teamId][tokenId].position = self.indexToPixel((7, 7))
        for team in self.sprites:
            for player in team:
                player.draw()

    def play(self, dt):
        self.playerPositions = self.ludo.playStep()
        if self.playerPositions:
            clock.schedule_once(self.play, 0.1)
        else:
            print("And the winner is", self.ludo.winner, "!")
            exit()

    def on_key_press(self, symbol, modifiers):
        if symbol == 32:
            self.play(1)


if __name__ == '__main__':
    window = LudoVisualizer()
    pyglet.app.run()
