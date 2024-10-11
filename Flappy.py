import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 400, 600
white = (255, 255, 255)
black = (0, 0, 0)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Game variables
gravity = 0.25
flap_force = -6
pipe_width = 50
gap_height = 200
pipe_speed = 3

# Bird class
class Bird:
    def __init__(self):
        self.x = width // 4
        self.y = height // 2
        self.velocity = 0
        self.color = (255, 255, 0)
        self.radius = 15

    def flap(self):
        self.velocity = flap_force

    def update(self):
        self.velocity += gravity # type: ignore
        self.y += self.velocity

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, int(self.y)), self.radius)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, height - gap_height - 100)
        self.color = (0, 255, 0)
        self.passed = False

    def move(self):
        self.x -= pipe_speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, 0, pipe_width, self.height))
        pygame.draw.rect(surface, self.color, (self.x, self.height + gap_height, pipe_width, height - self.height - gap_height))

    def collide(self, bird):
        if bird.y - bird.radius < 0 or bird.y + bird.radius > height:
            return True

        if (bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + pipe_width):
            if bird.y - bird.radius < self.height or bird.y + bird.radius > self.height + gap_height:
                return True

        return False

# Main game loop
clock = pygame.time.Clock()
bird = Bird()
pipes = [Pipe(width + i * (width // 2)) for i in range(2)]
score = 0
running = True
while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()

    bird.update()
    if bird.y < bird.radius or bird.y > height - bird.radius:
        # Restart the game if the bird hits the top or bottom
        bird = Bird()
        pipes = [Pipe(width + i * (width // 2)) for i in range(2)]
        score = 0
    for pipe in pipes:
        pipe.move()
        pipe.draw(screen)
        if pipe.x + pipe_width < bird.x and not pipe.passed:
            score += 1
            pipe.passed = True
        if pipe.collide(bird):
            # Restart the game if the bird collides with a pipe
            bird = Bird()
            pipes = [Pipe(width + i * (width // 2)) for i in range(2)]
            score = 0
            break
        if pipe.x < -pipe_width:
            pipes.remove(pipe)
            pipes.append(Pipe(width))

    bird.draw(screen)

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
