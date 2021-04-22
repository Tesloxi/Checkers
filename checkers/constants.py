from pygame import image, transform

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (128, 128, 128)
BEIGE = (255, 199, 143)
BROWN = (128, 64, 42)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CROWN = transform.scale(image.load("checkers/assets/crown.png"), (45, 25))