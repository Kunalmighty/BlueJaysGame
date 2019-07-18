"""
module for triggers
"""
import pygame
import enemy as E


class Trigger(pygame.sprite.Sprite):
    """
    trigger class
    """
    IMAGE = None
    KEY = None

# @param triggerps: a 2-tuple (x, y) for trigger possition
# @param pos: a 2-tuple (x, y) for "GE", (x_min, x_max) for "FE"
# "PE" only requires enemy_type and param platform
# "FE" and "GE" only requires param enemy_type and pos
    def __init__(self, enemy_type, triggerpos, pos=None, platform=None):
        pygame.sprite.Sprite.__init__(self)
        if Trigger.IMAGE is None:
            Trigger.IMAGE = pygame.image.load("imgs/bookpile.png").convert()
            Trigger.KEY = Trigger.IMAGE.get_at((0, 0))

        self.image = Trigger.IMAGE
        self.image.set_colorkey(Trigger.KEY)
        self.rect = pygame.Rect(triggerpos, (100, 100))
        if enemy_type == "PE":
            self.enemy = E.PlatformEnemy(platform)
        elif enemy_type == "GE":
            self.enemy = E.GhostEnemy(pos)
        elif enemy_type == "FE":
            self.enemy = E.FlyingEnemy(pos)
