"""Enemy classes"""

import pygame
import random as R
import items
import globes
import collision


class Enemy(pygame.sprite.Sprite):
    """Enemy base class"""
    IMAGESRIGHT = None
    IMAGESLEFT = None
    CYCLE = 1.0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # if Enemy.IMAGESRIGHT is None:
        #     self.load_images()
        # self.image = Enemy.IMAGESRIGHT[0]
        # self.rect = self.image.get_rect()
        self.time = 0.0
        self.frame = 0
        self.stun_num = 0

    def update(self, dtime):
        """Updates enemy"""
        self.stun()

    def load_images(self):
        """Loads enemy images"""
        pass

    def update_image(self):
        """Updates enemy images"""
        pass

    def stun_enemy(self, num=30):
        """Causes enemy to be stunned"""
        self.stun_num = num

    def stun(self):
        """Ticks stun duration"""
        self.stun_num -= 1


class FlyingEnemy(Enemy):
    """Flying enemy sprite"""
    IMAGESRIGHT = None
    IMAGESLEFT = None
    CYCLE = 1.0
    MAXVELOCITY = 400

    #xrange 2-tuple minimum x-coordinate, maximum x-coordinate
    def __init__(self, xrange):
        Enemy.__init__(self)
        if FlyingEnemy.IMAGESRIGHT is None:
            self.load_images()
        self.image = FlyingEnemy.IMAGESRIGHT[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (R.randint(800, xrange[1] - 75),
                                R.randint(75, 600))
        self.x_velocity = R.randint(100, 500)
        self.y_velocity = R.randint(100, 500)
        self.minx, self.maxx = xrange

#    def update(self, dtime=1):
#        self.time = self.time + dtime
#        if self.rect.left < self.minx or self.rect.right > self.maxx:
#            self.velocity *= -1
#
#        self.rect.x += self.velocity * dtime
#        if self.time > Enemy.CYCLE:
#            self.time = 0.0
#        frame = int(self.time / (Enemy.CYCLE / len(Enemy.IMAGESLEFT)))
#        if frame != self.frame:
#            self.frame = frame
#            self.update_image()

    def update(self, dtime=1):
        """Updates flying enemy"""
        Enemy.update(self, dtime)
        self.time = self.time + dtime
        if self.rect.left < self.minx:
            self.x_velocity = 400
        elif self.rect.right > self.maxx:
            self.x_velocity = -400
        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.y_velocity *= -1

        self.x_velocity += R.randint(-100, 100)
        self.y_velocity += R.randint(-100, 100)
        if self.x_velocity > FlyingEnemy.MAXVELOCITY:
            self.x_velocity = FlyingEnemy.MAXVELOCITY
        elif self.x_velocity < -1 * FlyingEnemy.MAXVELOCITY:
            self.x_velocity = -1 * FlyingEnemy.MAXVELOCITY
        if self.y_velocity > FlyingEnemy.MAXVELOCITY:
            self.y_velocity = FlyingEnemy.MAXVELOCITY
        elif self.y_velocity < -1 * FlyingEnemy.MAXVELOCITY:
            self.y_velocity = -1 * FlyingEnemy.MAXVELOCITY

        self.rect.x += self.x_velocity * dtime
        self.rect.y += self.y_velocity * dtime
        if self.time > Enemy.CYCLE:
            self.time = 0.0
        frame = int(self.time / (Enemy.CYCLE / len(FlyingEnemy.IMAGESLEFT)))
        # if frame != self.frame:
        self.frame = frame
        self.update_image()

    def load_images(self):
        """Loads flying enemy images"""
        FlyingEnemy.IMAGESLEFT = []
        FlyingEnemy.IMAGESRIGHT = []
        sheetleft = pygame.image.load("imgs/ghostspriteleft.png").convert()
        sheetright = pygame.image.load("imgs/ghostspriteright.png").convert()
        keyleft = sheetleft.get_at((0, 0))
        keyright = sheetright.get_at((0, 0))
        for i in range(2):
            surfaceleft = pygame.Surface((140, 147)).convert()
            surfaceright = pygame.Surface((140, 147)).convert()
            surfaceleft.set_colorkey(keyleft)
            surfaceright.set_colorkey(keyright)
            surfaceleft.blit(sheetleft, (0, 0), (i * 140, 0, 140, 147))
            surfaceright.blit(sheetright, (0, 0), (i * 140, 0, 140, 147))
            FlyingEnemy.IMAGESLEFT.append(surfaceleft)
            FlyingEnemy.IMAGESRIGHT.append(surfaceright)

    def update_image(self):
        """Updates flying enemy image"""
        if self.x_velocity < 0:
            self.image = FlyingEnemy.IMAGESLEFT[self.frame]
        else:
            self.image = FlyingEnemy.IMAGESRIGHT[self.frame]


class PlatformEnemy(Enemy):
    """Platform enemy sprite class"""
    IMAGESRIGHT = None
    IMAGESLEFT = None
    CYCLE = 1.0

    def __init__(self, platform):
        if PlatformEnemy.IMAGESRIGHT is None:
            self.load_images()
        self.image = PlatformEnemy.IMAGESRIGHT[0]
        self.rect = self.image.get_rect()
        Enemy.__init__(self)
        self.rect.bottomleft = platform.rect.topleft
        self.x_velocity = 200
        self.y_velocity = 0
        self.platform = platform

    def update(self, dtime=1):
        """Updates platform enemy"""
        Enemy.update(self, dtime)
        if self.stun_num > 0:
            return
        self.time = self.time + dtime
        if self.rect.left < self.platform.rect.left or \
                self.rect.right > self.platform.rect.right:
            self.x_velocity *= -1

        self.rect.x += self.x_velocity * dtime
        self.rect.y += self.y_velocity * dtime
        if self.time > Enemy.CYCLE:
            self.time = 0.0
        frame = int(self.time / (Enemy.CYCLE / len(PlatformEnemy.IMAGESLEFT)))
        # if frame != self.frame:
        self.frame = frame
        self.update_image()

    def load_images(self):
        """Loads platform enemy images"""
        PlatformEnemy.IMAGESLEFT = []
        PlatformEnemy.IMAGESRIGHT = []
        sheetleft = pygame.image.load("imgs/enemysprite.png").convert()
        sheetright = pygame.image.load("imgs/enemyspriteflip.png").convert()
        keyleft = sheetleft.get_at((0, 0))
        keyright = sheetright.get_at((0, 0))
        for i in range(2):
            surfaceleft = pygame.Surface((75, 67)).convert()
            surfaceright = pygame.Surface((75, 67)).convert()
            surfaceleft.set_colorkey(keyleft)
            surfaceright.set_colorkey(keyright)
            surfaceleft.blit(sheetleft, (0, 0), (i * 75, 0, 75, 67))
            surfaceright.blit(sheetright, (0, 0), (i * 75, 0, 75, 67))
            PlatformEnemy.IMAGESLEFT.append(surfaceleft)
            PlatformEnemy.IMAGESRIGHT.append(surfaceright)

    def update_image(self):
        """Updates platform enemy image"""
        if self.x_velocity < 0:
            self.image = PlatformEnemy.IMAGESLEFT[self.frame]
        else:
            self.image = PlatformEnemy.IMAGESRIGHT[self.frame]


class ShooterEnemy(Enemy):
    """Shooter enemy sprite class"""
    IMAGES = None

    def __init__(self, pos, freq):
        Enemy.__init__(self)
        if ShooterEnemy.IMAGES is None:
            self.load_images()
        self.image = ShooterEnemy.IMAGES[0]
        self.rect = self.image.get_rect()
        self.pos = pos
        airplanex, airplaney = pos
        self.airplanepos = (airplanex, (airplaney + 40))
        self.rect.topleft = pos
        self.frequency = freq

    def update(self, dtime=1):
        """Updates shooter enemy"""
        Enemy.update(self, dtime)
        if self.stun_num > 0:
            return
        self.time = self.time + dtime
        if self.time > self.frequency:
            self.time = 0.0
        frame = int(self.time / (self.frequency / len(ShooterEnemy.IMAGES)))
        if frame != self.frame:
            self.frame = frame
            self.update_image()
            if self.frame == 2:
                # Create airplane object
                return items.Airplane(self.airplanepos, -400)
            else:
                return None

    def update_image(self):
        """Updates shooter enemy image"""
        self.image = ShooterEnemy.IMAGES[self.frame]

    def load_images(self):
        """Loads shooter enemy images"""
        ShooterEnemy.IMAGES = []
        sheet = pygame.image.load("imgs/airplane_enemy.png").convert()
        key = sheet.get_at((0, 0))
        for i in range(3):
            surface = pygame.Surface((187, 227)).convert()
            surface.set_colorkey(key)
            surface.blit(sheet, (0, 0), (i * 187, 0, 187, 227))
            ShooterEnemy.IMAGES.append(surface)


class GhostEnemy(Enemy):
    """Ghost enemy sprite class"""
    IMAGESRIGHT = None
    IMAGESLEFT = None
    CYCLE = 1.0

    def __init__(self, pos):  # pos = (x, y)
        Enemy.__init__(self)
        if GhostEnemy.IMAGESRIGHT is None:
            self.load_images()
        self.image = GhostEnemy.IMAGESRIGHT[0]
        self.rect = self.image.get_rect().inflate(-20, -20)
        self.pos = pos
        self.rect.topleft = pos
        self.x_velocity = 0
        self.y_velocity = 0
        self.image = GhostEnemy.IMAGESLEFT[0]
        self.cycle = R.random() + 0.3  # so not all sprites sync'd?

    def update(self, dtime=1):
        """Updates ghost enemy"""
        Enemy.update(self, dtime)
        if self.stun_num > 0:
            return
        self.time = self.time + dtime
        if self.rect.top < self.pos[1] + 100:
            self.y_velocity += 10
        elif self.rect.top > self.pos[1] + 100:
            self.y_velocity -= 10

        self.rect.x += self.x_velocity * dtime
        self.rect.y += self.y_velocity * dtime
        if self.time > self.cycle:  # Enemy.CYCLE:
            self.time = 0.0  # Enemy.CYCLE
        frame = int(self.time / (self.cycle / len(GhostEnemy.IMAGESLEFT)))
        if frame != self.frame:
            self.frame = frame
            self.update_image()

    def load_images(self):
        """Loads ghost enemy images"""
        GhostEnemy.IMAGESLEFT = []
        GhostEnemy.IMAGESRIGHT = []
        sheetleft = pygame.image.load("imgs/ghostspriteleft.png").convert()
        sheetright = pygame.image.load("imgs/ghostspriteright.png").convert()
        keyleft = sheetleft.get_at((0, 0))
        keyright = sheetright.get_at((0, 0))
        for i in range(2):
            surfaceleft = pygame.Surface((140, 147)).convert()
            surfaceright = pygame.Surface((140, 147)).convert()
            surfaceleft.set_colorkey(keyleft)
            surfaceright.set_colorkey(keyright)
            surfaceleft.blit(sheetleft, (0, 0), (i * 140, 0, 140, 147))
            surfaceright.blit(sheetright, (0, 0), (i * 140, 0, 140, 147))
            GhostEnemy.IMAGESLEFT.append(surfaceleft)
            GhostEnemy.IMAGESRIGHT.append(surfaceright)

    def update_image(self):
        """Updates ghost enemy image"""
        if self.x_velocity <= 0:
            self.image = GhostEnemy.IMAGESLEFT[self.frame]
        else:
            self.image = GhostEnemy.IMAGESRIGHT[self.frame]


class Spider(Enemy):
    """Spider enemy sprite class"""
    IMAGES = None
    CYCLE = 1.0

    def __init__(self, pos):  # pos = (x, y)
        Enemy.__init__(self)
        if Spider.IMAGES is None:
            self.load_images()

        #width, height = 20, 20
        #self.rect = pygame.Rect(pos[0], pos[1], width, height)
        #surface = pygame.Surface((width, height))
        #surface.fill(globes.Globals.WHITE)
        #surface.set_colorkey(globes.Globals.WHITE)
        #self.image = surface

        self.image = Spider.IMAGES[0]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = pos
        self.x_velocity = 0
        self.y_velocity = 200

        #self.cycle = R.random() + 0.3
        self.time = 0.0
        self.stop = 0.0
        self.toggle = 0

    def update(self, dtime=1):
        """Updates spider enemy"""
        Enemy.update(self, dtime)
        if self.stun_num > 0:
            return
        if self.stop > 0.0:
            self.stop -= dtime * 10
            self.toggle = 4
            return

        self.time = self.time + dtime

        if self.toggle % 4 == 0:
            self.rect.x += self.x_velocity * dtime
            self.rect.y += self.y_velocity * dtime

        if self.rect.top > self.pos[1] + 150:
            self.y_velocity = -200
            self.stop = 20.0
        if self.rect.top < self.pos[1]:
            self.y_velocity = 200
            self.stop = 20.0

        self.toggle += 1
        if self.time > Spider.CYCLE:  # Enemy.CYCLE:
            self.time = 0.0  # Enemy.CYCLE
        #frame = int(self.time / (Spider.CYCLE / len(Spider.IMAGES)))
        #if frame != self.frame:
        #    self.frame = frame
        #    self.update_image()

    def load_images(self):
        """Loads spider enemy images"""
        Spider.IMAGES = []
        sheet = pygame.image.load("imgs/spider.png").convert()
        key = sheet.get_at((0, 0))
        for i in range(1):
            surface = pygame.Surface((50, 31)).convert()
            surface.set_colorkey(key)
            surface.blit(sheet, (0, 0), (i * 50, 0, 50, 31))
            Spider.IMAGES.append(surface)

    def update_image(self):
        """Updates spider enemy image"""


class BookEnemy(Enemy):
    """Platform enemy sprite class"""
    IMAGESRIGHT = None
    IMAGESLEFT = None
    CYCLE = 1.0
    MAXSPEEDY = 250
    SPEEDX = 201

    def __init__(self, topleft, facing):
        if BookEnemy.IMAGESRIGHT is None:
            self.load_images()
        self.image = BookEnemy.IMAGESRIGHT[0]
        self.rect = self.image.get_rect()
        Enemy.__init__(self)
        self.rect.topleft = topleft
        self.x_velocity = 1
        self.y_velocity = 0
        if facing == "right":
            self.direction = 1
        elif facing == "left":
            self.direction = -1
        self.onground = False

    def update(self, dtime=1):
        """Updates platform enemy"""
        Enemy.update(self, dtime)
        if self.stun_num > 0:
            return
        self.time = self.time + dtime
        self.dtime = dtime

        self.update_position(dtime)

        if self.time > Enemy.CYCLE:
            self.time = 0.0
        frame = int(self.time / (Enemy.CYCLE / len(BookEnemy.IMAGESLEFT)))
        # if frame != self.frame:
        self.frame = frame
        self.update_image()

    def load_images(self):
        """Loads platform enemy images"""
        BookEnemy.IMAGESLEFT = []
        BookEnemy.IMAGESRIGHT = []
        sheetleft = pygame.image.load("imgs/enemysprite.png").convert()
        sheetright = pygame.image.load("imgs/enemyspriteflip.png").convert()
        keyleft = sheetleft.get_at((0, 0))
        keyright = sheetright.get_at((0, 0))
        for i in range(2):
            surfaceleft = pygame.Surface((75, 67)).convert()
            surfaceright = pygame.Surface((75, 67)).convert()
            surfaceleft.set_colorkey(keyleft)
            surfaceright.set_colorkey(keyright)
            surfaceleft.blit(sheetleft, (0, 0), (i * 75, 0, 75, 67))
            surfaceright.blit(sheetright, (0, 0), (i * 75, 0, 75, 67))
            BookEnemy.IMAGESLEFT.append(surfaceleft)
            BookEnemy.IMAGESRIGHT.append(surfaceright)

    def update_image(self):
        """Updates platform enemy image"""
        if self.x_velocity < 0:
            self.image = BookEnemy.IMAGESLEFT[self.frame]
        else:
            self.image = BookEnemy.IMAGESRIGHT[self.frame]

    def update_position(self, dtime):
        if self.rect.top > globes.Globals.CAMERA.world.realheight:
            self.kill()

        if self.x_velocity == 0:
            self.direction *= -1
        if self.onground:
            self.x_velocity = BookEnemy.SPEEDX * self.direction
        elif abs(self.x_velocity) > 1:
            self.x_velocity = self.direction * abs(self.x_velocity) - \
                20 * cmp(self.x_velocity, 0)
        self.rect.x += self.x_velocity * dtime

        collision.horizontal_collision(self)

        if self.y_velocity < BookEnemy.MAXSPEEDY:
            self.y_velocity += 20
        self.rect.y += self.y_velocity * dtime
        if self.y_velocity > 0:
            self.rect.y += 2

        collision.vertical_collision(self)
