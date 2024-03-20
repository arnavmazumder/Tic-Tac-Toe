class BoardState:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.board = [[' ' for i in range(m)] for _ in range(n)]

    def print_board(self):
        result = ("----" * self.m) + "-\n"
        for i in range(len(self.board)):
            result += "| "
            for j in range(len(self.board[0]) - 1):
                result += (self.board[i][j] + " | ")
            result += (self.board[i][self.m - 1] + " |\n")
        result += ("----" * self.m) + "-\n"
        print(result)
    

    def move(self, move, mark):
        i = move[0] - 1
        j = move[1] - 1
        self.board[i][j] = mark
    

    def is_valid_move(self, move):
        try:
            mark = self.board[move[0]-1][move[1]-1]
            if mark!=' ': return False
        except Exception:
            return False
        return True


    def is_goal_state(self, k, move, counter):
        if counter < 2*k - 1: return False, False
        i = move[0]-1
        j = move[1]-1
        n = len(self.board)
        m = len(self.board[0])
        mark = self.board[i][j]

        #Horizontal
        mark_count = 0
        while (j!=m and self.board[i][j]==mark):
            mark_count += 1
            if mark_count==k: return True, False
            j+=1
        
        j = move[1]-1-1
        while (j!=-1 and self.board[i][j]==mark):
            mark_count += 1
            if mark_count==k: return True, False
            j-=1

        #Vertical
        j = move[1]-1
        mark_count = 0
        while (i!=n and self.board[i][j]==mark):
            mark_count += 1
            if mark_count==k: return True, False
            i+=1
        
        i = move[0]-1-1
        while (i!=-1 and self.board[i][j]==mark):
            mark_count += 1
            if mark_count==k: return True, False
            i-=1


        #Diagonal 1
        i = move[0]-1
        mark_count = 0
        while (i!=n and j!=m and self.board[i][j]==mark):
            mark_count += 1
            if mark_count==k: return True, False
            i+=1
            j+=1
        
        i = move[0]-1-1
        j = move[1]-1-1
        while (i!=-1 and j!=-1 and self.board[i][j]==mark):
            mark_count += 1
            if mark_count==k: return True, False
            i-=1
            j-=1


        #Diagonal 2
        i = move[0]-1
        j = move[1]-1
        mark_count = 0
        while (i!=-1 and j!=m and self.board[i][j]==mark):
            mark_count += 1
            if mark_count==k: return True, False
            i-=1
            j+=1
        
        i = move[0]
        j = move[1]-1-1
        while (i!=n and j!=-1 and self.board[i][j]==mark):
            mark_count += 1
            if mark_count==k: return True, False
            i+=1
            j-=1

        if counter==self.n*self.m: return True, True
        return False, False