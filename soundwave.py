"""
module for soundwave attack
"""
import pygame
import globes

WHITE = (255, 255, 255)


class Soundwave(pygame.sprite.Sprite):
    """
    soundwave class
    """
    IMAGES = None
    IMAGESRIGHT = None
    IMAGESLEFT = None
    CYCLE = 0.4
    SOUND = None

    def __init__(self, player_facing, player_rect):
        pygame.sprite.Sprite.__init__(self)
        if Soundwave.SOUND is None:
            Soundwave.SOUND = pygame.mixer.Sound("soundwave.ogg")
            if globes.Globals.MUTE:
                volume = 0
            else:
                volume = globes.Globals.VOLUME
            Soundwave.SOUND.set_volume(volume)
        if Soundwave.IMAGESRIGHT is None or Soundwave.IMAGESLEFT is None:
            self.load_images()
        if player_facing == "right":
            self.image = Soundwave.IMAGESRIGHT[0]
            self.rect = self.image.get_rect()
            cord_a, cord_b = player_rect.bottomright
            self.rect.bottomleft = (cord_a, 0.97 * cord_b)
        else:
            self.image = Soundwave.IMAGESLEFT[0]
            self.rect = self.image.get_rect()
            cord_a, cord_b = player_rect.bottomleft
            self.rect.bottomright = (cord_a, 0.97 * cord_b)
        Soundwave.SOUND.play()

        self.facing = player_facing
        self.velocity = 7
        self.time = 0.0
        self.delta = 0.0
        self.frame = 0
        self.do_attack = False

    def update(self, delta=1):
        """
        update calls
        """
        self.delta = delta
        self.update_image()
        self.update_position()

    def load_images(self):
        """
        load sprites for soundwave attacks in both direction (left and right).
        """
        Soundwave.IMAGESRIGHT = []
        Soundwave.IMAGESLEFT = []

        dim_x_indices = [0, 21, 65, 127]
        widths = [21, 44, 62, 76]

        sheet1 = pygame.image.load("imgs/soundwaves.png").convert()
        key1 = sheet1.get_at((0, 0))
        sheet2 = pygame.image.load("imgs/soundwavesleft.png").convert()
        key2 = sheet2.get_at((0, 0))

        for i in range(4):
            surface1 = pygame.Surface((widths[i], 84)).convert()
            surface1.set_colorkey(key1)
            surface1.blit(sheet1, (0, 0), (dim_x_indices[i], 0, widths[i], 84))
            Soundwave.IMAGESRIGHT.append(surface1)

            surface2 = pygame.Surface((widths[i], 84)).convert()
            surface2.set_colorkey(key2)
            surface2.blit(sheet2, (0, 0), (dim_x_indices[i], 0, widths[i], 84))
            Soundwave.IMAGESLEFT.append(surface2)

    def update_image(self):
        """
        animation of soundwave attacks relative to the main game loop
        """
        if self.time < Soundwave.CYCLE:  # don't update frame if thru cycle
            dim_x, dim_y = self.rect.center
            if self.facing == "right":
                frame = int(
                    self.time / (Soundwave.CYCLE / len(Soundwave.IMAGESRIGHT)))
                self.image = Soundwave.IMAGESRIGHT[frame]

            elif self.facing == "left":
                frame = int(self.time / (Soundwave.CYCLE
                            / len(Soundwave.IMAGESLEFT)))
                self.image = Soundwave.IMAGESLEFT[frame]
            self.time += self.delta
            self.rect = self.image.get_rect()
            self.rect.center = (dim_x, dim_y)

    def update_position(self):
        """
        move the soundwaves across the screen
        """
        if self.facing == "right":
            self.rect.x += self.velocity
        elif self.facing == "left":
            self.rect.x -= self.velocity
