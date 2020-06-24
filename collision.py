"""A module for collision detecting in a pong-type game

Contains functions for detecting collisions between two rectangles
and between a circle and a rectangle.
Also contains a CollisionSystem class that stores lists of game objects
and checks the collision between them.
"""
def collided_circle_rectangle(circle, rectangle):
    """Returns true if the passed circle is intersecting with the passed tectangle.
    """
    distance_vector = circle.position - rectangle.position
    if (abs(distance_vector.x) < rectangle.width / 2 + circle.radius
            and abs(distance_vector.y) < rectangle.height / 2 + circle.radius):
        return True
    return False

def collided_2_rectangle(rectangle_a, rectangle_b):
    """Returns true if the two passed rectangles are intersecting.
    """
    distance_x = abs(rectangle_a.position.x - rectangle_b.position.x)
    distance_y = abs(rectangle_a.position.y - rectangle_b.position.y)
    if (distance_x < rectangle_a.width / 2  + rectangle_b.width / 2
            and distance_y < rectangle_a.height / 2 + rectangle_b.height /2):
        return True
    return False

class CollisionSystem:
    """Checks if there is a collision between objects from the lists on the update function.

    Takes a game object as a constructor argument.
    """
    def __init__(self, game):
        self.paddle_list = game.paddle_list
        self.wall_list = game.wall_list
        self.ball_list = game.ball_list

    def update(self):
        """Checks collision between all game objects that can collide with each other.

        If collision occured it calls appropriate response function.
        """
        for wall in self.wall_list:
            for paddle in self.paddle_list:
                if collided_2_rectangle(paddle, wall):
                    paddle.wall_collision_response(wall)
            for ball in self.ball_list:
                if collided_circle_rectangle(ball, wall):
                    ball.wall_collision_response()
        for paddle in self.paddle_list:
            for ball in self.ball_list:
                if collided_circle_rectangle(ball, paddle):
                    ball.paddle_collision_response(paddle)
