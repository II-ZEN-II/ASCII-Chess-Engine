import constants

def set_moves(move_set, squares, start, piece):
    possible_moves = []
    for move in move_set:
        new_x = start[0] + move[0]
        new_y = start[1] + move[1]
        
        if new_x < 0 or new_x > 7 or new_y < 0 or new_y > 7:
            continue #not valid -> outside board
        
        target = squares[new_y][new_x].get_piece()
        if target is not None and target.get_colour() == piece.get_colour():
            continue #not valid -> move onto one of your pieces
        
        possible_moves.append((new_x,new_y))

    return possible_moves

def directional_moves(move_set, squares, start, piece):
    possible_moves = []
    for direction in move_set:
        saved_x = start[0]
        saved_y = start[1]
        while True:
            saved_x += direction[0]
            saved_y += direction[1]
            
            if saved_x < 0 or saved_x > 7 or saved_y < 0 or saved_y > 7:
                break #not valid -> outside board
            
            target = squares[saved_y][saved_x].get_piece()
            if target is not None and target.get_colour() == piece.get_colour():
                break #not valid -> move onto one of your pieces
            
            possible_moves.append((saved_x,saved_y))
            if target is not None and target.get_colour() != piece.get_colour():
                break
                
    return possible_moves


class Piece:
    '''A basic piece object'''
    def __init__(self, sprite, colour, value):
        self._sprite = sprite
        self._colour = colour
        self._value = value
    
    def possible_moves(self, squares, start, piece):
        #to be overridden
        return
    
    def get_colour(self):
        return self._colour
    
    def display(self):
        return self._sprite


class Pawn(Piece):
    '''A pawn object'''
    def __init__(self, colour):
        sprite = constants.white_pawn if colour else constants.black_pawn
        super().__init__(sprite, colour, 1)
    
    def possible_moves(self, squares, start, piece):
        possible_moves = []
        direction = -1 if piece.get_colour() else 1 #ensures it moves the correct way only
        
        #move forward
        if squares[start[1]+direction][start[0]].get_piece() is None:
            if start[1]+direction < 7 and start[1]+direction > 0:
                possible_moves.append((start[0],start[1]+direction))
            
        #move forward two if start square
        if (direction == -1 and start[1] == 6) or (direction == 1 and start[1] == 1):
            if squares[start[1]+direction][start[0]].get_piece() is None:
                if squares[start[1]+direction*2][start[0]].get_piece() is None:
                    possible_moves.append((start[0],start[1]+direction*2))
                    #TODO store for en-passant later
        
        #attacking
        target = squares[start[1]+direction][start[0]-1].get_piece()
        if target is not None and target.get_colour() != piece.get_colour():
            possible_moves.append((start[0]-1,start[1]+direction))
            
        target = squares[start[1]+direction][start[0]+1].get_piece()
        if target is not None and target.get_colour() != piece.get_colour():
            possible_moves.append((start[0]+1,start[1]+direction))
        
        return possible_moves

        
class Knight(Piece):
    '''A knight object'''
    def __init__(self, colour):
        sprite = constants.white_knight if colour else constants.black_knight
        super().__init__(sprite, colour, 3)
        
    def possible_moves(self, squares, start, piece):
        moves = [(-1,2),(1,2),(2,-1),(2,1),(1,-2),(-1,-2),(-2,-1),(-2,1)]
        return set_moves(moves, squares, start, piece)


class Bishop(Piece):
    '''A bishop object'''
    def __init__(self, colour):
        sprite = constants.white_bishop if colour else constants.black_bishop
        super().__init__(sprite, colour, 3)
    
    def possible_moves(self, squares, start, piece):
        directions = [(-1,-1),(1,-1),(1,1),(-1,1)]
        return directional_moves(directions, squares, start, piece)


class Rook(Piece):
    '''A rook object'''
    def __init__(self, colour):
        sprite = constants.white_rook if colour else constants.black_rook
        super().__init__(sprite, colour, 5)
    
    def possible_moves(self, squares, start, piece):
        directions = [(0,-1),(1,0),(0,1),(-1,0)]
        return directional_moves(directions, squares, start, piece)


class Queen(Piece):
    '''A queen object'''
    def __init__(self, colour):
        sprite = constants.white_queen if colour else constants.black_queen
        super().__init__(sprite, colour, 9)
    
    def possible_moves(self, squares, start, piece):
        directions = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
        return directional_moves(directions, squares, start, piece)


class King(Piece):
    '''A king object'''
    def __init__(self, colour):
        sprite = constants.white_king if colour else constants.black_king
        super().__init__(sprite, colour, 999)
    
    def possible_moves(self, squares, start, piece):
        moves = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
        return set_moves(moves, squares, start, piece)