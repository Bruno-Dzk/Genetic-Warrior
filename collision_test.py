from collision import CollisionSystem
import unittest
import pygame

class TestCircle():
    def __init__(self, coords, radius):
        self.pos = pygame.Vector2(coords)
        self.radius = radius

class TestRect():
    def __init__(self, coords, width, height):
        self.pos = pygame.Vector2(coords)
        self.width = width
        self.height = height

class CollisionTest(unittest.TestCase):
    def setUp(self):
        self.collision_system = CollisionSystem([],[])

    def test_collided_circle_rect(self):
        for x in range(-1,1):
            for y in range(-1,1):
                circle = TestCircle((100+x*30,100+y*30),20)
                rect = TestRect((100,100),40,40)
                self.assertTrue(self.collision_system.collided_circle_rect(circle, rect))

if __name__ == '__main__':
    unittest.main()