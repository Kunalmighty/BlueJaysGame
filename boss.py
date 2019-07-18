import pygame
import enemy
import globes
import collision
import random
import FinalCutscene


class Boss(pygame.sprite.Sprite):
    """Boss sprite class"""
    IMAGELEFT = None
    IMAGERIGHT = None
    IMAGEHITLEFT = None
    IMAGEHITRIGHT = None
    SOUND = None
#    CYCLE = 5.0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if Boss.IMAGELEFT is None:
            Boss.IMAGELEFT = pygame.image.load("imgs/marktwain.png"
                                               ).convert()
            Boss.IMAGERIGHT = pygame.image.load("imgs/marktwainflipped.png"
                                                ).convert()
            Boss.SOUND = pygame.mixer.Sound("audio/twainshort1.ogg")
            self.load_images()

        self.image = Boss.IMAGELEFT
        self.rect = self.image.get_rect()
        self.rect.topright = (800, 0)
        self.time = 0.0
        self.dtime = 0.0
        self.stop_num = 200
        self.x_velocity = 400
        self.y_velocity = 300
        self.lives = 3

        self.facing = "left"
        self.invincible = 0
        self.states = (7, 9, 10)
        self.count = 3
        self.state = 10
        self.fireball = 0
#        Boss.SOUND.play()

    def update(self, dtime=1):
        """Updates the Boss sprite"""
        self.dtime = dtime
        self.time += dtime
        self.update_position()
        self.player_collision()
        self.update_image()

    def update_position(self):
        """Updates the position of the sprite"""
        if self.stop_num > 0:
            self.stop_num -= 1
            return
        if self.state == 1:  # move down (right side)
            self.rect.y += self.y_velocity * self.dtime
            if self.rect.bottom >= 600:
                self.rect.bottom = 600
                self.state = 2
        elif self.state == 2:  # move left (bottom)
            self.rect.x -= self.x_velocity * self.dtime
            if self.rect.left <= 0:
                self.rect.left = 0
                self.state = 3
        elif self.state == 3:  # move up (left side)
            self.rect.y -= self.y_velocity * self.dtime
            if self.rect.top <= 0:
                self.rect.top = 0
                self.facing = "right"
                #self.shoot_fireball()
                #self.stop()
                #self.spawn_enemies()
                self.state = self.random_state()  # change
        elif self.state == 4:  # move down (left side)
            self.rect.y += self.y_velocity * self.dtime
            if self.rect.bottom >= 600:
                self.rect.bottom = 600
                self.state = 5
        elif self.state == 5:  # move right (bottom)
            self.rect.x += self.x_velocity * self.dtime
            if self.rect.right >= 800:
                self.rect.right = 800
                self.state = 6
        elif self.state == 6:  # move up (right side)
            self.rect.y -= self.y_velocity * self.dtime
            if self.rect.top <= 0:
                self.rect.top = 0
                self.facing = "left"
                #self.shoot_fireball()
                #self.stop()
                #self.spawn_enemies()
                self.state = self.random_state()  # change
        elif self.state == 7:  # move down and shoot fireballs
            self.rect.y += .5 * self.y_velocity * self.dtime
            self.tentative_shoot_fireball()
            if self.rect.bottom >= 600:
                self.state = 8
        elif self.state == 8:  # move up and shoot fireballs
            self.rect.y -= .5 * self.y_velocity * self.dtime
            self.tentative_shoot_fireball()
            if self.rect.top <= 0:
                self.state = self.random_state()
        elif self.state == 9:  # shoot a bunch of fireballs
            self.shoot_fireballs()
            if self.fireball == 11:
                self.fireball = 0
                self.state = self.random_state()
                self.stop(200)
        elif self.state == 10:  # spawn enemies
            self.state = self.random_state()
            if self.time < 4.0:
                self.state = self.random_fireball_state()
            self.spawn_enemies()

    def load_images(self):
        surf = pygame.image.load("imgs/marktwain.png").convert()
        surf2 = pygame.image.load("imgs/marktwainflipped.png").convert()
        surf3 = pygame.image.load("imgs/marktwainhit.png").convert()
        surf4 = pygame.image.load("imgs/marktwainhitflipped.png").convert()

        surface = pygame.Surface((150, 274)).convert()
        surface2 = pygame.Surface((150, 274)).convert()
        surface3 = pygame.Surface((150, 274)).convert()
        surface4 = pygame.Surface((150, 274)).convert()
        for i in range(1):
            surface.blit(surf, (0, 0), (i * 150, 0, 150, 274))
            surface2.blit(surf2, (0, 0), (i * 150, 0, 150, 274))
            surface3.blit(surf3, (0, 0), (i * 150, 0, 150, 274))
            surface4.blit(surf4, (0, 0), (i * 150, 0, 150, 274))
        key = surface.get_at((0, 0))
        key2 = surface2.get_at((0, 0))
        key3 = surface3.get_at((0, 0))
        key4 = surface4.get_at((0, 0))
        surface.set_colorkey(key)
        surface2.set_colorkey(key2)
        surface3.set_colorkey(key3)
        surface4.set_colorkey(key4)
        Boss.IMAGELEFT = surface
        Boss.IMAGERIGHT = surface2
        Boss.IMAGEHITLEFT = surface3
        Boss.IMAGEHITRIGHT = surface4

    def stop(self, num=500):
        self.stop_num = num

    def spawn_enemies(self):
        enemy1 = enemy.BookEnemy((0, 0), "right")
        globes.Globals.GAME.enemies.add(enemy1)
#        enemy1 = enemy.BookEnemy((150, 0), "right")
#        globes.Globals.GAME.enemies.add(enemy1)
        enemy1 = enemy.BookEnemy((300, 0), "left")
        globes.Globals.GAME.enemies.add(enemy1)
#        enemy1 = enemy.BookEnemy((450, 0), "left")
#        globes.Globals.GAME.enemies.add(enemy1)
        enemy1 = enemy.BookEnemy((600, 0), "left")
        globes.Globals.GAME.enemies.add(enemy1)
        self.stop(700)

    def stun_enemy(self, num=80):
        self.stop(num / 8)

    def hit(self):
        self.lives -= 1
        if self.lives == 0:
            globes.Globals.STATE = FinalCutscene.HackFinal()
        self.invincible = 200

    def shoot_fireball(self, x_speed=200, y_velocity=-11):
        if self.facing == "right":
            fireball = Fireball((self.rect.right - 10, self.rect.top + 40),
                                x_speed, y_velocity)
        elif self.facing == "left":
            fireball = Fireball((self.rect.left + 10, self.rect.top + 40),
                                -x_speed, y_velocity)
        globes.Globals.GAME.fireballs.add(fireball)

    def tentative_shoot_fireball(self):
        if int(self.time * 100) % 100 % 50 == 0:
            self.shoot_fireball(200, -51)

    def shoot_fireballs(self):
        fire = int(self.time * 100) % 100 % 25 == 0
        if fire:
            self.fireball += 1
            x, y = 70 + self.fireball * 15, -31 - 14 * self.fireball
            self.shoot_fireball(x, y)
        #if self.fireball == 1 and fire:
        #    self.shoot_fireball(10, 10)
        #elif self.fireball == 2 and fire:
        #    self.shoot_fireball(30, 5)
        #elif self.fireball == 3 and fire:
        #    self.shoot_fireball(50, 0)
        #elif self.fireball == 4 and fire:
        #    self.shoot_fireball(70, -5)
        #elif self.fireball

    def player_collision(self):
        player1 = globes.Globals.GAME.player1
        if ((self.rect.left + 15 < player1.rect.left < self.rect.right
                - 10 or self.rect.left + 15 < player1.rect.right <
                self.rect.right - 10) and
                pygame.sprite.collide_rect(self, player1)):
            if 0 < player1.rect.bottom - self.rect.top < 20 and \
                    self.invincible <= 0 and not player1.killed:
                self.hit()
                player1.rect.bottom = self.rect.top
                player1.y_velocity = -800
            elif self.invincible <= 0 and not player1.killed:
                player1.player_killed()

    def update_image(self):
        if self.invincible > 0:
            self.invincible -= 1
            if self.facing == "left":
                self.image = Boss.IMAGEHITLEFT
            else:
                self.image = Boss.IMAGEHITRIGHT
        else:
            if self.facing == "left":
                self.image = Boss.IMAGELEFT
            else:
                self.image = Boss.IMAGERIGHT

    def random_state(self):
        self.stop(100)
        self.count -= 1
        if self.count == 0:
            self.count = 3
            if self.image == Boss.IMAGERIGHT:
                return 4
            else:
                return 1
        num = random.randint(0, 2)
        return self.states[num]

    def random_fireball_state(self):
        self.count -= 1
        num = random.randint(0, 1)
        return self.states[num]


class Fireball(pygame.sprite.Sprite):
    """Fireball sprite class"""
    IMAGE = None
    SOUND = None
    MAXSPEEDY = 200
#    OSCILLATION = 0.5  # oscillation cycle

    def __init__(self, top_left, xvelocity=0, yvelocity=0):
        pygame.sprite.Sprite.__init__(self)
        if Fireball.IMAGE is None:
            Fireball.IMAGE = pygame.image.load("imgs/fireball.png").convert()
            Fireball.IMAGE.set_colorkey(Fireball.IMAGE.get_at((0, 0)))
            #Fireball.SOUND = pygame.mixer.Sound("audio/fireball.ogg")
        self.image = Fireball.IMAGE
        self.rect = self.image.get_rect()
        self.rect.topleft = top_left
        self.x_velocity = xvelocity
        self.y_velocity = yvelocity
        self.time = 0.0
        self.dir = 0
#        Fireball.SOUND.play()

    def update(self, dtime=1):
        """Updates the sprite"""
        self.time = self.time + dtime
        self.dtime = dtime

        self.rect.x += dtime * self.x_velocity
        collision.horizontal_collision(self)
        if self.x_velocity == 0:
            self.kill()

        if self.y_velocity < Fireball.MAXSPEEDY:
            self.y_velocity += 2
        self.rect.y += dtime * self.y_velocity
        if self.y_velocity > 0:
            self.rect.y += 2
        collision.vertical_collision(self)
        if self.y_velocity == 0:
            self.kill()

        if int(self.time * 100) % 100 % 4 == 0:
            self.turn(random.randint(4, 15))

        soundwaves = globes.Globals.GAME.soundwaves
        if len(pygame.sprite.spritecollide(self, soundwaves, False)) > 0:
            self.kill()

        player1 = globes.Globals.GAME.player1
        if pygame.sprite.collide_rect(self, player1):
            player1.player_killed()

        enemies = globes.Globals.GAME.enemies
        pygame.sprite.spritecollide(self, enemies, True)

    def turn(self, amount):
        oldCenter = self.rect.center
        self.dir += amount
        self.image = pygame.transform.rotate(Fireball.IMAGE, self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
