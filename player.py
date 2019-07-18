"""Player Sprite"""

import pygame
import globes
import collision

WHITE = (255, 255, 255)
WIDTH = 800
HEIGHT = 600
MAXSPEEDX = 360
MAXSPEEDY = 500
ACCELERATIONX = 20


class Player(pygame.sprite.Sprite):
    """Player Sprite"""
    IMAGESRIGHT = None
    IMAGESLEFT = None
    IMAGESIDLE = None
    IMAGESJUMPLEFT = None
    IMAGESJUMPRIGHT = None
    IMAGESDEADLEFT = None
    IMAGESDEADRIGHT = None
    WALLSOUND = None
    CYCLE = 1.0
    JUMPCYCLE = .25

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if Player.WALLSOUND is None:
            Player.WALLSOUND = pygame.mixer.Sound("audio/smack.ogg")
            Player.WALLSOUND.set_volume(globes.Globals.VOLUME)
        if Player.IMAGESRIGHT is None:
            self.load_images()

        self.image = Player.IMAGESIDLERIGHT[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (100, 100)
        self.x_velocity = 0
        self.y_velocity = 0
        self.onwall = True
        self.frame = 0
        self.facing = "right"
        self.state = "idleright"

        self.onground = False
        self.goup = False
        self.goright = False
        self.goleft = False
        self.turnright = False
        self.turnleft = False
        self.shift = False  # if shift is held
        self.onmp = False  # if on a moving platform. sorry for all the bools
        self.time = 0.0
        self.dtime = 0.0
        self.killed = False
        self.triggered = False  # whether player just triggered
        self.minigame = False  # whether player is in ghost hopper minigame

    def update(self, dtime=1):
        """Updates the player"""
        self.dtime = dtime
        self.update_image()
        if not self.killed:
            self.update_position()
        else:
            self.update_position_dead()
        self.update_sound()

    def moveright(self, move):
        """Tells the player to move right or stop moving right"""
        if self.facing == "left" and move:
            self.turnright = True
            self.facing = "right"
        #if self.rect.right < WIDTH:
        self.goright = True
        if not move:
            self.goright = False

    def moveleft(self, move):
        """Tells the player to move left or stop moving left"""
        if self.facing == "right" and move:
            self.turnleft = True
            self.facing = "left"
        if self.rect.left > 0:
            self.goleft = True
        if not move:
            self.goleft = False

    def moveup(self, move):
        """Tells the player to move up or stop moving up"""
        self.goup = True
        if not move:
            self.goup = False

    def load_images(self):
        """Loads the images for the player"""
        Player.IMAGESRIGHT = []
        Player.IMAGESLEFT = []
        Player.IMAGESIDLERIGHT = []
        Player.IMAGESIDLELEFT = []
        Player.IMAGESJUMPLEFT = []
        Player.IMAGESJUMPRIGHT = []
        Player.IMAGESDEADLEFT = []
        Player.IMAGESDEADRIGHT = []
        sheet1 = pygame.image.load("imgs/playersprite.png").convert()
        sheet2 = pygame.image.load("imgs/playerspriteflip.png").convert()
        sheet3 = pygame.image.load("imgs/idlesprite.png").convert()
        sheet4 = pygame.image.load("imgs/idlespriteflip.png").convert()
        sheet5 = pygame.image.load("imgs/jumpright.png").convert()
        sheet6 = pygame.image.load("imgs/jumpleft.png").convert()
        sheet7 = pygame.image.load("imgs/deadbluejayright.png").convert()
        sheet8 = pygame.image.load("imgs/deadbluejayleft.png").convert()
        key1 = sheet1.get_at((0, 0))
        key2 = sheet2.get_at((0, 0))
        key3 = sheet3.get_at((0, 0))
        key4 = sheet4.get_at((0, 0))
        key5 = sheet5.get_at((0, 0))
        key6 = sheet6.get_at((0, 0))
        key7 = sheet7.get_at((0, 0))
        key8 = sheet8.get_at((0, 0))
        for i in range(6):
            surface1 = pygame.Surface((50, 94)).convert()
            surface2 = pygame.Surface((49, 94)).convert()
            surface1.set_colorkey(key1)
            surface2.set_colorkey(key2)
            surface1.blit(sheet1, (0, 0), (i * 50, 0, 50, 94))
            surface2.blit(sheet2, (0, 0), (i * 49, 0, 49, 94))
            Player.IMAGESRIGHT.append(surface1)
            Player.IMAGESLEFT.append(surface2)
        for i in range(2):
            surface3 = pygame.Surface((50, 94)).convert()
            surface4 = pygame.Surface((50, 94)).convert()
            surface5 = pygame.Surface((50, 94)).convert()
            surface6 = pygame.Surface((50, 94)).convert()
            surface7 = pygame.Surface((50, 94)).convert()
            surface8 = pygame.Surface((50, 94)).convert()
            surface3.set_colorkey(key3)
            surface4.set_colorkey(key4)
            surface5.set_colorkey(key5)
            surface6.set_colorkey(key6)
            surface7.set_colorkey(key7)
            surface8.set_colorkey(key8)
            surface3.blit(sheet3, (0, 0), (i * 50, 0, 50, 94))
            surface4.blit(sheet4, (0, 0), (i * 50, 0, 50, 94))
            surface5.blit(sheet5, (0, 0), (i * 50, 0, 50, 94))
            surface6.blit(sheet6, (0, 0), (i * 50, 0, 50, 94))
            surface7.blit(sheet7, (0, 0), (i * 50, 0, 50, 94))
            surface8.blit(sheet8, (0, 0), (i * 50, 0, 50, 94))
            Player.IMAGESIDLERIGHT.append(surface3)
            Player.IMAGESIDLELEFT.append(surface4)
            Player.IMAGESJUMPRIGHT.append(surface5)
            Player.IMAGESJUMPLEFT.append(surface6)
            Player.IMAGESDEADRIGHT.append(surface7)
            Player.IMAGESDEADLEFT.append(surface8)

    def update_image(self):
        """Updates the player images"""
        if self.time > Player.CYCLE:
            self.time = 0.0
        xcenter, ycenter = self.rect.center
        if self.goleft and not self.goright and self.onground:
            if self.state is not "movingleft":
                self.time = 0.0
                self.state = "movingleft"
            frame = int(self.time / (Player.CYCLE / len(Player.IMAGESLEFT)))
            self.image = Player.IMAGESLEFT[frame]
            self.time = self.time + self.dtime
        elif self.goright and not self.goleft and self.onground:
            if self.state is not "movingright":
                self.time = 0.0
                self.state = "movingright"
            frame = int(self.time / (Player.CYCLE / len(Player.IMAGESRIGHT)))
            self.image = Player.IMAGESRIGHT[frame]
            self.time = self.time + self.dtime
        elif not self.onground:
            if self.time > Player.JUMPCYCLE:
                self.time = 0.0
            if (self.state is not "jumping"):
                self.time = 0.0
                self.state = "jumping"
            if cmp(self.y_velocity, 0) > 0:
                if self.facing == "left":
                    self.image = Player.IMAGESJUMPLEFT[0]
                elif self.facing == "right":
                    self.image = Player.IMAGESJUMPRIGHT[0]
            else:
                frame = int(
                    self.time / (Player.JUMPCYCLE /
                                 len(Player.IMAGESJUMPLEFT)))
                if self.facing == "left":
                    self.image = Player.IMAGESJUMPLEFT[frame]
                    if self.killed:
                        self.image = Player.IMAGESDEADLEFT[frame]
                else:
                    self.image = Player.IMAGESJUMPRIGHT[frame]
                    if self.killed:
                        self.image = Player.IMAGESDEADRIGHT[frame]
                self.time = self.time + self.dtime
        else:
            if self.facing == "left" and self.state is not "idleleft":
                self.time = 0.0
                self.state = "idleleft"
            elif self.facing == "right" and self.state is not "idleright":
                self.time = 0.0
                self.state = "idleright"
            frame = int(self.time / (Player.CYCLE /
                        len(Player.IMAGESIDLERIGHT)))
            if self.state == "idleright":
                self.image = Player.IMAGESIDLERIGHT[frame]
            elif self.state == "idleleft":
                self.image = Player.IMAGESIDLELEFT[frame]
            self.time = self.time + self.dtime
        self.rect = self.image.get_rect()
        self.rect.center = (xcenter, ycenter)
        self.turnright = False
        self.turnleft = False

    def update_position(self):
        """Updates the player's position"""
        # for x in movingbooks:
        #    platforms.add(x)

        if self.rect.top > globes.Globals.CAMERA.world.realheight:
            self.player_killed()

        # Horizontal Movement
        if self.goleft:
            if self.x_velocity >= -1 * MAXSPEEDX or self.onmp:
                self.x_velocity -= ACCELERATIONX
                if self.onmp:
                    self.x_velocity -= ACCELERATIONX * 11
        if self.goright:
            if self.x_velocity <= MAXSPEEDX or self.onmp:
                self.x_velocity += ACCELERATIONX
                if self.onmp:
                    self.x_velocity += ACCELERATIONX * 11

        if not self.goright and not self.goleft or (self.goright and
                                                    self.goleft):
            if not (not self.onground and self.shift) and not self.onmp:
                self.x_velocity += -1 * cmp(self.x_velocity, 0) * 20
                if -20 < self.x_velocity < 20:
                    self.x_velocity = 0

        self.rect.x += self.x_velocity * self.dtime

        # Horizontal Platform Collision
        if not self.minigame:
            collision.horizontal_collision(self)

        # Vertical Movement
        if self.goup and self.onground:
            self.onground = False
            self.y_velocity = -900

        if self.y_velocity < MAXSPEEDY:
            self.y_velocity += 20
        self.rect.y += self.y_velocity * self.dtime
        if self.y_velocity > 0:
            self.rect.y += 2

        # Vertical Platform Collision
        if not self.minigame:
            collision.vertical_collision(self)

    def update_position_dead(self):
        """Updates the position of a dead player"""
        self.rect.y += self.y_velocity * self.dtime

    def player_killed(self):
        """Called when the player is killed"""
        self.x_velocity = 0
        self.y_velocity = -250
        self.onground = False
        # self.rect.bottomleft = (100, 100)
        self.killed = True

    def update_sound(self):
        """Updates the player's sound"""
        if ((self.rect.left <= 0) and
                not self.onwall) or self.triggered:
            Player.WALLSOUND.play()
            self.onwall = True
            self.triggered = False
        elif self.rect.left > 1 and self.rect.right < WIDTH - 1:
            self.onwall = False
