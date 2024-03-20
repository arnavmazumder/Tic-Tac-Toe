from HumanPlayer import Human
from BotPlayer import Bot
from BoardState import BoardState

class Game:
    def __init__(self):
        self.n = 3
        self.m = 3
        self.k = 3
        self.bot_level = 'EASY'
        self.bot_time_limit = 1.0

    def set_settings(self):
        while(True):
            print("\n---SETTINGS---")
            print("Current board size (N x M):", self.n, "by", self.m)
            print(f'Current game: {self.k}-in-a-row')
            print(f'Current bot-level: {self.bot_level}')
            print(f'Current bot-time-limit: {self.bot_time_limit}\n')
            print('Please select an option (character):')
            print('--change-k-in-a-row k')
            print('--change-n n')
            print('--change-m m')
            print('--change-bot-level bl')
            print('--change-bot_time_limit bt')
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
                
                elif selection=='BL':
                    bot_level = input("Enter new bot-level (Easy, Medium, or Hard): ").upper()
                    if bot_level=="EASY" or bot_level=="MEDIUM" or bot_level=="HARD": self.bot_level = bot_level
                    else: raise

                elif selection=='BT':
                    bot_tl = float(input("Enter new bot-time-limit (between 0.0 and 15.0): "))
                    if bot_tl>0 and bot_tl<=15: self.bot_time_limit = bot_tl
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
            move = current_player.choose_move(board)
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
                while True:
                    marker = input("Please select a marker (X or O): ").upper()
                    if marker !='X' and marker!='O':
                        print("Invalid selection. Try again.")
                        continue
                    break

                player1 = input(f"Please enter your name ({marker}): ")
                if marker=='O': self.run(Bot('X', self.bot_level, self.bot_time_limit), Human(player1, marker), BoardState(self.n, self.m))
                else: self.run(Human(player1, marker), Bot('O', self.bot_level, self.bot_time_limit), BoardState(self.n, self.m))
                


            elif selection=='Q':
                break
            else:
                print("Invalid option. Try again.\n")
                continue

game = Game()
game.start()