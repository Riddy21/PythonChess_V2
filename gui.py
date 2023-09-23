import pygame
import popup
from player import *
from utils import run_in_thread
from settings import *
import logging

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TAN = (236, 235, 205)
GREEN = (104, 139, 80)
GREY = (200, 200, 200)
RED = (255, 200, 200)

class ChessboardGUI:
    def __init__(self, api, p1, p2, interactive=True):
        if p1.color == p2.color:
            raise RuntimeError("Player colors cannot be the same")
        self.api = api
        self.p1 = p1
        self.p2 = p2

        # If popups and user prompts are to be created
        self.interactive=interactive

        # Initialize Pygame
        pygame.init()

        # Set up the window
        self.WIDTH = 400
        self.HEIGHT = 400
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pygame Chessboard")

        # Define the size of each square
        self.SQUARE_SIZE = self.WIDTH // BOARD_WIDTH

        self.piece_images = {
                "r": pygame.image.load("./Assets/Chess_tile_rd.png"),
                "n": pygame.image.load("./Assets/Chess_tile_nd.png"),
                "b": pygame.image.load("./Assets/Chess_tile_bd.png"),
                "q": pygame.image.load("./Assets/Chess_tile_qd.png"),
                "k": pygame.image.load("./Assets/Chess_tile_kd.png"),
                "p": pygame.image.load("./Assets/Chess_tile_pd.png"),
                "R": pygame.image.load("./Assets/Chess_tile_rl.png"),
                "N": pygame.image.load("./Assets/Chess_tile_nl.png"),
                "Q": pygame.image.load("./Assets/Chess_tile_ql.png"),
                "B": pygame.image.load("./Assets/Chess_tile_bl.png"),
                "K": pygame.image.load("./Assets/Chess_tile_kl.png"),
                "P": pygame.image.load("./Assets/Chess_tile_pl.png"),
                }

    def draw_board(self):
        # Clear the window
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                color = GREEN if (row%2 == 1 and col%2 == 0) or (row%2 == 0 and col%2 == 1)else TAN
                col, row = self.orient((col, row))
                x = col * self.SQUARE_SIZE
                y = row * self.SQUARE_SIZE
                rect = pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.window, color, rect)

    # Draw the highlights of the board for next move
    def draw_poss_moves(self, locations):
        for col, row in locations:
            col, row = self.orient((col, row))
            self.draw_dot(col, row)

    # Draws the highligh on the king that is in check
    def draw_check_highlight(self, game_state):
        if 'check' not in game_state:
            return

        if 'black' in game_state:
            coords = self.api.get_piece_coords('k')
        elif 'white' in game_state:
            coords = self.api.get_piece_coords('K')
        if len(coords) != 1:
            logging.error('more than one king')
            return
        for col, row in coords:
            col, row = self.orient((col, row))
            self.draw_highlight(col, row)

    # draw the pieces from the game object
    def draw_pieces(self, board):
        # Get the current chessboard state from the API
        chessboard_state = self.api.get_chess_board_string_array()

        # Draw the chess pieces
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                piece = chessboard_state[row][col]
                self.draw_piece(piece, col, row)

    # Draw highlight on piece
    def draw_highlight(self, col, row):
        x = col * self.SQUARE_SIZE
        y = row * self.SQUARE_SIZE
        rect = pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)
        pygame.draw.rect(self.window, RED, rect)

    # Draw dot on pieces
    def draw_dot(self, col, row):
        x = col * self.SQUARE_SIZE + 0.5 * self.SQUARE_SIZE
        y = row * self.SQUARE_SIZE + 0.5 * self.SQUARE_SIZE
        rect = pygame.draw.circle(self.window, GREY, (x, y), self.SQUARE_SIZE/7)

    def draw_piece(self, piece, col, row):
        piece_image = self.piece_images.get(piece)
        if piece_image:
            col, row = self.orient((col, row))
            x = col * self.SQUARE_SIZE
            y = row * self.SQUARE_SIZE
            width, height = piece_image.get_size()
            self.window.blit(piece_image, (x+(self.SQUARE_SIZE- width)/2, y+(self.SQUARE_SIZE-height)/2))

    def handle_click(self, pos, player):
        # Calculate the clicked square
        col = pos[0] // self.SQUARE_SIZE
        row = pos[1] // self.SQUARE_SIZE

        # Get the chessboard position in algebraic notation
        position = f"{chr(97+col)}{8-row}"

        # Call the API method to interact with the chessboard
        col, row = self.orient((col, row))
        player.handle_move(col, row)
        #self.api.make_move(position)

    def prompt_mate_quit(self, game_state):
        if game_state == 'black checkmate' and self.api.turn == COLORS.BLACK:
            ans = popup.askyesno(title="Checkmate!",
                                 message="Checkmate! %s wins!\nWould you like to quit?" % self.get_prev_player().color.value)
        elif game_state == 'white checkmate' and self.api.turn == COLORS.WHITE:
            ans = popup.askyesno(title="Checkmate!",
                                 message="Checkmate! %s wins!\nWould you like to quit?" % self.get_prev_player().color.value)
        elif game_state == 'black stalemate' and self.api.turn == COLORS.BLACK:
            ans = popup.askyesno(title="Stalemate!",
                                 message="Stalemate!\nWould you like to quit?")
        elif game_state == 'white stalemate' and self.api.turn == COLORS.WHITE:
            ans = popup.askyesno(title="Stalemate!",
                                 message="Stalemate!\nWould you like to quit?")
        elif game_state == 'stalemate':
            ans = popup.askyesno(title="Stalemate!",
                                 message="Stalemate!\nWould you like to quit?")
        else:
            ans = False
            return ans

        if not ans:
            self.get_current_player().undo_move(2)
        return ans

    def get_current_player(self):
        if self.api.turn == self.p1.color:
            return self.p1
        else:
            return self.p2

    def get_prev_player(self):
        if self.api.turn == self.p1.color:
            return self.p2
        else:
            return self.p1

    def prompt_promo(self, game_state):
        # If it's the AI's turn and it is the COMPUTER
        if self.get_current_player().type == Player.COMPUTER:
            return
        if 'promo' in game_state:
            ans = popup.askchoice(title="Promotion",
                                  message="Choose Piece",
                                  options=['Queen', 'Rook', 'Knight', 'Bishop'],
                                  default='Queen')
            self.api.make_pawn_promo(PIECES.get_by_key('display_name', ans))


    def orient(self, coords):
        if self.get_current_player().type == Player.COMPUTER and\
                self.get_prev_player().type == Player.COMPUTER:
            return coords

        if self.get_current_player().type == Player.COMPUTER and\
                self.api.turn == COLORS.BLACK:
            return coords

        if self.get_current_player().type == Player.COMPUTER and\
                self.api.turn == COLORS.WHITE:
            return 7-coords[0], 7-coords[1]
        
        if self.api.turn == COLORS.WHITE:
            return coords
        elif self.api.turn == COLORS.BLACK:
            return 7-coords[0], 7-coords[1]

    def run(self):
        # Main game loop
        running = True

        try:
            while running:
                current_player = self.get_current_player()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.interactive:
                            # Get the position of the mouse click
                            pos = pygame.mouse.get_pos()
                            if current_player.type == Player.HUMAN:
                                self.handle_click(pos, current_player)

                    elif event.type == pygame.KEYDOWN:
                        # Ctrl-Z was pressed
                        if event.key == pygame.K_z and \
                                (pygame.key.get_mods() & pygame.KMOD_CTRL or \
                                 pygame.key.get_mods() & pygame.KMOD_META):
                            if self.interactive:
                                if current_player.type == Player.HUMAN:
                                    if Player.COMPUTER in (self.p1.type, self.p2.type):
                                        self.get_current_player().undo_move(2)
                                    else:
                                        self.get_current_player().undo_move(1)
                        # Save if Ctrl-S is pressed
                        if event.key == pygame.K_s and \
                                (pygame.key.get_mods() & pygame.KMOD_CTRL or \
                                 pygame.key.get_mods() & pygame.KMOD_META):

                            import datetime
                            filename = str(datetime.datetime.now()).replace(' ', '-')+".txt"
                            self.api.export_board(filename)
                            logging.info('Game saved in "%s"!' % filename)


                # Draw the chess board
                self.draw_board()

                # If in check, draw the error highlights
                self.draw_check_highlight(self.api.game_state)

                # Draw the pieces
                self.draw_pieces(self.api.get_chess_board_string_array())

                # Draw markers for next moves
                self.draw_poss_moves(self.api.get_current_poss_moves())

                # Update the display
                pygame.display.flip()

                if self.interactive:
                    if self.prompt_mate_quit(self.api.game_state):
                        running = False

                    self.prompt_promo(self.api.game_state)

                # Have AI do move if ai is enabled
                #if self.get_current_player().type == Player.COMPUTER:
                #        self.get_current_player().make_move()

        except KeyboardInterrupt:
            pass
        self.quit()

    def quit(self):
        # Quit the game
        pygame.quit()
        # only when non-interactive mode
        if self.interactive:
            if self.p1.type == Player.COMPUTER:
                self.p1.quit()
            if self.p2.type == Player.COMPUTER:
                self.p2.quit()
            self.api.quit()
