import random
import time
from BoardState import BoardState

class Bot:
    def __init__(self, mark, level, time_limit):
        self.name = "TTT-Engine"
        self.mark = mark
        self.time_limit = time_limit

        if level=="EASY": self.max_depth = 1
        elif level=="MEDIUM": self.max_depth = 5
        else: self.max_depth = float('inf')
    
    def choose_move(self, board: BoardState):

        zobrist_table = [[[random.randint(1, 2**64 - 1) for _  in range(board.m)] for _ in range(board.n)] for _ in range(2)]
        transposition_table = {}
        board_hash = self.__computeInitialZHash(board, zobrist_table)
        z_hashing = [zobrist_table, transposition_table, board_hash]

        self.time_limit += time.time()

        #begin with a random move
        while not board.is_valid_move(move := [random.randint(1, board.n), random.randint(1, board.m)]):
            pass
        
        #Perform IDDFS, storing best found move each iteration until time runs out
        depth_remaining=1

        while (time.time() + 0.2 < self.time_limit and depth_remaining <= self.max_depth):
            z_hashing[1] = {} #reinitialize the hashes every iteration, since new static values will be computed at a new depth
            #perform minimax with alpha-beta and zobrist hashing
            new_move, __ = self.minimax(board, depth_remaining, -float('inf'), float('inf'), z_hashing)

            #if time runs out return previously calculated move
            if new_move == None:
                return move
            
            #otherwise save this move and increase depth for next iteration
            else: move = new_move
            depth_remaining += 1
        return move
    
    
    def __computeInitialZHash(self, board, zobrist_table):
        hash = 0
        for i in range(board.n):
            for j in range(board.m):
                piece = None
                if board.board[i][j] == 'X': piece = 0
                elif board.board[i][j] == 'O': piece = 1
                if piece != None:
                    hash ^= zobrist_table[piece][i][j]
        return hash
        
    def minimax():
        pass