import constants

class Square:
    '''A basic square object'''
    def __init__(self, position, piece = None):
        self._position = position
        self._piece = piece
        
    def set_piece(self,new_piece):
        self._piece = new_piece

    def get_piece(self):
        return self._piece

    def get_position(self):
        return self._position

    def display(self):
        if self._piece is None:
            return constants.empty_square
        return self._piece.display()