from HumanPlayer import Human
from BotPlayer import Bot

class BoardState:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.board = [['X' for i in range(m)] for _ in range(n)]
    def print_board(self):
        result = ("----" * self.m) + "-\n"
        for i in range(len(self.board)):
            result += "| "
            for j in range(len(self.board[0]) - 1):
                result += (self.board[i][j] + " | ")
            result += (self.board[i][self.m - 1] + " |\n")
        result += ("----" * self.m) + "-\n"
        print(result)


class Game:
    def __init__(self):
        self.n = 3
        self.m = 3
        self.k = 3

    def set_settings(self):
        while(True):
            print("---SETTINGS---")
            print("\nCurrent board size (N x M):", self.n, "by", self.m)
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
            except:
                print("Invalid selection. Try again.")
                continue

    def run(self, p1, p2, board):
        pass

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
                player1 = input("Please enter the name of Player 1: ")
                player2 = input("Please enter the name of Player 2: ")
                self.run(Human(player1), Human(player2), BoardState())

            elif selection=='SP': 
                #TODO
                print()

            elif selection=='Q':
                break
            else:
                print("Invalid option. Try again.\n")
                continue

#game = Game()
#game.start()