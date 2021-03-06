"""Abstract class of player. 
Your players classes must inherit from this.
"""
import utils
import numpy as np
import copy


class AbstractPlayer:
    """Your player must inherit from this class.
    Your player class name must be 'Player', as in the given examples (SimplePlayer, LivePlayer).
    Use like this:
    from players.AbstractPlayer import AbstractPlayer
    class Player(AbstractPlayer):
    """
    def __init__(self, game_time):
        """
        Player initialization.
        """
        self.game_time = game_time
        self.board = np.array(24)
        self.directions = utils.get_directions

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array of the board.
        No output is expected.
        """
        raise NotImplementedError

    def make_move(self, time_limit):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, (pos, soldier, dead_opponent_pos)
        """
        raise NotImplementedError

    def set_rival_move(self, move):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        raise NotImplementedError

    def is_player(self, player, pos1, pos2, board=None):
        """
        Function to check if 2 positions have the player on them
        :param board:
        :param player: 1/2
        :param pos1: position
        :param pos2: position
        :return: boolean value
        """
        if board is None:
            board = self.board
        if board[pos1] == player and board[pos2] == player:
            return True
        else:
            return False

    def check_next_mill(self, position, player, board=None):
        """
        Function to check if a player can make a mill in the next move.
        :param position: curren position
        :param board: np.array
        :param player: 1/2
        :return:
        """
        if board is None:
            board = self.board
        mill = [
            (self.is_player(player, 1, 2, board) or self.is_player(player, 3, 5, board)),
            (self.is_player(player, 0, 2, board) or self.is_player(player, 9, 17, board)),
            (self.is_player(player, 0, 1, board) or self.is_player(player, 4, 7, board)),
            (self.is_player(player, 0, 5, board) or self.is_player(player, 11, 19, board)),
            (self.is_player(player, 2, 7, board) or self.is_player(player, 12, 20, board)),
            (self.is_player(player, 0, 3, board) or self.is_player(player, 6, 7, board)),
            (self.is_player(player, 5, 7, board) or self.is_player(player, 14, 22, board)),
            (self.is_player(player, 2, 4, board) or self.is_player(player, 5, 6, board)),
            (self.is_player(player, 9, 10, board) or self.is_player(player, 11, 13, board)),
            (self.is_player(player, 8, 10, board) or self.is_player(player, 1, 17, board)),
            (self.is_player(player, 8, 9, board) or self.is_player(player, 12, 15, board)),
            (self.is_player(player, 3, 19, board) or self.is_player(player, 8, 13, board)),
            (self.is_player(player, 20, 4, board) or self.is_player(player, 10, 15, board)),
            (self.is_player(player, 8, 11, board) or self.is_player(player, 14, 15, board)),
            (self.is_player(player, 13, 15, board) or self.is_player(player, 6, 22, board)),
            (self.is_player(player, 13, 14, board) or self.is_player(player, 10, 12, board)),
            (self.is_player(player, 17, 18, board) or self.is_player(player, 19, 21, board)),
            (self.is_player(player, 1, 9, board) or self.is_player(player, 16, 18, board)),
            (self.is_player(player, 16, 17, board) or self.is_player(player, 20, 23, board)),
            (self.is_player(player, 16, 21, board) or self.is_player(player, 3, 11, board)),
            (self.is_player(player, 12, 4, board) or self.is_player(player, 18, 23, board)),
            (self.is_player(player, 16, 19, board) or self.is_player(player, 22, 23, board)),
            (self.is_player(player, 6, 14, board) or self.is_player(player, 21, 23, board)),
            (self.is_player(player, 18, 20, board) or self.is_player(player, 21, 22, board))
        ]

        return mill[position]

    def is_mill(self, position, board=None):
        if board is None:
            board = self.board
        """
        Return True if a player has a mill on the given position
        :param position: 0-23
        :return:
        """
        if position < 0 or position > 23:
            return False
        p = int(board[position])

        # The player on that position
        if p != 0:
            # If there is some player on that position
            return self.check_next_mill(position, p, board)
        else:
            return False

    def incomplete_mill_count(self, position, player, board=None):
        # only use after the player is not represented on the board
        if board is None:
            board = self.board

        if position < 0 or position > 23:
            return -5 #maybe some error code

        diff = 0
        adjacent_mills = [
            [[1, 2], [3, 5]],
            [[0, 2], [9, 17]],
            [[0, 1], [4, 7]],
            [[0, 5], [11, 19]],
            [[2, 7], [12, 20]],
            [[0, 3], [6, 7]],
            [[5, 7], [14, 22]],
            [[2, 4], [5, 6]],
            [[9, 10], [11, 13]],
            [[8, 10], [1, 17]],
            [[8, 9], [12, 15]],
            [[3, 19], [8, 13]],
            [[10, 15], [4, 20]],
            [[8, 11], [14, 15]],
            [[13, 15], [6, 22]],
            [[10, 12], [13, 14]],
            [[17, 18], [19, 21]],
            [[16, 18], [1, 9]],
            [[16, 17], [20, 23]],
            [[16, 21], [3, 11]],
            [[18, 23], [4, 12]],
            [[16, 19], [22, 23]],
            [[21, 23], [6, 14]],
            [[18, 20], [21, 22]]
        ]

        incomplete_mill_pos1 = adjacent_mills[position][0][0]
        incomplete_mill_pos2 = adjacent_mills[position][0][1]
        incomplete_mill_pos3 = adjacent_mills[position][1][0]
        incomplete_mill_pos4 = adjacent_mills[position][1][1]

        incomplete_mill1 = ((board[incomplete_mill_pos1] == player and board[incomplete_mill_pos2] == 0) or
                            (board[incomplete_mill_pos1] == 0 and board[incomplete_mill_pos2] == player))
        incomplete_mill2 = ((board[incomplete_mill_pos3] == player and board[incomplete_mill_pos4] == 0) or
                            (board[incomplete_mill_pos3] == 0 and board[incomplete_mill_pos4] == player))
        return incomplete_mill1 + incomplete_mill2

    def player_pos_moves(self, pos, board=None):
        if board is None:
            board = self.board
        possible_moves = 0
        for next_moves in self.directions(pos):
            if board[next_moves] == 0:
                possible_moves += 1

        return possible_moves

    def moves_and_incomp_mills_calc(self, state):
        player_incomp_mills = 0
        player_avail_moves = 0
        rival_incomp_mills = 0
        rival_avail_moves = 0
        for player_pos, rival_pos in zip(state.playerPositions, state.rivalPositions):
            if player_pos >= 0:
                player_avail_moves += self.player_pos_moves(pos=player_pos, board=state.board)
                player_incomp_mills += self.incomplete_mill_count(position=player_pos, player=1, board=state.board)
            if rival_pos >= 0:
                rival_avail_moves += self.player_pos_moves(pos=rival_pos, board=state.board)
                rival_incomp_mills += self.incomplete_mill_count(position=rival_pos, player=2, board=state.board)

        return player_incomp_mills/2, player_avail_moves, rival_incomp_mills/2, rival_avail_moves


class State:
    def __init__(self):
        self.turn = True
        self.board = None
        self.playerSoldiersToPlace = 9
        self.rivalSoldiersToPlace = 9
        self.playerSoldiersRemaining = 0
        self.rivalSoldiersRemaining = 0
        self.playerIncompleteMills = 0
        self.rivalIncompleteMills = 0
        self.playerAvailableMoves = 0
        self.rivalAvailableMoves = 0
        self.playerPositions = np.full(9, -1)
        self.rivalPositions = np.full(9, -1)
        self.direction = None

    def __copy__(self):
        copy_state = State()
        copy_state.turn = self.turn
        copy_state.board = np.copy(self.board)
        copy_state.playerSoldiersToPlace = self.playerSoldiersToPlace
        copy_state.rivalSoldiersToPlace = self.rivalSoldiersToPlace
        copy_state.playerSoldiersRemaining = self.playerSoldiersRemaining
        copy_state.rivalSoldiersRemaining = self.rivalSoldiersRemaining
        copy_state.playerIncompleteMills = self.playerIncompleteMills
        copy_state.rivalIncompleteMills = self.playerIncompleteMills
        copy_state.playerAvailableMoves = self.playerAvailableMoves
        copy_state.rivalAvailableMoves = self.rivalAvailableMoves
        copy_state.playerPositions = np.copy(self.playerPositions)
        copy_state.rivalPositions = np.copy(self.rivalPositions)
        copy_state.direction = self.direction

        return copy_state

