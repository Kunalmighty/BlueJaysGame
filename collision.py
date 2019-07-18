import pygame
import globes


def horizontal_collision(self):
    # Horizontal Platform Collision
    if globes.Globals.GAME is None:
        return
    platforms = globes.Globals.GAME.platforms
    movingbooks = globes.Globals.GAME.movingbooks
    platforms2 = globes.Globals.GAME.platforms2
    chairs = globes.Globals.GAME.chairs

    collisions = pygame.sprite.spritecollide(self, platforms, False)
    num_collisions = len(collisions)
    if num_collisions > 0:
        if self.x_velocity > 0:
            self.rect.right = collisions[0].rect.left - 1
            self.x_velocity = 0
        elif self.x_velocity < 0:
            self.rect.left = collisions[0].rect.right + 1
            self.x_velocity = 0
    collisions = pygame.sprite.spritecollide(self, movingbooks, False)
    num_collisions = len(collisions)
    if num_collisions > 0:
        if self.rect.right < collisions[0].rect.centerx:
            self.rect.right = collisions[0].rect.left - 1
            self.x_velocity = 0
        elif self.rect.left > collisions[0].rect.centerx:
            self.rect.left = collisions[0].rect.right + 1
            self.x_velocity = 0

    collisions = pygame.sprite.spritecollide(self, chairs, False)
    for chair in collisions:
        if pygame.sprite.collide_rect(self, chair) and \
                self.rect.bottom > chair.rect.centery and chair != self:
            if (self.x_velocity > 0 and self.rect.right <
                    chair.rect.centerx) or (self.rect.right <
                                            chair.rect.centerx
                                            and self.x_velocity < 0):
                self.rect.right = chair.rect.left - 1
                chair.changex_velocity += 10
                #chair.x_velocity += 10
                self.x_velocity = chair.x_velocity
            elif (self.x_velocity < 0 and self.rect.right >
                    chair.rect.centerx) or (self.rect.right >
                                            chair.rect.centerx and
                                            self.x_velocity > 0):
                self.rect.left = chair.rect.right + 1
                chair.changex_velocity -= 10
                #chair.x_velocity -= 10
                self.x_velocity = chair.x_velocity

    collisions = pygame.sprite.spritecollide(self, platforms2, False)
    for i in collisions:
        if self.x_velocity > 0 and i.side == "l" \
                and self.rect.right < i.rect.left + 15:
            self.rect.right = i.rect.left - 1
            self.x_velocity = 0
        elif self.x_velocity < 0 and i.side == "r" \
                and self.rect.left > i.rect.right - 15:
            self.rect.left = i.rect.right + 1
            self.x_velocity = 0


def vertical_collision(self):
    # Vertical Platform Collision
    if globes.Globals.GAME is None:
        return
    platforms = globes.Globals.GAME.platforms
    movingbooks = globes.Globals.GAME.movingbooks
    platforms2 = globes.Globals.GAME.platforms2
    chairs = globes.Globals.GAME.chairs

    collisions = pygame.sprite.spritecollide(self, platforms, False)
    num_collisions = len(collisions)
    if num_collisions > 0:
        if self.y_velocity > 0:
            self.rect.bottom = collisions[0].rect.top - 1
            self.y_velocity = 0
            self.onground = True
        elif self.y_velocity < 0:
            self.rect.top = collisions[0].rect.bottom + 1
            self.y_velocity = 0
    else:
        self.onground = False

    collisions = pygame.sprite.spritecollide(self, platforms2, False)
    for i in collisions:
        if self.rect.bottom < i.rect.top + 15 \
                and self.y_velocity > 0:
            self.rect.bottom = i.rect.top - 1
            self.y_velocity = 0
            self.onground = True

    # Adjust position to account for moving platforms
    collisions = pygame.sprite.spritecollide(self, movingbooks, False)
    if len(collisions) > 0:
        if self.y_velocity > 0:
            self.rect.bottom = collisions[0].rect.top
            self.onground = True
        elif self.y_velocity < 0:
            self.rect.top = collisions[0].rect.bottom + 1
        self.y_velocity = 0
    for i in collisions:
        self.rect.x += i.x_velocity * self.dtime
        self.rect.y += i.y_velocity * self.dtime

    collisions = pygame.sprite.spritecollide(self, chairs, False)
    for i in collisions:
        if (i != self and self.rect.bottom > i.rect.centery):
            if self.y_velocity > 0:
                self.rect.bottom = i.rect.centery
                self.onground = True
            elif self.y_velocity < 0:
                self.rect.top = i.rect.bottom + 1
            self.y_velocity = 0
    #for i in collisions:
       # if i != self:
            if i.sitting:
                #temp = self.x_velocity
                self.x_velocity = i.x_velocity
                #if i.x_velocity - temp == 49 and \
                #        i.x_velocity % 100 > temp % 100:
                #    self.rect.x += 1
                #elif i.x_velocity - temp == -49 and \
                #        i.x_velocity % 100 < temp % 100:
                #    self.rect.x -= 1
                #if i.x_velocity > 0:
                #    self.x_velocity -= 1
                #elif i.x_velocity < 0:
                #    self.x_velocity +=1
            #self.rect.x += i.x_velocity * self.dtime
            self.rect.y += i.y_velocity * self.dtime
