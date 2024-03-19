from HumanPlayer import Human
from BotPlayer import Bot

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
    

class Game:
    def __init__(self):
        self.n = 3
        self.m = 3
        self.k = 3

    def set_settings(self):
        while(True):
            print("\n---SETTINGS---")
            print("Current board size (N x M):", self.n, "by", self.m)
            print(f'Current game is {self.k}-in-a-row')
            print('Please select an option (character):')
            print('--change-k-in-a-row k')
            print('--change-n n')
            print('--change-m m')
            print('--no-change nc\n')
            selection = input().upper()

            try:
                if selection=='K':
                    k = int(input("Enter k: "))
                    if k <= max(self.n, self.m):
                        self.k = k
                    else: raise 

                elif selection=='N':
                    print("Keep this value within the range 3-10")
                    n = int(input("Enter n: "))
                    if(n <= 10 and n >= 3): self.n = n
                    else: raise


                elif selection=='M':
                    print("Keep this value within the range 3-10")
                    m = int(input("Enter m: "))
                    if(m <= 10 and m >= 3): self.m = m
                    else: raise

                elif selection=='NC': break
                else: raise
            except Exception:
                print("Invalid selection. Try again.")
                continue


    def run(self, p1: Human, p2, board: BoardState):
        print(f'\n{p1.name} vs. {p2.name}\n')
        current_player = p2
        counter = 0
        move=[]
        is_goal, isdraw = board.is_goal_state(self.k, move, counter)
        while not is_goal:
            if current_player==p2: current_player = p1
            else: current_player = p2
            board.print_board()
            print(f'\n{current_player.name}\'s turn to play!')
            move = current_player.choose_move(board.board)
            board.move(move, current_player.mark)
            counter += 1
            is_goal, isdraw = board.is_goal_state(self.k, move, counter)
        
        board.print_board()
        if isdraw:
            print("Game ends in a draw!\n")
        else:
            print(f'{current_player.name} wins!\n')
            


    def start(self):
        while(True):
            print("\n---MENU---")
            print("Welcome to K-in-a-row, N x M Tic-Tac-Toe!\n")
            print('Please select an option (character):')
            print('--settings s')
            print('--multiplayer mp')
            print('--singleplayer sp')
            print('--quit q\n')
            selection = input().upper()
            if selection=='S':
                self.set_settings()

            elif selection=='MP':
                player1 = input("Please enter the name of Player 1 (X): ")
                player2 = input("Please enter the name of Player 2 (O): ")
                self.run(Human(player1, 'X'), Human(player2, 'O'), BoardState(self.n, self.m))

            elif selection=='SP': 
                #TODO
                print()

            elif selection=='Q':
                break
            else:
                print("Invalid option. Try again.\n")
                continue

game = Game()
game.start()