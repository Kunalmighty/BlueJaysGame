""" Define platform Sprite objects including generic platform
    Books, Moving Books, and Spikes """


import pygame
import globes
import collision
import player


class Platform(pygame.sprite.Sprite):
    """ Generic platform """

    def __init__(self, upper_left, bottom_right):
        """ @param upper_left coordinate tuple of (x, y) format
            @param bottom_right coordinate tuple, (x, y) """
        pygame.sprite.Sprite.__init__(self)

        topx, topy = upper_left
        bottomx, bottomy = bottom_right
        width = bottomx - topx
        height = bottomy - topy
        self.rect = pygame.Rect(topx, topy, width, height)

        surface = pygame.Surface((width, height))
        surface.fill(globes.Globals.WHITE)
        surface.set_colorkey(globes.Globals.WHITE)

        self.image = surface


class Books(pygame.sprite.Sprite):
    """ Static book platform with dimensions 100x40 """

#   IMAGE = None

    def __init__(self, upper_left, num):
        pygame.sprite.Sprite.__init__(self)

        width = num * 100
        height = 40
        topx, topy = upper_left
        self.rect = pygame.Rect(topx, topy, width, height)

        # if Books.IMAGE is None:
        #   self.load_image()
        image1 = pygame.image.load("imgs/bookplatform1.png").convert()
        surface = pygame.Surface((width, height)).convert()
        key = image1.get_at((0, 0))
        surface.set_colorkey(key)

        for x_index in range(num):
            surface.blit(image1, (x_index * 100, 0))
        self.image = surface

    # def load_image(self):
    #    image1 = pygame.image.load("imgs/bookplatform1.png").convert()
    #    surface = pygame.Surface((width, height)).convert()
    #    key = image1.get_at((0, 0))
    #    surface.set_colorkey(key)


class MovingBook(pygame.sprite.Sprite):
    """ Book(s) that move with constant x and y velocity """

    def __init__(self, upper_left, num, ranges, velocities):
        """ @param ranges int 2-tuple of width of x, y movement
            @param velocities int 2-tuple of x_velocity, y_velocity
                   Note: minimum of 100 """

        pygame.sprite.Sprite.__init__(self)

        width = num * 100
        height = 40
        topx, topy = upper_left
        self.rect = pygame.Rect(topx, topy, width, height)

        image1 = pygame.image.load("imgs/bookplatform1.png").convert()
        surface = pygame.Surface((width, height)).convert()
        key = image1.get_at((0, 0))
        surface.set_colorkey(key)

        for x_index in range(num):
            surface.blit(image1, (x_index * 100, 0))
        self.image = surface

        self.xwidth, self.yheight = ranges
        self.x_velocity, self.y_velocity = velocities
        if self.x_velocity < 100 and self.xwidth > 0:
            self.x_velocity = 100
        if self.y_velocity < 100 and self.yheight > 0:
            self.y_velocity = 100
        self.relativex = 0  # position relative to initialized position
        self.relativey = 0

    def update(self, delta_t=1):
        """ Moving books update method override """

        if self.relativex < 0 or self.relativex > self.xwidth:
            self.x_velocity *= -1
        if self.relativey < 0 or self.relativey > self.yheight:
            self.y_velocity *= -1

        x_change = self.x_velocity * delta_t
        y_change = self.y_velocity * delta_t

        self.rect.x += x_change
        self.relativex += x_change
        self.rect.y += y_change
        self.relativey += y_change


class Spikes(pygame.sprite.Sprite):
    """ Spikes object, used in player-killing collisions """

    IMAGE = None
    KEY = None

    def __init__(self, upper_left, num):
        pygame.sprite.Sprite.__init__(self)

        if Spikes.IMAGE is None:
            Spikes.IMAGE = pygame.image.load("imgs/spikes.png").convert()
            Spikes.KEY = Spikes.IMAGE.get_at((0, 0))

        width = num * 100
        height = 65
        topx, topy = upper_left
        self.rect = pygame.Rect(topx, topy, width, height)

        surface = pygame.Surface((width, height)).convert()
        surface.set_colorkey(Spikes.KEY)
        surface.fill(Spikes.KEY)

        for x_pos in range(num):
            surface.blit(Spikes.IMAGE, (x_pos * 100, 0))
            x_pos += 100
        self.image = surface


class Platform2(pygame.sprite.Sprite):
    """ Platform with collision detection on left OR right """

    def __init__(self,  upper_left, bottom_right, side):
        pygame.sprite.Sprite.__init__(self)
        #Platform.__init__(self, upper_left, bottom_right)
        topx, topy = upper_left
        bottomx, bottomy = bottom_right
        width = bottomx - topx
        height = bottomy - topy
        self.rect = pygame.Rect(topx, topy, width, height)

        surface = pygame.Surface((width, height))
        surface.fill(globes.Globals.WHITE)
        surface.set_colorkey(globes.Globals.WHITE)

        self.image = surface

        self.side = side  # the side that can't be moved through


class Chair(pygame.sprite.Sprite):

    IMAGES = None
    CYCLE = 1.0
    MAXSPEEDY = 500
    ACCELERATIONX = 1

    def __init__(self, bottom_left):
        pygame.sprite.Sprite.__init__(self)
        if Chair.IMAGES is None:
            self.load_images()

        self.image = Chair.IMAGES[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = bottom_left
        self.frame = 0
        self.time = 0.0
        self.dtime = 0.0
        self.old = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.sitting = False
        self.changex_velocity = 0

    def update(self, dtime=1, player1=None):
        """Updates the sprite"""
        self.dtime = dtime
        self.update_position(player1)
        #self.update_image()

    def load_images(self):
        """Loads the chair images"""
        Chair.IMAGES = []
        sheet = pygame.image.load("imgs/chair2.png").convert()
        key = sheet.get_at((0, 0))

        for i in range(1):
            surface = pygame.Surface((90, 151)).convert()
            surface.set_colorkey(key)
            surface.blit(sheet, (0, 0), (i * 90, 0, 90, 151))
            Chair.IMAGES.append(surface)

    def update_image(self):
        """Updates the chair image"""
        if self.time > Chair.CYCLE:
            self.time = 0.0

        frame = int(self.time / (Chair.CYCLE / len(Chair.IMAGES)))
        self.image = Chair.IMAGES[frame]
        self.time = self.time + self.dtime

    def update_position(self, player1):
        """Updates the chair's position"""

        if self.rect.top > globes.Globals.CAMERA.world.realheight or \
                self.rect.bottom < 0:
            self.kill()

        sprite = pygame.sprite.Sprite()
        sprite.rect = player1.rect.copy()
        sprite.rect.y = sprite.rect.y + 3 - self.rect.height / 2
        if not self.sitting and pygame.sprite.collide_rect(self, sprite):
            self.sitting = True
            self.x_velocity = player1.x_velocity / 2 + self.x_velocity / 2
            player1.onmp = True
        elif self.sitting and not pygame.sprite.collide_rect(self, sprite):
            self.sitting = False
            player1.onmp = False
#        elif pygame.sprite.collide_rect(self, sprite):
#            player.x_velocity = self.x_velocity

        # Horizontal Movement
        prev_velocity = self.x_velocity
        self.x_velocity += self.changex_velocity
        self.changex_velocity = 0
        self.x_velocity += -1 * cmp(self.x_velocity, 0) * Chair.ACCELERATIONX
        if (prev_velocity < self.x_velocity and 0 < self.x_velocity < 100):
            self.x_velocity = 100
        self.rect.x += self.x_velocity * self.dtime

        # Horizontal Platform Collision
        collision.horizontal_collision(self)

        # Vertical Movement
        if self.y_velocity < Chair.MAXSPEEDY:
            self.y_velocity += 20
        self.rect.y += self.y_velocity * self.dtime
        if self.y_velocity > 0:
            self.rect.y += 2

        # Vertical Platform Collision
        collision.vertical_collision(self)

    def __eq__(self, other):
        if (isinstance(other, self.__class__)):
            return self.rect == other.rect
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
