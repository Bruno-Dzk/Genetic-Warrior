"""A module for testing the in-game collisions.

Contains tests for circle rectangle collision.
"""
import unittest
import pygame

import collision

class MockCircle:
    """A mock circle class, has only radius and position attributes.
    """
    def __init__(self, coordinates, radius):
        self.position = pygame.Vector2(coordinates)
        self.radius = radius

class MockRectangle:
    """A mock rectangle class, has only dimension and position attributes.
    """
    def __init__(self, coordinates, width, height):
        self.position = pygame.Vector2(coordinates)
        self.width = width
        self.height = height

class CollisionTest(unittest.TestCase):
    """A unittest class for collision testing.
    """
    def test_collision_circle_rectangle(self):
        """Function for collision detection between a circle and a rectangle.
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                circle = MockCircle((100 + x * 30, 100 + y * 30), 20)
                rectangle = MockRectangle((100, 100), 40, 40)
                self.assertTrue(collision.collided_circle_rectangle(circle, rectangle))
        circle = MockCircle((100, 100), 10)
        rectangle = MockRectangle((100, 100), 30, 30)
        self.assertTrue(collision.collided_circle_rectangle(circle, rectangle))

    def test_negative_collision_circle_rectangle(self):
        """Function for negative collision detection between a circle and a rectangle.
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x != 0 or y != 0:
                    circle = MockCircle((100 + x * 40, 100 + y * 40), 20)
                    rectangle = MockRectangle((100, 100), 40, 40)
                    self.assertFalse(collision.collided_circle_rectangle(circle, rectangle))

if __name__ == '__main__':
    unittest.main()
    