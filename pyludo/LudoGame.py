import random
import logging
import numpy as np
from pyludo.utils import player_colors


class LudoState:
    def __init__(self, state=None, empty=False):
        if state is not None:
            self.state = state
        else:
            self.state = np.empty((4, 4), dtype=np.int)  # 4 players, 4 tokens per player
            if not empty:
                self.state.fill(-1)

    def copy(self):
        return LudoState(self.state.copy())

    def __getitem__(self, item):
        return self.state[item]

    def __iter__(self):
        return self.state.__iter__()

    def get_relative_to_player(self, rel_player_id, keep_player_order=False):
        if rel_player_id == 0:
            return self.copy()

        rel = LudoState(empty=True)
        new_player_ids = list(range(4)) if keep_player_order else [(x - rel_player_id) % 4 for x in range(4)]

        for player_id, player_tokens in enumerate(self):
            new_player_id = new_player_ids[player_id]
            for token_id, token_pos in enumerate(player_tokens):
                if token_pos == -1 or token_pos == 99:  # start and end pos are independent of player id
                    rel[new_player_id][token_id] = token_pos
                elif token_pos < 52:  # in common area
                    rel[new_player_id][token_id] = (token_pos - rel_player_id * 13) % 52
                else:  # in end area, 52 <= x < 52 + 20
                    rel[new_player_id][token_id] = ((token_pos - 52 - rel_player_id * 5) % 20) + 52

        return rel

    def move_token(self, token_id, dice_roll, is_jump=False):
        """ move token for player 0 """
        cur_pos = self[0][token_id]
        if cur_pos == 99:
            return False  # can't move tokens in goal

        new_state = self.copy()
        player = new_state[0]
        opponents = new_state[1:]

        # start move
        if cur_pos == -1:
            if dice_roll != 6:
                return False  # can only enter the board by rolling a 6
            player[token_id] = 1
            opponents[opponents == 1] = -1
            return new_state

        target_pos = cur_pos + dice_roll

        # common area move
        if target_pos < 52:
            occupants = opponents == target_pos
            occupant_count = np.sum(occupants)
            if occupant_count > 1 or (occupant_count == 1 and self.is_globe_pos(target_pos)):
                player[token_id] = -1  # sends self home
                return new_state
            if occupant_count == 1:
                opponents[occupants] = -1
            player[token_id] = target_pos
            star_jump_length = 0 if is_jump else self.star_jump(target_pos)
            if star_jump_length:
                if target_pos == 51:  # landed on the last star
                    player[token_id] = 99  # send directly to goal
                else:
                    new_state = new_state.move_token(token_id, star_jump_length, is_jump=True)
            return new_state

        # end zone move
        if target_pos == 57:  # token reached goal
            player[token_id] = 99
        elif target_pos < 57:  # no goal bounce
            player[token_id] = target_pos
        else:  # bounce back from goal pos
            player[token_id] = 57 - (target_pos - 57)
        return new_state

    def get_winner(self):
        for player_id in range(4):
            if np.all(self[player_id] == 99):
                return player_id
        return -1

    @staticmethod
    def star_jump(pos):
        if pos % 13 == 6:
            return 6
        if pos % 13 == 12:
            return 7
        return 0

    @staticmethod
    def is_globe_pos(pos):
        if pos % 13 == 1:
            return True
        if pos % 13 == 9:
            return True
        return False


class LudoGame:
    def __init__(self, players, state=None, info=False):
        assert len(players) == 4, "there must be four players in the game"
        self.players = players
        self.currentPlayerId = -1
        self.state = LudoState() if state is None else state

        if info:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.WARNING)

    def step(self):
        state = self.state
        self.currentPlayerId = (self.currentPlayerId + 1) % 4
        player = self.players[self.currentPlayerId]

        dice_roll = random.randint(1, 6)
        logging.info("Dice roll: {} - {}".format(dice_roll, player_colors[self.currentPlayerId]))

        relative_state = state.get_relative_to_player(self.currentPlayerId)
        rel_next_states = np.array(
            [relative_state.move_token(token_id, dice_roll) for token_id in range(4)]
        )
        if np.any(rel_next_states != False):
            token_id = player.play(relative_state, dice_roll, rel_next_states)
            if rel_next_states[token_id] is False:
                logging.warning("Player chose invalid move. Choosing first valid move.")
                token_id = np.argwhere(rel_next_states != False)[0][0]
            self.state = rel_next_states[token_id].get_relative_to_player((-self.currentPlayerId) % 4)

    def play_full_game(self):
        while self.state.get_winner() == -1:
            self.step()
        return self.state.get_winner()
