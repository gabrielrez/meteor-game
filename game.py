import pygame
from time import sleep
import sys
import random
from player import Player
from enemy import Enemy

pygame.init()

pygame.display.set_caption("Game")

WIDTH, HEIGHT = 1280, 720

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load("bg.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_y = 0

meteor_img = pygame.image.load("meteor.png").convert_alpha()
spaceship_img = pygame.image.load("spaceship.png").convert_alpha()
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))

bullet_img = pygame.image.load("bullet.png").convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (15, 45))

clock = pygame.time.Clock()

bullets = []

screen_shake = 0

spawn_timer = 0
spawn_delay = 1


def spawn_enemy():
    return Enemy(
        x=random.randint(0, WIDTH),
        y=HEIGHT + 100,
        size=100,
        speed=random.randint(100, 600),
        color=RED,
        screen_width=WIDTH,
        screen_height=HEIGHT,
        level=2,
    )


def background_move(offset_x, offset_y, dt):
    global background_y
    background_y -= 300 * dt
    if background_y <= -HEIGHT:
        background_y = 0
    screen.blit(background, (offset_x, background_y + offset_y))
    screen.blit(background, (offset_x, background_y + HEIGHT + offset_y))


def reset_game():
    player = Player((WIDTH / 2 - 50), 100, 50, 800, BLUE, WIDTH, HEIGHT)
    enemies = []
    return player, enemies


def game_over_effect():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((255, 0, 0))
    overlay.set_alpha(0)

    font = pygame.font.SysFont(None, 100)
    text = font.render("GAME OVER", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    for i in range(10):
        overlay.set_alpha(i * 25)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))

    for alpha in range(0, 255, 5):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)

    screen.blit(fade, (0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()

    pygame.time.delay(1500)


player, enemies = reset_game()

running = True
while running:
    dt = clock.tick(60) / 1000

    spawn_timer += dt

    if spawn_timer >= spawn_delay:
        enemies.append(spawn_enemy())
        spawn_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    offset_x = random.randint(-int(screen_shake), int(screen_shake))
    offset_y = random.randint(-int(screen_shake), int(screen_shake))

    background_move(offset_x, offset_y, dt)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        bullet = player.shoot()
        if bullet:
            bullets.append(bullet)

    for bullet in bullets:
        bullet.update(dt)

    bullets = [b for b in bullets if b.y < HEIGHT + 50]

    player.update(dt, keys)

    for enemy in enemies:
        enemy.update(dt)

    for enemy in enemies[:]:
        if player.get_rect().colliderect(enemy.get_rect()):
            game_over_effect()
            player, enemies = reset_game()
            bullets.clear()
            break

        for bullet in bullets[:]:
            if bullet.get_rect().colliderect(enemy.get_rect()):
                bullets.remove(bullet)
                screen_shake = 10

                if enemy.level > 1:
                    new_level = enemy.level - 1
                    new_size = enemy.size * 0.6

                    for _ in range(2):
                        enemies.append(
                            Enemy(
                                enemy.x,
                                enemy.y,
                                new_size,
                                random.randint(100, 600),
                                RED,
                                WIDTH,
                                HEIGHT,
                                level=new_level,
                            )
                        )

                enemies.remove(enemy)
                break

    for bullet in bullets:
        screen.blit(bullet_img, (bullet.x + offset_x, bullet.y + offset_y))

    screen.blit(spaceship_img, (player.x + offset_x, player.y + offset_y))

    for enemy in enemies:
        scaled = pygame.transform.scale(meteor_img, (int(enemy.size), int(enemy.size)))
        rotated = pygame.transform.rotate(scaled, enemy.angle)
        rect = rotated.get_rect(center=(enemy.x + offset_x, enemy.y + offset_y))
        screen.blit(rotated, rect.topleft)

    screen_shake *= 0.9
    if screen_shake < 0.1:
        screen_shake = 0

    pygame.display.flip()

pygame.quit()
sys.exit()
