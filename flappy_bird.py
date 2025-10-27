import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()


WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 200, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 50)

def draw_bird(x, y, radius=20):
    pygame.draw.circle(screen, (255, 255, 0), (x, int(y)), radius)

def create_pipe(pipe_width, pipe_gap):
    pipe_height = random.randint(150, 500)
    top_rect = pygame.Rect(WIDTH, 0, pipe_width, pipe_height)
    bottom_rect = pygame.Rect(WIDTH, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap)
    return top_rect, bottom_rect

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def check_collision(bird_rect, pipes, height):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= height:
        return True
    return False

def show_message(text, size=72, y_offset=0, color=WHITE):
    font_temp = pygame.font.Font(None, size)
    surface = font_temp.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH//2, HEIGHT//2 + y_offset))
    screen.blit(surface, rect)

def countdown():
    for num in ["3", "2", "1", "GO!"]:
        screen.fill(BLUE)
        show_message(num, 100)
        pygame.display.update()
        time.sleep(1)

def game_loop():
    bird_x = 100
    bird_y = HEIGHT // 2
    bird_radius = 20
    gravity = 0.5
    bird_movement = 0

    pipe_width = 80
    pipe_gap = 200
    pipes = []
    pipe_frequency = 1500  # ms
    last_pipe = pygame.time.get_ticks()

    score = 0
    passed_pipes = []

    countdown()

    running = True
    while running:
        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_movement = -8  # flap

        bird_movement += gravity
        bird_y += bird_movement  #position updation
        bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius*2, bird_radius*2)

        draw_bird(bird_x, bird_y, bird_radius)

        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > pipe_frequency:
            pipes.extend(create_pipe(pipe_width, pipe_gap))
            last_pipe = current_time

        for pipe in pipes:
            pipe.x -= 4   #for moving the pipes left
        draw_pipes(pipes)

        pipes = [pipe for pipe in pipes if pipe.right > 0]

        for i in range(0, len(pipes), 2):  # pipes are stored in pairs
            pipe = pipes[i]
            if pipe.right < bird_x and pipe not in passed_pipes:
                score += 1
                passed_pipes.append(pipe)

        score_surface = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (10, 10))

        if check_collision(bird_rect, pipes, HEIGHT):
            return score  # end game, return final score

        pygame.display.update()
        clock.tick(FPS)

def game_over_screen(score):
    while True:
        screen.fill(BLUE)
        show_message("GAME OVER", 100, -100, WHITE)
        show_message(f"Score: {score}", 72, 0, WHITE)
        show_message("Press SPACE to Restart", 50, 100, WHITE)
        show_message("Press ESC to Quit", 50, 160, WHITE)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True  # restart
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

while True:
    final_score = game_loop()
    restart = game_over_screen(final_score)
    if not restart:
        break
