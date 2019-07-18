"""Game module"""

import state
import menu
import minigame as mini
import player
import globes
import enemy as E
import platform
import pygame
import soundwave
import gameover
import trigger
import items
import level
import camera
import boss

WIDTH = 800
HEIGHT = 600


class Game(state.State):
    """Game state class - user controls the blue jay"""

    ENEMY_BOUNCE = None
    EVIL_LAUGH = None

    def __init__(self):
        state.State.__init__(self)

        if Game.ENEMY_BOUNCE is None:
            Game.ENEMY_BOUNCE = pygame.mixer.Sound("audio/enemydeath2.ogg")
            Game.ENEMY_BOUNCE.set_volume(globes.Globals.VOLUME)
            Game.EVIL_LAUGH = pygame.mixer.Sound("audio/sinisterlaugh.ogg")
            Game.EVIL_LAUGH.set_volume(globes.Globals.VOLUME)

        self.sprites = []
        self.shooters = []
        self.projectiles = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.dead_enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.platforms2 = pygame.sprite.Group()
        self.movingbooks = pygame.sprite.Group()
        self.chairs = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.pairedDoors = pygame.sprite.Group()
        self.miniDoor = None
        self.triggers = []

        self.player1 = player.Player()
        self.players.add(self.player1)
        self.lives = 5

        self.soundwaves = pygame.sprite.Group()
        self.soundwave1 = None
        self.timeremaining = 100.0
        self.score = 0

        self.mark = None
        self.door_num = -1
        self.initialize_lvl(0)

    # @param int lvl
    def initialize_lvl(self, level_num):
        """Initializes the level based on level_num parameter"""
#        level.build_level(level_num)
        if level_num > 0:
            globes.Globals.LVL_NUM = level_num
        self.sprites = level.LVL_SPRITES[level_num]
        level.load_tiles(level.LVL_TILES[(level_num)])
        globes.Globals.WORLD = level.LVL_WORLDS[level_num]
        globes.Globals.CAMERA = camera.Camera(globes.Globals.WORLD)
        if self.lives != 5 and self.score > 0:
            globes.save_game(self.lives, self.score)

        self.enemies.empty()
        self.bosses.empty()
        self.shooters = []
        self.projectiles.empty()  # projectiles hazardous to player
        self.fireballs.empty()
        self.dead_enemies.empty()
        self.platforms.empty()
        self.platforms2.empty()
        self.movingbooks.empty()
        self.chairs.empty()
        self.spikes.empty()
        self.doors.empty()
        self.pairedDoors.empty()
        self.miniDoor = None
        self.triggers = []

        self.build_level()
        self.spawn_enemies()
        self.timeremaining = 100
        if level_num == 0:
            self.timeremaining = -1

        # self.player1.rect.bottomleft = (50, 100)

    def render(self):
        """Renders the sprites, game information and background on screen"""

        globes.Globals.CAMERA.update(self.player1)
        globes.Globals.CAMERA.render(globes.Globals.SCREEN)
        for sprite in self.doors:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.pairedDoors:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        if self.miniDoor is not None:
            globes.Globals.SCREEN.blit(self.miniDoor.image,
                                       globes.Globals.CAMERA
                                       .apply(self.miniDoor))
        for sprite in self.platforms2:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.shooters:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.projectiles:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.movingbooks:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.chairs:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.players:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.enemies:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.bosses:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.dead_enemies:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.platforms:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.spikes:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.triggers:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.soundwaves:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        for sprite in self.fireballs:
            globes.Globals.SCREEN.blit(sprite.image,
                                       globes.Globals.CAMERA.apply(sprite))
        globes.Globals.SCREEN.blit(self.endS.image,
                                   globes.Globals.CAMERA.apply(self.endS))
        for enemy in self.enemies:
            if enemy.__class__.__name__ == "Spider":
                self.draw_web(enemy)
        if self.mark is not None:
            globes.Globals.SCREEN.blit(self.mark.image,
                                       globes.Globals.CAMERA.apply(self.mark))
        # Game Information
        surf = globes.Globals.FONT.render("Lives: %d" % self.lives, True,
                                          globes.Globals.BLACK)
        globes.Globals.SCREEN.blit(surf, (10, 5))
        surf = globes.Globals.FONT.render("Score: %d" % self.score,
                                          True, globes.Globals.BLACK)
        globes.Globals.SCREEN.blit(surf, (680, 5))
        if self.timeremaining >= 0:
            surf = \
                globes.Globals.FONT.render("Time: %3.0f" % self.timeremaining,
                                           True, globes.Globals.BLACK)
            globes.Globals.SCREEN.blit(surf, (690, 25))
        # globes.Globals.SCREEN.fill(globes.Globals.BLACK)
        # globes.Globals.SCREEN.blit(Game.BACKGROUND, (0, 0))
        # self.players.draw(globes.Globals.SCREEN)
        # self.enemies.draw(globes.Globals.SCREEN)
        # self.platforms.draw(globes.Globals.SCREEN)
        # self.soundwaves.draw(globes.Globals.SCREEN)

    def update(self, time):
        """Updates the game"""
        self.endS.update(time)
        if self.mark is not None:
            self.update_complete(time)
            return
        self.chairs.update(time, self.player1)
        self.players.update(time)
        self.enemies.update(time)
        self.bosses.update(time)
        for every in self.shooters:
            plane = every.update(time)  # return airplane or none
            if plane is not None:
                self.projectiles.add(plane)
        self.projectiles.update(time)
        self.fireballs.update(time)
        for every in self.projectiles:
            if every.should_remove():
                self.projectiles.remove(every)
        self.enemy_deaths(time)
        self.movingbooks.update(time)
        if len(self.soundwaves) != 0:
            for s in self.soundwaves:
                if (globes.Globals.CAMERA.apply(s).left <= 0 or
                        globes.Globals.CAMERA.apply(s).right >= WIDTH * 4):
                    self.soundwaves.remove(s)
        self.soundwaves.update(time)

            # self.level_complete()  # if you get to end of level
        if self.player1.killed and self.player1.rect.bottom <= 0:
            self.death()
        self.timeremaining -= time
        if -0.1 < self.timeremaining < 0.1:  # if time is zero, player is kild
            self.player1.player_killed()
        if not self.player1.killed:
            self.enemy_collision()
            self.projectile_collision()
            self.door_collision()
            self.trigger_detection()
            self.chair_collision()
            if self.player1.rect.colliderect(self.endRect):
                if globes.Globals.LVL_NUM == len(level.LVL_FILES) - 1:
                    self.level_complete()
                else:  # decrease music volume and play voice over
                    if not globes.Globals.MUTE:
                        globes.Globals.SOUND.set_volume(0.4 *
                                                        globes.Globals.VOLUME)
                        Game.EVIL_LAUGH.play()
                self.mark = \
                    items.Twain((self.endRect.right +
                                 globes.Globals.WIDTH / 2, 0),
                               (self.endRect.right, self.endRect.top +
                                self.endRect.height / 2))

    def event(self, event):
        """Processes events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                globes.stop_music()
                globes.Globals.STATE = menu.Menu()
            elif event.key == pygame.K_RETURN:
                self.paired_door_collision()
                self.minidoor_collision()
            elif event.key == pygame.K_RIGHT:
                self.player1.moveright(True)
            elif event.key == pygame.K_LEFT:
                self.player1.moveleft(True)
            elif event.key == pygame.K_UP:
                if self.door_num >= 0 \
                        and self.door_num <= globes.Globals.LVLS_UNLOCKED:
                    self.player1.y_velocity = 0
                    self.initialize_lvl(self.door_num)
                else:
                    self.player1.moveup(True)
            elif (event.key == pygame.K_SPACE):
                if self.door_num >= 0 \
                        and self.door_num <= globes.Globals.LVLS_UNLOCKED:
                    self.player1.y_velocity = 0
                    self.initialize_lvl(self.door_num)
                elif (not self.player1.killed):
                    sw = soundwave.Soundwave(
                        self.player1.facing, self.player1.rect)
                    self.soundwaves.add(sw)
                    self.move_chair()
            elif event.key == pygame.K_c:
                if globes.Globals.LVL_NUM == 5:
                    for i in self.bosses:
                        i.hit()
                    return
                self.player1.rect.right = self.endS.rect.left + 2
                self.player1.rect.top = self.endS.rect.top + \
                    self.endS.rect.height / 2
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.player1.shift = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.player1.moveright(False)
            elif event.key == pygame.K_LEFT:
                self.player1.moveleft(False)
            elif event.key == pygame.K_UP:
                self.player1.moveup(False)
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.player1.shift = False

    def enemy_collision(self):
        """Determines and handles enemy collisions"""
        for i in self.enemies.sprites():  # player-enemy collisions
            if 0 < self.player1.rect.bottom - i.rect.top < 20 \
                    and (i.rect.left + 15 < self.player1.rect.left
                         < i.rect.right - 10 or i.rect.left + 15
                         < self.player1.rect.right < i.rect.right - 10):
                Game.ENEMY_BOUNCE.play()
                self.player1.rect.bottom = i.rect.top
                self.player1.y_velocity = -800
                self.score += 5 * self.lives  # points given based on lives
                self.dead_enemies.add(i)
                self.enemies.remove(i)
            elif (((i.rect.left + 15 < self.player1.rect.left < i.rect.right
                  - 10 or i.rect.left + 15 < self.player1.rect.right <
                  i.rect.right - 10)
                  and pygame.sprite.collide_rect(i, self.player1))
                  or (i.__class__.__name__ == "Spider" and
                      pygame.sprite.collide_rect(i, self.player1))):
                self.player1.player_killed()

        collisions = pygame.sprite.groupcollide(self.enemies, self.soundwaves,
                                                False, True)
        for i in collisions:
            i.stun_enemy(80)
        for i in pygame.sprite.groupcollide(self.bosses, self.soundwaves,
                                            False, True):
            i.stun_enemy(80)
        #if len(pygame.sprite.groupcollide(self.soundwaves, self.enemies,
         #                                 True, True)) > 0:
          #  self.score += 10 * self.lives  # points given based on lives

    def projectile_collision(self):
        """Determines and handles projectile collisions"""
        collisions = pygame.sprite.groupcollide(self.projectiles,
                                                self.soundwaves, False, True)
        for i in collisions:
            self.dead_enemies.add(i)
            self.projectiles.remove(i)
            self.score += 5

        for i in self.projectiles.sprites():
            if (i.rect.left < self.player1.rect.left < i.rect.right
                    or i.rect.left < self.player1.rect.right < i.rect.right):
                # Jumping on projectiles
                if 0 < self.player1.rect.bottom - i.rect.top < 10:
                    self.player1.rect.bottom = i.rect.top
                    self.player1.y_velocity = -800
                    self.score += 10  # points
                    self.dead_enemies.add(i)
                    self.projectiles.remove(i)
        collisions = pygame.sprite.spritecollide(self.player1,
                                                 self.projectiles, False)
        if len(collisions) > 0:
            self.player1.player_killed()

    def door_collision(self):
        """Determines and handles door collisions"""
        collision = pygame.sprite.spritecollide(self.player1,
                                                self.doors, False)
        if len(collision) > 0:
            self.door_num = collision[0].lvl_num
        else:
            self.door_num = -1

    def paired_door_collision(self):
        # Paired door collisions
        collision = pygame.sprite.spritecollide(self.player1,
                                                self.pairedDoors, False)
        if len(collision) > 0:
            collision[0].transport(self.player1)

    def minidoor_collision(self):
        if self.miniDoor is None:
            return
        if (pygame.sprite.collide_rect(self.miniDoor, self.player1)
                and self.miniDoor.use_door(self.player1)):
            self.miniDoor = None
            globes.Globals.MINIGAME = mini.Minigame(self.player1, 0)
            globes.Globals.STATE = globes.Globals.MINIGAME

    def chair_collision(self):
        """Chair collision"""
        for chair in self.chairs:
            if chair.x_velocity != 0 or chair.y_velocity != 0:
                for i in pygame.sprite.spritecollide(chair, self.enemies,
                                                     False):
                    self.dead_enemies.add(i)
                    self.enemies.remove(i)

    def move_chair(self):
        """Called when soundwave is used"""
        for chair in self.chairs:
            if chair.sitting:
                if self.player1.facing == "left":
                    chair.changex_velocity += 50
                    #chair.x_velocity += 50
                    #chair.old += 50
                else:
                    chair.changex_velocity -= 50
                    #chair.x_velocity -= 50
                    #chair.old -= 50

    def trigger_detection(self):
        """Detects and handles triggers"""
        for i in self.triggers:
            if (pygame.sprite.collide_rect(self.player1, i) or
                    pygame.sprite.collide_rect(i, self.player1)):
                self.player1.x_velocity = -400
                self.player1.triggered = True
                self.enemies.add(i.enemy)
                self.triggers.remove(i)  # set trigger to be one-time only

    def build_level(self):
        """Builds the "static" components of the level"""
        temp = None
        for i in self.sprites:
            if i[0] == "P":
                self.plat = platform.Platform((int(i[1]), int(i[2])),
                                             (int(i[3]), int(i[4])))
                self.platforms.add(self.plat)
            elif i[0] == "B":
                self.plat = platform.Books((int(i[1]), int(i[2])), int(i[3]))
                self.platforms.add(self.plat)
            elif i[0] == "SP":
                self.spike = platform.Spikes((int(i[1]), int(i[2])), int(i[3]))
                self.spikes.add(self.spike)
            elif i[0] == "P2":
                self.plat = platform.Platform2((int(i[1]), int(i[2])),
                                               (int(i[3]), int(i[4])), i[5])
                self.platforms2.add(self.plat)
            elif i[0] == "D":
                self.door = items.Door((int(i[1]), int(i[2])),
                                       len(self.doors) + 1)
                self.doors.add(self.door)
            elif i[0] == "MB":
                temp = platform.MovingBook((int(i[1]), int(i[2])), int(i[3]),
                                           (int(i[4]), int(i[5])), (int(i[6]),
                                                                    int(i[7])))
                self.movingbooks.add(temp)
            elif i[0] == "S":
                self.player1.rect.bottomleft = ((int(i[1]), int(i[2])))
            elif i[0] == "C":
                chair = platform.Chair((int(i[1]), int(i[2])))
                self.chairs.add(chair)
            elif i[0] == "DoorPr":
                temp = items.PairedDoor((int(i[1]), int(i[2])), (int(i[3]),
                                                                 int(i[4])))
                self.pairedDoors.add(temp)
                temp = items.PairedDoor((int(i[3]), int(i[4])), (int(i[1]),
                                                                 int(i[2])))
                self.pairedDoors.add(temp)
            elif i[0] == "MiniDoor":
                temp = mini.MiniDoor(int(i[1]), (int(i[2]), int(i[3])))
                self.miniDoor = temp

        if globes.Globals.LVL_NUM == 3:
            self.endS = items.EndS((5000, 200))
        elif globes.Globals.LVL_NUM == 4:
            self.endS = items.EndS((4875, 220))
        else:
            self.endS = items.EndS((3050, 100))
        self.endRect = (self.endS.rect)

    def spawn_enemies(self):
        """Spawns enemies"""
        self.enemies.empty()
        self.shooters = []

        for i in self.sprites:
            if i[0] == "P":
                self.plat = platform.Platform((int(i[1]), int(i[2])),
                                             (int(i[3]), int(i[4])))
            elif i[0] == "B":
                self.plat = platform.Books((int(i[1]), int(i[2])), int(i[3]))
            elif i[0] == "PE":
                self.enemy = E.PlatformEnemy(self.plat)
                self.enemies.add(self.enemy)
            elif i[0] == "GE":
                self.enemy = E.GhostEnemy((int(i[1]), int(i[2])))
                self.enemies.add(self.enemy)
            elif i[0] == "TRFE":
                self.triggers.append(trigger.Trigger("FE", (int(i[1]),
                                                            int(i[2])),
                                                    (int(i[3]), int(i[4]))))
            elif i[0] == "TRGE":
                self.triggers.append(trigger.Trigger("GE", (int(i[1]),
                                                            int(i[2])),
                                                    (int(i[3]), int(i[4]))))
            elif i[0] == "TRPE":
                self.plat = platform.Platform((int(i[1]), int(i[2])),
                                             (int(i[3]), int(i[4])),
                                             (int(i[5]), int(i[6])))
                self.triggers.append(trigger.Trigger("PE", (-1, -1),
                                                     self.plat))
            elif i[0] == "SH":
                enemy = E.ShooterEnemy((int(i[1]), int(i[2])), float(i[3]))
                self.shooters.append(enemy)
            elif i[0] == "I":
                self.enemy = E.Spider((int(i[1]), int(i[2])))
                self.enemies.add(self.enemy)
            elif i[0] == "T":
                enemy = boss.Boss()
                self.bosses.add(enemy)
            elif i[0] == "BE":
                enemy = E.BookEnemy((int(i[1]), int(i[2])), i[3])
                self.enemies.add(enemy)

    def death(self):
        """Handles the player death"""
        self.player1.killed = False  # reset killed
        self.player1.onmp = False
        self.lives -= 1  # decrease lives by 1
        if self.lives < 0:  # if lives are less than 0: GAME OVER
            globes.Globals.GAME = None
            globes.stop_music()
            globes.Globals.STATE = \
                gameover.GameOver(self.score, 0, self.lives)
        #else:
            #self.spawn_enemies()  # respawn enemies
        self.initialize_lvl(0)
        for door in self.doors:  # put player in front of door of curr level
            if door.lvl_num == globes.Globals.LVL_NUM:
                self.player1.rect.bottomleft = door.rect.bottomleft
        self.player1.x_velocity, self.player1.y_velocity = 0, 0

    def level_complete(self):
        """Handles level completion"""
        if globes.Globals.LVL_NUM == len(level.LVL_FILES) - 1:
            globes.Globals.GAME = None
            globes.stop_music()
            globes.Globals.STATE = gameover.GameOver(self.score,
                                                     self.timeremaining,
                                                     self.lives)
        else:
            if globes.Globals.LVL_NUM == globes.Globals.LVLS_UNLOCKED:
                globes.Globals.LVLS_UNLOCKED += 1
            if self.timeremaining >= 0:
                self.score += self.timeremaining
            self.initialize_lvl(0)
            for door in self.doors:
                if door.lvl_num == globes.Globals.LVL_NUM:
                    self.player1.rect.bottomleft = door.rect.bottomleft
            self.player1.x_velocity, self.player1.y_velocity = 0, 0

    def enemy_deaths(self, time):
        """Enacts enemy death sequence"""
        for i in self.dead_enemies:
            if i.rect.top > globes.Globals.CAMERA.world.realheight:
                self.dead_enemies.remove(i)
            else:
                i.rect.y += 500 * time

    def update_complete(self, time):
        """Is called when end level sequence is initiated
        Moves Mark and endS"""
        self.mark.update(time)
        if self.mark.rect.left - self.endS.rect.right < 10:
            self.endS.rect.right = self.mark.rect.left
            self.endS.rect.top = self.mark.rect.top + \
                self.mark.rect.height / 2
        if self.mark.time >= items.Twain.CYCLE:
            # Voice over complete, restore music volume
            if not globes.Globals.MUTE:
                globes.Globals.SOUND.set_volume(globes.Globals.VOLUME)
            self.mark = None
            self.level_complete()

    def draw_web(self, enemy):
        sprite = pygame.sprite.Sprite()
        width = 1
        height = max(enemy.rect.top - enemy.pos[1], 0)
        sprite.rect = pygame.Rect(enemy.pos[0] + enemy.rect.width / 2 - 1,
                                  enemy.pos[1], width, height)
        surface = pygame.Surface((width, height))
        surface.fill(globes.Globals.WHITE)
        #surface.set_colorkey(globes.Globals.WHITE)
        sprite.image = surface
        globes.Globals.SCREEN.blit(sprite.image,
                                   globes.Globals.CAMERA.apply(sprite))
