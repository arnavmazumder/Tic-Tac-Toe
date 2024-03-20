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
            

            try:
                selection = input().upper()
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
            except KeyboardInterrupt:
                exit(0)


    def run(self, p1: Human, p2, board: BoardState):
        print(f'\n{p1.name} vs. {p2.name}\n')
        current_player = p2
        winner = board.is_goal_state()
        while winner==None:

            if current_player==p2: current_player = p1
            else: current_player = p2

            board.print_board()
            print(f'\n{current_player.name}\'s turn to play!')

            move = current_player.choose_move(board)
            board = board.move(move)

            winner = board.is_goal_state()
        
        board.print_board()
        if winner=='draw':
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

            try:
                selection = input().upper()
                if selection=='S':
                    self.set_settings()

                elif selection=='MP':
                    player1 = input("Please enter the name of Player 1 (X): ")
                    player2 = input("Please enter the name of Player 2 (O): ")
                    self.run(Human(player1), Human(player2), BoardState(self.n, self.m, self.k))

                elif selection=='SP':
                    while True:
                        marker = input("Please select a marker (X or O): ").upper()
                        if marker !='X' and marker!='O':
                            print("Invalid selection. Try again.")
                            continue
                        break

                    player1 = input(f"Please enter your name ({marker}): ")
                    if marker=='O': self.run(Bot(self.bot_level, self.bot_time_limit), Human(player1), BoardState(self.n, self.m, self.k))
                    else: self.run(Human(player1), Bot(self.bot_level, self.bot_time_limit), BoardState(self.n, self.m, self.k))
                    

                elif selection=='Q':
                    break
                else:
                    print("Invalid option. Try again.\n")
                    continue
            except KeyboardInterrupt:
                exit(0)


game = Game()
game.start()