import random
import time
import re
from BoardState import BoardState

class Bot:
    def __init__(self, level, time_limit):
        self.name = "TTT-Engine"
        self.time_limit = time_limit

        if level=="EASY": self.max_depth = 1
        elif level=="MEDIUM": self.max_depth = 5
        else: self.max_depth = float('inf')
    
    def choose_move(self, board: BoardState):

        time_limit = self.time_limit + time.time()

        zobrist_table = [[[random.randint(1, 2**64 - 1) for _  in range(board.m)] for _ in range(board.n)] for _ in range(2)]
        transposition_table = {}
        board_hash = self.__computeInitialZHash(board, zobrist_table)
        z_hashing = [zobrist_table, transposition_table, board_hash]


        #begin with a random move
        while not board.is_valid_move(move := [random.randint(1, board.n), random.randint(1, board.m)]):
            pass
        
        #Perform IDDFS, storing best found move each iteration until time runs out
        depth_remaining=1

        while (time.time() + 0.2 < time_limit and depth_remaining <= self.max_depth):
            z_hashing[1] = {} #reinitialize the hashes every iteration, since new static values will be computed at a new depth
            #perform minimax with alpha-beta and zobrist hashing
            new_move, __ = self.minimax(board, depth_remaining, time_limit, -float('inf'), float('inf'), z_hashing)

            #if time runs out return previously calculated move
            if new_move == None:
                return move
            
            #otherwise save this move and increase depth for next iteration
            else: move = new_move
            depth_remaining += 1
        return move
    

    def __computeInitialZHash(self, board: BoardState, zobrist_table):
        hash = 0
        for i in range(board.n):
            for j in range(board.m):
                piece = None
                if board.board[i][j] == 'X': piece = 0
                elif board.board[i][j] == 'O': piece = 1
                if piece != None:
                    hash ^= zobrist_table[piece][i][j]
        return hash
    
        
    def minimax(self, board: BoardState, depth_remaining, time_limit, alpha, beta, z_hashing):

        if (time.time() + 0.2 > time_limit): return None, 0.0 

        # if the current board has already been visited return its value
        # Since using z_hashing and alph-beta, distinguish between exact and bounded values
        board_hash = z_hashing[2]
        transposition_table = z_hashing[1]
        if board_hash in transposition_table:
            stored_val = transposition_table[board_hash]
            if stored_val['flag'] == 'exact':
                return None, stored_val['value']
            
            elif stored_val['flag'] == 'lower' and stored_val['value'] >= beta:
                return None, stored_val['value']
            
            elif stored_val['flag'] == 'upper' and stored_val['value'] <= alpha:
                return None, stored_val['value']


        #if depth reached or leaf node reached perform a static evaluation on the board and save in the transposition table with z_hashing
        if depth_remaining == 0 or board.is_goal_state()!=None:
            score = self.static_eval(board)
            transposition_table[board_hash] = {'value': score, 'flag': 'exact'}
            return None, score
        
        #generates and then sorts moves based on values already stored in the transposition table to improve pruning
        #also reverse order depending on whether current player is minimizing or maximizing
        moves = self.__generate_moves(board)
        moves.sort(key=lambda move: transposition_table.get(self.__updateHash(board, z_hashing[0], move, board_hash), {'value': 0}).get('value'), reverse=board.next_player=='X') 
        

        #initialize provisional values and other variables
        if board.next_player == 'X': provisional = -float('inf')
        else: provisional = float('inf')
        bestMove = None
        pruned = False

        for move in moves:
            #for each move, generate the corresponding child state
            child = board.move(move)

            #compute the hash of the child
            child_hash = self.__updateHash(board, z_hashing[0], move, board_hash)
            z_hashing[2] = child_hash

            #recursively call minimax
            __, newProv = self.minimax(child, depth_remaining - 1, time_limit, alpha, beta, z_hashing)

            #check time limit to prevent the generation of the next state
            if time.time() + 0.2 > time_limit: return None, 0.0

            #Update provisional value and bestMove if the provisional value has improved
            if (board.next_player=='X' and newProv > provisional) or (board.next_player=='O' and newProv < provisional):
                provisional = newProv
                bestMove = move

                #update alpha-beta if needed and prune the branch if beta <= alpha
                if board.next_player=='X': alpha = max(alpha, provisional)
                else: beta = min(beta, provisional)
                if beta <= alpha:
                    pruned = True
                    break

        #save the best provisional. indicate whether the provisional was exact or a bound

        if not pruned: transposition_table[board_hash] = {'value': provisional, 'flag': 'exact'}
        else:
            if board.next_player == 'X':
                transposition_table[board_hash] = {'value': provisional, 'flag': 'lower'}
            else:
                transposition_table[board_hash] = {'value': provisional, 'flag': 'upper'}

        return bestMove, provisional
    

    def __updateHash(self, board: BoardState, zobrist_table, move, currHash):
        if board.next_player == 'X': piece = 0
        else: piece = 1

        return currHash ^ zobrist_table[piece][move[0]-1][move[1]-1]

    def __generate_moves(self, board: BoardState):
        return [[x, y] for x in range(1, board.n + 1) for y in range(1, board.m + 1) if board.board[x-1][y-1] == ' ']

    def static_eval(self, board: BoardState):

        val = 0
        rows, cols, diagonals = self.__process_board(board)
        total_lines = rows + cols + diagonals


        #if winning state, return maximum or minimum values
        winner = self.__winning_state(rows, cols, diagonals, board)
        if winner =='X': return float('inf')
        elif winner =='O': return -float('inf')

        #weights difference between maximum consecutive length of both sides
        val = self.__consecutive_pieces(total_lines)

        linesDiff, maxDiff, Xalmost_winning, Oalmost_winning = self.__potential_winning_lines(total_lines, board)

        #fork cases
        #if (Xalmost_winning > 1 and Oalmost_winning==0): return float('inf')
        #elif(Xalmost_winning==0 and Oalmost_winning > 1): return float('inf')

        val += 30 * (Xalmost_winning - Oalmost_winning)
        val += maxDiff
        val += linesDiff

        return val
    
    def __potential_winning_lines(self, all_seq, board: BoardState):
        Xlines = 0
        Olines = 0
        maxX = 0
        maxO = 0
        Xalmost_winning = 0
        Oalmost_winning = 0

        for seq in all_seq:
            if board.k <= len(seq):
                for i in range(len(seq) - board.k + 1):
                    window = seq[i:i+board.k]
                    if ('X' in window and 'O' in window) or '-' in window: continue
                    Xs = 0
                    Os = 0

                    for elem in window:
                        if elem == 'X': Xs += 1
                        elif elem =='O': Os += 1
                    
                    if Xs==board.k-1: Xalmost_winning+=1
                    elif Os==board.k-1: Oalmost_winning+=1

                    if Xs!=0: Xlines+=1
                    else: Olines += 1

                    maxX = max(maxX, Xs)
                    maxO = max(maxO, Os)
                        
        return Xlines - Olines, maxX - maxO, Xalmost_winning, Oalmost_winning
            
    

    def __consecutive_pieces(self, all_seq):
        
        maxX = 0
        maxO = 0
        for seq in all_seq:
            xmatches = re.findall(r'X+', seq)
            maxX = max(len(max(xmatches, key=len) if xmatches else ''), maxX)

            omatches = re.findall(r'O+', seq)
            maxO = max(len(max(omatches, key=len) if omatches else ''), maxO)
        return maxX - maxO
    
    
    
    def __winning_state(self, rows, cols, diagonals, board: BoardState):
        temp_rows = rows.copy()
        temp_rows.extend(cols)
        temp_rows.extend(diagonals)

        for r in temp_rows:
            if re.search(f'[X]{{{board.k}}}', r):
                return 'X'
            if re.search(f'[O]{{{board.k}}}', r):
                return 'O'

        if not sum(row.count(' ') for row in board.board):
            return "draw"

        return None


    def __process_board(self, board: BoardState):

        # lists of strings consiting of each row and column        
        rows = [''.join(row) for row in board.board]
        cols = [''.join(col) for col in list(zip(*board.board))]

        #consider main and 'inverse' diagonals (together they make an X)
        diags = []
        main_diag = [board.board[i][i] for i in range(min(board.m, board.n))]
        invmain_diag =  [board.board[i][board.m - 1 - i] for i in range(min(board.m, board.n))]

        
        diags.append(main_diag)
        #Adding diagonals below main diagonal
        for i in range(1, board.n):
            below_main_diag = [board.board[j+i][j] for j in range(min(board.n - i, board.m))]
            diags.append(below_main_diag)

        #Adding diagonals above main diagonal
        for i in range(1, board.m):
            above_main_diag = [board.board[j][i+j] for j in range(min(board.m - i, board.n))]
            diags.append(above_main_diag)

        diags.append(invmain_diag)
        #Adding diagonals below invmain diagonal
        for i in range(1, board.n):  
            below_maininv_diag = [board.board[i+j][board.m - 1 - j] for j in range(min(board.n - i, board.m))]
            diags.append(below_maininv_diag)

        #Adding diagonals below invmain diagonal
        for i in range(board.m - 2, -1, -1):  # Start from the second last column to the first
            above_invmain_diags = [board.board[j][i - j] for j in range(min(i + 1, board.n))]
            diags.append(above_invmain_diags)

        diagonals = [''.join(diag) for diag in diags]

        return rows, cols, diagonals
    