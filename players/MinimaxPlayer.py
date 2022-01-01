"""
MiniMax Player
"""
import copy

import numpy as np
import time
import utils

from players.AbstractPlayer import AbstractPlayer, State
#TODO: you can import more modules, if needed
from SearchAlgos import MiniMax

class Player(AbstractPlayer):
    def __init__(self, game_time):
        AbstractPlayer.__init__(self, game_time) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        #TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.currState = State()
        self.searchAlgo = MiniMax(utility=self.utility, succ=self.succ, goal=self.goal)

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, of the board.
        No output is expected.
        """
        self.currState.board = np.copy(board)
        self.board = board
        # TODO: erase the following line and implement this function.
        # raise NotImplementedError

    def make_move(self, time_limit):

        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement
        """
        d = 0
        move = None
        turn_time = 0
        while True:
            start_time = time.time()
            value, move = self.searchAlgo.search(state=self.currState, depth=d, maximizing_player=True)
            d += 1
            end_time = time.time()
            turn_time += end_time - start_time
            if turn_time > time_limit/(24*24):
                break

        self.currState.board[self.currState.playerPositions[move[1]]] = 0
        self.board[self.currState.playerPositions[move[1]]] = 0
        if self.currState.playerSoldiersToPlace > 0:
            self.currState.playerSoldiersRemaining += 1
            self.currState.playerSoldiersToPlace -= 1

        self.currState.playerIncompleteMills += self.incomplete_mill_diff(
            position=self.currState.playerPositions[move[1]], player=1, add=False)
        self.currState.playerIncompleteMills += self.incomplete_mill_diff(position=move[0], player=1, add=True)

        self.currState.board[move[0]] = 1
        self.board[move[0]] = 1
        self.currState.playerPositions[move[1]] = move[0]
        if move[2] != -1:
            self.currState.rivalSoldiersRemaining -= 1
            self.currState.board[move[2]] = 0
            self.currState.rivalIncompleteMills += self.incomplete_mill_diff(position=move[2], player=2, add=False)
            for rival, pos in enumerate(self.currState.rivalPositions):
                if pos == move[2]:
                    self.currState.rivalPositions[rival] = -1

        self.currState.turn = False
        utils.printBoard(self.currState.board)
        return move
        #TODO: erase the following line and implement this function.
        # raise NotImplementedError

    def set_rival_move(self, move):
        """Update your info, given the new position of the rival.
        input:
            - move: tuple, the new position of the rival.
        No output is expected
        """
        self.currState.board[self.currState.rivalPositions[move[1]]] = 0
        if self.currState.rivalSoldiersToPlace > 0:
            self.currState.rivalSoldiersRemaining += 1
            self.currState.rivalSoldiersToPlace -= 1
        self.board[self.currState.rivalPositions[move[1]]] = 0

        self.currState.rivalIncompleteMills += self.incomplete_mill_diff(
            position=self.currState.rivalPositions[move[1]], player=2, add=False)
        self.currState.rivalIncompleteMills += self.incomplete_mill_diff(position=move[0], player=2, add=True)

        self.currState.board[move[0]] = 2
        self.currState.rivalPositions[move[1]] = move[0]
        if move[2] != -1:
            self.currState.playerSoldiersRemaining -= 1
            self.currState.board[move[2]] = 0
            self.currState.playerIncompleteMills += self.incomplete_mill_diff(position=move[2], player=1,
                                                                                        add=False)
            for player, pos in enumerate(self.currState.playerPositions):
                if pos == move[2]:
                    self.currState.playerPositions[player] = -1


        self.currState.turn = True
        # TODO: erase the following line and implement this function.
        #raise NotImplementedError



    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    def succ_phase1_player(self, state):
        states = []
        for pos in range(24):
            next_state = state.__copy__()
            next_state.turn = not next_state.turn
            soldier_to_place = 9 - next_state.playerSoldiersToPlace
            if next_state.board[pos] == 0:
                next_state.playerIncompleteMills += self.incomplete_mill_diff(position=pos, player=1, add=True,
                                                                              board=next_state.board)
                next_state.board[pos] = 1
                next_state.playerPositions[soldier_to_place] = pos
                next_state.playerSoldiersToPlace -= 1

                next_state.playerSoldiersRemaining += 1
                if self.is_mill(position=pos, board=next_state.board):
                    for rival in range(9 - next_state.rivalSoldiersToPlace):
                        if next_state.rivalPositions[rival] >= 0:
                            tmp = next_state.rivalPositions[rival]
                            next_state.board[tmp] = 0
                            next_state.rivalIncompleteMills += self.incomplete_mill_diff(position=tmp, player=2,
                                                                                         add=False, board=next_state.board)
                            next_state.rivalPositions[rival] = -1
                            next_state.rivalSoldiersRemaining -= 1
                            if next_state.direction is None:
                                next_state.direction = (pos, soldier_to_place, tmp)
                            states.append(next_state)
                else:
                    if next_state.direction is None:
                        next_state.direction = (pos, soldier_to_place, -1)
                    states.append(next_state)
        return states

    def succ_phase1_rival(self, state):
        states = []
        for pos in range(24):
            next_state = state.__copy__()
            next_state.turn = not next_state.turn
            soldierToPlace = 9 - next_state.rivalSoldiersToPlace
            if next_state.board[pos] == 0:
                next_state.rivalIncompleteMills += self.incomplete_mill_diff(position=pos, player=2, add=True,
                                                                             board=next_state.board)
                next_state.board[pos] = 2
                next_state.rivalPositions[soldierToPlace] = pos
                next_state.rivalSoldiersToPlace -= 1
                next_state.rivalSoldiersRemaining += 1
                if self.is_mill(pos, next_state.board):
                    for player in range(9 - next_state.playerSoldiersToPlace):
                        if next_state.playerPositions[player] >= 0:
                            tmp = next_state.playerPositions[player]
                            next_state.board[tmp] = 0
                            next_state.playerIncompleteMills += self.incomplete_mill_diff(position=tmp, player=1,
                                                                                          add=False,
                                                                                          board=next_state.board)
                            next_state.playerPositions[player] = -1
                            next_state.playerSoldiersRemaining -= 1
                            if next_state.direction is None:
                                next_state.direction = (pos, soldierToPlace, tmp)
                            states.append(next_state)
                else:
                    if next_state.direction is None:
                        next_state.direction = (pos, soldierToPlace, -1)
                    states.append(next_state)
        return states

    def succ_phase2_player(self, state):
        states = []
        for soldier in range(9):
            next_state = state.__copy__()
            next_state.turn = not next_state.turn
            soldierPos = next_state.playerPositions[soldier]
            if soldierPos >= 0:
                for pos in self.directions(soldierPos):
                    if next_state.board[pos] == 0:
                        next_state.playerPositions[soldier] = pos
                        next_state.board[soldierPos] = 0
                        next_state.playerIncompleteMills += self.incomplete_mill_diff(position=soldierPos, player=1,
                                                                                      add=False, board=next_state.board)
                        next_state.playerIncompleteMills += self.incomplete_mill_diff(pos, 1, True)
                        next_state.board[pos] = 1
                        if self.is_mill(pos, next_state.board):
                            for rival in range(9 - next_state.rivalSoldiersToPlace):
                                if next_state.rivalPositions[rival] >= 0:
                                    tmp = next_state.rivalPositions[rival]
                                    next_state.board[tmp] = 0
                                    next_state.rivalIncompleteMills += self.incomplete_mill_diff(position=tmp, player=2,
                                                                                                 add=False,
                                                                                                 board=next_state.board)
                                    next_state.rivalPositions[rival] = -1
                                    next_state.rivalSoldiersRemaining -= 1
                                    if next_state.direction is None:
                                        next_state.direction = (pos, soldier, tmp)
                                    states.append(next_state)
                        else:
                            if next_state.direction is None:
                                next_state.direction = (pos, soldier, -1)
                            states.append(next_state)
        return states

    def succ_phase2_rival(self, state):
        states = []
        for soldier in range(9):
            next_state = state.__copy__()
            next_state.turn = not next_state.turn
            soldierPos = next_state.rivalPositions[soldier]
            if soldierPos >= 0:
                for pos in self.directions(soldierPos):
                    if next_state.board[pos] == 0:
                        next_state.rivalPositions[soldier] = pos
                        next_state.board[soldierPos] = 0
                        next_state.rivalIncompleteMills += self.incomplete_mill_diff(position=soldierPos, player=2,
                                                                                     add=False, board=next_state.board)
                        next_state.rivalIncompleteMills += self.incomplete_mill_diff(position=pos, player=2, add=True,
                                                                                     board=next_state.board)
                        next_state.board[pos] = 2
                        if self.is_mill(pos, next_state.board):
                            for player in range(9 - next_state.playerSoldiersToPlace):
                                if next_state.playerPositions[player] >= 0:
                                    tmp = next_state.playerPositions[player]
                                    next_state.board[tmp] = 0
                                    next_state.playerIncompleteMills += self.incomplete_mill_diff(position=tmp, player=1,
                                                                                                  add=False,
                                                                                                  board=next_state.board)
                                    next_state.playerPositions[player] = -1
                                    next_state.playerSoldiersRemaining -= 1
                                    if next_state.direction is None:
                                        next_state.direction = (pos, soldier, tmp)
                                    states.append(next_state)
                        else:
                            if next_state.direction is None:
                                next_state.direction = (pos, soldier, -1)
                            states.append(next_state)
        if len(states) == 0:
            utils.printBoard(state.board)
        return states

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, an
    def goal(self, state):
        if (state.rivalSoldiersToPlace == 0 and state.playerSoldiersToPlace == 0) and \
                ((state.playerSoldiersRemaining < 3 or state.rivalSoldiersRemaining < 3) or
                 (self.player_cannot_move(state) != (True, True))):
            return True
        return False

    def succ(self, state):
        if state.turn:
            if state.playerSoldiersToPlace > 0:
                return self.succ_phase1_player(state)
            else:
                return self.succ_phase2_player(state)
        else:
            if state.rivalSoldiersToPlace > 0:
                return self.succ_phase1_rival(state)
            else:
                return self.succ_phase2_rival(state)

    def utility(self, state):
        if state.playerSoldiersRemaining < 3 or self.player_cannot_move(state)[0] is False:
            return -30
        if state.rivalSoldiersRemaining < 3 or self.player_cannot_move(state)[1] is False:
            return 30

        return (state.playerSoldiersRemaining - state.rivalSoldiersRemaining) * 2 + \
               (state.playerIncompleteMills - state.rivalIncompleteMills)
