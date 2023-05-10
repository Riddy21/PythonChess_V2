import pygame

# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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

        # Load the chessboard image
        self.chessboard_image = pygame.image.load("./Assets/Blank.png")

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
            "N": pygame.image.load("./Assets/Chess_tile_bl.png"),
            "Q": pygame.image.load("./Assets/Chess_tile_ql.png"),
            "K": pygame.image.load("./Assets/Chess_tile_kl.png"),
            "P": pygame.image.load("./Assets/Chess_tile_pl.png"),
        }

    def draw_piece(self, piece, col, row):
        piece_image = self.piece_images.get(piece)
        if piece_image:
            x = col * self.SQUARE_SIZE
            y = row * self.SQUARE_SIZE
            self.window.blit(piece_image, (x, y))

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

                    # Calculate the clicked square
                    col = pos[0] // self.SQUARE_SIZE
                    row = pos[1] // self.SQUARE_SIZE

                    # Get the chessboard position in algebraic notation
                    position = f"{chr(97+col)}{8-row}"

                    # Call the API method to interact with the chessboard
                    print(position)
                    #self.api.make_move(position)

            # Clear the window
            self.window.fill(WHITE)

            # Draw the chessboard image
            self.window.blit(self.chessboard_image, (0, 0))

            # Get the current chessboard state from the API
            chessboard_state = [['r' for i in range(8)] for i in range(8)]

            # Draw the chess pieces
            for row in range(8):
                for col in range(8):
                    piece = chessboard_state[row][col]
                    self.draw_piece(piece, col, row)

            # Update the display
            pygame.display.flip()

        # Quit the game
        pygame.quit()

ChessboardGUI(None).run()
