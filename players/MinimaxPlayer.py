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

        if self.currState.playerSoldiersToPlace > 0:
            time_divisor = ((24 - (self.currState.playerSoldiersRemaining + self.currState.rivalSoldiersRemaining)) *
                            (self.currState.rivalSoldiersRemaining+1)*1.5)
        else:
            time_divisor = (self.currState.playerAvailableMoves*(self.currState.rivalSoldiersRemaining+1)*1.5)
        d = 1
        turn_time = 0
        while True:
            start_time = time.time()
            value, move = self.searchAlgo.search(state=self.currState, depth=d, maximizing_player=True)
            d += 1
            end_time = time.time()
            turn_time += end_time - start_time
            if turn_time > time_limit/time_divisor or value == 500:
                break

        self.currState.board[self.currState.playerPositions[move[1]]] = 0
        self.board[self.currState.playerPositions[move[1]]] = 0
        if self.currState.playerSoldiersToPlace > 0:
            self.currState.playerSoldiersRemaining += 1
            self.currState.playerSoldiersToPlace -= 1

        self.currState.board[move[0]] = 1
        self.board[move[0]] = 1
        self.currState.playerPositions[move[1]] = move[0]
        if move[2] != -1:
            self.currState.rivalSoldiersRemaining -= 1
            self.currState.board[move[2]] = 0

            for rival, pos in enumerate(self.currState.rivalPositions):
                if pos == move[2]:
                    self.currState.rivalPositions[rival] = -2
                    break

        self.currState.turn = False
        self.currState.playerIncompleteMills, self.currState.playerAvailableMoves, self.currState.rivalIncompleteMills,\
            self.currState.rivalAvailableMoves = self.moves_and_incomp_mills_calc(state=self.currState)
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

        self.currState.board[move[0]] = 2
        self.currState.rivalPositions[move[1]] = move[0]
        if move[2] != -1:
            self.currState.playerSoldiersRemaining -= 1
            self.currState.board[move[2]] = 0
            for player, pos in enumerate(self.currState.playerPositions):
                if pos == move[2]:
                    self.currState.playerPositions[player] = -2

        self.currState.turn = True
        self.currState.playerIncompleteMills, self.currState.playerAvailableMoves, self.currState.rivalIncompleteMills,\
            self.currState.rivalAvailableMoves = self.moves_and_incomp_mills_calc(state=self.currState)

        # TODO: erase the following line and implement this function.
        #raise NotImplementedError



    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    def succ_phase1_player(self, state):
        states = []
        next_state = state.__copy__()
        next_state.turn = not next_state.turn
        soldier_to_place = 9 - next_state.playerSoldiersToPlace
        for pos in range(24):
            if next_state.board[pos] == 0:
                save_state_pre_dir = next_state.__copy__()
                next_state.board[pos] = 1
                next_state.playerPositions[soldier_to_place] = pos
                next_state.playerSoldiersToPlace -= 1
                next_state.playerSoldiersRemaining += 1
                if self.is_mill(position=pos, board=next_state.board):
                    save_state_pre_kill = next_state.__copy__()
                    for rival in range(9 - next_state.rivalSoldiersToPlace):
                        if next_state.rivalPositions[rival] >= 0:
                            tmp = next_state.rivalPositions[rival]
                            next_state.board[tmp] = 0

                            next_state.rivalPositions[rival] = -2
                            next_state.rivalSoldiersRemaining -= 1
                            if next_state.direction is None:
                                next_state.direction = (pos, soldier_to_place, tmp)
                            next_state.playerIncompleteMills, next_state.playerAvailableMoves, \
                                next_state.rivalIncompleteMills, next_state.rivalAvailableMoves = \
                                self.moves_and_incomp_mills_calc(state=next_state)
                            states.append(next_state.__copy__())
                            next_state = save_state_pre_kill.__copy__()
                    next_state = save_state_pre_dir.__copy__()
                else:
                    if next_state.direction is None:
                        next_state.direction = (pos, soldier_to_place, -1)
                    next_state.playerIncompleteMills, next_state.playerAvailableMoves,\
                        next_state.rivalIncompleteMills, next_state.rivalAvailableMoves =\
                        self.moves_and_incomp_mills_calc(state=next_state)
                    states.append(next_state)
                    next_state = save_state_pre_dir.__copy__()
        return states

    def succ_phase1_rival(self, state):
        states = []
        next_state = state.__copy__()
        next_state.turn = not next_state.turn
        soldierToPlace = np.where(next_state.rivalPositions == -1)
        for pos in range(24):
            if next_state.board[pos] == 0:
                save_state_pre_dir = next_state.__copy__()
                next_state.board[pos] = 2
                next_state.rivalPositions[soldierToPlace] = pos
                next_state.rivalSoldiersToPlace -= 1
                next_state.rivalSoldiersRemaining += 1
                if self.is_mill(pos, next_state.board):
                    save_state_pre_kill = next_state.__copy__()
                    for player in range(9 - next_state.playerSoldiersToPlace):
                        if next_state.playerPositions[player] >= 0:
                            tmp = next_state.playerPositions[player]
                            next_state.board[tmp] = 0
                            next_state.playerPositions[player] = -2
                            next_state.playerSoldiersRemaining -= 1
                            if next_state.direction is None:
                                next_state.direction = (pos, soldierToPlace, tmp)
                            next_state.playerIncompleteMills, next_state.playerAvailableMoves, \
                                next_state.rivalIncompleteMills, next_state.rivalAvailableMoves = \
                                self.moves_and_incomp_mills_calc(state=next_state)
                            states.append(next_state.__copy__())
                            next_state = save_state_pre_kill.__copy__()
                    next_state = save_state_pre_dir.__copy__()
                else:
                    if next_state.direction is None:
                        next_state.direction = (pos, soldierToPlace, -1)
                    next_state.playerIncompleteMills, next_state.playerAvailableMoves, \
                        next_state.rivalIncompleteMills, next_state.rivalAvailableMoves = \
                        self.moves_and_incomp_mills_calc(state=next_state)
                    states.append(next_state.__copy__())
                    next_state = save_state_pre_dir.__copy__()
        return states

    def succ_phase2_player(self, state):
        states = []
        next_state = state.__copy__()
        next_state.turn = not next_state.turn
        for soldier in range(9):
            save_state_pre_sold = next_state.__copy__()
            soldierPos = next_state.playerPositions[soldier]
            if soldierPos >= 0:
                save_state_pre_dir = next_state.__copy__()
                for pos in self.directions(soldierPos):
                    if next_state.board[pos] == 0:
                        next_state.playerPositions[soldier] = pos
                        next_state.board[soldierPos] = 0

                        next_state.board[pos] = 1
                        if self.is_mill(pos, next_state.board):
                            save_state_pre_kill = next_state.__copy__()
                            for rival in range(9 - next_state.rivalSoldiersToPlace):
                                if next_state.rivalPositions[rival] >= 0:

                                    tmp = next_state.rivalPositions[rival]
                                    next_state.board[tmp] = 0
                                    next_state.rivalPositions[rival] = -2
                                    next_state.rivalSoldiersRemaining -= 1
                                    if next_state.direction is None:
                                        next_state.direction = (pos, soldier, tmp)

                                    next_state.playerIncompleteMills, next_state.playerAvailableMoves, \
                                        next_state.rivalIncompleteMills, next_state.rivalAvailableMoves = \
                                        self.moves_and_incomp_mills_calc(state=next_state)
                                    states.append(next_state.__copy__())
                                    next_state = save_state_pre_kill.__copy__()
                            next_state = save_state_pre_dir.__copy__()
                        else:
                            if next_state.direction is None:
                                next_state.direction = (pos, soldier, -1)

                            next_state.playerIncompleteMills, next_state.playerAvailableMoves, \
                                next_state.rivalIncompleteMills, next_state.rivalAvailableMoves = \
                                self.moves_and_incomp_mills_calc(state=next_state)
                            states.append(next_state.__copy__())
                            next_state = save_state_pre_dir.__copy__()
            next_state = save_state_pre_sold.__copy__()
        return states

    def succ_phase2_rival(self, state):
        states = []
        next_state = state.__copy__()
        next_state.turn = not next_state.turn
        for soldier in range(9):
            save_state_pre_sold = next_state.__copy__()
            soldierPos = next_state.rivalPositions[soldier]
            if soldierPos >= 0:
                save_state_pre_dir = next_state.__copy__()
                for pos in self.directions(soldierPos):
                    if next_state.board[pos] == 0:
                        next_state.rivalPositions[soldier] = pos
                        next_state.board[soldierPos] = 0

                        next_state.board[pos] = 2
                        if self.is_mill(pos, next_state.board):
                            save_state_pre_kill = next_state.__copy__()
                            for player in range(9 - next_state.playerSoldiersToPlace):
                                if next_state.playerPositions[player] >= 0:
                                    tmp = next_state.playerPositions[player]
                                    next_state.board[tmp] = 0

                                    next_state.playerPositions[player] = -2
                                    next_state.playerSoldiersRemaining -= 1
                                    if next_state.direction is None:
                                        next_state.direction = (pos, soldier, tmp)

                                    next_state.playerIncompleteMills, next_state.playerAvailableMoves, \
                                        next_state.rivalIncompleteMills, next_state.rivalAvailableMoves = \
                                        self.moves_and_incomp_mills_calc(state=next_state)
                                    states.append(next_state.__copy__())
                                    next_state = save_state_pre_kill.__copy__()
                            next_state = save_state_pre_dir.__copy__()
                        else:
                            if next_state.direction is None:
                                next_state.direction = (pos, soldier, -1)

                            next_state.playerIncompleteMills, next_state.playerAvailableMoves, \
                            next_state.rivalIncompleteMills, next_state.rivalAvailableMoves = \
                                self.moves_and_incomp_mills_calc(state=next_state)
                            states.append(next_state.__copy__())
                            next_state = save_state_pre_dir.__copy__()
            next_state = save_state_pre_sold.__copy__()
        return states

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, an
    def goal(self, state):
        return (state.rivalSoldiersToPlace == 0 and state.playerSoldiersToPlace == 0) and \
                (((state.playerSoldiersRemaining < 3 or state.rivalSoldiersRemaining < 3 or
                 state.playerAvailableMoves == 0 or state.rivalAvailableMoves == 0)))

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
        if self.goal(state) and (state.playerSoldiersRemaining < 3 or state.playerAvailableMoves == 0):
            return -500
        if self.goal(state) and (state.rivalSoldiersRemaining < 3 or state.rivalAvailableMoves == 0):
            return 500

        return (state.playerSoldiersRemaining - state.rivalSoldiersRemaining) * 10 + \
               (state.playerIncompleteMills - state.rivalIncompleteMills)
