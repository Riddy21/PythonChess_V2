from typing import Any


# detects if pieces are blocking the way of other pieces
def _piece_detect(frox, froy, tox, toy, board):
    # make sure its not checking its self
    if tox != frox or toy != froy:
        # Same colour pieces
        if getattr(board[tox][toy], 'colour') == getattr(board[frox][froy], 'colour'):
            return 'self obstructed'
        # opponent pieces
        elif getattr(board[tox][toy], 'colour') != 'none':
            return 'opponent obstructed'
        else:
            return 'unobstructed'


# Abstract Piece Class
class _Piece():
    def __init__(self, value, colour, move_pattern, image, str_rep):
        # initiate variables
        self.value = value
        self.colour = colour
        self.image = image
        self.str_rep = str_rep
        self.move_count = 0

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)


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

    # Pawn move set given the location of the piece
    def get_moves(self, x, y, board):
        poss_moves = []

        # Black moves
        if getattr(board[x][y], 'colour') == 'black':
            i = 1

            while (i <= 2 and y + i <= 7):
                piece_detect = _piece_detect(x, y, x, y + i, board)
                # piece in front blocks move
                if getattr(board[x][y + i], 'colour') == 'white':
                    break

                # basic
                elif piece_detect == 'self obstructed':
                    break

                elif piece_detect == 'opponent obstructed':
                    break

                # no 2nd move on 2nd turn
                if (self.move_count >= 1):
                    poss_moves.append([x, y + i])
                    break

                # add the position and increment counter
                poss_moves.append([x, y + i])
                i += 1

            # Sideways Capture
            if x < 7 and y <= 7 and getattr(board[x + 1][y + 1], 'colour') == 'white':
                poss_moves.append([x + 1, y + 1])
            if x > 0 and y <= 7 and getattr(board[x - 1][y + 1], 'colour') == 'white':
                poss_moves.append([x - 1, y + 1])


        # white moves
        elif getattr(board[x][y], 'colour') == 'white':
            i = 1

            while (i <= 2 and y - i >= 0):
                piece_detect = _piece_detect(x, y, x, y - i, board)

                # piece in front blocks move
                if getattr(board[x][y - i], 'colour') == 'black':
                    break

                # basic
                elif piece_detect == 'self obstructed':
                    break

                elif piece_detect == 'opponent obstructed':
                    break

                # no 2nd move on 2nd turn
                elif (self.move_count >= 1):
                    poss_moves.append([x, y - i])
                    break

                # add the position and increment counter
                poss_moves.append([x, y - i])
                i += 1

            # Sideways Capture
            if x < 7 and y >= 0 and getattr(board[x + 1][y - 1], 'colour') == 'black':
                poss_moves.append([x + 1, y - 1])
            if x > 0 and y >= 0 and getattr(board[x - 1][y - 1], 'colour') == 'black':
                poss_moves.append([x - 1, y - 1])

        # returns a list of all the places the pawn can move
        return poss_moves


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
        super().__init__(100000000, colour, 'placeholder', image, str)  # TODO: make value max int value


class Blank(_Piece):
    def __init__(self):
        super().__init__(0, 'none', 'placeholder', 'Assets/Blank.png', '-')
