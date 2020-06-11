from typing import Any

#TODO: Move into Class
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

#TODO: Make a piece with movecount and move history set to 0 and one with inserting a piece with a history
# Abstract Piece Class
class _Piece():
    def __init__(self, value, colour, image, str_rep):
        # initiate variables
        self.value = value
        self.colour = colour
        self.image = image
        self.str_rep = str_rep
        self.move_count = 0

        # A list of all the move ids this piece made a move
        self.move_num_history = []

    def add_move(self, move_id):
        self.move_num_history.append(move_id)

    def delete_move(self):
        self.move_num_history.pop(-1)

    def is_castle(self, x, y):
        return -1

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
        super().__init__(1, colour, image, str)

    # Pawn move set given the location of the piece
    def get_moves(self, x, y, board):
        poss_moves = []

        # Black moves
        if getattr(board[x][y], 'colour') == 'black':
            i = 1

            # Do Move detection
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
            
        #enPassante
        if self.colour == 'white' and y == 3:
            if getattr(board[x + 1][y], 'colour') == 'black' and \
                    getattr(board[x + 1][y], 'move_count') == 1 and \
                    getattr(board[x + 1][y], 'move_num_history')[-1] == (self.move_num_history[-1] - 1):
                if _piece_detect(x, y, x + 1, y - 1, board) == 'opponent obstructed' or \
                        _piece_detect(x, y, x + 1, y - 1, board) == 'unobstructed':
                    poss_moves.append([x + 1, y - 1])    
            if getattr(board[x - 1][y], 'colour') == 'black' and \
                    getattr(board[x - 1][y], 'move_count') == 1 and \
                    getattr(board[x - 1][y], 'move_num_history')[-1] == (self.move_num_history[-1] - 1):
                if _piece_detect(x, y, x - 1, y - 1, board) == 'opponent obstructed' or \
                        _piece_detect(x, y, x - 1, y - 1, board) == 'unobstructed':
                    poss_moves.append([x - 1, y - 1]) 
        elif self.colour == 'black' and y == 4:
            if getattr(board[x + 1][y], 'colour') == 'white' and \
                    getattr(board[x + 1][y], 'move_count') == 1 and \
                    getattr(board[x + 1][y], 'move_num_history')[-1] == (self.move_num_history[-1] - 1):
                if _piece_detect(x, y, x + 1, y + 1, board) == 'opponent obstructed' or \
                        _piece_detect(x, y, x + 1, y + 1, board) == 'unobstructed':
                    poss_moves.append([x + 1, y + 1])    
            if getattr(board[x - 1][y], 'colour') == 'white' and \
                    getattr(board[x - 1][y], 'move_count') == 1 and \
                    getattr(board[x - 1][y], 'move_num_history')[-1] == (self.move_num_history[-1] - 1):
                if _piece_detect(x, y, x - 1, y + 1, board) == 'opponent obstructed' or \
                        _piece_detect(x, y, x - 1, y + 1, board) == 'unobstructed':
                    poss_moves.append([x - 1, y + 1]) 
                    


#            if (Main.piece[x][y].getColour() == 'w' and y == 3):
#               if (Main.piece[x + 1][y].getColour() == 'b' and Main.piece[x + 1][y].getMoveC() == 1 and Main.move[
#                    -2] == [
#                    x + 1, y]):
#                    pieceDetect(x, y, x + 1, y - 1)
#                if (Main.piece[x - 1][y].getColour() == 'b' and Main.piece[x - 1][y].getMoveC() == 1 and Main.move[
#                    -2] == [
#                    x - 1, y]):
#                    pieceDetect(x, y, x - 1, y - 1)
#                Move.enpass = True
#            elif (Main.piece[x][y].getColour() == 'b' and y == 4):
#                if (Main.piece[x + 1][y].getColour() == 'w' and Main.piece[x + 1][y].getMoveC() == 1 and Main.move[
#                    -2] == [
#                    x + 1, y]):
#                    pieceDetect(x, y, x + 1, y + 1)
#                if (Main.piece[x - 1][y].getColour() == 'w' and Main.piece[x - 1][y].getMoveC() == 1 and Main.move[
#                    -2] == [
#                    x - 1, y]):
#                    pieceDetect(x, y, x - 1, y + 1)
#                Move.enpass = True

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
        super().__init__(5, colour, image, str)

    # Returns possible moves this piece can make
    def get_moves(self, x, y, board):
        poss_moves = []

        i = 1
        # All x moves below x
        while x - i >= 0:
            if _piece_detect(x, y, x - i, y, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x - i, y, board) == 'opponent obstructed':
                poss_moves.append([x - i, y])
                break
            poss_moves.append([x - i, y])
            i += 1

        i = 1
        # All x moves above x
        while (x + i) <= 7:
            if _piece_detect(x, y, x + i, y, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x + i, y, board) == 'opponent obstructed':
                poss_moves.append([x + i, y])
                break
            poss_moves.append([x + i, y])
            i += 1

        i = 1
        # All y moves below y
        while y - i >= 0:
            if _piece_detect(x, y, x, y - i, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x, y - i, board) == 'opponent obstructed':
                poss_moves.append([x, y - i])
                break
            poss_moves.append([x, y - i])
            i += 1
        i = 1
        # All x moves above y
        while (y + i) <= 7:
            if _piece_detect(x, y, x, y + i, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x, y + i, board) == 'opponent obstructed':
                poss_moves.append([x, y + i])
                break
            poss_moves.append([x, y + i])
            i += 1

        return poss_moves


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
        super().__init__(3, colour, image, str)

    # Returns possible moves this piece can make
    def get_moves(self, x, y, board):
        poss_moves = []
        if (x + 2 <= 7):
            if (y + 1 <= 7):
                if _piece_detect(x, y, x + 2, y + 1, board) == 'opponent obstructed' or \
                        _piece_detect(x, y, x + 2, y + 1, board) == 'unobstructed':
                    poss_moves.append([x + 2, y + 1])
            if (y - 1 >= 0):
                if _piece_detect(x, y, x + 2, y - 1, board) == 'opponent obstructed' or \
                        _piece_detect(x, y, x + 2, y - 1, board) == 'unobstructed':
                    poss_moves.append([x + 2, y - 1])

        if (x + 1 <= 7):
            if (y + 2 <= 7):
                if _piece_detect(x, y, x + 1, y + 2, board) == 'opponent obstructed' or \
                        _piece_detect(x, y, x + 1, y + 2, board) == 'unobstructed':
                    poss_moves.append([x + 1, y + 2])
            if (y - 2 >= 0):
                if _piece_detect(x, y, x + 1, y - 2, board) == 'opponent obstructed' or \
                        _piece_detect(x, y, x + 1, y - 2, board) == 'unobstructed':
                    poss_moves.append([x + 1, y - 2])
        if (x - 2 >= 0):
            if (y + 1 <= 7):
                if _piece_detect(x, y, x - 2, y + 1, board) == 'opponent obstructed' or \
                        _piece_detect(x, y, x - 2, y + 1, board) == 'unobstructed':
                    poss_moves.append([x - 2, y + 1])
            if (y - 1 >= 0):
                if _piece_detect(x, y, x - 2, y - 1, board) == 'opponent obstructed' or \
                        _piece_detect(x, y, x - 2, y - 1, board) == 'unobstructed':
                    poss_moves.append([x - 2, y - 1])
        if (x - 1 >= 0):
            if (y + 2 <= 7):
                if _piece_detect(x, y, x - 1, y + 2, board) == 'opponent obstructed' or \
                        _piece_detect(x, y, x - 1, y + 2, board) == 'unobstructed':
                    poss_moves.append([x - 1, y + 2])
            if (y - 2 >= 0):
                if _piece_detect(x, y, x - 1, y - 2, board) == 'opponent obstructed' or \
                        _piece_detect(x, y, x - 1, y - 2, board) == 'unobstructed':
                    poss_moves.append([x - 1, y - 2])

        return poss_moves


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
        super().__init__(1, colour, image, str)

    def get_moves(self, x, y, board):
        poss_moves = []

        i = 1
        # All moves top left
        while x - i >= 0 and y - i >= 0:
            if _piece_detect(x, y, x - i, y - i, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x - i, y - i, board) == 'opponent obstructed':
                poss_moves.append([x - i, y - i])
                break
            poss_moves.append([x - i, y - i])
            i += 1

        i = 1
        # All moves bottom right
        while x + i <= 7 and y + i <= 7:
            if _piece_detect(x, y, x + i, y + i, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x + i, y + i, board) == 'opponent obstructed':
                poss_moves.append([x + i, y + i])
                break
            poss_moves.append([x + i, y + i])
            i += 1

        i = 1
        # All y moves below y
        while x - i >= 0 and y + i <= 7:
            if _piece_detect(x, y, x - i, y + i, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x - i, y + i, board) == 'opponent obstructed':
                poss_moves.append([x - i, y + i])
                break
            poss_moves.append([x - i, y + i])
            i += 1

        i = 1
        # All x moves above y
        while x + i <= 7 and y - i >= 0:
            if _piece_detect(x, y, x + i, y - i, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x + i, y - i, board) == 'opponent obstructed':
                poss_moves.append([x + i, y - i])
                break
            poss_moves.append([x + i, y - i])
            i += 1

        return poss_moves


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
        super().__init__(9, colour, image, str)

    def get_moves(self, x, y, board):
        poss_moves = []

        # Rook moves + Bishop moves
        i = 1
        # All moves top left
        while x - i >= 0 and y - i >= 0:
            if _piece_detect(x, y, x - i, y - i, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x - i, y - i, board) == 'opponent obstructed':
                poss_moves.append([x - i, y - i])
                break
            poss_moves.append([x - i, y - i])
            i += 1

        i = 1
        # All moves bottom right
        while x + i <= 7 and y + i <= 7:
            if _piece_detect(x, y, x + i, y + i, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x + i, y + i, board) == 'opponent obstructed':
                poss_moves.append([x + i, y + i])
                break
            poss_moves.append([x + i, y + i])
            i += 1

        i = 1
        # All y moves below y
        while x - i >= 0 and y + i <= 7:
            if _piece_detect(x, y, x - i, y + i, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x - i, y + i, board) == 'opponent obstructed':
                poss_moves.append([x - i, y + i])
                break
            poss_moves.append([x - i, y + i])
            i += 1

        i = 1
        # All x moves above y
        while x + i <= 7 and y - i >= 0:
            if _piece_detect(x, y, x + i, y - i, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x + i, y - i, board) == 'opponent obstructed':
                poss_moves.append([x + i, y - i])
                break
            poss_moves.append([x + i, y - i])
            i += 1

        i = 1
        # All x moves below x
        while x - i >= 0:
            if _piece_detect(x, y, x - i, y, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x - i, y, board) == 'opponent obstructed':
                poss_moves.append([x - i, y])
                break
            poss_moves.append([x - i, y])
            i += 1

        i = 1
        # All x moves above x
        while (x + i) <= 7:
            if _piece_detect(x, y, x + i, y, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x + i, y, board) == 'opponent obstructed':
                poss_moves.append([x + i, y])
                break
            poss_moves.append([x + i, y])
            i += 1

        i = 1
        # All y moves below y
        while y - i >= 0:
            if _piece_detect(x, y, x, y - i, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x, y - i, board) == 'opponent obstructed':
                poss_moves.append([x, y - i])
                break
            poss_moves.append([x, y - i])
            i += 1
        i = 1
        # All x moves above y
        while (y + i) <= 7:
            if _piece_detect(x, y, x, y + i, board) == 'self obstructed':
                break
            elif _piece_detect(x, y, x, y + i, board) == 'opponent obstructed':
                poss_moves.append([x, y + i])
                break
            poss_moves.append([x, y + i])
            i += 1

        return poss_moves


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
        super().__init__(100000000, colour, image, str)  # TODO: make value max int value

        # Parameter for storing castle coordinates if castle move is possible
        self.left_castle = -1, -1
        self.right_castle = -1, -1

    # TODO:
    def get_moves(self, x, y, board):
        # TODO: beyond doing regular moves, make castle move checker
        # If castle move is possible, store castle coordinates into parameters
        poss_moves = []

        # All moves top left
        if x - 1 >= 0 and y - 1 >= 0:
            if _piece_detect(x, y, x - 1, y - 1, board) == 'opponent obstructed' or \
                    _piece_detect(x, y, x - 1, y - 1, board) == 'unobstructed':
                poss_moves.append([x - 1, y - 1])

        # All moves bottom right
        if x + 1 <= 7 and y + 1 <= 7:
            if _piece_detect(x, y, x + 1, y + 1, board) == 'opponent obstructed' or \
                    _piece_detect(x, y, x + 1, y + 1, board) == 'unobstructed':
                poss_moves.append([x + 1, y + 1])

        # All y moves below y
        if x - 1 >= 0 and y + 1 <= 7:
            if _piece_detect(x, y, x - 1, y + 1, board) == 'opponent obstructed' or \
                    _piece_detect(x, y, x - 1, y + 1, board) == 'unobstructed':
                poss_moves.append([x - 1, y + 1])

        # All x moves above y
        if x + 1 <= 7 and y - 1 >= 0:
            if _piece_detect(x, y, x + 1, y - 1, board) == 'opponent obstructed' or \
                    _piece_detect(x, y, x + 1, y - 1, board) == 'unobstructed':
                poss_moves.append([x + 1, y - 1])

        # All x moves below x
        if x - 1 >= 0:
            if _piece_detect(x, y, x - 1, y, board) == 'opponent obstructed' or \
                    _piece_detect(x, y, x - 1, y, board) == 'unobstructed':
                poss_moves.append([x - 1, y])

        # All x moves above x
        if x + 1 <= 7:
            if _piece_detect(x, y, x + 1, y, board) == 'opponent obstructed' or \
                    _piece_detect(x, y, x + 1, y, board) == 'unobstructed':
                poss_moves.append([x + 1, y])

        # All y moves below y
        if y - 1 >= 0:
            if _piece_detect(x, y, x, y - 1, board) == 'opponent obstructed' or \
                    _piece_detect(x, y, x, y - 1, board) == 'unobstructed':
                poss_moves.append([x, y - 1])

        # All x moves above y
        if y + 1 <= 7:
            if _piece_detect(x, y, x, y + 1, board) == 'opponent obstructed' or \
                    _piece_detect(x, y, x, y + 1, board) == 'unobstructed':
                poss_moves.append([x, y + 1])

        # Castling

        # White Piece
        if getattr(board[x][y], 'colour') == 'white':
            # The king must be at starting position with 0 move count
            if x == 4 and y == 7 and getattr(board[x][y], 'move_count') == 0:
                # The rook on the left must be at starting position with 0 move count
                if getattr(board[0][7], 'str_rep') == 'R' and getattr(board[0][7], 'move_count') == 0:
                    # there must not be anything blocking the path
                    if getattr(board[1][7], 'str_rep') == '-' and \
                            getattr(board[2][7], 'str_rep') == '-' and \
                            getattr(board[3][7], 'str_rep') == '-':
                        # append move to possible moves
                        poss_moves.append([2, 7])
                        # add left castle to self
                        self.left_castle = 2, 7

            if x == 4 and y == 7 and getattr(board[x][y], 'move_count') == 0:
                # The rook on the right must be at starting position with 0 move count
                if getattr(board[7][7], 'str_rep') == 'R' and getattr(board[7][7], 'move_count') == 0:
                    # there must not be anything blocking the path
                    if getattr(board[5][7], 'str_rep') == '-' and \
                            getattr(board[6][7], 'str_rep') == '-':
                        # append move to possible moves
                        poss_moves.append([6, 7])
                        # add right castle to self
                        self.right_castle = 6, 7
        # Black Piece
        if getattr(board[x][y], 'colour') == 'black':
            # The king must be at starting position with 0 move count
            if x == 4 and y == 0 and getattr(board[x][y], 'move_count') == 0:
                # The rook on the left must be at starting position with 0 move count
                if getattr(board[0][0], 'str_rep') == 'r' and getattr(board[0][0], 'move_count') == 0:
                    # there must not be anything blocking the path
                    if getattr(board[1][0], 'str_rep') == '-' and \
                            getattr(board[2][0], 'str_rep') == '-' and \
                            getattr(board[3][0], 'str_rep') == '-':
                        # append move to possible moves
                        poss_moves.append([2, 0])
                        # add left castle to self
                        self.left_castle = 2, 0

            if x == 4 and y == 0 and getattr(board[x][y], 'move_count') == 0:
                # The rook on the right must be at starting position with 0 move count
                if getattr(board[7][0], 'str_rep') == 'r' and getattr(board[7][0], 'move_count') == 0:
                    # there must not be anything blocking the path
                    if getattr(board[5][0], 'str_rep') == '-' and \
                            getattr(board[6][0], 'str_rep') == '-':
                        # append move to possible moves
                        poss_moves.append([6, 0])
                        # add right castle to self
                        self.right_castle = 6, 0

        return poss_moves

    # TODO: Check for whether castle move was made
    def is_castle(self, x, y):
        # Clear both castle variables
        left = self.left_castle
        right = self.right_castle
        print('castle', x, y)
        # check passed parameters with castle possible coordinates
        if (x, y) == left:
            self.right_castle = -1, -1
            self.left_castle = -1, -1
            return 'left'
        elif (x, y) == right:
            self.right_castle = -1, -1
            self.left_castle = -1, -1
            return 'right'
        else:
            return -1

class Blank(_Piece):
    def __init__(self):
        super().__init__(0, 'none', 'Assets/Blank.png', '-')
