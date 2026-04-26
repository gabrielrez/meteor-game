import pygame
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
score = 0

in_menu = True
menu_font = pygame.font.Font("PressStart2P-Regular.ttf", 24)
menu_alpha_timer = 0

score_font = pygame.font.Font("PressStart2P-Regular.ttf", 24)
popup_font = pygame.font.Font("PressStart2P-Regular.ttf", 16)

score_popups = []
POPUP_DURATION = 0.8


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


def game_over_effect(final_score):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((255, 0, 0))
    overlay.set_alpha(0)

    font = pygame.font.Font("PressStart2P-Regular.ttf", 56)
    text = font.render("GAME OVER", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))

    score_surf = score_font.render(f"Score: {final_score}", True, WHITE)
    score_rect = score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

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
    screen.blit(score_surf, score_rect)
    pygame.display.flip()

    pygame.time.delay(2000)


player, enemies = reset_game()

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if in_menu:
        if (
            keys[pygame.K_LEFT]
            or keys[pygame.K_RIGHT]
            or keys[pygame.K_UP]
            or keys[pygame.K_DOWN]
            or keys[pygame.K_SPACE]
        ):
            in_menu = False

    offset_x = random.randint(-int(screen_shake), int(screen_shake))
    offset_y = random.randint(-int(screen_shake), int(screen_shake))

    background_move(offset_x, offset_y, dt)

    if not in_menu:
        if keys[pygame.K_SPACE]:
            bullet = player.shoot()
            if bullet:
                bullets.append(bullet)

        player.update(dt, keys)

        spawn_timer += dt
        if spawn_timer >= spawn_delay:
            enemies.append(spawn_enemy())
            spawn_timer = 0

        for bullet in bullets:
            bullet.update(dt)

        bullets = [b for b in bullets if b.y < HEIGHT + 50]

        for enemy in enemies:
            enemy.update(dt)

        for enemy in enemies[:]:
            if player.get_rect().colliderect(enemy.get_rect()):
                game_over_effect(score)
                player, enemies = reset_game()
                bullets.clear()
                score_popups.clear()
                score = 0
                in_menu = True
                spawn_timer = 0
                break

            for bullet in bullets[:]:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    bullets.remove(bullet)
                    screen_shake = 10

                    if enemy.level > 1:
                        points = 10
                        score += points
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
                    else:
                        points = 5
                        score += points

                    score_popups.append(
                        [enemy.x, enemy.y, f"+{points}", POPUP_DURATION]
                    )

                    enemies.remove(enemy)
                    break

    for popup in score_popups:
        popup[3] -= dt
        popup[1] -= 100 * dt

    score_popups[:] = [p for p in score_popups if p[3] > 0]

    for bullet in bullets:
        screen.blit(bullet_img, (bullet.x + offset_x, bullet.y + offset_y))

    screen.blit(spaceship_img, (player.x + offset_x, player.y + offset_y))

    for enemy in enemies:
        scaled = pygame.transform.scale(meteor_img, (int(enemy.size), int(enemy.size)))
        rotated = pygame.transform.rotate(scaled, enemy.angle)
        rect = rotated.get_rect(center=(enemy.x + offset_x, enemy.y + offset_y))
        screen.blit(rotated, rect.topleft)

    for popup in score_popups:
        x, y, text, lifetime = popup
        alpha = int(255 * (lifetime / POPUP_DURATION))
        surf = popup_font.render(text, True, WHITE)
        surf.set_alpha(alpha)
        screen.blit(surf, (x, y))

    screen_shake *= 0.9
    if screen_shake < 0.1:
        screen_shake = 0

    if in_menu:
        menu_alpha_timer += dt
        alpha = int(
            180 + 75 * abs(pygame.math.Vector2(1, 0).rotate(menu_alpha_timer * 120).x)
        )
        surf = menu_font.render("Use as setas do teclado para se mover", True, WHITE)
        surf.set_alpha(alpha)
        rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(surf, rect)
    else:
        score_surf = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (20, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
