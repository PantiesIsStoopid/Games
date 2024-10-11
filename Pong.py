import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Define game variables
BALL_RADIUS = 10
PAD_WIDTH = 10
PAD_HEIGHT = 100
PADDLE_SPEED = 5
BALL_SPEED = 5
score_left = 0
score_right = 0

# Define paddle class
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PAD_WIDTH
        self.height = PAD_HEIGHT

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        if direction == 'up':
            self.y -= PADDLE_SPEED
        elif direction == 'down':
            self.y += PADDLE_SPEED

        # Keep paddle within screen bounds
        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height

# Define ball class
class Ball:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.angle = angle
        self.speed = BALL_SPEED

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Ball collision with top and bottom walls
        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.angle = -self.angle

# Create paddles and ball
paddle_left = Paddle(20, HEIGHT // 2 - PAD_HEIGHT // 2)
paddle_right = Paddle(WIDTH - PAD_WIDTH - 20, HEIGHT // 2 - PAD_HEIGHT // 2)
ball = Ball(WIDTH // 2, HEIGHT // 2, random.uniform(-math.pi/4, math.pi/4))

# Main game loop
clock = pygame.time.Clock()
running = True
playing = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if playing:
        if keys[pygame.K_w]:
            paddle_left.move('up')
        if keys[pygame.K_s]:
            paddle_left.move('down')
        if keys[pygame.K_UP]:
            paddle_right.move('up')
        if keys[pygame.K_DOWN]:
            paddle_right.move('down')
        if keys[pygame.K_r]:
            # Reset scores
            score_left = 0
            score_right = 0

    # Ball collision with paddles
    if (paddle_left.x + PAD_WIDTH >= ball.x - ball.radius >= paddle_left.x and
            paddle_left.y + PAD_HEIGHT >= ball.y >= paddle_left.y):
        ball.x = paddle_left.x + PAD_WIDTH + ball.radius
        ball.angle = math.pi - ball.angle
        ball.speed *= 1.05  # type: ignore # Increase ball speed by 5%

    elif (paddle_right.x <= ball.x + ball.radius <= paddle_right.x + PAD_WIDTH and
          paddle_right.y + PAD_HEIGHT >= ball.y >= paddle_right.y):
        ball.x = paddle_right.x - ball.radius
        ball.angle = math.pi - ball.angle
        ball.speed *= 1.05  # type: ignore # Increase ball speed by 5%

    # Ball movement and scoring
    ball.move()
    if ball.x <= 0:
        score_right += 1
        ball.__init__(WIDTH // 2, HEIGHT // 2, random.uniform(-math.pi/4, math.pi/4))
        ball.speed = BALL_SPEED  # Reset ball speed
    elif ball.x >= WIDTH:
        score_left += 1
        ball.__init__(WIDTH // 2, HEIGHT // 2, random.uniform(-math.pi/4, math.pi/4))
        ball.speed = BALL_SPEED  # Reset ball speed

    # Draw everything
    paddle_left.draw()
    paddle_right.draw()
    ball.draw()

    # Display scores
    font = pygame.font.Font(None, 36)
    text_left = font.render(str(score_left), True, WHITE)
    text_right = font.render(str(score_right), True, WHITE)
    screen.blit(text_left, (WIDTH // 4, 50))
    screen.blit(text_right, (3 * WIDTH // 4, 50))

    if playing:
        if score_left == 10 or score_right == 10:
            playing = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
