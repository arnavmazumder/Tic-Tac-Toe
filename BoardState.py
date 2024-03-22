class BoardState:
    def __init__(self, n, m, k, board=None, next_player=None):
        self.n = n
        self.m = m
        self.k = k
        if next_player==None: self.next_player = 'X'
        else: self.next_player = next_player
        if (board==None): self.board = [[' ' for i in range(m)] for _ in range(n)]
        else: self.board = board

    def print_board(self):
        result = ("----" * self.m) + "-\n"
        for i in range(len(self.board)):
            result += "| "
            for j in range(len(self.board[0]) - 1):
                result += (self.board[i][j] + " | ")
            result += (self.board[i][self.m - 1] + " |\n")
        result += ("----" * self.m) + "-\n"
        print(result)
    

    def move(self, move):
        newBoard = [row.copy() for row in self.board]
    
        i = move[0] - 1
        j = move[1] - 1
        newBoard[i][j] = self.next_player

        if self.next_player == 'X': next_player = 'O'
        else: next_player = 'X'

        return BoardState(self.n, self.m, self.k, newBoard, next_player)

    

    def is_valid_move(self, move):
        try:
            mark = self.board[move[0]-1][move[1]-1]
            if mark!=' ': return False
        except Exception:
            return False
        return True


    def is_goal_state(self):
        if self.next_player == 'X': to_check = 'O'
        else: to_check = 'X'

        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == to_check:

                    #horizontal
                    if j <= self.m - self.k and all(self.board[i][j + k] == to_check for k in range(self.k)):
                        return to_check
                    
                    # vertical
                    if i <= self.n - self.k and all(self.board[i + k][j] == to_check for k in range(self.k)):
                        return to_check
                    
                    #diagonal 1
                    if i <= self.n - self.k and j <= self.m - self.k:
                        if all(self.board[i + k][j + k] == to_check for k in range(self.k)):
                            return to_check
                    # diagonal 2
                    if i >= self.k - 1 and j <= self.m - self.k:
                        if all(self.board[i - k][j + k] == to_check for k in range(self.k)):
                            return to_check

        # draw
        if all(self.board[i][j]!=' ' for i in range(self.n) for j in range(self.m)):
            return 'draw'

        return None