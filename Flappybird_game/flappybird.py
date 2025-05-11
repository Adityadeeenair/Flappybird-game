# Flappy Bird clone: To some extent at least...
import pygame
import random
import sys

pygame.init()

# Screen settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 32)

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)

# Game constants
bird_radius = 20
gravity = 0.5
jump_strength = -8
pipe_width = 80
pipe_gap = 180
pipe_velocity = 4

# Cloud data
clouds = [{'x': x, 'y': y} for x, y in [(50, 100), (200, 150), (400, 90), (300, 200), (600, 160)]]

def create_pipe():
    height = random.randint(100, 400)
    top = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, height)
    bottom = pygame.Rect(SCREEN_WIDTH, height + pipe_gap, pipe_width, SCREEN_HEIGHT - height - pipe_gap)
    return top, bottom

def draw_bird(x, y):
    # Body with outline
    pygame.draw.circle(screen, BLACK, (int(x), int(y)), bird_radius + 2)  # outline
    pygame.draw.circle(screen, YELLOW, (int(x), int(y)), bird_radius)

    # Eye
    pygame.draw.circle(screen, WHITE, (int(x + 6), int(y - 6)), 6)
    pygame.draw.circle(screen, BLACK, (int(x + 6), int(y - 6)), 2)

    # Beak (triangle)
    pygame.draw.polygon(screen, ORANGE, [(x + 10, y), (x + 22, y - 5), (x + 22, y + 5)])

    # Wings
    pygame.draw.polygon(screen, BROWN, [(x - 10, y), (x - 30, y - 10), (x - 30, y + 10)])  #The most realisitic bird ever made :))

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def draw_cloud(cloud):
    x, y = cloud['x'], cloud['y']
    pygame.draw.circle(screen, WHITE, (x, y), 25)
    pygame.draw.circle(screen, WHITE, (x + 25, y), 20)
    pygame.draw.circle(screen, WHITE, (x - 25, y), 20)
    pygame.draw.circle(screen, WHITE, (x, y - 15), 15)

def draw_background():
    screen.fill(BLUE)
    for cloud in clouds:
        draw_cloud(cloud)

def move_clouds():
    for cloud in clouds:
        cloud['x'] -= 1  # Slow movement
        if cloud['x'] < -50:
            cloud['x'] = SCREEN_WIDTH + 50
            cloud['y'] = random.randint(50, 200)

def check_collision(bird_rect, pipes):
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return False

def display_score(score):
    text = FONT.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

def show_start_message():
    text = FONT.render("Press SPACE to Start", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 20))

def show_game_over(score):
    screen.blit(FONT.render("Game Over!", True, (200, 0, 0)), (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 60))
    screen.blit(FONT.render(f"Final Score: {score}", True, BLACK), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
    screen.blit(FONT.render("Press R to Restart", True, BLACK), (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 20))

def reset_game():
    return {
        'bird_x': 80,
        'bird_y': 300,
        'bird_velocity': 0,
        'pipes': list(create_pipe()),
        'score': 0,
        'game_started': False,
        'game_over': False
    }      #Allows the user to restart the game and try again..

# Initial game state
state = reset_game()

# Game loop
while True:
    draw_background()
    move_clouds()

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
            if keys[pygame.K_SPACE]:
                state['bird_velocity'] = jump_strength

            state['bird_velocity'] += gravity
            state['bird_y'] += state['bird_velocity']
            bird_rect = pygame.Rect(state['bird_x'] - bird_radius, state['bird_y'] - bird_radius, bird_radius * 2, bird_radius * 2)

            for pipe in state['pipes']:
                pipe.x -= pipe_velocity

            if state['pipes'][0].x + pipe_width < 0:
                state['pipes'].pop(0)
                state['pipes'].pop(0)
                state['pipes'].extend(create_pipe())
                state['score'] += 1

            if check_collision(bird_rect, state['pipes']):
                state['game_over'] = True

            draw_pipes(state['pipes'])
            display_score(state['score'])

        draw_bird(state['bird_x'], state['bird_y'])

    pygame.display.update()
    clock.tick(60)
#Feel free to edit and improve the code ;)
