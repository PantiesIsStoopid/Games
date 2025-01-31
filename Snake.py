import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
Width, Height = 800, 600
White = (255, 255, 255)
Black = (0, 0, 0)
Green = (0, 255, 0)
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Snake")

# Game variables
GridSize = 20
GridWidth = Width // GridSize
GridHeight = Height // GridSize
InitialLength = 3
SnakeSpeed = 10

# Define directions
Up = (0, -1)
Down = (0, 1)
Left = (-1, 0)
Right = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.Length = InitialLength
        self.Positions = [(GridWidth // 2, GridHeight // 2)]
        self.Direction = random.choice([Up, Down, Left, Right])
        self.Color = Green

    def GetHeadPosition(self):
        return self.Positions[0]

    def Turn(self, Direction):
        if self.Length > 1 and (Direction[0] * -1, Direction[1] * -1) == self.Direction:
            return
        else:
            self.Direction = Direction

    def Move(self):
        Cur = self.GetHeadPosition()
        X, Y = self.Direction
        New = (((Cur[0] + X) % GridWidth), (Cur[1] + Y) % GridHeight)
        if len(self.Positions) > 2 and New in self.Positions[2:]:
            self.Reset()
        else:
            self.Positions.insert(0, New) # type: ignore
            if len(self.Positions) > self.Length:
                self.Positions.pop()

    def Reset(self):
        self.Length = InitialLength
        self.Positions = [(GridWidth // 2, GridHeight // 2)]
        self.Direction = random.choice([Up, Down, Left, Right])

    def Draw(self, Surface):
        for P in self.Positions:
            R = pygame.Rect((P[0] * GridSize, P[1] * GridSize), (GridSize, GridSize))
            pygame.draw.rect(Surface, self.Color, R)
            pygame.draw.rect(Surface, White, R, 1)

# Fruit class
class Fruit:
    def __init__(self):
        self.Position = (0, 0)
        self.Color = Black
        self.RandomizePosition()

    def RandomizePosition(self):
        self.Position = (random.randint(0, GridWidth - 1), random.randint(0, GridHeight - 1))

    def Draw(self, Surface):
        R = pygame.Rect((self.Position[0] * GridSize, self.Position[1] * GridSize), (GridSize, GridSize))
        pygame.draw.rect(Surface, self.Color, R)
        pygame.draw.rect(Surface, White, R, 1)

# Main game loop
Clock = pygame.time.Clock()
Snake = Snake()
Fruit = Fruit()
Running = True
while Running:
    Screen.fill(Black)

    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False
        elif Event.type == pygame.KEYDOWN:
            if Event.key == pygame.K_UP:
                Snake.Turn(Up)
            elif Event.key == pygame.K_DOWN:
                Snake.Turn(Down)
            elif Event.key == pygame.K_LEFT:
                Snake.Turn(Left)
            elif Event.key == pygame.K_RIGHT:
                Snake.Turn(Right)

    Snake.Move()
    if Snake.GetHeadPosition() == Fruit.Position:
        Snake.Length += 1
        Fruit.RandomizePosition()

    Snake.Draw(Screen)
    Fruit.Draw(Screen)
    pygame.display.flip()
    Clock.tick(SnakeSpeed)

pygame.quit()
