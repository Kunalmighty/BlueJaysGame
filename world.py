"""World module"""

import globes
import pygame


class World(object):
    """World class - background tiles"""

    def __init__(self, filename):
        self.map = []  # array that stores tile layout
        from_file = open(filename)  # file with tile layout
        for line in from_file:
            self.map.append(line.strip())
        self.height = len(self.map)  # number of tiles vertically
        self.width = len(self.map[0])  # number of tiles horizontally
        # height of level in pixels:
        self.realheight = self.height *\
            globes.Globals.TILES.values()[0].get_height()
        # width of level in pixels:
        self.realwidth = self.width *\
            globes.Globals.TILES.values()[0].get_width()

    def tile(self, tile_numbers):  # determine which tile to use
        """ Returns the tile at given position
            @param tile_numbers 2-tuple of (x, y) tile numbers """

        xnum, ynum = tile_numbers

        if xnum < 0 or ynum < 0 or xnum >= self.width or ynum >= self.height:
            return pygame.Surface((self.realwidth / self.width,
                                   self.realheight / self.width))
        xnum = (self.width + xnum) % self.width
        ynum = (self.height + ynum) % self.height
        code = self.map[ynum][xnum]  # get key of desired tile
        if code == "0":
            return pygame.Surface((self.realwidth / self.width,
                                   self.realheight / self.width))
        return globes.Globals.TILES[code]  # return tile surface based on key
