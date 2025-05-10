import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images (replace with your asset paths)
try:
    player_img = pygame.image.load("player.png")
    enemy_img = pygame.image.load("enemy.png")
    bullet_img = pygame.image.load("bullet.png")
    background_img = pygame.image.load("background.png")
except pygame.error as e:
    print(f"Error loading images: {e}")
    print("Please ensure 'player.png', 'enemy.png', 'bullet.png', and 'background.png' are in the project folder.")
    pygame.quit()
    exit()

# Player settings
player_width = 64
player_height = 64
player_img = pygame.transform.scale(player_img, (player_width, player_height))
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5
player_rect = player_img.get_rect(topleft=(player_x, player_y))

# Enemy settings
enemy_width = 64
enemy_height = 64
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))
num_enemies = 6
enemy_speed = 2
enemy_drop = 40
enemies = []
for i in range(num_enemies):
    enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
    enemy_y = random.randint(50, 150)
    enemies.append({
        "rect": enemy_img.get_rect(topleft=(enemy_x, enemy_y)),
        "x_change": enemy_speed
    })

# Bullet settings
bullet_width = 32
bullet_height = 32
bullet_img = pygame.transform.scale(bullet_img, (bullet_width, bullet_height))
bullet_speed = 20
bullet_state = "ready"  # "ready" or "fire"
bullet_x = 0
bullet_y = 0
bullet_rect = bullet_img.get_rect()

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game over
game_over = False
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, WHITE)
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, WHITE)
    screen.blit(over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    return distance < 27  # Adjust based on image sizes

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y
                bullet_rect.topleft = (bullet_x, bullet_y)
                bullet_state = "fire"

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed
        player_rect.topleft = (player_x, player_y)

        # Enemy movement
        for enemy in enemies:
            enemy["rect"].x += enemy["x_change"]
            if enemy["rect"].x <= 0 or enemy["rect"].x >= SCREEN_WIDTH - enemy_width:
                enemy["x_change"] *= -1
                enemy["rect"].y += enemy_drop
            # Check for game over
            if enemy["rect"].y > SCREEN_HEIGHT - player_height - 10:
                game_over = True

        # Bullet movement
        if bullet_state == "fire":
            bullet_y -= bullet_speed
            bullet_rect.topleft = (bullet_x, bullet_y)
            if bullet_y < 0:
                bullet_state = "ready"

        # Collision detection
        for enemy in enemies[:]:
            if bullet_state == "fire" and is_collision(
                enemy["rect"].x + enemy_width // 2,
                enemy["rect"].y + enemy_height // 2,
                bullet_x + bullet_width // 2,
                bullet_y + bullet_height // 2
            ):
                bullet_state = "ready"
                enemies.remove(enemy)
                score_value += 10
                # Respawn enemy
                enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
                enemy_y = random.randint(50, 150)
                enemies.append({
                    "rect": enemy_img.get_rect(topleft=(enemy_x, enemy_y)),
                    "x_change": enemy_speed
                })

    # Render
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    screen.blit(player_img, player_rect)
    for enemy in enemies:
        screen.blit(enemy_img, enemy["rect"])
    if bullet_state == "fire":
        screen.blit(bullet_img, bullet_rect)
    show_score(text_x, text_y)
    if game_over:
        game_over_text()

    pygame.display.update()
    clock.tick(60)

pygame.quit()