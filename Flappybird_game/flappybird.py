import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock and font
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 32)

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)

# Constants
bird_radius = 20
gravity = 0.5
jump_strength = -8
pipe_width = 60
pipe_gap = 150
pipe_velocity = 4

def create_pipe():
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, height + pipe_gap, pipe_width, SCREEN_HEIGHT - height - pipe_gap)
    return top_pipe, bottom_pipe

def draw_bird(x, y):
    pygame.draw.circle(screen, (255, 200, 0), (int(x), int(y)), bird_radius)
    pygame.draw.circle(screen, (0, 0, 0), (int(x + 6), int(y - 6)), 3)

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def check_collision(bird_rect, pipes):
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return False

def display_score(score):
    text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

def show_start_message():
    text = FONT.render("Press SPACE to Start", True, (0, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 20))

def show_game_over(score):
    text1 = FONT.render("Game Over!", True, (200, 0, 0))
    text2 = FONT.render(f"Final Score: {score}", True, (0, 0, 0))
    text3 = FONT.render("Press R to Restart", True, (0, 0, 0))
    screen.blit(text1, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 60))
    screen.blit(text2, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
    screen.blit(text3, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 20))

def reset_game():
    return {
        'bird_x': 50,
        'bird_y': 300,
        'bird_velocity': 0,
        'pipes': list(create_pipe()),
        'score': 0,
        'game_started': False,
        'game_over': False
    }

# Initialize game state
state = reset_game()

# Game loop
while True:
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if state['game_over']:
        show_game_over(state['score'])
        if keys[pygame.K_r]:
            state = reset_game()
    else:
        if not state['game_started']:
            show_start_message()
            if keys[pygame.K_SPACE]:
                state['game_started'] = True
                state['bird_velocity'] = jump_strength
        else:
            # Jumping
            if keys[pygame.K_SPACE]:
                state['bird_velocity'] = jump_strength

            # Update bird
            state['bird_velocity'] += gravity
            state['bird_y'] += state['bird_velocity']
            bird_rect = pygame.Rect(state['bird_x'] - bird_radius, state['bird_y'] - bird_radius, bird_radius * 2, bird_radius * 2)

            # Move pipes
            for pipe in state['pipes']:
                pipe.x -= pipe_velocity

            # Recycle pipes
            if state['pipes'][0].x + pipe_width < 0:
                state['pipes'].pop(0)
                state['pipes'].pop(0)
                state['pipes'].extend(create_pipe())
                state['score'] += 1

            # Check collision
            if check_collision(bird_rect, state['pipes']):
                state['game_over'] = True

            draw_pipes(state['pipes'])
            display_score(state['score'])

        # Draw bird
        draw_bird(state['bird_x'], state['bird_y'])

    pygame.display.update()
    clock.tick(60)
