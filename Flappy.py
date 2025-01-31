import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
Width, Height = 400, 600
White = (255, 255, 255)
Black = (0, 0, 0)
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Flappy Bird")

# Game variables
Gravity = 0.25
FlapForce = -6
PipeWidth = 50
GapHeight = 200
PipeSpeed = 3

# Bird class
class Bird:
    def __init__(self):
        self.X = Width // 4
        self.Y = Height // 2
        self.Velocity = 0
        self.Color = (255, 255, 0)
        self.Radius = 15

    def Flap(self):
        self.Velocity = FlapForce

    def Update(self):
        self.Velocity += Gravity # type: ignore
        self.Y += self.Velocity

    def Draw(self, Surface):
        pygame.draw.circle(Surface, self.Color, (self.X, int(self.Y)), self.Radius)

# Pipe class
class Pipe:
    def __init__(self, X):
        self.X = X
        self.Height = random.randint(100, Height - GapHeight - 100)
        self.Color = (0, 255, 0)
        self.Passed = False

    def Move(self):
        self.X -= PipeSpeed

    def Draw(self, Surface):
        pygame.draw.rect(Surface, self.Color, (self.X, 0, PipeWidth, self.Height))
        pygame.draw.rect(Surface, self.Color, (self.X, self.Height + GapHeight, PipeWidth, Height - self.Height - GapHeight))

    def Collide(self, Bird):
        if Bird.Y - Bird.Radius < 0 or Bird.Y + Bird.Radius > Height:
            return True

        if (Bird.X + Bird.Radius > self.X and Bird.X - Bird.Radius < self.X + PipeWidth):
            if Bird.Y - Bird.Radius < self.Height or Bird.Y + Bird.Radius > self.Height + GapHeight:
                return True

        return False

# Main game loop
Clock = pygame.time.Clock()
Bird = Bird()
Pipes = [Pipe(Width + i * (Width // 2)) for i in range(2)]
Score = 0
Running = True
while Running:
    Screen.fill(Black)

    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False
        elif Event.type == pygame.KEYDOWN:
            if Event.key == pygame.K_SPACE:
                Bird.Flap()

    Bird.Update()
    if Bird.Y < Bird.Radius or Bird.Y > Height - Bird.Radius:
        # Restart the game if the bird hits the top or bottom
        Bird = Bird()
        Pipes = [Pipe(Width + i * (Width // 2)) for i in range(2)]
        Score = 0
    for Pipe in Pipes:
        Pipe.Move()
        Pipe.Draw(Screen)
        if Pipe.X + PipeWidth < Bird.X and not Pipe.Passed:
            Score += 1
            Pipe.Passed = True
        if Pipe.Collide(Bird):
            # Restart the game if the bird collides with a pipe
            Bird = Bird()
            Pipes = [Pipe(Width + i * (Width // 2)) for i in range(2)]
            Score = 0
            break
        if Pipe.X < -PipeWidth:
            Pipes.remove(Pipe)
            Pipes.append(Pipe(Width))

    Bird.Draw(Screen)

    # Display score
    Font = pygame.font.Font(None, 36)
    Text = Font.render("Score: " + str(Score), True, White)
    Screen.blit(Text, (10, 10))

    pygame.display.flip()
    Clock.tick(60)

pygame.quit()
