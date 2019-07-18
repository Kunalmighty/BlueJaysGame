"""Title module"""

import menu
import pygame
import state
import globes


class Title(state.State):
    """Title state class - displays title screen"""
    FLYTIME = 5.0
    IMAGE = None

    def __init__(self):
        state.State.__init__(self)
        globes.play_music("title.ogg")
        self.color = pygame.color.Color("black")
        self.time = 0.25
        self.posx = 0
        self.posy = 0
        self.velocity = 0
        self.direction = 0  # (1 for down, -1 for up)
        self.width = 0
        self.height = 0
        if Title.IMAGE is None:
            Title.IMAGE = \
                pygame.image.load("bg/titlescreen.png").convert()
        globes.Globals.SCREEN.fill(pygame.color.Color("black"))

    def render(self):
        """Renders the title screen"""
        surf = globes.Globals.FONT.render("#EmbraceTheS",
                                          True, self.color)
        self.width, self.height = surf.get_size()
        globes.Globals.SCREEN.blit(Title.IMAGE, (0, 0))
        globes.Globals.SCREEN.blit(surf, (self.posx, self.posy))

    def update(self, time):
        """Updates the title screen title"""
        self.time += time
        if self.time < Title.FLYTIME:
            self.posx += (time / Title.FLYTIME) * \
                (5 * globes.Globals.WIDTH / 6 - self.width / 2)
            self.posy += (time / Title.FLYTIME) * \
                (globes.Globals.HEIGHT / 6 - self.height / 2)
        self.posy += self.velocity
        if self.time % 1 < .5:
            self.velocity += 15 * time
        else:
            self.velocity -= 15 * time

    def event(self, event):
        """Does something if an event occurs (escape, keydown)"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            globes.Globals.RUNNING = False
        elif event.type == pygame.KEYDOWN:
            globes.Globals.STATE = menu.Menu(True)
