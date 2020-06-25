"""A pong game main module

Contains the game class nad the main loop of the game.
Should be executed as a script.
"""
# pylint: disable=maybe-no-member
import random

import pygame

import collision
import entities

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BORDER_HEIGHT = 20
PLAYER_ONE, PLAYER_TWO = range(2)
PLAYER_ONE_SCOREBOARD_POSITION = (SCREEN_WIDTH / 2 - 50, 60)
PLAYER_TWO_SCOREBOARD_POSITION = (SCREEN_WIDTH / 2 + 50, 60)
PLAYER_ONE_STARTING_POSITION = (50, SCREEN_HEIGHT / 2)
PLAYER_TWO_STARTING_POSITION = (SCREEN_WIDTH - 50, SCREEN_HEIGHT / 2)
FONTNAME = "comicsansms"
FONTSIZE = 72
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80
DIVIDER_WIDTH = 2

class Colors:
    """Colors used in game.
    """
    # pylint: disable=too-few-public-methods
    WALL_COLOR = pygame.Color("#00171F")
    BACKGROUND_COLOR = pygame.Color("#F5F5F5")
    PLAYER_ONE_COLOR = pygame.Color("#007EA7")
    PLAYER_TWO_COLOR = pygame.Color("#8E3B46")
    BALL_COLOR = pygame.Color("#F58700")
    DIVIDER_COLOR = pygame.Color("#a3a3a3")

class Controls:
    """Controls for the game.
    """
    # pylint: disable=too-few-public-methods
    PLAYER_ONE_UP = pygame.K_w
    PLAYER_ONE_DOWN = pygame.K_s
    PLAYER_TWO_UP = pygame.K_UP
    PLAYER_TWO_DOWN = pygame.K_DOWN
    BALL_UNFREEZE = pygame.K_SPACE

class Game:
    """Contains the game state.

    Contains the lists of game objects by type (eg. paddle, ball, mobile objects).
    Also contains the current score, method to draw it and the font used to display it.
    Has methods for creating, updating and moving objects.
    """
    def __init__(self, screen):
        """Initiates Game and game object lists with 0-0 score, two scoreboards and a divider.
        """
        self.score = [0, 0]
        self.font = pygame.font.SysFont(FONTNAME, FONTSIZE)
        self.player_one_scoreboard = entities.Scoreboard(PLAYER_ONE_SCOREBOARD_POSITION,
                                                         Colors.PLAYER_ONE_COLOR,
                                                         self.font, 0)
        self.player_two_scoreboard = entities.Scoreboard(PLAYER_TWO_SCOREBOARD_POSITION,
                                                         Colors.PLAYER_TWO_COLOR,
                                                         self.font, 0)
        self.divider = entities.Rectangle((SCREEN_WIDTH/2, SCREEN_HEIGHT/2),
                                          Colors.DIVIDER_COLOR,
                                          DIVIDER_WIDTH,
                                          SCREEN_HEIGHT)
        self.screen = screen
        self.entity_list = [self.player_one_scoreboard, self.player_two_scoreboard, self.divider]
        self.mobile_list = []
        self.paddle_list = []
        self.ball_list = []
        self.wall_list = []

    def create_player(self, coordinates, color, key_up, key_down):
        """Creates a player object and adds it to the appropriate lists.
        """
        player = entities.Paddle(coordinates, color, PADDLE_WIDTH, PADDLE_HEIGHT, key_up, key_down)
        self.entity_list.append(player)
        self.paddle_list.append(player)
        self.mobile_list.append(player)
        return player

    def create_wall(self, coordinates, color, width, height):
        """Creates a wall object and adds it to the appropriate lists.
        """
        wall = entities.Rectangle(coordinates, color, width, height)
        self.entity_list.append(wall)
        self.wall_list.append(wall)
        return wall

    def create_ball(self, coordinates, target_coordinates, color):
        """Creates a ball object and adds it to the appropriate lists.
        """
        ball = entities.Ball(coordinates, target_coordinates, color)
        self.entity_list.append(ball)
        self.ball_list.append(ball)
        self.mobile_list.append(ball)
        return ball

    def draw(self):
        """Draws all game objects on the screen.
        """
        for entity in self.entity_list:
            entity.draw(self.screen)

    def move(self, delta_milliseconds):
        """Moves all game objects.
        """
        for mobile in self.mobile_list:
            mobile.move(delta_milliseconds)

    def check_scores(self):
        """Checks if the ball has left the screen and updates the score.

        If it left on the right screen side player one gets one point.
        If on the left side player two gets one point.
        """
        for ball in self.ball_list:
            if ball.position.x > SCREEN_WIDTH - ball.radius:
                self.score[PLAYER_ONE] += 1
                self.player_one_scoreboard.update_score(self.score[PLAYER_ONE])
                ball.cleanup_needed = True
                self.create_ball((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
                                 (SCREEN_WIDTH, SCREEN_HEIGHT/2),
                                 Colors.BALL_COLOR)
            if ball.position.x < ball.radius:
                self.score[PLAYER_TWO] += 1
                self.player_two_scoreboard.update_score(self.score[PLAYER_TWO])
                ball.cleanup_needed = True
                self.create_ball((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
                                 (0, SCREEN_HEIGHT/2), Colors.BALL_COLOR)

    def unfreeze_balls(self):
        """Unblocks all balls in play if they are blocked.
        """
        for ball in self.ball_list:
            if ball.frozen:
                ball.frozen = False

    def cleanup(self):
        """Check if balls need to be removed and removes them from the appropriate lists if so.
        """
        for ball in self.ball_list:
            if ball.cleanup_needed:
                self.ball_list.pop(self.ball_list.index(ball))
                self.entity_list.pop(self.entity_list.index(ball))

def create_world_borders(game):
    """Creates the walls on the top and bottom of the screen.
    """
    game.create_wall((SCREEN_WIDTH/ 2, BORDER_HEIGHT / 2),
                     Colors.WALL_COLOR, SCREEN_WIDTH, BORDER_HEIGHT)
    game.create_wall((SCREEN_WIDTH/ 2, SCREEN_HEIGHT - BORDER_HEIGHT / 2),
                     Colors.WALL_COLOR, SCREEN_WIDTH, BORDER_HEIGHT)

# define a main function
def main():
    """The main function of the program

    Initializes the pygame package and starts the main game loop.
    """
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    #logo = pygame.image.load("logo32x32.png")
    # pygame.display.set_icon(logo)
    pygame.display.set_caption("Pong")
    #pygame.font.init()
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # define a variable to control the main loop
    running = True

    # create an instance of Game class
    game = Game(screen)

    # crate a collision detection system
    collision_system = collision.CollisionSystem(game)

    create_world_borders(game)

    # defining clock
    clock = pygame.time.Clock()

    # defining player
    player_one = game.create_player(PLAYER_ONE_STARTING_POSITION,
                                    Colors.PLAYER_ONE_COLOR,
                                    Controls.PLAYER_ONE_UP,
                                    Controls.PLAYER_ONE_DOWN)
    player_two = game.create_player(PLAYER_TWO_STARTING_POSITION,
                                    Colors.PLAYER_TWO_COLOR,
                                    Controls.PLAYER_TWO_UP,
                                    Controls.PLAYER_TWO_DOWN)

    #character = game.create_npc((500,500),RED)
    game.create_ball((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
                     (random.choice((0, SCREEN_WIDTH)), SCREEN_HEIGHT / 2),
                     Colors.BALL_COLOR)

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == player_one.key_up or event.key == player_one.key_down:
                    player_one.update_input(event)
                elif event.key == player_two.key_up or event.key == player_two.key_down:
                    player_two.update_input(event)
                elif event.key == Controls.BALL_UNFREEZE:
                    game.unfreeze_balls()
            elif event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        # set delta time from clock to normalize speeds
        delta_milliseconds = clock.tick(360)
        # drawing
        screen.fill(Colors.BACKGROUND_COLOR)
        game.cleanup()
        #collisionSystem.draw()
        game.move(delta_milliseconds)
        collision_system.update()
        game.check_scores()
        game.draw()
        pygame.display.flip()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
