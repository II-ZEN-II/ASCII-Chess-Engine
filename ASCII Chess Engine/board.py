import constants
import square
import pieces

class Board:
    '''A basic board object'''
    def __init__(self):
        self._turn = True
        self._squares = self.setup_board()
        
        self._check = False
        self._gameover = False #changed when game is over
    
    def player_turn(self):
        print('WHITE\'s turn' if self._turn else 'BLACK\'s turn')
        while True:
            #IS GAME OVER
            self._gameover = self.is_gameover()
            if self._gameover:
                break
            
            #PARSING MOVE
            start = self.parse_move('start')
            piece = self._squares[start[1]][start[0]].get_piece()
            if piece is None or piece.get_colour() != self._turn:
                continue #piece was empty or opponents
            
            valid_moves = piece.valid_moves(self,self._squares, start, piece)
            self.display(valid_moves)
            
            end = self.parse_move('end')
            target = self._squares[end[1]][end[0]].get_piece()
            if target is not None and target.get_colour() == self._turn:
                #TODO re-assign as start square if it is your piece
                continue #moving onto your own piece
            
            #IS MOVE VALID
            if end not in valid_moves[0] and end not in valid_moves[1]:
                continue #move is not valid with piece or current board state
            
            #PIECE promotion (NEW FUNCTION)
            if type(piece) == pieces.Pawn and (end[1] == 7 or end[1] == 0):
                print('promotion')
                while True:
                    new = input('(new piece)>>').strip().upper()
                    
                    #assign piece
                    new_piece = None
                    if new == 'N' or new == 'KNIGHT':
                        new_piece = pieces.Knight(piece.get_colour())
                    elif new == 'B' or new == 'BISHOP':
                        new_piece = pieces.Bishop(piece.get_colour())
                    elif new == 'R' or new == 'ROOK':
                        new_piece = pieces.Rook(piece.get_colour())
                    elif new == 'Q' or new == 'QUEEN':
                        new_piece = pieces.Queen(piece.get_colour())
                    else:
                        continue
                    
                    #update board
                    piece = new_piece
                    break
            
            #PERFORM MOVE (new function)
            self._squares[end[1]][end[0]].set_piece(piece)
            self._squares[start[1]][start[0]].set_piece(None)
            print('successful move')

            #IS OPPONENT IN CHECK
            self._check = self.is_in_check(not(self._turn))
            print('opponent in check=',self._check)
            
            #CHANGE TURN
            self._turn = not(self._turn)
            break
    
    def is_in_check(self, colour_to_check):
        #TODO make more optimised
        
        #find king
        for y in range(8):
            for x in range(8):
                piece = self._squares[y][x].get_piece()
                if piece is not None and piece.get_colour() == colour_to_check and type(piece) == pieces.King:
                    #save pos
                    king_position = (x,y)
        
        #search for check
        for y in range(8):
            for x in range(8):
                coord = (x,y)
                piece = self._squares[y][x].get_piece()
                if piece is not None and piece.get_colour() != colour_to_check:
                    moves = piece.possible_moves(self._squares, coord, piece)
                    if king_position in moves[1]:
                        #check!
                        return True
        
        return False
    
    def is_gameover(self):
        #CHECK FOR STALEMATE AND CHECKMATE
        for y in range(8):
            for x in range(8):
                coord = (x,y)
                piece = self._squares[y][x].get_piece()
                if piece is not None and piece.get_colour() == self._turn:
                    valid_moves = piece.valid_moves(self,self._squares, coord, piece)
                    #print(piece, valid_moves)
                    if len(valid_moves[0]) > 0 or len(valid_moves[1]) > 0:
                        return False
        
        if self._check:
            print('CHECKMATE!')
        else:
            print('STALEMATE!')                    
        return True
    
    def get_gameover(self):
        return self._gameover
    
    def parse_move(self, instruction):
        translation = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
        while True:
            square = input(f'({instruction})>>').lower()
            try:
                move = (translation[square[0]],8-int(square[1]))
            except:
                continue
            break
        return move
    
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
    
    def display(self, moves = [[],[]]):
        for y, row in enumerate(self._squares):
            line = []
            for x, square in enumerate(row):
                char = square.display()
                if (x,y) in moves[0]:
                    if char == constants.empty_square:
                        char = constants.possible_move
                elif (x,y) in moves[1]:
                    if char == constants.empty_square:
                        char = constants.possible_move
                    else:
                        char = constants.possible_capture
                line.append(char)
            print(f'{8-y}    '+' '.join(line))
        print('\n     a b c d e f g h\n')
    