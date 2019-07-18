"""Camera module"""

import globes
import pygame
import random


class Camera(object):
    """Camera class"""
    def __init__(self, world, xpos=0, ypos=0):
        self.world = world
        self.maxheight = globes.Globals.MAX_HEIGHT[globes.Globals.LVL_NUM - 1]
        self.shake_num = 0
        self.xpos = xpos
        self.ypos = ypos

    def set(self, xpos, ypos):
        """Sets the position of the camera"""
        self.xpos = (self.world.realwidth + xpos) % self.world.realwidth
        self.ypos = (self.world.realheight + ypos) % self.world.realheight

    def update(self, player):     # updates the camera so it offsets the
        """Updates the camera position based on player parameter"""
        left, top, width, height = player.rect
        # extra = 40 if player.facing == "right" else  -40
        newleft = left - globes.Globals.WIDTH / 2  # + extra
        newtop = top - globes.Globals.HEIGHT / 2
        diffx = newleft - self.xpos
        diffy = newtop - self.ypos
        self.xpos = int(self.xpos + .15 * diffx)  # New camera left
        self.ypos = int(self.ypos + .25 * diffy)  # New camera top
        self.shake()
        self.xpos = max(0, self.xpos)  # to make sure the left is at least 0
        self.xpos = min(self.world.realwidth - globes.Globals.WIDTH,
                        self.xpos)
        self.ypos = max(0, self.ypos)  # to make sure the top is at least 0
        self.ypos = min(self.world.realheight - globes.Globals.HEIGHT,
                        self.ypos)
        if self.maxheight is not None:
            self.ypos = min(self.maxheight - globes.Globals.HEIGHT, self.ypos)

    def apply(self, target):  # offsets the target sprite
        """Applys camera offset to the target parameter"""
        return target.rect.move(-self.xpos, -self.ypos)

    def render(self, screen, radius=1):  # blits tiles on the screen
        """Renders the background onto the screen"""
        width = self.world.realwidth / self.world.width  # pixels in 1 image
        height = self.world.realheight / self.world.height
        # centerx = self.xpos + globes.Globals.WIDTH / 2
        # centery = self.ypos + globes.Globals.HEIGHT / 2
        temp = pygame.Surface((width * (radius * 2 + 1),
                              height * (radius * 2 + 1))).convert()
        sdy = 0
        for i in range(self.ypos / height - radius,
                       self.ypos / height + radius + 1):
            sdx = 0
            for j in range(self.xpos / width - radius,
                           self.xpos / width + radius + 1):
                tile = self.world.tile((j, i))
                temp.blit(tile, (sdx, sdy), (0, 0, width, height))
                sdx += width
            sdy += height
        screen.blit(temp, (0, 0),
                   (width + self.xpos % width, height + self.ypos % height,
                    width, height))

    def shake_camera(self, num=10):
        """Causes the camera to shake num times"""
        self.shake_num = num

    def shake(self):
        """Ticks camera shake num and shakes camera"""
        self.shake_num -= 1
        if self.shake_num > 0:
            self.xpos += random.randint(-20, 20)
            self.ypos += random.randint(-20, 20)
