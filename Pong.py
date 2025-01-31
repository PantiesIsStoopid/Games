import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
Width, Height = 800, 600
White = (255, 255, 255)
Black = (0, 0, 0)
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Pong")

# Define game variables
BallRadius = 10
PadWidth = 10
PadHeight = 100
PaddleSpeed = 5
BallSpeed = 5
ScoreLeft = 0
ScoreRight = 0

# Define paddle class
class Paddle:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.Width = PadWidth
        self.Height = PadHeight

    def Draw(self):
        pygame.draw.rect(Screen, White, (self.X, self.Y, self.Width, self.Height))

    def Move(self, Direction):
        if Direction == 'up':
            self.Y -= PaddleSpeed
        elif Direction == 'down':
            self.Y += PaddleSpeed

        # Keep paddle within screen bounds
        if self.Y < 0:
            self.Y = 0
        elif self.Y > Height - self.Height:
            self.Y = Height - self.Height

# Define ball class
class Ball:
    def __init__(self, x, y, angle):
        self.X = x
        self.Y = y
        self.Radius = BallRadius
        self.Angle = angle
        self.Speed = BallSpeed

    def Draw(self):
        pygame.draw.circle(Screen, White, (self.X, self.Y), self.Radius)

    def Move(self):
        self.X += self.Speed * math.cos(self.Angle)
        self.Y += self.Speed * math.sin(self.Angle)

        # Ball collision with top and bottom walls
        if self.Y <= self.Radius or self.Y >= Height - self.Radius:
            self.Angle = -self.Angle

# Create paddles and ball
PaddleLeft = Paddle(20, Height // 2 - PadHeight // 2)
PaddleRight = Paddle(Width - PadWidth - 20, Height // 2 - PadHeight // 2)
Ball = Ball(Width // 2, Height // 2, random.uniform(-math.pi/4, math.pi/4))

# Main game loop
Clock = pygame.time.Clock()
Running = True
Playing = True
while Running:
    Screen.fill(Black)

    # Event handling
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False

    Keys = pygame.key.get_pressed()
    if Playing:
        if Keys[pygame.K_w]:
            PaddleLeft.Move('up')
        if Keys[pygame.K_s]:
            PaddleLeft.Move('down')
        if Keys[pygame.K_UP]:
            PaddleRight.Move('up')
        if Keys[pygame.K_DOWN]:
            PaddleRight.Move('down')
        if Keys[pygame.K_r]:
            # Reset scores
            ScoreLeft = 0
            ScoreRight = 0

    # Ball collision with paddles
    if (PaddleLeft.X + PadWidth >= Ball.X - Ball.Radius >= PaddleLeft.X and
            PaddleLeft.Y + PadHeight >= Ball.Y >= PaddleLeft.Y):
        Ball.X = PaddleLeft.X + PadWidth + Ball.Radius
        Ball.Angle = math.pi - Ball.Angle
        Ball.Speed *= 1.05  # type: ignore # Increase ball speed by 5%

    elif (PaddleRight.X <= Ball.X + Ball.Radius <= PaddleRight.X + PadWidth and
          PaddleRight.Y + PadHeight >= Ball.Y >= PaddleRight.Y):
        Ball.X = PaddleRight.X - Ball.Radius
        Ball.Angle = math.pi - Ball.Angle
        Ball.Speed *= 1.05  # type: ignore # Increase ball speed by 5%

    # Ball movement and scoring
    Ball.Move()
    if Ball.X <= 0:
        ScoreRight += 1
        Ball.__init__(Width // 2, Height // 2, random.uniform(-math.pi/4, math.pi/4))
        Ball.Speed = BallSpeed  # Reset ball speed
    elif Ball.X >= Width:
        ScoreLeft += 1
        Ball.__init__(Width // 2, Height // 2, random.uniform(-math.pi/4, math.pi/4))
        Ball.Speed = BallSpeed  # Reset ball speed

    # Draw everything
    PaddleLeft.Draw()
    PaddleRight.Draw()
    Ball.Draw()

    # Display scores
    Font = pygame.font.Font(None, 36)
    TextLeft = Font.render(str(ScoreLeft), True, White)
    TextRight = Font.render(str(ScoreRight), True, White)
    Screen.blit(TextLeft, (Width // 4, 50))
    Screen.blit(TextRight, (3 * Width // 4, 50))

    if Playing:
        if ScoreLeft == 10 or ScoreRight == 10:
            Playing = False

    pygame.display.flip()
    Clock.tick(60)

pygame.quit()
