import pygame

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TAN = (236, 235, 205)
GREEN = (104, 139, 80)

class ChessboardGUI:
    def __init__(self, api):
        self.api = api

        # Initialize Pygame
        pygame.init()

        # Set up the window
        self.WIDTH = 480
        self.HEIGHT = 480
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pygame Chessboard")

        # Define the size of each square
        self.SQUARE_SIZE = self.WIDTH // 8

        # Load the chess piece images
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
        # TODO: Delete that line and write a generative board
        # Clear the window
        self.window.fill(WHITE)

        for row in range(8):
            for col in range(8):
                color = GREEN if (row%2 == 1 and col%2 == 0) or (row%2 == 0 and col%2 == 1)else TAN
                x = col * self.SQUARE_SIZE
                y = row * self.SQUARE_SIZE
                rect = pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.window, color, rect)

    # TODO: Draw the highlights of the board for next move
    def draw_highlights(self, locations):
        pass

    # TODO: draw the pieces from the game object
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
            x = col * self.SQUARE_SIZE
            y = row * self.SQUARE_SIZE
            self.window.blit(piece_image, (x, y))

    def handle_click(self, pos):
        # Calculate the clicked square
        col = pos[0] // self.SQUARE_SIZE
        row = pos[1] // self.SQUARE_SIZE

        # Get the chessboard position in algebraic notation
        position = f"{chr(97+col)}{8-row}"

        # Call the API method to interact with the chessboard
        print(position)
        #self.api.make_move(position)


    def run(self):
        # Main game loop
        running = True
        
        # Draw the chess board
        self.draw_board()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the position of the mouse click
                    pos = pygame.mouse.get_pos()

                    self.handle_click(pos)
                # TODO: Add undo buttons based on keyboard shortcut Ctrl-z

            # Draw highlights for next moves
            self.draw_highlights(None)

            # Draw the pieces
            self.draw_pieces(self.api.get_chess_board_string_array())

            # TODO: If in check, show Popup use TKinter

            # TODO: If in checkmate, show GUI for quitting

            # Update the display
            pygame.display.flip()

        # Quit the game
        pygame.quit()

#ChessboardGUI(None).run()
