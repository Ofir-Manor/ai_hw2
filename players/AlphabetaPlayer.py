"""
MiniMax Player with AlphaBeta pruning
"""
from players.AbstractPlayer import *
import numpy as np
from SearchAlgos import *
from utils import *
import copy


class Player(AbstractPlayer):
    def __init__(self, game_time):
        AbstractPlayer.__init__(self, game_time)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.currState = State()
        self.searchAlgo = AlphaBeta(utility=self.utility, succ=self.succ, goal=self.goal)

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

    def make_move(self, time_limit):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement
        """
        """if self.currState.playerSoldiersToPlace > 0:
            time_divisor = ((24 - (self.currState.playerSoldiersRemaining + self.currState.rivalSoldiersRemaining)) *
                            (self.currState.rivalSoldiersRemaining + 1) * 1.2)
        else:
            time_divisor = (self.currState.playerAvailableMoves * (self.currState.rivalSoldiersRemaining + 1) * 1.2)
            """
        d = 0
        turn_time = 0
        while True:
            start_time = time.time()
            value, move = self.searchAlgo.search(state=self.currState, depth=d, maximizing_player=True)
            d += 1
            end_time = time.time()
            turn_time += end_time - start_time
            if turn_time > time_limit / 20 or value >= 500:
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

    ########## helper functions in class ##########

    def succ_phase1_player(self, state):
        states = []
        soldier_to_place = 9 - state.playerSoldiersToPlace
        save_state_pre_dir = state.__copy__()

        for pos in range(24):
            if state.board[pos] == 0:
                state.board[pos] = 1
                state.playerPositions[soldier_to_place] = pos
                state.playerSoldiersToPlace -= 1
                state.playerSoldiersRemaining += 1

                if self.is_mill(position=pos, board=state.board):
                    save_state_pre_kill = state.__copy__()

                    for rival in range(9 - state.rivalSoldiersToPlace):
                        if state.rivalPositions[rival] >= 0:
                            tmp = state.rivalPositions[rival]
                            state.board[tmp] = 0
                            state.rivalPositions[rival] = -2
                            state.rivalSoldiersRemaining -= 1

                            if state.direction is None:
                                state.direction = (pos, soldier_to_place, tmp)

                            state.playerIncompleteMills, state.playerAvailableMoves, state.rivalIncompleteMills, \
                                state.rivalAvailableMoves = self.moves_and_incomp_mills_calc(state=state)

                            states.append(state.__copy__())

                        state = save_state_pre_kill.__copy__()

                else:
                    if state.direction is None:
                        state.direction = (pos, soldier_to_place, -1)

                    state.playerIncompleteMills, state.playerAvailableMoves, state.rivalIncompleteMills,\
                        state.rivalAvailableMoves = self.moves_and_incomp_mills_calc(state=state)

                    states.append(state.__copy__())

            state = save_state_pre_dir.__copy__()

        return states

    def succ_phase1_rival(self, state):
        states = []
        soldier_to_place = np.where(state.rivalPositions == -1)
        save_state_pre_dir = state.__copy__()
        for pos in range(24):
            if state.board[pos] == 0:
                state.board[pos] = 2
                state.rivalPositions[soldier_to_place] = pos
                state.rivalSoldiersToPlace -= 1
                state.rivalSoldiersRemaining += 1

                if self.is_mill(pos, state.board):
                    save_state_pre_kill = state.__copy__()

                    for player in range(9 - state.playerSoldiersToPlace):
                        if state.playerPositions[player] >= 0:
                            tmp = state.playerPositions[player]
                            state.board[tmp] = 0
                            state.playerPositions[player] = -2
                            state.playerSoldiersRemaining -= 1

                            if state.direction is None:
                                state.direction = (pos, soldier_to_place, tmp)

                            state.playerIncompleteMills, state.playerAvailableMoves, state.rivalIncompleteMills, \
                                state.rivalAvailableMoves = self.moves_and_incomp_mills_calc(state=state)

                            states.append(state.__copy__())
                        state = save_state_pre_kill.__copy__()
                else:
                    if state.direction is None:
                        state.direction = (pos, soldier_to_place, -1)

                    state.playerIncompleteMills, state.playerAvailableMoves, state.rivalIncompleteMills,\
                        state.rivalAvailableMoves = self.moves_and_incomp_mills_calc(state=state)
                    states.append(state.__copy__())

            state = save_state_pre_dir.__copy__()

        return states

    def succ_phase2_player(self, state):
        states = []
        save_state_pre_sold = state.__copy__()
        for soldier in range(9):
            soldier_pos = state.playerPositions[soldier]

            if soldier_pos >= 0:
                save_state_pre_dir = state.__copy__()

                for pos in self.directions(soldier_pos):
                    if state.board[pos] == 0:
                        state.playerPositions[soldier] = pos
                        state.board[soldier_pos] = 0
                        state.board[pos] = 1

                        if self.is_mill(pos, state.board):
                            save_state_pre_kill = state.__copy__()

                            for rival in range(9 - state.rivalSoldiersToPlace):
                                if state.rivalPositions[rival] >= 0:
                                    tmp = state.rivalPositions[rival]
                                    state.board[tmp] = 0
                                    state.rivalPositions[rival] = -2
                                    state.rivalSoldiersRemaining -= 1

                                    if state.direction is None:
                                        state.direction = (pos, soldier, tmp)

                                    state.playerIncompleteMills, state.playerAvailableMoves, \
                                        state.rivalIncompleteMills, state.rivalAvailableMoves = \
                                        self.moves_and_incomp_mills_calc(state=state)
                                    states.append(state.__copy__())

                                state = save_state_pre_kill.__copy__()

                        else:
                            if state.direction is None:
                                state.direction = (pos, soldier, -1)
                            state.playerIncompleteMills, state.playerAvailableMoves, \
                                state.rivalIncompleteMills, state.rivalAvailableMoves = \
                                self.moves_and_incomp_mills_calc(state=state)
                            states.append(state.__copy__())

                    state = save_state_pre_dir.__copy__()

            state = save_state_pre_sold.__copy__()
        return states

    def succ_phase2_rival(self, state):
        states = []
        save_state_pre_sold = state.__copy__()
        for soldier in range(9):

            soldier_pos = state.rivalPositions[soldier]

            if soldier_pos >= 0:
                save_state_pre_dir = state.__copy__()

                for pos in self.directions(soldier_pos):
                    if state.board[pos] == 0:
                        state.rivalPositions[soldier] = pos
                        state.board[soldier_pos] = 0
                        state.board[pos] = 2

                        if self.is_mill(pos, state.board):
                            save_state_pre_kill = state.__copy__()

                            for player in range(9 - state.playerSoldiersToPlace):
                                if state.playerPositions[player] >= 0:
                                    tmp = state.playerPositions[player]
                                    state.board[tmp] = 0
                                    state.playerPositions[player] = -2
                                    state.playerSoldiersRemaining -= 1

                                    if state.direction is None:
                                        state.direction = (pos, soldier, tmp)

                                    state.playerIncompleteMills, state.playerAvailableMoves, \
                                        state.rivalIncompleteMills, state.rivalAvailableMoves = \
                                        self.moves_and_incomp_mills_calc(state=state)
                                    states.append(state.__copy__())

                                state = save_state_pre_kill.__copy__()

                        else:
                            if state.direction is None:
                                state.direction = (pos, soldier, -1)

                            state.playerIncompleteMills, state.playerAvailableMoves, \
                                state.rivalIncompleteMills, state.rivalAvailableMoves = \
                                self.moves_and_incomp_mills_calc(state=state)
                            states.append(state.__copy__())
                    state = save_state_pre_dir.__copy__()

            state = save_state_pre_sold.__copy__()

        return states

    ########## helper functions for AlphaBeta algorithm ##########
    def goal(self, state):
        return (state.rivalSoldiersToPlace == 0 and state.playerSoldiersToPlace == 0) and \
               (((state.playerSoldiersRemaining < 3 or state.rivalSoldiersRemaining < 3 or
                  state.playerAvailableMoves == 0 or state.rivalAvailableMoves == 0)))

    def succ(self, state):
        next_state = state.__copy__()
        if state.turn:
            next_state.turn = not next_state.turn
            if state.playerSoldiersToPlace > 0:
                return self.succ_phase1_player(next_state)
            else:
                return self.succ_phase2_player(next_state)
        else:
            next_state.turn = not next_state.turn
            if state.rivalSoldiersToPlace > 0:
                return self.succ_phase1_rival(next_state)
            else:
                return self.succ_phase2_rival(next_state)

    def diff_mill_count(self, state):
        count_1 = 0
        count_2 = 0
        player_pos = state.playerPositions
        rival_pos = state.rivalPositions
        for i in player_pos:
            if i >= 0:
                if self.check_next_mill(i, 1, state.board):
                    count_1 += 1
        for i in rival_pos:
            if i >=0:
                if self.check_next_mill(i, 2, state.board):
                    count_2 += 1
        return count_1 - count_2

    def utility(self, state):
        if self.goal(state) and (state.playerSoldiersRemaining < 3 or state.playerAvailableMoves == 0):
            return -500
        if self.goal(state) and (state.rivalSoldiersRemaining < 3 or state.rivalAvailableMoves == 0):
            return 500

        return (state.playerSoldiersRemaining - state.rivalSoldiersRemaining) * 10 + \
               (state.playerIncompleteMills - state.rivalIncompleteMills) + self.diff_mill_count(state)
