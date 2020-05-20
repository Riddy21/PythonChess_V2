# Abstract Piece Class
class _Piece():
    def __init__(self, value, colour, move_pattern, image):
        # initiate variables
        self.value = value
        self.colour = colour
        # TODO: Implement later
        # self.move_pattern = move_pattern
        self.image = image


class Pawn(_Piece):
    def __init__(self, colour):
        if colour == 'white':
            image = 'Assets/Chess_tile_pl.png'
        elif colour == 'black':
            image = 'Assets/Chess_tile_pd.png'

        # Makes a piece with set values and images
        super().__init__(1, colour, 'placeholder', image)


