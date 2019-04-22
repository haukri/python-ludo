import random
import numpy as np


class LudoPlayerRandom:
    def play(self, state, dice_roll, next_states):
        """
        :param state:
            current state relative to this player
        :param dice_roll:
            [1, 6]
        :param next_states:
            np array of length 4 with each entry being the next state moving the corresponding token.
            False indicates an invalid move. 'play' won't be called, if there are no valid moves.
        :return:
            index of the token that is wished to be moved. If it is invalid, the first valid token will be chosen.
        """
        return random.choice(np.argwhere(next_states != False))[0]
