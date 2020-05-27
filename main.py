import pygame
from collision import CollisionSystem
from pygame.time import Clock
from entities import Player, Wall, Character

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE =     (255, 255, 255)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
BLACK = (  0,   0,  0)

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

    # list of all entities
    entity_list = []

    # list of all walls
    wall_list = []

    # list of all characters
    character_list = []

    # collision system
    collision_system = CollisionSystem(character_list, wall_list)

    # defining clock
    clock = Clock()

    # defining player
    player = Player((200,200), BLUE)
    entity_list.append(player)
    character_list.append(player)

    character = Character((500,500), RED)
    entity_list.append(character)
    character_list.append(character)

    # defining a wall
    wall = Wall(BLACK, (400, 300))
    entity_list.append(wall)
    wall_list.append(wall)
     
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
                character = Character(pygame.mouse.get_pos(), RED)
                entity_list.append(character)
                character_list.append(character)
        # set delta time from clock to normalize speeds
        dt = clock.tick(60)
        # drawing
        screen.fill(WHITE)
        collision_system.update()
        for entity in entity_list:
            entity.update(screen)
        for character in character_list:
            character.move(dt, character_list)
        pygame.display.flip()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()