import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
Width, Height = 800, 600
White = (255, 255, 255)
Gray = (200, 200, 200)
Black = (0, 0, 0)
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Minesweeper")

# Game variables
Rows, Cols = 10, 10
TileSize = 50
MineCount = 10
Font = pygame.font.Font(None, 40)

# Define colors for numbers
NumColors = {
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
Mines = set()
while len(Mines) < MineCount:
    Mines.add((random.randint(0, Rows - 1), random.randint(0, Cols - 1)))

# Initialize game board
Board = [[0 for _ in range(Cols)] for _ in range(Rows)]
for Row, Col in Mines:
    Board[Row][Col] = -1

# Calculate adjacent mine counts
for Row in range(Rows):
    for Col in range(Cols):
        if Board[Row][Col] != -1:
            Count = sum(1 for i in range(Row - 1, Row + 2)
                        for j in range(Col - 1, Col + 2)
                        if (0 <= i < Rows and 0 <= j < Cols and Board[i][j] == -1))
            Board[Row][Col] = Count

# Function to reveal tiles
def Reveal(Row, Col):
    if 0 <= Row < Rows and 0 <= Col < Cols and not Revealed[Row][Col]:
        Revealed[Row][Col] = True
        if Board[Row][Col] == 0:
            for i in range(Row - 1, Row + 2):
                for j in range(Col - 1, Col + 2):
                    Reveal(i, j)

# Function to draw game over screen and restart game
def DrawGameOver():
    Screen.fill(Gray)
    GameOverText = Font.render("Game Over! Press R to restart", True, Black)
    GameOverRect = GameOverText.get_rect(center=(Width // 2, Height // 2))
    Screen.blit(GameOverText, GameOverRect)
    pygame.display.flip()
    while True:
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if Event.type == pygame.KEYDOWN:
                if Event.key == pygame.K_r:
                    # Restart the game
                    return True

# Main game loop
Clock = pygame.time.Clock()
Revealed = [[False for _ in range(Cols)] for _ in range(Rows)]
Flagged = [[False for _ in range(Cols)] for _ in range(Rows)]
GameOver = False
Running = True
while Running:
    Screen.fill(Gray)

    # Event handling
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False
        elif not GameOver and Event.type == pygame.MOUSEBUTTONDOWN:
            if Event.button == 1:
                X, Y = Event.pos
                Row, Col = Y // TileSize, X // TileSize
                if (Row, Col) in Mines:
                    GameOver = True
                else:
                    Reveal(Row, Col)
            elif Event.button == 3:
                X, Y = Event.pos
                Row, Col = Y // TileSize, X // TileSize
                Flagged[Row][Col] = not Flagged[Row][Col]
        elif GameOver and Event.type == pygame.KEYDOWN:
            if Event.key == pygame.K_r:
                # Restart the game
                GameOver = False
                Mines = set()
                while len(Mines) < MineCount:
                    Mines.add((random.randint(0, Rows - 1), random.randint(0, Cols - 1)))
                Board = [[0 for _ in range(Cols)] for _ in range(Rows)]
                for Row, Col in Mines:
                    Board[Row][Col] = -1
                for Row in range(Rows):
                    for Col in range(Cols):
                        if Board[Row][Col] != -1:
                            Count = sum(1 for i in range(Row - 1, Row + 2)
                                        for j in range(Col - 1, Col + 2)
                                        if (0 <= i < Rows and 0 <= j < Cols and Board[i][j] == -1))
                            Board[Row][Col] = Count
                Revealed = [[False for _ in range(Cols)] for _ in range(Rows)]
                Flagged = [[False for _ in range(Cols)] for _ in range(Rows)]
                break

    # Draw tiles
    for Row in range(Rows):
        for Col in range(Cols):
            Rect = pygame.Rect(Col * TileSize, Row * TileSize, TileSize, TileSize)
            pygame.draw.rect(Screen, White, Rect, 2)
            if Revealed[Row][Col]:
                if Board[Row][Col] == -1:
                    pygame.draw.circle(Screen, Black, Rect.center, TileSize // 4)
                elif Board[Row][Col] != 0:
                    Text = Font.render(str(Board[Row][Col]), True, NumColors[Board[Row][Col]])
                    TextRect = Text.get_rect(center=Rect.center)
                    Screen.blit(Text, TextRect)
                else:
                    pygame.draw.rect(Screen, Gray, Rect)
            elif Flagged[Row][Col]:
                pygame.draw.line(Screen, Black, Rect.topleft, Rect.bottomright, 2)
                pygame.draw.line(Screen, Black, Rect.bottomleft, Rect.topright, 2)

    # Check for game over
    if GameOver:
        if DrawGameOver():
            GameOver = False
            Mines = set()
            while len(Mines) < MineCount:
                Mines.add((random.randint(0, Rows - 1), random.randint(0, Cols - 1)))
            Board = [[0 for _ in range(Cols)] for _ in range(Rows)]
            for Row, Col in Mines:
                Board[Row][Col] = -1
            for Row in range(Rows):
                for Row in range(Rows):
                    for Col in range(Cols):
                        if Board[Row][Col] != -1:
                            Count = sum(1 for i in range(Row - 1, Row + 2)
                        for j in range(Col - 1, Col + 2)
                        if (0 <= i < Rows and 0 <= j < Cols and Board[i][j] == -1))
                            Board[Row][Col] = Count
                            Revealed = [[False for _ in range(Cols)] for _ in range(Rows)]
                            Flagged = [[False for _ in range(Cols)] for _ in range(Rows)]


    # Draw tiles
    for Row in range(Rows):
        for Col in range(Cols):
            Rect = pygame.Rect(Col * TileSize, Row * TileSize, TileSize, TileSize)
            pygame.draw.rect(Screen, White, Rect, 2)
            if Revealed[Row][Col]:
                if Board[Row][Col] == -1:
                    pygame.draw.circle(Screen, Black, Rect.center, TileSize // 4)
                elif Board[Row][Col] != 0:
                    Text = Font.render(str(Board[Row][Col]), True, NumColors[Board[Row][Col]])
                    TextRect = Text.get_rect(center=Rect.center)
                    Screen.blit(Text, TextRect)
                else:
                    pygame.draw.rect(Screen, Gray, Rect)
            elif Flagged[Row][Col]:
                pygame.draw.line(Screen, Black, Rect.topleft, Rect.bottomright, 2)
                pygame.draw.line(Screen, Black, Rect.bottomleft, Rect.topright, 2)

    # Check for game over
    if GameOver:
        if DrawGameOver():
            GameOver = False
            Mines = set()
            while len(Mines) < MineCount:
                Mines.add((random.randint(0, Rows - 1), random.randint(0, Cols - 1)))
            Board = [[0 for _ in range(Cols)] for _ in range(Rows)]
            for Row, Col in Mines:
                Board[Row][Col] = -1
            for Row in range(Rows):
                for Col in range(Cols):
                    if Board[Row][Col] != -1:
                        Count = sum(1 for i in range(Row - 1, Row + 2)
                                    for j in range(Col - 1, Col + 2)
                                    if (0 <= i < Rows and 0 <= j < Cols and Board[i][j] == -1))
                        Board[Row][Col] = Count
            Revealed = [[False for _ in range(Cols)] for _ in range(Rows)]
    pygame.display.flip()
    Clock.tick(60)

pygame.quit()











