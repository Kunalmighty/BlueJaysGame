"""Module with global variables and functions"""

import pygame
import pygame.event as EV
import game

BLACK = (0, 0, 0)

# Player variables
# initialized in main, used in lvlselect, updated at end of each level
LVLS_UNLOCKED = 0


class Globals(object):
    """Globals class - contains global variables"""
    RUNNING = True
    SCREEN = None
    WIDTH = None
    HEIGHT = None
    FONT = None
    STATE = None
    TILES = {}
    WORLD = None
    CAMERA = None
    HIGHSCORES = None

    # Game variables
    GAME = None
    LVLS_UNLOCKED = 1
    SOUND = None
    LVL_NUM = 1
    MAX_HEIGHT = [1035, None, None, None, None]
    MINIGAME = None

    # Setup
    CONTROLLER = False
    JOYSTICK = None
    EVENTS = None
    EVENT_MAP = None
    VOLUME = 1.0
    MUTE = False
    BRIGHTNESS = 1.0

    #Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


# Horizontally center a surface on the screen.
# @return the surface's desired left x index
def hcenter(surface):
    """Returns the left index of a centered surface on the screen"""
    return Globals.WIDTH / 2 - surface.get_width() / 2


def play_music(soundfile):
    """Plays music from given soundfile"""
    Globals.SOUND = pygame.mixer.Sound(soundfile)
    if Globals.MUTE:
        Globals.SOUND.set_volume(0)
    else:
        Globals.SOUND.set_volume(Globals.VOLUME)
    Globals.SOUND.play(-1)


def stop_music():
    """Stops music that is currently playing"""
    Globals.SOUND.fadeout(200)


def save_game(lives, score):
    """Saves game state variables to file"""
    tofile = open("save.txt", 'w')
    tofile.write("%d %d %d" % (Globals.LVLS_UNLOCKED, lives, score))
    tofile.close()


def load_game():
    """Loads previously saved game from file"""
    file = open("save.txt")
    lvls, lives, score = 1, 5, 0
    for line in file:
        if len(line) < 2:
            file.close()
            return
        else:
            lvls, lives, score = line.strip().split()
            lvls, lives, score = int(lvls), int(lives), int(score)
    Globals.LVLS_UNLOCKED = lvls
    game1 = game.Game()
    game1.lives = lives
    game1.score = score
    Globals.LVLS_UNLOCKED = lvls
    Globals.GAME = game1
    file.close()


def map_event(event):
    if (event.type == pygame.JOYBUTTONDOWN or
            event.type == pygame.JOYHATMOTION):
        for index, value in enumerate(Globals.EVENT_MAP):
            if value == event:
                return Globals.EVENTS[index]
    if (event.type == pygame.JOYAXISMOTION):
        if significant_magnitude(event.value):
            for index, mapped in enumerate(Globals.EVENT_MAP):
                if (significant_magnitude(mapped.value)
                        and event.axis == mapped.axis
                        and same_sign(mapped.value, event.value)):
                    return Globals.EVENTS[index]
        else:
            for index, mapped in enumerate(Globals.EVENT_MAP):
                if (not significant_magnitude(mapped.value) and
                        event.axis == mapped.axis and
                        same_sign(mapped.value, event.value)):
                    return Globals.EVENTS[index]
    return event


def significant_magnitude(num):
    """ Return an integer of -1, 0, or 1 based on magnitude with an arbitrary
    significance of 0.07 """

    if -0.08 < num < 0.08:
        return False
    return True


def same_sign(num1, num2):
    if ((num1 < 0 and num2 < 0) or (num1 > 0 and num2 > 0)
            or (num1 == 0 and num2 == 0)):
        return True
    return False


def is_numeric(str):
    try:
        x = int(str)
        return True
    except ValueError:
        return False
