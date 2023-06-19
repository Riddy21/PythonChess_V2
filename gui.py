import pygame
import popup

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TAN = (236, 235, 205)
GREEN = (104, 139, 80)
GREY = (200, 200, 200)
RED = (255, 200, 200)

class ChessboardGUI:
    def __init__(self, api, ai=None):
        self.api = api
        self.ai = ai

        # Initialize Pygame
        pygame.init()

        # Set up the window
        self.WIDTH = 400
        self.HEIGHT = 400
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pygame Chessboard")

        # Define the size of each square
        self.SQUARE_SIZE = self.WIDTH // 8

        # Load the chess piece images
        self.piece_images = {
            "-": pygame.image.load("./Assets/Blank.png"),
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
        for row in range(8):
            for col in range(8):
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
            print('Error: more than one king')
            return
        for col, row in coords:
            self.draw_highlight(col, row)

    # draw the pieces from the game object
    def draw_pieces(self, board):
        # Get the current chessboard state from the API
        chessboard_state = self.api.get_chess_board_string_array()

        # Draw the chess pieces
        for row in range(8):
            for col in range(8):
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

    def handle_click(self, pos):
        # Calculate the clicked square
        col = pos[0] // self.SQUARE_SIZE
        row = pos[1] // self.SQUARE_SIZE

        # Get the chessboard position in algebraic notation
        position = f"{chr(97+col)}{8-row}"

        # Call the API method to interact with the chessboard
        col, row = self.orient((col, row))
        self.api.handle_move(col, row)
        #self.api.make_move(position)

    def prompt_checkmate_quit(self, game_state):
        if 'mate' in game_state:
            ans = popup.askyesno(title="Checkmate!",
                                 message="Checkmate!\nWould you like to quit?")
            self.api.undo_move()
            return ans
        return False

    def prompt_promo(self, game_state):
        if 'promo' in game_state:
            ans = popup.askchoice(options=['Queen', 'Rook', 'Knight', 'Bishop'],
                                  default='Queen')
            print(ans)
            self.api.make_pawn_promo(ans)


    def orient(self, coords):
        if self.ai:
            return coords
        
        if self.api.turn == 'white':
            return coords
        elif self.api.turn == 'black':
            return 7-coords[0], 7-coords[1]

    def run(self):
        # Main game loop
        running = True

        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Get the position of the mouse click
                        pos = pygame.mouse.get_pos()

                        if self.api.turn != self.ai.color:
                            self.handle_click(pos)

                    elif event.type == pygame.KEYDOWN:
                        # Ctrl-Z was pressed
                        if event.key == pygame.K_z and \
                                (pygame.key.get_mods() & pygame.KMOD_CTRL or \
                                 pygame.key.get_mods() & pygame.KMOD_META):
                            if self.api.turn != self.ai.color:
                                # One player undo twice
                                if self.ai:
                                    self.api.undo_move()

                                self.api.undo_move()

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

                if self.prompt_checkmate_quit(self.api.game_state):
                    running = False

                self.prompt_promo(self.api.game_state)

                # Have AI do move if ai is enabled
                if self.ai and self.api.turn == self.ai.color:
                    self.ai.make_move()

        except KeyboardInterrupt:
            self.quit()

    def quit(self):
        # Quit the game
        pygame.quit()
