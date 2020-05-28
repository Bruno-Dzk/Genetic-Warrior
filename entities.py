import pygame
from pygame import Vector2
import math
from pygame import gfxdraw

DIAGONAL_CORRECTION = 0.7
LEFT = pygame.K_a
UP = pygame.K_w
RIGHT = pygame.K_d
DOWN = pygame.K_s

class Bullet():
    def __init__(self, pos, color, target):
        self.pos = pos
        self.color = color
        self.radius = 10
        self.speed = 5.0
    def update(self, screen):
        screen_x = math.floor(self.pos.x)
        screen_y = math.floor(self.pos.y)
        gfxdraw.aacircle(screen, screen_x, screen_y, self.radius, self.color)
        pygame.gfxdraw.filled_circle(screen, screen_x, screen_y, self.radius, self.color)
    def move(self, x, y):
        pass

class Character():
    def __init__(self, coords, color):
        self.pos = Vector2(coords)
        self.__backup_pos = self.pos
        self.color = color
        self.radius = 20
        self.speed = 2.0
        self.input_map = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False
        }
    def update(self, screen):
        screen_x = math.floor(self.pos.x)
        screen_y = math.floor(self.pos.y)
        gfxdraw.aacircle(screen, screen_x, screen_y, self.radius, self.color)
        pygame.gfxdraw.filled_circle(screen, screen_x, screen_y, self.radius, self.color)

    def wall_collision_response(self):
        self.pos = self.__backup_pos

    def move(self, dt):
        v = Vector2(0.0,0.0)
        if self.input_map["up"]:
            v.y -= self.speed / dt
        if self.input_map["down"]:
            v.y += self.speed / dt
        if self.input_map["left"]:
            v.x -= self.speed / dt
        if self.input_map["right"]:
            v.x += self.speed / dt
        if abs(v.x) == abs(v.y):
            v *= DIAGONAL_CORRECTION
        self.__backup_pos = self.pos
        self.pos = self.pos + v

class Player(Character):
    def __init__(self, coords, color):
        super().__init__(coords, color)
    def update_input(self, event):
        key = event.key
        if event.type == pygame.KEYDOWN:
            if key == LEFT:
                self.input_map["left"] = True
            if key == UP:
                self.input_map["up"] = True
            if key == RIGHT:
                self.input_map["right"] = True
            if key == DOWN:
                self.input_map["down"] = True
        if event.type == pygame.KEYUP:
            if key == LEFT:
                self.input_map["left"] = False
            if key == UP:
                self.input_map["up"] = False
            if key == RIGHT:
                self.input_map["right"] = False
            if key == DOWN:
                self.input_map["down"] = False

class Wall():
    def __init__(self, coords, color):
        self.pos = Vector2(coords)
        self.color = color
        self.width = 40
        self.height = 40
    def update(self, screen):
        screen_x = math.floor(self.pos.x) - self.width / 2
        screen_y = math.floor(self.pos.y) - self.height / 2
        pygame.draw.rect(screen, self.color, pygame.Rect(screen_x, screen_y, self.width, self.height))
        