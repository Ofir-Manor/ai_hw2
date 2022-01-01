"""
MiniMax Player
"""
import copy

import numpy as np
import time

from players.AbstractPlayer import AbstractPlayer, State
#TODO: you can import more modules, if needed

class Player(AbstractPlayer):
    def __init__(self, game_time):
        AbstractPlayer.__init__(self, game_time) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        #TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.currState = State()

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, of the board.
        No output is expected.
        """
        self.currState.board = np.copy(board)
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
        turn_time = 0
        move = None
        while True:
            start_time = time.time()
            end_time = time.time()
            turn_time = end_time - start_time
            time_limit -= turn_time
            move = self.sea
            d += 1
            if time_limit < #need to find answer
                break
            #do turn
        #TODO: erase the following line and implement this function.
        # raise NotImplementedError

    def set_rival_move(self, move):
        """Update your info, given the new position of the rival.
        input:
            - move: tuple, the new position of the rival.
        No output is expected
        """
        self.currState.board[self.currState.rivalPositions[move[1]]] = 0

        self.currState.rivalIncompleteMills += self.incomplete_mill_diff(self.currState.rivalPositions[move[1]],2, False)
        self.currState.rivalIncompleteMills += self.incomplete_mill_diff(move[0], 2, True)

        self.currState.board[move[0]] = 2
        self.currState.rivalPositions[move[1]] = move[0]
        if move[2] != -1:
            self.playerSoldiersRemaining -= 1
            self.board[move[2]] = 0
            self.currState.playerIncompleteMills += self.incomplete_mill_diff(move[2], 1, False)
            for player in self.playerPositions:
                if player == move[2]:
                    self.playerPositions[player] = -1


        self.currState.turn = True
        # TODO: erase the following line and implement this function.
        raise NotImplementedError



    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    def succ_phase1_player(self, state):
        states = []
        for pos in range(24):
            next_state = copy.deepcopy(state)
            next_state.turn = not next_state.turn
            if next_state.board[pos] == 0:
                next_state.playerIncompleteMills += self.incomplete_mill_diff(pos, 1, True)
                next_state.board = 1
                next_state.playerPositions[9 - next_state.playerSoldiersToPlace] = pos
                next_state.playerSoldiersToPlace -= 1

                next_state.playerSoldiersRemaining += 1
                if self.is_mill(pos, next_state.board):
                    for rival in range(9 - next_state.rivalSoldiersToPlace):
                        if next_state.rivalPositions[rival] >= 0:
                            tmp = next_state.rivalPositions[rival]
                            next_state.board[tmp] = 0
                            next_state.rivalIncompleteMills += self.incomplete_mill_diff(tmp, 2, False)
                            next_state.rivalPositions[rival] = -1
                            next_state.rivalSoldiersRemaining -= 1
                            next_state.direction = (pos, 8-next_state.playerSoldiersToPlace, tmp)
                            states.append(next_state)
                else:
                    next_state.direction = (pos, 8-state.playerSoldiersToPlace, -1)
                    states.append(next_state)
        return states

    def succ_phase1_rival(self, state):
        states = []
        for pos in range(24):
            next_state = copy.deepcopy(state)
            next_state.turn = not next_state.turn
            if next_state.board[pos] == 0:
                next_state.rivalIncompleteMills += self.incomplete_mill_diff(pos, 2, True)
                next_state.board = 2
                next_state.rivalPositions[9 - next_state.rivalSoldiersToPlace] = pos
                next_state.rivalSoldiersToPlace -= 1
                next_state.rivalSoldiersRemaining += 1
                # check incomplete mills
                if self.is_mill(pos, next_state.board):
                    for player in range(9 - next_state.playerSoldiersToPlace):
                        if next_state.playerPositions[player] >= 0:
                            tmp = next_state.playerPositions[player]
                            next_state.board[tmp] = 0
                            next_state.playerIncompleteMills += self.incomplete_mill_diff(tmp, 1, False)
                            next_state.playerPositions[player] = -1
                            next_state.playerSoldiersRemaining -= 1
                            # check incomplete mills
                            next_state.direction = (pos, 8-next_state.rivalSoldiersToPlace, tmp)
                            states.append(next_state)
                else:
                    next_state.direction = (pos, 8-next_state.rivalSoldiersToPlace, -1)
                    states.append(next_state)
        return states

    def succ_phase2_player(self, state):
        states = []
        for soldier in range(9):
            next_state = copy.deepcopy(state)
            next_state.turn = not next_state.turn
            soldierPos = next_state.SoldiersPosition[soldier]
            if soldierPos >= 0:
                for pos in self.directions[soldierPos]:
                    if next_state.board[pos] == 0:
                        next_state.playerPositions[soldierPos] = pos
                        next_state.board[soldierPos] = 0
                        next_state.playerIncompleteMills += self.incomplete_mill_diff(soldierPos, 1, False)
                        next_state.playerIncompleteMills += self.incomplete_mill_diff(pos, 1, True)
                        next_state.board[pos] = 1
                        if self.is_mill(pos, next_state.board):
                            for rival in range(9 - next_state.rivalSoldiersToPlace):
                                if next_state.rivalPositions[rival] >= 0:
                                    tmp = next_state.rivalPositions[rival]
                                    next_state.board[tmp] = 0
                                    next_state.rivalIncompleteMills += self.incomplete_mill_diff(tmp, 2, False)
                                    next_state.rivalPositions[rival] = -1
                                    next_state.rivalSoldiersRemainig -= 1
                                    next_state.direction = (pos, soldier, tmp)
                                    states.append(next_state)
                        else:
                            next_state.direction = (pos, soldier, -1)
                            states.append(next_state)

    def succ_phase2_rival(self,state):
        states = []
        for soldier in range(9):
            next_state = copy.deepcopy(state)
            next_state.turn = not next_state.turn
            soldierPos = next_state.rivalPositions[soldier]
            if soldierPos >= 0:
                for pos in self.directions[soldierPos]:
                    if next_state.board[pos] == 0:
                        next_state.rivalPositions[soldierPos] = pos
                        next_state.board[soldierPos] = 0
                        next_state.rivalIncompleteMills += self.incomplete_mill_diff(soldierPos, 2, False)
                        next_state.rivalIncompleteMills += self.incomplete_mill_diff(pos, 2, True)
                        next_state.board[pos] = 2
                        if self.is_mill(pos, next_state.board):
                            for player in range(9 - next_state.PlayerSoldiersToPlace):
                                if next_state.playerPositions[player] >= 0:
                                    tmp = next_state.playerPositions[player]
                                    next_state.board[tmp] = 0
                                    next_state.playerIncompleteMills += self.incomplete_mill_diff(tmp, 1, False)
                                    next_state.playerPositions[player] = -1
                                    next_state.playerSoldiersRemaining -= 1
                                    # check incomplete mills
                                    next_state.direction = (pos, soldier, tmp)
                                    states.append(next_state)
                        else:
                            next_state.direction = (pos, soldier, -1)
                            states.append(next_state)
        return states

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, an
    def goal(self, state):
        if (state.rivalSoldiersToPlace == 0 and state.playerSoldiersToPlace == 0) and \
                (state.playerSoldiersRemaining < 3 or state.rivalSoldiersRemaining < 3):
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
        if state.playerSoldiersRemaining < 3:
            return -30
        if state.rivalSoldiersRemaining < 3:
            return 30

        return (state.playerSoldiersRemaining - state.rivalSoldiersRemaining) * 2 + \
               (state.playerIncompleteMills - state.rivalIncompleteMills)