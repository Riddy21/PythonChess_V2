# Abstract Piece Class
class _Piece():
    def __init__(self, value, colour, move_pattern, image, str_rep):
        # initiate variables
        self.value = value
        self.colour = colour
        # TODO: Implement later
        # self.move_pattern = move_pattern
        self.image = image
        self.str_rep = str_rep


class Pawn(_Piece):
    def __init__(self, colour):
        if colour == 'white':
            image = 'Assets/Chess_tile_pl.png'
            str = 'P'
        elif colour == 'black':
            image = 'Assets/Chess_tile_pd.png'
            str = 'p'
        else:
            print("colour typo")

        # Makes a piece with set values and images
        super().__init__(1, colour, 'placeholder', image, str)

class Rook(_Piece):
    def __init__(self, colour):
        if colour == 'white':
            image = 'Assets/Chess_tile_rl.png'
            str = 'R'
        elif colour == 'black':
            image = 'Assets/Chess_tile_rd.png'
            str = 'r'
        else:
            print("colour typo")

        # Makes a piece with set values and images
        super().__init__(5, colour, 'placeholder', image, str)

class Knight(_Piece):
    def __init__(self, colour):
        if colour == 'white':
            image = 'Assets/Chess_tile_nl.png'
            str = 'N'
        elif colour == 'black':
            image = 'Assets/Chess_tile_nd.png'
            str = 'n'
        else:
            print("colour typo")

        # Makes a piece with set values and images
        super().__init__(3, colour, 'placeholder', image, str)

class Bishop(_Piece):
    def __init__(self, colour):
        if colour == 'white':
            image = 'Assets/Chess_tile_bl.png'
            str = 'B'
        elif colour == 'black':
            image = 'Assets/Chess_tile_bd.png'
            str = 'b'
        else:
            print("colour typo")

        # Makes a piece with set values and images
        super().__init__(1, colour, 'placeholder', image, str)

class Queen(_Piece):
    def __init__(self, colour):
        if colour == 'white':
            image = 'Assets/Chess_tile_ql.png'
            str = 'Q'
        elif colour == 'black':
            image = 'Assets/Chess_tile_qd.png'
            str = 'q'
        else:
            print("colour typo")

        # Makes a piece with set values and images
        super().__init__(9, colour, 'placeholder', image, str)

class King(_Piece):
    def __init__(self, colour):
        if colour == 'white':
            image = 'Assets/Chess_tile_kl.png'
            str = 'K'
        elif colour == 'black':
            image = 'Assets/Chess_tile_kd.png'
            str = 'k'
        else:
            print("colour typo")

        # Makes a piece with set values and images
        super().__init__(100000000, colour, 'placeholder', image, str) # TODO: make value max int value

class Blank(_Piece):
    def __init__(self):
        super().__init__(0,'none','placeholder','Assets/Blank.png','-')