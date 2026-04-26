import pygame
from bullet import Bullet


class Player:
    def __init__(self, x, y, size, speed, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.shoot_cooldown = 0.08
        self.time_since_last_shoot = 0

    def update(self, dt, keys):
        self.move(dt, keys)
        self.time_since_last_shoot += dt

    def get_rect(self):
        hitbox_size = self.size * 0.6
        offset = (self.size - hitbox_size) / 2
        return pygame.Rect(self.x + offset, self.y + offset, hitbox_size, hitbox_size)

    def move(self, dt, keys):
        vector_x = 0
        vector_y = 0

        if keys[pygame.K_RIGHT]:
            if not self.x > self.screen_width - self.size:
                vector_x += 1
        if keys[pygame.K_LEFT]:
            if not self.x < 0:
                vector_x -= 1
        if keys[pygame.K_DOWN]:
            if not self.y > self.screen_height - self.size:
                vector_y += 1
        if keys[pygame.K_UP]:
            if not self.y < 0:
                vector_y -= 1

        vector_length = (vector_x**2 + vector_y**2) ** 0.5

        if vector_length > 0:
            vector_x /= vector_length
            vector_y /= vector_length

        self.x += vector_x * self.speed * dt
        self.y += vector_y * self.speed * dt

    def shoot(self):
        if self.time_since_last_shoot >= self.shoot_cooldown:
            self.time_since_last_shoot = 0
            return Bullet(
                self.x + self.size / 2 - 5,
                self.y,
                20,
                45,
                1500,
                (255, 255, 0),
            )
        return None
