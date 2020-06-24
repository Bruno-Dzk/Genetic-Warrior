"""A module storing various types of game enitites for a pong-type game.

The types of the entities are: ball, paddle, rectangle, scoreboard.
"""
import math

import pygame
import pygame.gfxdraw
# pylint: disable=maybe-no-member

MAX_BOUNCE_ANGLE = math.radians(60)
DIAGONAL_CORRECTION = 0.7
UP, DOWN = range(2)
BALL_SPEED = 3.0
BALL_RADIUS = 8
BALL_FREEZE_DEFAULT = True
PADDLE_SPEED = 3.0

class Ball:
    """The ball that players play pong with.
    """
    def __init__(self, coordinates, target_coordinates, color):
        self.position = pygame.Vector2(coordinates)
        self.__backup_position = self.position
        self.color = color
        self.radius = BALL_RADIUS
        self.speed = BALL_SPEED
        self.direction_vector = (pygame.Vector2(target_coordinates) - self.position).normalize()
        self.cleanup_needed = False
        self.frozen = True

    def draw(self, screen):
        """Draws the ball on screen.

        Floors the coordinates because they are floats and integer values are needed.
        """
        screen_x = math.floor(self.position.x)
        screen_y = math.floor(self.position.y)
        pygame.gfxdraw.aacircle(screen, screen_x, screen_y, self.radius, self.color)
        pygame.gfxdraw.filled_circle(screen, screen_x, screen_y, self.radius, self.color)

    def move(self, delta_milliseconds):
        """Saves the backup position and moves the ball if not frozen.
        """
        if not self.frozen:
            self.__backup_position = self.position
            self.position.x += self.direction_vector.x * (self.speed / delta_milliseconds)
            self.position.y += self.direction_vector.y * (self.speed / delta_milliseconds)

    def wall_collision_response(self):
        """Handles wall collision reversing y coordinate od the direction_vector.
        """
        self.position = self.__backup_position
        self.direction_vector.y *= -1.0

    def paddle_collision_response(self, paddle):
        """Handles collision with the paddle.

        Changes direction and angle of the direction_vector according to how far from the center
        the ball hit the paddle.
        """
        signed_distance_to_center = self.position.y - paddle.position.y
        normalized_distance_to_center = (signed_distance_to_center /
                                         (paddle.height / 2 + self.radius / 2))
        bounce_angle = MAX_BOUNCE_ANGLE * normalized_distance_to_center
        self.direction_vector.x = (math.cos(bounce_angle) *
                                   (-self.direction_vector.x / abs(self.direction_vector.x)))
        self.direction_vector.y = math.sin(bounce_angle)
        self.position = self.__backup_position

class Rectangle:
    """Represents a rectangular game object.

    Can be used to represent wall, paddles or the dividing line.
    """
    def __init__(self, coordinates, color, width, height):
        self.position = pygame.Vector2(coordinates)
        self.color = color
        self.width = width
        self.height = height

    def draw(self, screen):
        """Draws the rectangle on screen.

        Floors the coordinates because they are floats and integer values are needed.
        """
        screen_x = math.floor(self.position.x) - self.width / 2
        screen_y = math.floor(self.position.y) - self.height / 2
        pygame.draw.rect(screen,
                         self.color,
                         pygame.Rect(screen_x, screen_y, self.width, self.height))

class Paddle(Rectangle):
    """Represents the paddle that the player uses to hit the ball.
    """
    def __init__(self, coordinates, color, width, height, key_up, key_down):
        super().__init__(coordinates, color, width, height)
        self.__backup_position = self.position
        self.speed = PADDLE_SPEED
        self.input_map = [False, False]
        self.key_up = key_up
        self.key_down = key_down

    def wall_collision_response(self, wall):
        """Handles collision with the wall.

        On collision moves the paddle back so it no longer intersects with the wall.
        """
        closest_point = abs(abs(wall.position.y - self.position.y) - wall.height / 2)
        penetration_vector = abs(closest_point - self.height / 2)
        if self.position.y > wall.position.y:
            self.position.y += penetration_vector
        else:
            self.position.y -= penetration_vector

    def move(self, delta_milliseconds):
        """Moves the paddle.
        """
        velocity = pygame.Vector2(0.0, 0.0)
        if self.input_map[UP]:
            velocity.y -= self.speed / delta_milliseconds
        if self.input_map[DOWN]:
            velocity.y += self.speed / delta_milliseconds
        self.__backup_position = self.position
        self.position = self.position + velocity

    def update_input(self, event):
        """Updates the input list of the paddle according to event.
        """
        key = event.key
        if event.type == pygame.KEYDOWN:
            if key == self.key_up:
                self.input_map[UP] = True
            if key == self.key_down:
                self.input_map[DOWN] = True
        if event.type == pygame.KEYUP:
            if key == self.key_up:
                self.input_map[UP] = False
            if key == self.key_down:
                self.input_map[DOWN] = False

class Scoreboard:
    """Displays the font surface with the current score.
    """
    def __init__(self, coordinates, color, font, score):
        self.position = pygame.Vector2(coordinates)
        self.color = color
        self.__score = score
        self.font = font

    def update_score(self, score):
        """Updates the score to be displayed on the board.
        """
        self.__score = score

    def draw(self, screen):
        """Draws the scoreboard on the screen.
        """
        font_surface = self.font.render(str(self.__score), True, self.color)
        width, height = font_surface.get_size()
        screen.blit(font_surface, (self.position.x - width / 2, self.position.y - height / 2))
