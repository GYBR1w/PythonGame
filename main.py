import pygame
import sys
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = SCREEN_HEIGHT // 2

OBSTACLE_GAP = SCREEN_WIDTH // 16

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Гравитационный переключатель")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.vel_y = 0
        self.gravity = 0.5

    def update(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
        elif self.rect.top <= 0:
            self.rect.top = 0
            self.vel_y = 0

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, y, is_top):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        if is_top:
            self.rect.topleft = (SCREEN_WIDTH, 0)
        else:
            self.rect.bottomleft = (SCREEN_WIDTH, SCREEN_HEIGHT)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

obstacles = pygame.sprite.Group()

next_obstacle_is_top = False

score = 0

def create_obstacles():
    global next_obstacle_is_top
    if next_obstacle_is_top:
        obstacle = Obstacle(0, True)
        next_obstacle_is_top = False
    else:
        obstacle = Obstacle(0, False)
        next_obstacle_is_top = True
    obstacles.add(obstacle)
    all_sprites.add(obstacle)

def show_game_over_screen():
    all_sprites.empty()

    game_over_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_over_screen.fill(BLACK)

    font = pygame.font.Font(None, 36)
    score_text = font.render("Счёт: " + str(score), True, WHITE)
    game_over_screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    quit_text = font.render("Выйти", True, BLACK)
    pygame.draw.rect(game_over_screen, WHITE, quit_button)
    game_over_screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

    screen.blit(game_over_screen, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.vel_y = -10
            elif event.key == pygame.K_s:
                player.vel_y = 10

    all_sprites.update()

    if len(obstacles) == 0:
        create_obstacles()

    hits = pygame.sprite.spritecollide(player, obstacles, False)
    if hits:
        show_game_over_screen()

    for obstacle in obstacles:
        if obstacle.rect.right < player.rect.left:
            score += 1

    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
