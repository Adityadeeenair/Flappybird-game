import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings for the user...
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Game constants
bird_radius = 20
gravity = 0.5
jump_strength = -8
pipe_width = 80
pipe_gap = 180
pipe_velocity = 4

# Loads the flappy bird sprite
bird_img = pygame.image.load('flappybird.png').convert_alpha()
bird_img = pygame.transform.smoothscale(bird_img, (bird_radius * 2, bird_radius * 2))

# Clock & font
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 32)

# Colors
WHITE  = (255, 255, 255)
BLUE   = (135, 206, 250)
GREEN  = (0, 200, 0)
DARK_GREEN = (0, 150, 0)  
BLACK  = (0, 0, 0)

# Cloud data
clouds = [{'x': x, 'y': y} for x, y in [(50, 100), (200, 150), (400, 90), (300, 200), (600, 160)]]

def create_pipe():
    height = random.randint(100, 400)
    top = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, height)
    bottom = pygame.Rect(SCREEN_WIDTH, height + pipe_gap, pipe_width, SCREEN_HEIGHT - height - pipe_gap)
    return top, bottom

def draw_bird(x, y):
    """Blit the bird sprite centered on (x, y)."""
    rect = bird_img.get_rect(center=(int(x), int(y)))
    screen.blit(bird_img, rect)

def draw_pipes(pipes):
    """Draw layered pipes with shading and caps."""
    cap_height = 20
    for pipe in pipes:
        # Draws a dark green border (pipe outline)
        pygame.draw.rect(screen, DARK_GREEN, pipe.inflate(6, 6))

        # Draws a vertical gradient type shade inside pipe body
        for i in range(pipe.height):
            color_ratio = i / pipe.height
            r = int(GREEN[0] * (1 - color_ratio) + DARK_GREEN[0] * color_ratio)
            g = int(GREEN[1] * (1 - color_ratio) + DARK_GREEN[1] * color_ratio)
            b = int(GREEN[2] * (1 - color_ratio) + DARK_GREEN[2] * color_ratio)
            pygame.draw.line(screen, (r, g, b), (pipe.left + 2, pipe.top + i), (pipe.right - 2, pipe.top + i))

        # Draws a pipe cap
        if pipe.top == 0:  # Top pipe
            cap = pygame.Rect(pipe.left - 5, pipe.bottom - cap_height, pipe.width + 10, cap_height)
        else:  # Bottom pipe
            cap = pygame.Rect(pipe.left - 5, pipe.top, pipe.width + 10, cap_height)
        pygame.draw.rect(screen, DARK_GREEN, cap)
        pygame.draw.rect(screen, GREEN, cap.inflate(-4, -4))

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
        cloud['x'] -= 1
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
    screen.blit(FONT.render("Game Over!", True, (200, 0, 0)),
                (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 60))
    screen.blit(FONT.render(f"Final Score: {score}", True, BLACK),
                (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
    screen.blit(FONT.render("Press R to Restart", True, BLACK),
                (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 20))

def reset_game():
    return {
        'bird_x': 80,
        'bird_y': 300,
        'bird_velocity': 0,
        'pipes': list(create_pipe()),
        'score': 0,
        'game_started': False,
        'game_over': False
    }

# Initialize game state
state = reset_game()   #restarts the game so that the users can play the game again :)

# Main game loop
while True:
    # Background & clouds
    draw_background()
    move_clouds()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Game over screen
    if state['game_over']:
        show_game_over(state['score'])
        if keys[pygame.K_r]:
            state = reset_game()

    else:
        # Start screen
        if not state['game_started']:
            show_start_message()
            if keys[pygame.K_SPACE]:
                state['game_started'] = True
                state['bird_velocity'] = jump_strength

        # Active gameplay
        else:
            if keys[pygame.K_SPACE]:
                state['bird_velocity'] = jump_strength

            # Apply physics
            state['bird_velocity'] += gravity
            state['bird_y'] += state['bird_velocity']

            # Bird collision box
            bird_rect = pygame.Rect(
                state['bird_x'] - bird_radius,
                state['bird_y'] - bird_radius,
                bird_radius * 2,
                bird_radius * 2
            )

            # Move pipes
            for pipe in state['pipes']:
                pipe.x -= pipe_velocity

            # Recycle pipes & increment score
            if state['pipes'][0].x + pipe_width < 0:
                state['pipes'].pop(0)
                state['pipes'].pop(0)
                state['pipes'].extend(create_pipe())
                state['score'] += 1

            # Check for collisions
            if check_collision(bird_rect, state['pipes']):
                state['game_over'] = True

            # Draw pipes & score
            draw_pipes(state['pipes'])
            display_score(state['score'])

        # Draws the bird sprite
        draw_bird(state['bird_x'], state['bird_y'])

    # Refresh display & tick
    pygame.display.update()
    clock.tick(60)
#Feel free to edit and improvise the code ;)
