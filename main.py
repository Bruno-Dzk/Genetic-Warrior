import pygame
from collision import CollisionSystem
from pygame.time import Clock
from entities import Player, Wall, Character, Bullet

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE =     (255, 255, 255)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
BLACK = (  0,   0,  0)

class Game():
    def __init__(self, screen):
        self.screen = screen
        self.entity_list = []
        self.character_list = []
        self.wall_list = []
    
    def create_player(self, coords, color):
        player = Player(coords, color)
        self.entity_list.append(player)
        self.character_list.append(player)
        return player

    def create_npc(self, coords, color):
        npc = Character(coords, color)
        self.entity_list.append(npc)
        self.character_list.append(npc)
        return npc

    def create_wall(self, coords, color):
        wall = Wall(coords, color)
        self.entity_list.append(wall)
        self.wall_list.append(wall)
        return wall

    def update(self, dt):
        for entity in self.entity_list:
            entity.update(self.screen)
        for character in self.character_list:
            character.move(dt)

# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    # logo = pygame.image.load("logo32x32.png")
    # pygame.display.set_icon(logo)
    pygame.display.set_caption("Genetic Warrior")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
     
    # define a variable to control the main loop
    running = True

    # create an instance of Game class
    game = Game(screen)

    # crate a collision detection system
    collisionSystem = CollisionSystem(game)

    # defining clock
    clock = Clock()

    # defining player
    player = game.create_player((200,200),BLUE)

    character = game.create_npc((500,500),RED)

    # defining a wall
    game.create_wall((400,300),BLACK)
    game.create_wall((440,300),BLACK)
    game.create_wall((480,300),BLACK)
    game.create_wall((520,300),BLACK)
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                player.update_input(event)
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        # set delta time from clock to normalize speeds
        dt = clock.tick(360)
        # drawing
        screen.fill(WHITE)
       
        game.update(dt)
        collisionSystem.update()

        pygame.display.flip()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()