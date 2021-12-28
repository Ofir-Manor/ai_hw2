"""
MiniMax Player
"""
import numpy as np

from players.AbstractPlayer import AbstractPlayer
#TODO: you can import more modules, if needed

class Player(AbstractPlayer):
    def __init__(self, game_time):
        AbstractPlayer.__init__(self, game_time) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        #TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.playerSoldiersToPlace = 9
        self.rivalSoldiersToPlace = 9
        self.playerSoldiersRemaining = 0
        self.rivalSoldiersRemaining = 0
        self.playerIncompleteMills = 0
        self.rivalIncompleteMills = 0
        self.playerPositions = np.empty(9, dtype=int)
        self.rivalPositions = np.empty(9, dtype=int)


    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, of the board.
        No output is expected.
        """
        for i in self.playerPositions:
            self.playerPositions[i] = -1
            self.rivalPositions[i] = -1
        # TODO: erase the following line and implement this function.
        raise NotImplementedError

    def make_move(self, time_limit):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement
        """
        #TODO: erase the following line and implement this function.
        raise NotImplementedError

    def set_rival_move(self, move):
        """Update your info, given the new position of the rival.
        input:
            - move: tuple, the new position of the rival.
        No output is expected
        """
        self.board[move[0]] = 2
        self.rivalPositions[move[1]] = move[0]
        self.playerIncompleteMills += self.is_incomplete_mill(move[0])
        if move[2] != -1:
            self.playerSoldiersRemaining -= 1
            self.playerIncompleteMills -= self.is_incomplete_mill(move[2])
            self.board[move[2]] = 0
            for player in self.playerPositions:
                if player == move[2]:
                    self.playerPositions[player] = -1


        # TODO: erase the following line and implement this function.
        raise NotImplementedError



    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed
    def state_parser(self, state):
        for i in state:
            yield i

    # def succ_phase1_player(self, state):

    # def succ_phase1_rival(self,state):

    # def succ_phase2_player(self,state):

    # def succ_phase2_rival(self,state):

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, an
    def goal(self,state):
        player_soldiers_remaining = state[6]
        rival_soldiers_remaining = state[7]

        if player_soldiers_remaining < 3 or rival_soldiers_remaining < 3:
            return True
        return False

    def succ(self, state):
        turn, board, player_positions, rival_positions, player_soldiers_to_place, rival_soldiers_to_place, \
            player_soldiers_remaining, rival_soldiers_remaining, player_incomplete_mills, rival_incomplete_mills = \
            self.state_parser(state)

        if turn:
            if player_soldiers_to_place > 0:
                for pos in range(24):
                    if board[pos] == 0:
                        board[pos] = 1
                        player_positions[9-player_soldiers_to_place] = pos
                        player_soldiers_to_place -= 1
                        #check incomplete mills
                        if self.is_mill(pos, board):
                            for rival in range(9-rival_soldiers_to_place):
                                if rival_positions[rival] >= 0:
                                    board[rival_positions[rival]] = 0
                                    rival_soldiers_remaining -= 1
                                    #check incomplete mills
                                    return [not turn, board, player_positions, rival_positions, player_soldiers_to_place
                                        , rival_soldiers_to_place, player_soldiers_remaining, rival_soldiers_remaining,
                                            player_incomplete_mills, rival_incomplete_mills]
                        else:
                            return [not turn, board, player_positions, rival_positions, player_soldiers_to_place,
                                    rival_soldiers_to_place, player_soldiers_remaining, rival_soldiers_remaining,
                                    player_incomplete_mills, rival_incomplete_mills]
            else:
                for soldier in player_positions:
                    if soldier >= 0:
                        for pos in self.directions[soldier]:
                            if board[pos] == 0:
                                player_positions[soldier] = pos
                                #check incomplete mills
                                if self.is_mill(pos, board):
                                    for rival in range(9 - rival_soldiers_to_place):
                                        if rival_positions[rival] >= 0:
                                            board[rival_positions[rival]] = 0
                                            rival_soldiers_remaining -= 1
                                            # check incomplete mills
                                            return [not turn, board, player_positions, rival_positions,
                                                    player_soldiers_to_place, rival_soldiers_to_place,
                                                    player_soldiers_remaining, rival_soldiers_remaining,
                                                    player_incomplete_mills, rival_incomplete_mills]
                                else:
                                    return [not turn, board, player_positions, rival_positions,
                                            player_soldiers_to_place, rival_soldiers_to_place, player_soldiers_remaining
                                        , rival_soldiers_remaining, player_incomplete_mills, rival_incomplete_mills]
        else:
            if rival_soldiers_to_place > 0:
                for pos in range(24):
                    if board[pos] == 0:
                        board[pos] = 1
                        rival_positions[9-rival_soldiers_to_place] = pos
                        rival_soldiers_to_place -= 1
                        #check incomplete mills
                        if self.is_mill(pos, board):
                            for player in range(9-player_soldiers_to_place):
                                if player_positions[player] >= 0:
                                    board[player_positions[player]] = 0
                                    player_soldiers_remaining -= 1
                                    #check incomplete mills
                                    return [not turn, board, player_positions, rival_positions, player_soldiers_to_place
                                        , rival_soldiers_to_place, player_soldiers_remaining, rival_soldiers_remaining,
                                            player_incomplete_mills, rival_incomplete_mills]
                        else:
                            return [not turn, board, player_positions, rival_positions, player_soldiers_to_place,
                                    rival_soldiers_to_place, player_soldiers_remaining, rival_soldiers_remaining,
                                    player_incomplete_mills, rival_incomplete_mills]
            else:
                for soldier in rival_positions:
                    if soldier >= 0:
                        for pos in self.directions[soldier]:
                            if board[pos] == 0:
                                rival_positions[soldier] = pos
                                #check incomplete mills
                                if self.is_mill(pos, board):
                                    for player in range(9 - player_soldiers_to_place):
                                        if player_positions[player] >= 0:
                                            board[player_positions[player]] = 0
                                            player_soldiers_remaining -= 1
                                            # check incomplete mills
                                            return [not turn, board, player_positions, rival_positions,
                                                    player_soldiers_to_place
                                                , rival_soldiers_to_place, player_soldiers_remaining,
                                                    rival_soldiers_remaining,
                                                    player_incomplete_mills, rival_incomplete_mills]
                                else:
                                    return [not turn, board, player_positions, rival_positions,
                                            player_soldiers_to_place,
                                            rival_soldiers_to_place, player_soldiers_remaining,
                                            rival_soldiers_remaining,
                                            player_incomplete_mills, rival_incomplete_mills]

    def utility(self, state):
        player_soldiers_remaining = state[6]
        rival_soldiers_remaining = state[7]
        player_incomplete_mills = state[8]
        rival_incomplete_mills = state[9]

        if player_soldiers_remaining < 3:
            return -30
        if rival_soldiers_remaining < 3:
            return 30

        return (player_soldiers_remaining - rival_soldiers_remaining) * 2 + \
               (player_incomplete_mills - rival_incomplete_mills)


    #state is a list [turn, board, player soldiers, rival soldiers, player incomplete mills, rival incomplete mills]