"""Search Algos: MiniMax, AlphaBeta
"""
#TODO: you can import more modules, if needed
#TODO: update ALPHA_VALUE_INIT, BETA_VALUE_INIT in utils
import time
import numpy as np
import math
ALPHA_VALUE_INIT = -np.inf
BETA_VALUE_INIT = np.inf  # !!!!!

class SearchAlgos:
    def __init__(self, utility, succ, perform_move=None, goal=None):
        """The constructor for all the search algos.
        You can code these functions as you like to, 
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move
        self.goal = goal

    def search(self, state, depth, maximizing_player):
        pass


class MiniMax(SearchAlgos):

    def search(self, state, depth, maximizing_player):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        turn = state.turn
        #if turn == maximizing_player:
        #    direction = state.direction
        #else:
        #    direction = None
        if self.goal(state) or depth == 0:
            return self.utility(state), state.direction
        children = self.succ(state)
        if turn == maximizing_player:
            currMax = -np.inf
            currV = None
            for c in children:
                v = self.search(c, depth-1, maximizing_player)
                if v[0] > currMax:
                    currMax = v[0]
                    currV = v
            return currV
        else:
            currMin = np.inf
            currV = None
            for c in children:
                v = self.search(c, depth-1, maximizing_player)
                if v[0] < currMin:
                    currMin = v[0]
                    currV = v
            return currV
        #TODO: erase the following line and implement this function.
        # raise NotImplementedError




class AlphaBeta(SearchAlgos):

    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        turn = state.turn
        if self.goal(state) or depth == 0:
            return self.utility(state), state.direction
        children = self.succ(state)
        if turn == maximizing_player:
            currMax = -np.inf
            currV = None
            for c in children:
                v = self.search(c, depth-1, maximizing_player, alpha, beta)
                if v[0] > currMax:
                    currMax = v[0]
                    currV = v
                alpha = max(currMax, alpha)
                if currMax >= beta:
                    return np.inf, state.direction
            return currV
        else:
            currMin = np.inf
            currV = None
            for c in children:
                v = self.search(c, depth-1, maximizing_player)
                if v[0] < currMin:
                    currMin = v[0]
                    currV = v
                beta = min(currMin, beta)
                if currMin <= alpha:
                    return -np.inf, state.direction
            return currV