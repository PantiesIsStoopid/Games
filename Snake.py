import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Game variables
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
INITIAL_LENGTH = 3
SNAKE_SPEED = 10

# Define directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = INITIAL_LENGTH
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def turn(self, direction):
        if self.length > 1 and (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        else:
            self.direction = direction

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + x) % GRID_WIDTH), (cur[1] + y) % GRID_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new) # type: ignore
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = INITIAL_LENGTH
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

# Fruit class
class Fruit:
    def __init__(self):
        self.position = (0, 0)
        self.color = BLACK
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        r = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

# Main game loop
clock = pygame.time.Clock()
snake = Snake()
fruit = Fruit()
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.turn(UP)
            elif event.key == pygame.K_DOWN:
                snake.turn(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.turn(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.turn(RIGHT)

    snake.move()
    if snake.get_head_position() == fruit.position:
        snake.length += 1
        fruit.randomize_position()

    snake.draw(screen)
    fruit.draw(screen)
    pygame.display.flip()
    clock.tick(SNAKE_SPEED)

pygame.quit()
