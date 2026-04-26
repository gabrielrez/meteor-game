import pygame
import random


class Bullet:
    def __init__(self, x, y, width, height, speed, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.direction = random.choice([True, False])

    def update(self, dt):
        self.move(dt)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dt):
        self.speed += 2000 * dt
        self.y += self.speed * dt

        if self.direction:
            self.x += 80 * dt
        else:
            self.x -= 80 * dt
