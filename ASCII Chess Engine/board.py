import constants
import square
import pieces

class Board:
    '''A basic board object'''
    def __init__(self):
        self._turn = True
        self._squares = self.setup_board()
    
    def player_turn(self):
        #TODO not allow empty or invalid input -> separate functions for parsing
        print('WHITE\'s turn' if self._turn else 'BLACK\'s turn')
        while True:
            start = input('(start)>>').split(',')
            start = tuple([int(val) for val in start])
            
            piece = self._squares[start[1]][start[0]].get_piece()
            if piece is None or piece.get_colour() != self._turn:
                continue #piece was empty or opponents
            
            possible_moves = piece.possible_moves(self._squares, start, piece)
            self.display_moves(possible_moves)
            
            end = input('(end)>>').split(',')
            end = tuple([int(val) for val in end])
            
            target = self._squares[end[1]][end[0]].get_piece()
            if target is not None and target.get_colour() == self._turn:
                continue #moving onto your own piece
            
            #IS MOVE VALID
            if end not in possible_moves:
                continue #move is not possible with current board state
            
            #TODO PIECE promotion
            if type(piece) == pieces.Pawn and (end[1] == 7 or end[1] == 0):
                print('promotion')
                pass
            
            #PERFORM MOVE (new function)
            self._squares[end[1]][end[0]].set_piece(piece)
            self._squares[start[1]][start[0]].set_piece(None)
            self._turn = not(self._turn)
            print('sucessful move')
            break
    
    def setup_board(self):
        #instantiate a 2d array of empty squares
        board = []
        for y in range(8):
            row = []
            for x in range(8):
                row.append(square.Square((x,y)))
            board.append(row)
            
        #assign pieces to the squares
        board[0][0].set_piece(pieces.Rook(False))
        board[0][1].set_piece(pieces.Knight(False))
        board[0][2].set_piece(pieces.Bishop(False))
        board[0][3].set_piece(pieces.Queen(False))
        board[0][4].set_piece(pieces.King(False))
        board[0][5].set_piece(pieces.Bishop(False))
        board[0][6].set_piece(pieces.Knight(False))
        board[0][7].set_piece(pieces.Rook(False))
        
        board[1][0].set_piece(pieces.Pawn(False))
        board[1][1].set_piece(pieces.Pawn(False))
        board[1][2].set_piece(pieces.Pawn(False))
        board[1][3].set_piece(pieces.Pawn(False))
        board[1][4].set_piece(pieces.Pawn(False))
        board[1][5].set_piece(pieces.Pawn(False))
        board[1][6].set_piece(pieces.Pawn(False))
        board[1][7].set_piece(pieces.Pawn(False))
        
        board[7][0].set_piece(pieces.Rook(True))
        board[7][1].set_piece(pieces.Knight(True))
        board[7][2].set_piece(pieces.Bishop(True))
        board[7][3].set_piece(pieces.Queen(True))
        board[7][4].set_piece(pieces.King(True))
        board[7][5].set_piece(pieces.Bishop(True))
        board[7][6].set_piece(pieces.Knight(True))
        board[7][7].set_piece(pieces.Rook(True))
        
        board[6][0].set_piece(pieces.Pawn(True))
        board[6][1].set_piece(pieces.Pawn(True))
        board[6][2].set_piece(pieces.Pawn(True))
        board[6][3].set_piece(pieces.Pawn(True))
        board[6][4].set_piece(pieces.Pawn(True))
        board[6][5].set_piece(pieces.Pawn(True))
        board[6][6].set_piece(pieces.Pawn(True))
        board[6][7].set_piece(pieces.Pawn(True))
        
        return board
    
    def display(self):
        for y, row in enumerate(self._squares):
            line = []
            for square in row:
                line.append(square.display())
            print(f'{y}    '+' '.join(line))
        print('\n     0 1 2 3 4 5 6 7\n')
    
    def display_moves(self, moves):
        for y, row in enumerate(self._squares):
            line = []
            for x, square in enumerate(row):
                char = square.display()
                if (x,y) in moves:
                    if char == constants.empty_square:
                        char = constants.possible_move
                    else:
                        char = constants.possible_capture
                line.append(char)
            print(f'{y}    '+' '.join(line))
        print('\n     0 1 2 3 4 5 6 7\n')
    