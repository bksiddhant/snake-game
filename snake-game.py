import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Window size
WINDOW_X = 600
WINDOW_Y = 400

# Colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREEN = pygame.Color(0, 255, 0)
RED = pygame.Color(255, 0, 0)

# FPS controller
clock = pygame.time.Clock()

# Game window
screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
pygame.display.set_caption("🐍 Snake Game")

# Snake and food settings
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = "RIGHT"
change_to = direction

speed = 10
food_pos = [random.randrange(1, (WINDOW_X//10)) * 10,
            random.randrange(1, (WINDOW_Y//10)) * 10]
food_spawn = True

score = 0


def show_score(choice=1, color=WHITE, font="times new roman", size=20):
    """Display the score on screen"""
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score : " + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (WINDOW_X / 10, 15)
    else:
        score_rect.midtop = (WINDOW_X / 2, WINDOW_Y / 4)
    screen.blit(score_surface, score_rect)


def game_over():
    """End the game and display score"""
    my_font = pygame.font.SysFont("times new roman", 40)
    game_over_surface = my_font.render(
        "Your Score is : " + str(score), True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (WINDOW_X / 2, WINDOW_Y / 4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # Wait for 2 seconds then quit
    pygame.time.sleep(2)
    pygame.quit()
    sys.exit()


# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                change_to = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                change_to = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                change_to = "RIGHT"
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Change direction
    direction = change_to

    # Move snake
    if direction == "UP":
        snake_pos[1] -= 10
    if direction == "DOWN":
        snake_pos[1] += 10
    if direction == "LEFT":
        snake_pos[0] -= 10
    if direction == "RIGHT":
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 10
        speed += 0.5  # Increase speed with score
        food_spawn = False
    else:
        snake_body.pop()

    # Spawn food
    if not food_spawn:
        food_pos = [random.randrange(1, (WINDOW_X//10)) * 10,
                    random.randrange(1, (WINDOW_Y//10)) * 10]
    food_spawn = True

    # Background
    screen.fill(BLACK)

    # Draw snake
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(
            pos[0], pos[1], 10, 10))

    # Draw food
    pygame.draw.rect(screen, RED, pygame.Rect(
        food_pos[0], food_pos[1], 10, 10))

    # Game Over conditions
    if snake_pos[0] < 0 or snake_pos[0] > (WINDOW_X-10):
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > (WINDOW_Y-10):
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    # Show score
    show_score()

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    clock.tick(speed)
