import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Game variables
ROWS, COLS = 10, 10
TILE_SIZE = 50
MINE_COUNT = 10
FONT = pygame.font.Font(None, 40)

# Define colors for numbers
NUM_COLORS = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128),
}

# Generate mines
mines = set()
while len(mines) < MINE_COUNT:
    mines.add((random.randint(0, ROWS - 1), random.randint(0, COLS - 1)))

# Initialize game board
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
for row, col in mines:
    board[row][col] = -1

# Calculate adjacent mine counts
for row in range(ROWS):
    for col in range(COLS):
        if board[row][col] != -1:
            count = sum(1 for i in range(row - 1, row + 2)
                        for j in range(col - 1, col + 2)
                        if (0 <= i < ROWS and 0 <= j < COLS and board[i][j] == -1))
            board[row][col] = count

# Function to reveal tiles
def reveal(row, col):
    if 0 <= row < ROWS and 0 <= col < COLS and not revealed[row][col]:
        revealed[row][col] = True
        if board[row][col] == 0:
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    reveal(i, j)

# Function to draw game over screen and restart game
def draw_game_over():
    screen.fill(GRAY)
    game_over_text = FONT.render("Game Over! Press R to restart", True, BLACK)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    return True

# Main game loop
clock = pygame.time.Clock()
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
game_over = False
running = True
while running:
    screen.fill(GRAY)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                row, col = y // TILE_SIZE, x // TILE_SIZE
                if (row, col) in mines:
                    game_over = True
                else:
                    reveal(row, col)
            elif event.button == 3:
                x, y = event.pos
                row, col = y // TILE_SIZE, x // TILE_SIZE
                flagged[row][col] = not flagged[row][col]
        elif game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Restart the game
                game_over = False
                mines = set()
                while len(mines) < MINE_COUNT:
                    mines.add((random.randint(0, ROWS - 1), random.randint(0, COLS - 1)))
                board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                for row, col in mines:
                    board[row][col] = -1
                for row in range(ROWS):
                    for col in range(COLS):
                        if board[row][col] != -1:
                            count = sum(1 for i in range(row - 1, row + 2)
                                        for j in range(col - 1, col + 2)
                                        if (0 <= i < ROWS and 0 <= j < COLS and board[i][j] == -1))
                            board[row][col] = count
                revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
                flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
                break

    # Draw tiles
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 2)
            if revealed[row][col]:
                if board[row][col] == -1:
                    pygame.draw.circle(screen, BLACK, rect.center, TILE_SIZE // 4)
                elif board[row][col] != 0:
                    text = FONT.render(str(board[row][col]), True, NUM_COLORS[board[row][col]])
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
            elif flagged[row][col]:
                pygame.draw.line(screen, BLACK, rect.topleft, rect.bottomright, 2)
                pygame.draw.line(screen, BLACK, rect.bottomleft, rect.topright, 2)

    # Check for game over
    if game_over:
        if draw_game_over():
            game_over = False
            mines = set()
            while len(mines) < MINE_COUNT:
                mines.add((random.randint(0, ROWS - 1), random.randint(0, COLS - 1)))
            board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
            for row, col in mines:
                board[row][col] = -1
            for row in range(ROWS):
                for row in range(ROWS):
                    for col in range(COLS):
                        if board[row][col] != -1:
                            count = sum(1 for i in range(row - 1, row + 2)
                        for j in range(col - 1, col + 2)
                        if (0 <= i < ROWS and 0 <= j < COLS and board[i][j] == -1))
                            board[row][col] = count
                            revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
                            flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]


    # Draw tiles
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 2)
            if revealed[row][col]:
                if board[row][col] == -1:
                    pygame.draw.circle(screen, BLACK, rect.center, TILE_SIZE // 4)
                elif board[row][col] != 0:
                    text = FONT.render(str(board[row][col]), True, NUM_COLORS[board[row][col]])
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
            elif flagged[row][col]:
                pygame.draw.line(screen, BLACK, rect.topleft, rect.bottomright, 2)
                pygame.draw.line(screen, BLACK, rect.bottomleft, rect.topright, 2)

    # Check for game over
    if game_over:
        if draw_game_over():
            game_over = False
            mines = set()
            while len(mines) < MINE_COUNT:
                mines.add((random.randint(0, ROWS - 1), random.randint(0, COLS - 1)))
            board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
            for row, col in mines:
                board[row][col] = -1
            for row in range(ROWS):
                for col in range(COLS):
                    if board[row][col] != -1:
                        count = sum(1 for i in range(row - 1, row + 2)
                                    for j in range(col - 1, col + 2)
                                    if (0 <= i < ROWS and 0 <= j < COLS and board[i][j] == -1))
                        board[row][col] = count
            revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    pygame.display.flip()
    clock.tick(60)

pygame.quit()












