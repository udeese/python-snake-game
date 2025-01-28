import sys
import pygame
import time
import random

# Initialize pygame
pygame.init()

# Direction constants
UP = (0, -20)
DOWN = (0, 20)
LEFT = (-20, 0)
RIGHT = (20, 0)

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake setup
snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake body
direction = RIGHT  # Initial direction

pygame.mixer.init() # Initialize the mixer

# Load sound effects
chomp_sound = pygame.mixer.Sound("chomp.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

# Load high score from a file
def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            content = file.read().strip() # Remove extra spaces/newlines
            return int(content) if content.isdigit() else 0 # Check if content is a number
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
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20  # Size of snake and food blocks

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SNAKE_COLOR = (128, 0, 128) # Purple
FOOD_COLOR = (255, 0, 0) # Red

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

# Food setup
food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))

# Score
score = 0
font = pygame.font.Font(None, 35)

# Check for collision with walls or itself
def check_game_over(new_head):
    print(f"Checking new head position: {new_head}") # Debugging
    if new_head in snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            print("Game over triggered!") # Debugging
            game_over_sound.play() # Play game over sound
            draw_game_over_screen() # Show restart prompt
            return True # Reset game state
    return False
        
# Game loop
def reset_game():
    global snake, direction, score, food, running
    snake = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2 - BLOCK_SIZE, HEIGHT //2)] # Reset snake position
    direction = (BLOCK_SIZE, 0) # Reset direction
    score = 0 # Reset score
    food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)) # New food
    running = True # Restart game

def draw_game_over_screen():
    global running
    # Fill screen with black
    screen.fill(BLACK)

    # Display game over text
    font = pygame.font.Font(None, 50)  
    text = font.render("Game Over! Press R to restart or Q to quit", True, WHITE)
    text_x = (WIDTH - text.get_width()) // 2
    text_y = (HEIGHT - text.get_height()) // 2
    screen.blit(text, (text_x, text_y))# Center text

    # Update the screen to show the text
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

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
            elif event.key == pygame.K_r:
                reset_game()

    # Move snake
    if snake:  # Ensure snake is not empty
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        if check_game_over(new_head):
            continue

        # Add new head to snake
        snake.insert(0, new_head)

        if new_head == food:
            chomp_sound.play() # Play chomp sound
            score += 1
            food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE)) # New food
        else:
            snake.pop()

        # Check if food is eaten
        if new_head == food:
            chomp_sound.play() # Play chomp sound
            score += 1
            food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
        
        if score > high_score:
            high_score = score
            save_high_score(high_score) # Save high score to file

        print(snake)
        # Draw snake
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, SNAKE_COLOR, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

        # Draw food
        pygame.draw.rect(screen, FOOD_COLOR, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

        # Display score
        score_text = font.render(f"Score: {score} High Score {high_score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(10)  # Control speed

# Main game loop
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

    if check_game_over(new_head):
        draw_game_over_screen()
        continue

    # Update snake position
    snake.insert(0, new_head)
    if new_head == food:
        chomp_sound.play()
        score += 1
        food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
    else:
        snake.pop()

    # Draw everything
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
