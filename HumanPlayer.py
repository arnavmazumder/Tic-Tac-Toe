from BoardState import BoardState

class Human:
    def __init__(self, name, mark):
        self.name = name
        self.mark = mark

    def choose_move(self, board: BoardState):
        while(True):
            try:
                move = [int(coord) for coord in input("Enter move as \"row column\": ").split()]
                if board.board[move[0]-1][move[1]-1] != ' ': raise
            except Exception:
                print("Invalid move. Try again")
                continue
            return move
        
