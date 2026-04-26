import pygame
import random


class Enemy:
    def __init__(self, x, y, size, speed, color, screen_width, screen_height, level=2):
        self.x = x
        self.y = y
        self.size = size
        self.angle = 0
        self.rotation_speed = random.randint(-180, 180)
        self.speed = speed
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.direction = random.choice([True, False])
        self.offset_x = random.randrange(150, 350)
        self.level = level

    def update(self, dt):
        self.angle += self.rotation_speed * dt
        self.move(dt)
        self.screen_wrap()

    def get_rect(self):
        hitbox_size = self.size * 0.6
        return pygame.Rect(
            self.x - hitbox_size / 2,
            self.y - hitbox_size / 2,
            hitbox_size,
            hitbox_size,
        )

    def move(self, dt):
        self.y -= self.speed * dt

        if self.direction:
            self.x += self.offset_x * dt
        else:
            self.x -= self.offset_x * dt

    def screen_wrap(self):
        if self.y < -self.size:
            self.y = self.screen_height + self.size
            self.x = random.randint(0, int(self.screen_width - self.size))
