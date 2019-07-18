"""Items module"""

import pygame
import globes


class EndS(pygame.sprite.Sprite):
    """EndS sprite class"""
    IMAGES = None
    CYCLE = 1.0

    def __init__(self, bottom_left):
        pygame.sprite.Sprite.__init__(self)
        if EndS.IMAGES is None:
            self.load_images()

        self.image = EndS.IMAGES[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = bottom_left
        self.frame = 0
        self.time = 0.0
        self.dtime = 0.0

    def update(self, dtime=1):
        """Updates the sprite"""
        self.dtime = dtime
        self.update_image()

    def load_images(self):
        """Loads the endS images"""
        EndS.IMAGES = []
        sheet = pygame.image.load("imgs/endS.png").convert()
        key = sheet.get_at((0, 0))

        for i in range(3):
            surface = pygame.Surface((66, 120)).convert()
            surface.set_colorkey(key)
            surface.blit(sheet, (0, 0), (i * 66, 0, 66, 120))
            EndS.IMAGES.append(surface)

    def update_image(self):
        """Updates the sprite image"""
        if self.time > EndS.CYCLE:
            self.time = 0.0

        frame = int(self.time / (EndS.CYCLE / len(EndS.IMAGES)))
        self.image = EndS.IMAGES[frame]
        self.time = self.time + self.dtime


class PairedDoor(pygame.sprite.Sprite):
    """ One of a pair of doors (in-game) """

    IMAGES = None

    def __init__(self, bot_left, new_botleft):
        """ @param new_botleft 2-tuple coordinates to translate player's
            (bottom, left) """
        pygame.sprite.Sprite.__init__(self)
        if PairedDoor.IMAGES is None:
            self.load_images()

        left, bottom = bot_left
        self.image = PairedDoor.IMAGES[0]
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(left, bottom - self.rect.height,
                                self.rect.width, self.rect.height)
        self.new_coords = new_botleft
        self.open = False

    def load_images(self):
        PairedDoor.IMAGES = []
        door = pygame.image.load("imgs/door.png").convert()
        PairedDoor.IMAGES.append(door)
#        door = door.fill(globes.BLACK)
#        PairedDoor.IMAGES.append(door)

    def transport(self, sprite):
        sprite.rect.bottomleft = self.new_coords


class Door(pygame.sprite.Sprite):
    """Door sprite class"""
    IMAGES = None

    def __init__(self, bot_left, num):
        pygame.sprite.Sprite.__init__(self)
        if Door.IMAGES is None:
            Door.IMAGES = []
            Door.IMAGES.append(pygame.image.load("imgs/locked_door.png")
                               .convert())
            Door.IMAGES.append(pygame.image.load("imgs/door1.png").convert())
            Door.IMAGES.append(pygame.image.load("imgs/door2.png").convert())
            Door.IMAGES.append(pygame.image.load("imgs/door3.png").convert())
            Door.IMAGES.append(pygame.image.load("imgs/door4.png").convert())
            Door.IMAGES.append(pygame.image.load("imgs/door5.png").convert())

        if num <= globes.Globals.LVLS_UNLOCKED:
            self.image = Door.IMAGES[num]
        else:
            self.image = Door.IMAGES[0]
        self.rect = self.image.get_rect()
        l, b = bot_left
        width, height = 70, 100
        self.rect = pygame.Rect(l, b - height, width, height)

        # surface = pygame.Surface((width, height))
        # surface.fill(globes.Globals.WHITE)
        # surface.set_colorkey(globes.Globals.WHITE)
        # self.image = surface

        self.lvl_num = num


class Twain(pygame.sprite.Sprite):
    """Twain sprite class"""
    IMAGE = None
    SOUND = None
    CYCLE = 5.0

    def __init__(self, bottom_left, dest):
        pygame.sprite.Sprite.__init__(self)
        if Twain.IMAGE is None:
            Twain.IMAGE = pygame.image.load("imgs/" +
                                            "marktwain.png").convert()
            key = Twain.IMAGE.get_at((0, 0))
            Twain.IMAGE.set_colorkey(key)
            Twain.SOUND = pygame.mixer.Sound("audio/twainshort1.ogg")
            Twain.SOUND.set_volume(globes.Globals.VOLUME)
            # self.load_image()

        self.image = Twain.IMAGE
        self.rect = self.image.get_rect()
        self.rect.bottomleft = bottom_left
        self.time = 0.0
        self.dtime = 0.0
        self.destx, self.desty = dest
        self.diffx = self.destx - self.rect.left
        self.diffy = self.desty - (self.rect.bottom - self.rect.height / 2)
        self.sign = 1
        self.toggle = 0
#        Twain.SOUND.play()

    def update(self, dtime=1):
        """Updates the Twain sprite"""
        self.dtime = dtime
        self.time += dtime
        self.toggle += 1
        self.update_position()

    def update_position(self):
        """Updates the position of the sprite"""
        if self.toggle % 4 == 0:
            self.rect.x += 4 * self.sign * self.diffx * self.dtime / \
                (Twain.CYCLE / 2)
            self.rect.y += 4 * self.sign * self.diffy * self.dtime / \
                (Twain.CYCLE / 2)

        if self.rect.left - self.destx <= 0 and self.sign == 1:
            self.sign *= -1

    # def load_images(self):
    #    surf = pygame.image.load("imgs/marktwain.png").convert()
    #    key = surf.get_at((0, 0))

#        surface = pygame.Surface((66, 120)).convert()
#        surface.set_colorkey(key)
#        surface.blit(surf, (0, 0), (i * 66, 0, 66, 120))
#        Twain.IMAGE = surface


class Airplane(pygame.sprite.Sprite):
    """Airplane sprite class"""
    IMAGE = None
    SOUND = None
    LIFESPAN = 1200  # remove from sprite group when traveled 800 pixels
#    OSCILLATION = 0.5  # oscillation cycle

    def __init__(self, top_left, xvelocity):
        pygame.sprite.Sprite.__init__(self)
        if Airplane.IMAGE is None:
            Airplane.IMAGE = pygame.image.load("imgs/airplane.png").convert()
            Airplane.IMAGE.set_colorkey(Airplane.IMAGE.get_at((0, 0)))
            Airplane.SOUND = pygame.mixer.Sound("audio/airplane.ogg")
            if globes.Globals.MUTE:
                volume = 0
            else:
                volume = globes.Globals.VOLUME
            Airplane.SOUND.set_volume(volume)
        self.image = Airplane.IMAGE
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left
        self.xtraversal = 0
        self.velocityx = xvelocity
        self.velocityy = 100
        self.time = 0.0
#        Airplane.SOUND.play()

    def update(self, dtime=1):
        """Updates the sprite"""
        self.time = self.time + dtime
#        if self.time > Airplane.OSCILLATION:
#            self.time = 0.0
#            self.velocityy *= -1
        self.rect.x += dtime * self.velocityx
        self.xtraversal += dtime * self.velocityx
        self.rect.y += dtime * self.velocityy

    def should_remove(self):
        """Determines if the airplane should be removed"""
        if (self.xtraversal > Airplane.LIFESPAN or
                -self.xtraversal > Airplane.LIFESPAN):
            return True
        else:
            return False
