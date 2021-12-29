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
        self.initialState = {}


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
        self.currState = {"Turn": True, "Board": self.board, "PlayerPositions": self.playerPositions,
                             "RivalPositions": self.rivalPositions, "PlayerSoldiersToPlace": 9,
                             "RivalSoldiersToPlace": 9, "PlayerSoldiersRemain": 0, "RivalSoldiersRemain": 0,
                             "PlayerIncompMills": 0, "RivalIncompMills": 0, "Direction": None}
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

    def succ_phase1_player(self, state):
        for pos in range(24):
            if state["Board"][pos] == 0:
                state["Board"] = 1
                state["PlayerPositions"][9 - state["PlayerSoldierToPlace"]] = pos
                state["PlayerSoldierToPlace"] -= 1

                state["PlayerSoldiersRemain"] += 1
                # check incomplete mills
                if self.is_mill(pos, state["Board"]):
                    for rival in range(9 - state["RivalSoldiersToPlace"]):
                        if state["RivalPositions"][rival] >= 0:
                            tmp = state["RivalPositions"][rival]
                            state["Board"][tmp] = 0
                            state["RivalPositions"][rival] = -1
                            state["RivalSoldiersRemain"] -= 1
                            # check incomplete mills
                            state["Direction"] = (pos, 9-state["PlayerSoldierToPlace"], tmp)
                            return state
                else:
                    state["Direction"] = (pos, 8-state["PlayerSoldierToPlace"], -1)
                    return state

    def succ_phase1_rival(self, state):
        for pos in range(24):
            if state["Board"][pos] == 0:
                state["Board"] = 2
                state["RivalPositions"][9 - state["RivalSoldiersToPlace"]] = pos
                state["RivalSoldiersToPlace"] -= 1
                state["RivalSoldiersRemain"] += 1
                # check incomplete mills
                if self.is_mill(pos, state["Board"]):
                    for player in range(9 - state["PlayerSoldiersToPlace"]):
                        if state["PlayerPositions"][player] >= 0:
                            tmp = state["PlayerPositions"][player]
                            state["Board"][tmp] = 0
                            state["PlayerPositions"][player] = -1
                            state["PlayerSoldiersRemain"] -= 1
                            # check incomplete mills
                            state["Turn"] = not state["Turn"]
                            state["Direction"] = (pos, 8-state["RivalSoldiersToPlace"], tmp)
                            return state
                else:
                    state["Direction"] = (pos, 8-state["RivalSoldiersToPlace"], -1)
                    return state

    def succ_phase2_player(self, state):
        for soldier in range(9):
            soldierPos = state["SoldierPositions"][soldier]
            if soldierPos >= 0:
                for pos in self.directions[soldierPos]:
                    if state["Board"][pos] == 0:
                        state["PlayerPositions"][soldierPos] = pos
                        state["Board"][soldierPos] = 0
                        state["Board"][pos] = 1
                        # check incomplete mills
                        if self.is_mill(pos, state["Board"]):
                            for rival in range(9 - state["RivalSoldiersToPlace"]):
                                if state["RivalPositions"][rival] >= 0:
                                    tmp = state["RivalPositions"][rival]
                                    state["Board"][tmp] = 0
                                    state["RivalPositions"][rival] = -1
                                    state["RivalSoldiersRemaining"] -= 1
                                    # check incomplete mills
                                    state["Direction"] = (pos, soldier, tmp)
                                    return state
                        else:
                            state["Direction"] = (pos, soldier, -1)
                            return state

    def succ_phase2_rival(self,state):
        for soldier in range(9):
            soldierPos = state["RivalPositions"][soldier]
            if soldierPos >= 0:
                for pos in self.directions[soldierPos]:
                    if state["Board"][pos] == 0:
                        state["RivalPositions"][soldierPos] = pos
                        state["Board"][soldierPos] = 0
                        state["Board"][pos] = 2
                        # check incomplete mills
                        if self.is_mill(pos, state["Board"]):
                            for player in range(9 - state["PlayerSoldiersToPlace"]):
                                if state["PlayerPositions"][player] >= 0:
                                    tmp = state["PlayerPositions"][player]
                                    state["Board"][tmp] = 0
                                    state["PlayerPositions"][player] = -1
                                    state["PlayerSoldiersRemaining"] -= 1
                                    # check incomplete mills
                                    state["Direction"] = (pos, soldier, tmp)
                                    return state
                        else:
                            state["Direction"] = (pos, soldier, -1)
                            return state

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, an
    def goal(self, state):
        if state["PlayerSoldiersRemain"] < 3 or state["RivalSoldiersRemain"] < 3:
            return True
        return False

    def succ(self, state):
        if state["Turn"]:
            state["Turn"] = not state["Turn"]
            if state["PlayerSoldiersToPlace"] > 0:
                return self.succ_phase1_player(state)
            else:
                return self.succ_phase2_player(state)
        else:
            state["Turn"] = not state["Turn"]
            if state["RivalSoldiersToPlace"] > 0:
                return self.succ_phase1_rival(state)
            else:
                return self.succ_phase2_rival(state)

    def utility(self, state):
        if state["PlayerSoldiersRemain"] < 3:
            return -30
        if state["RivalSoldiersRemain"] < 3:
            return 30

        return (state["PlayerSoldiersRemain"] - state["RivalSoldiersRemain"]) * 2 + \
               (state["PlayerIncompMills"] - state["RivalIncompMills"])
    #state is a list [turn, board, player soldiers, rival soldiers, player incomplete mills, rival incomplete mills]