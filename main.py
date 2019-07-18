"""
main module of the game
"""

import globes
import title
import pygame
import scorelist
import level
import minigame
import volume
import joystick


def main():
    """
    entry point
    """
    initialize()
    main_loop()
    close()


def initialize():
    """
    initialization of the game
    """
    # init() returns number of modules successfully and insuccessfully loaded
    num_passed, num_failed = pygame.init()
    if num_failed > 0:
        print "WARNING: %d Pygame modules failed to initialize.\n" % num_failed
    else:
        print "%d modules loaded. \n" % num_passed

    globes.Globals.SCREEN = pygame.display.set_mode((800, 600))
#    globes.load_events()
    level.initialize_levels()
    minigame.global_init()  # intialize minigame layouts
    globes.load_game()
    globes.Globals.SCREEN.fill(globes.Globals.WHITE)
    globes.Globals.WIDTH, globes.Globals.HEIGHT = \
        globes.Globals.SCREEN.get_size()
    globes.Globals.FONT = pygame.font.Font(None, 30)
    globes.Globals.HIGHSCORES = scorelist.ScoreList("highscores.txt")
    globes.Globals.STATE = title.Title()  # menu.Menu()


def main_loop():
    """
    main update loop of the game
    """
    interval = 0.01
    new_time = 0.0
    current_time = 0.0
    leftover = 0.0

    while globes.Globals.RUNNING:
        globes.Globals.STATE.render()
        pygame.display.flip()

        new_time = pygame.time.get_ticks()
        frame_time = (new_time - current_time) / 1000.0
        current_time = new_time
        leftover += frame_time
        while leftover > interval:
            globes.Globals.STATE.update(interval)
            leftover -= interval

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globes.Globals.RUNNING = False
            elif (globes.Globals.STATE.__class__.__name__ != "Joystick" and
                    event.type == pygame.KEYDOWN and event.key == pygame.K_m):
                globes.Globals.MUTE = not globes.Globals.MUTE
                volume.set_volume_levels()
            else:
                if (globes.Globals.STATE.__class__.__name__ != "Joystick" and
                        globes.Globals.CONTROLLER):
                    event = globes.map_event(event)
                globes.Globals.STATE.event(event)


def close():
    """
    exit the game
    """
    pygame.quit()


main()
