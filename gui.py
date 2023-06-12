import pygame
import tkinter as tk
import tkinter.messagebox

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TAN = (236, 235, 205)
GREEN = (104, 139, 80)
GREY = (200, 200, 200)

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
    def draw_highlights(self, locations):
        for col, row in locations:
            col, row = self.orient((col, row))
            x = col * self.SQUARE_SIZE + 0.5 * self.SQUARE_SIZE
            y = row * self.SQUARE_SIZE + 0.5 * self.SQUARE_SIZE
            rect = pygame.draw.circle(self.window, GREY, (x, y), self.SQUARE_SIZE/7)

    # draw the pieces from the game object
    def draw_pieces(self, board):
        # Get the current chessboard state from the API
        chessboard_state = self.api.get_chess_board_string_array()

        # Draw the chess pieces
        for row in range(8):
            for col in range(8):
                piece = chessboard_state[row][col]
                self.draw_piece(piece, col, row)


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

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the position of the mouse click
                    pos = pygame.mouse.get_pos()

                    self.handle_click(pos)

                elif event.type == pygame.KEYDOWN:
                    # Ctrl-Z was pressed
                    if event.key == pygame.K_z and \
                            (pygame.key.get_mods() & pygame.KMOD_CTRL or \
                             pygame.key.get_mods() & pygame.KMOD_META):
                        self.api.undo_move()

            # Draw the chess board
            self.draw_board()

            # Draw the pieces
            self.draw_pieces(self.api.get_chess_board_string_array())

            # Draw highlights for next moves
            self.draw_highlights(self.api.get_current_poss_moves())

            # TODO: If in check, show Popup using TKinter
            game_state = self.api.get_game_state()
            if 'checkmate' in game_state:
                response = tk.messagebox.askyesno("Checkmate", "Checkmate! Do you want to quit?")
                if response:
                    running = False
            # TODO: If in checkmate, show GUI for quitting
            elif 'check' in game_state:
                tk.messagebox.showinfo("Check", "You are in check!")


            # Have AI do move if ai is enabled
            if self.ai and self.api.turn == self.ai.color:
                self.ai.make_move()


            # Update the display
            pygame.display.flip()

        # Quit the game
        pygame.quit()

#ChessboardGUI(None).run()
