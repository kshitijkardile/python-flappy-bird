import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 150
GRAVITY = 0.25
FLAP_STRENGTH = -6.5
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (135, 206, 235)
GREEN = (0, 200, 0)
BROWN = (222, 184, 135)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Bird class
def load_bird():
    bird_surface = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT), pygame.SRCALPHA)
    pygame.draw.ellipse(bird_surface, (255, 255, 0), [0, 0, BIRD_WIDTH, BIRD_HEIGHT])
    pygame.draw.circle(bird_surface, (0, 0, 0), (int(BIRD_WIDTH*0.8), int(BIRD_HEIGHT*0.3)), 3)  # Eye
    return bird_surface

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.vel = 0
        self.surface = load_bird()
        self.rect = self.surface.get_rect(center=(self.x, self.y))

    def flap(self):
        self.vel = FLAP_STRENGTH

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.centery = int(self.y)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - GROUND_HEIGHT - PIPE_GAP - 50)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT - (self.height + PIPE_GAP))

    def update(self):
        self.x -= 3
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.top_rect)
        pygame.draw.rect(surface, GREEN, self.bottom_rect)
        pygame.draw.rect(surface, BROWN, (self.top_rect.x, self.top_rect.bottom-10, PIPE_WIDTH, 10))
        pygame.draw.rect(surface, BROWN, (self.bottom_rect.x, self.bottom_rect.y, PIPE_WIDTH, 10))

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def collide(self, bird_rect):
        return self.top_rect.colliderect(bird_rect) or self.bottom_rect.colliderect(bird_rect)

# Game functions
def draw_ground(surface):
    pygame.draw.rect(surface, BROWN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

def show_text(surface, text, size, color, center):
    font = pygame.font.SysFont(None, size)
    label = font.render(text, True, color)
    rect = label.get_rect(center=center)
    surface.blit(label, rect)

def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 100)]
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                if event.key == pygame.K_SPACE and game_over:
                    main()  # Restart
                    return

        if not game_over:
            bird.update()
            # Pipes
            for pipe in pipes:
                pipe.update()
                if pipe.collide(bird.rect):
                    game_over = True
            # Remove off-screen pipes
            if pipes and pipes[0].off_screen():
                pipes.pop(0)
            # Add new pipes
            if pipes and pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe(SCREEN_WIDTH))
            # Score
            for pipe in pipes:
                if not hasattr(pipe, 'scored') and pipe.x + PIPE_WIDTH < bird.x:
                    score += 1
                    pipe.scored = True
            # Ground collision
            if bird.y + BIRD_HEIGHT//2 > SCREEN_HEIGHT - GROUND_HEIGHT or bird.y - BIRD_HEIGHT//2 < 0:
                game_over = True

        # Draw everything
        screen.fill(SKY)
        for pipe in pipes:
            pipe.draw(screen)
        bird.draw(screen)
        draw_ground(screen)
        show_text(screen, str(score), 48, WHITE, (SCREEN_WIDTH//2, 50))
        if game_over:
            show_text(screen, 'Game Over', 64, BLACK, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50))
            show_text(screen, 'Press SPACE to restart', 32, BLACK, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2+10))
        pygame.display.flip()

if __name__ == '__main__':
    main() 