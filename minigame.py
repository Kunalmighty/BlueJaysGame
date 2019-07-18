"""Minigame module"""

import state
import world
import menu
import player
import globes
import enemy as E
import platform
import pygame
import soundwave
import level
import camera

WIDTH = 800
HEIGHT = 600
ENEMY_BOUNCE = None

# layout-specific globals
WORLD_FILES = ["maps/minimap0.txt"]
TILE_FILES = ["tiles/minitiles0.txt"]
LAYOUT_FILES = ["lvls/mini0.txt"]
THRESHOLDS = [10]  # Number of kills for an extra life
SPEEDS = [(100, 0)]
MAX_HEIGHT = [3000]
WORLDS = []
ENEMIES = [None]


def global_init():
    """ load ENEMIES sprite groups and WORLDS """
    ENEMY_BOUNCE = pygame.mixer.Sound("audio/enemydeath2.ogg")
    for index in range(len(LAYOUT_FILES)):
        parse_layout(index)

        level.load_tiles(TILE_FILES[index])
        WORLDS.append(world.World(WORLD_FILES[index]))


def parse_layout(index):
    """ Load the tiles, world and sprites of a given layout file
        @param index the index of LAYOUT_FILES """

    ENEMIES[index] = pygame.sprite.Group()

    level = []
    file = open(LAYOUT_FILES[index])
    for line in file:
        level.append(line)

    for i in range(0, len(level)):
        for j in range(0, len(level[i])):
            symbol = level[i][j]
            if symbol == 'X':
                x_pos, y_pos = j * 25, (i * 25 + 500)
                ENEMIES[index].add(E.GhostEnemy((x_pos, y_pos)))

    file.close()


class Minigame(state.State):
    """Minigame state class - User jumps on ghosts to earn extra life"""

    DELAY = 3.0

    def __init__(self, player, layout_code=None):
        state.State.__init__(self)

        if ENEMY_BOUNCE is None:  # safety for uninitialized layout globals
            global_init()

        self.sprites = []
        self.enemies = pygame.sprite.Group()
        self.dead_enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.soundwaves = pygame.sprite.Group()
        self.empty_group = pygame.sprite.Group()  # dummy group for params

        if layout_code is None:
            pass  # layout_code = rand # between 0 and len(LAYOUT_FILES)-1
        self.enemies = ENEMIES[layout_code]
        self.threshold = THRESHOLDS[layout_code]
        self.speed = SPEEDS[layout_code]

        globes.Globals.WORLD = WORLDS[layout_code]
        globes.Globals.CAMERA = camera.Camera(globes.Globals.WORLD)
        globes.Globals.CAMERA.maxheight = MAX_HEIGHT[layout_code]

        self.xstart, self.ystart = player.rect.bottomleft
        self.player = player
        self.player.minigame = True
        self.player.onground = False
        self.player.y_velocity = 100
        self.player.rect.bottomleft = (380, 200)
        self.players.add(self.player)
        self.num_killed = 0
        self.time = 0

    def render(self):
        """Renders the sprites, game information and background on screen"""

        globes.Globals.CAMERA.update(self.player)
        globes.Globals.CAMERA.render(globes.Globals.SCREEN)
        for sprite in self.players:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.enemies:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.dead_enemies:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.soundwaves:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))

        # Game Information
        surf = globes.Globals.FONT.render("Lives: %d" %
                                          globes.Globals.GAME.lives, True,
                                          globes.Globals.WHITE)
        globes.Globals.SCREEN.blit(surf, (10, 5))
        surf = globes.Globals.FONT.render("Ghosts Killed: %d" %
                                          self.num_killed, True,
                                          globes.Globals.WHITE)
        globes.Globals.SCREEN.blit(surf, (600, 5))

    def update(self, time):
        """Updates the game"""
        self.time += time
        if self.time < Minigame.DELAY:
            return
        self.players.update(time)
        self.enemies.update(time)
        for sprite in self.enemies:
            sprite.rect.x += self.speed[0] * time
            sprite.rect.y += self.speed[1] * time
            if sprite.rect.bottom < globes.Globals.CAMERA.ypos:
                self.enemies.remove(sprite)
        self.enemy_deaths(time)
        if len(self.soundwaves) != 0:
            for s in self.soundwaves:
                if (globes.Globals.CAMERA.apply(s).left <= 0 or
                        globes.Globals.CAMERA.apply(s).right >= WIDTH * 4):
                    self.soundwaves.remove(s)
        self.soundwaves.update(time)

        if self.player.killed and self.player.rect.bottom <= 0:
            self.end()
#        if self.player.rect.bottom > HEIGHT:  # if player fell off screen
#            self.player.player_killed()
        if not self.player.killed:
            self.enemy_collision()

    def event(self, event):
        """Processes events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                globes.stop_music()
                globes.Globals.STATE = menu.Menu()
            elif event.key == pygame.K_RIGHT:
                self.player.moveright(True)
            elif event.key == pygame.K_LEFT:
                self.player.moveleft(True)
            elif event.key == pygame.K_UP:
                self.player.moveup(True)
            elif (event.key == pygame.K_SPACE and not self.player.killed):
                sw = soundwave.Soundwave(
                    self.player.facing, self.player.rect)
                self.soundwaves.add(sw)
            elif event.key == pygame.K_c:
                pass  # put cheat code here
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.player.moveright(False)
            elif event.key == pygame.K_LEFT:
                self.player.moveleft(False)
            elif event.key == pygame.K_UP:
                self.player.moveup(False)

    def enemy_collision(self):
        """Determines and handles enemy collisions"""
        for i in self.enemies.sprites():  # player-enemy collisions
            if 0 < self.player.rect.bottom - i.rect.top < 20 \
                    and (i.rect.left < self.player.rect.left < i.rect.right
                         or i.rect.left < self.player.rect.right
                         < i.rect.right):
                globes.Globals.GAME.ENEMY_BOUNCE.play()
                self.player.rect.bottom = i.rect.top
                self.player.y_velocity = -800
                self.num_killed += 1
                self.dead_enemies.add(i)
                self.enemies.remove(i)
            elif ((i.rect.left < self.player.rect.left < i.rect.right
                  or i.rect.left < self.player.rect.right < i.rect.right)
                  and (i.rect.top < self.player.rect.top < i.rect.bottom
                       or i.rect.top < self.player.rect.bottom
                       < i.rect.bottom)):
                self.player.rect.y = 600
                self.player.player_killed()

        collisions = pygame.sprite.groupcollide(self.enemies, self.soundwaves,
                                                False, True)
        for i in collisions:
            i.stun_enemy(80)

    def end(self):
        """Handles the end of the minigame"""
        globes.Globals.MINIGAME = None
        self.player.killed = False  # reset killed
        self.player.minigame = False
        self.player.velocityx, self.player.velocityy = 0, 0
        if self.num_killed >= self.threshold:
            globes.Globals.GAME.lives += 1

        lvl = globes.Globals.LVL_NUM
        level.load_tiles(level.LVL_TILES[lvl])
        globes.Globals.WORLD = level.LVL_WORLDS[lvl]
        globes.Globals.CAMERA = camera.Camera(globes.Globals.WORLD)
        globes.Globals.GAME.player1.rect.bottomleft = (self.xstart,
                                                       self.ystart)
        globes.Globals.STATE = globes.Globals.GAME

    def enemy_deaths(self, time):
        """Enacts enemy death sequence"""
        for i in self.dead_enemies:
            if i.rect.bottom < globes.Globals.CAMERA.world.realheight:
                self.dead_enemies.remove(i)
            else:
                i.rect.y += 4 * self.player.x_velocity * time


class MiniDoor(pygame.sprite.Sprite):
    """ Door to ghost bounce minigame """

    IMAGES = None
    DEFAULT_TRANSPORT = (50, 100)

    def __init__(self, layout, bot_left):
        pygame.sprite.Sprite.__init__(self)
        if MiniDoor.IMAGES is None:
            self.load_images()

        left, bottom = bot_left
        self.image = MiniDoor.IMAGES[0]
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(left, bottom - self.rect.height,
                                self.rect.width, self.rect.height)
        self.open = False
        self.used = False

    def use_door(self, sprite):
        if not self.used:
            self.used = True
            self.image = MiniDoor.IMAGES[1]
            return True  # successful minigame entrance
        else:
            sprite.rect.bottomleft = MiniDoor.DEFAULT_TRANSPORT
            return False

    def load_images(self):
        MiniDoor.IMAGES = []
        MiniDoor.IMAGES.append(pygame.image.load("imgs/doorstar.png")
                               .convert())
        MiniDoor.IMAGES.append(pygame.image.load("imgs/door.png")
                               .convert())
