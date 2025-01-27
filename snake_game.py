import pygame
import time
import random

# Initialize pygame
pygame.init()

# Load high score from a file
def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
        except FileNotFoundError:
            return 0
    
# Save high score to a file
def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

# Initialize score
score = 0
high_score = load_high_score()

# Screen size
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20  # Size of snake and food blocks

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Directions
UP = (0, -BLOCK_SIZE)
DOWN = (0, BLOCK_SIZE)
LEFT = (-BLOCK_SIZE, 0)
RIGHT = (BLOCK_SIZE, 0)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font = pygame.font.SysFont(None, 35)

def show_score(score, high_score):
    score_text = font.render(f"Score: {score} High Score: {high_score}", True, (255, 255, 255))
    screen.blit(score_text, [10, 10]) #Draw at the top-left corner

# Inside your game loop, call:
show_score(score, high_score)

# Snake setup
snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake body
direction = RIGHT  # Initial direction

# Food setup
food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))

# Score
score = 0
font = pygame.font.Font(None, 35)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != DOWN:
                direction = UP
            elif event.key == pygame.K_DOWN and direction != UP:
                direction = DOWN
            elif event.key == pygame.K_LEFT and direction != RIGHT:
                direction = LEFT
            elif event.key == pygame.K_RIGHT and direction != LEFT:
                direction = RIGHT

    # Move snake
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    
    # Check for collision with walls or itself
    if new_head in snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
        running = False  # Game over
    
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    score = 0  # Reset score after game over

    # Add new head to snake
    snake.insert(0, new_head)
    
    # Check if food is eaten
    if new_head == food:
        score += 1
        food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
    else:
        snake.pop()  # Remove last segment

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

    # Draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(10)  # Control speed

pygame.quit()