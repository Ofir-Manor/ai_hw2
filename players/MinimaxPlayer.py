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
        self.board
        # TODO: erase the following line and implement this function.
        raise NotImplementedError



    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed



    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, an
    def succ(self, state):
        if state[0]:
            if self.playerSoldiersToPlace > 0:
                for place in range(24):
                    if self.board[place] == 0:
                        self.playerPositions[9 - self.playerSoldiersToPlace] = place
                        self.board[place] = 1
                        self.playerSoldiersToPlace -= 1
                        self.playerSoldiersRemaining += 1


    #state is a list [turn, board, player soldiers, rival soldiers, player incomplete mills, rival incomplete mills]