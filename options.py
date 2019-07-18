""" #EmbraceTheS's options menu state. """

import state
import menu
import globes
import pygame
import joystick
import volume


class Options(state.State):
    """ Option menu state with the options to clear high scores, and
        adjust brightness/volume (not yet implemented) """

    TEXT = []
    BACKGROUND = None
    LEFT_MARGIN = None
    HEIGHTS = None

    def __init__(self, sound=False, option=0):
        state.State.__init__(self)
        if not sound:
            globes.play_music("title.ogg")
        if (Options.BACKGROUND is None):
            Options.BACKGROUND = pygame.image.load("bg/titlescreen.png")\
                .convert()
        self.option = option
        self.blink = 0  # cycle through 0-9, display if < 7
        self.confirmation = False  # if asking for action confirmation
        self.confirmed = 0  # 0: no, 1: yes
        if (len(Options.TEXT) == 0):
            Options.TEXT = [globes.Globals.FONT.render("Clear High Scores",
                                                       True, globes.BLACK),
                            globes.Globals.FONT.render("Setup Joystick",
                                                       True, globes.BLACK),
                            globes.Globals.FONT.render("Volume & Brightness",
                                                       True, globes.BLACK),
                            globes.Globals.FONT.render("Return to Menu",
                                                       True, globes.BLACK)]
        if Options.LEFT_MARGIN is None:
            Options.LEFT_MARGIN = 2 * globes.Globals.WIDTH / 3
        if Options.HEIGHTS is None:
            Options.HEIGHTS = [
                (globes.Globals.HEIGHT / 2 - globes.Globals.HEIGHT / 8),
                globes.Globals.HEIGHT / 2 - globes.Globals.HEIGHT / 16,
                globes.Globals.HEIGHT / 2,
                globes.Globals.HEIGHT / 2 + globes.Globals.HEIGHT / 16,
                (globes.Globals.HEIGHT / 2 + globes.Globals.HEIGHT / 8)
            ]

    def render(self):
        globes.Globals.SCREEN.blit(Options.BACKGROUND, (0, 0))

        if not self.confirmation:
            for i in range(4):
                if ((not (self.option == i)) or self.blink < 7):
                    globes.Globals.SCREEN.blit(Options.TEXT[i],
                                               (Options.LEFT_MARGIN,
                                                Options.HEIGHTS[i]))
        else:
            surf = globes.Globals.FONT.render("Are you absolutely certain " +
                                              "you want to erase", True,
                                              globes.BLACK)
            globes.Globals.SCREEN.blit(surf, (270, 70))
            surf = globes.Globals.FONT.render("your legendary legacy?", True,
                                              globes.BLACK)
            globes.Globals.SCREEN.blit(surf, (370, 95))
            if self.blink < 7 or not self.confirmed == 1:
                surf = globes.Globals.FONT.render("Yes", True,
                                                  globes.BLACK)
                globes.Globals.SCREEN.blit(surf, (430, 130))
            if self.blink < 7 or not self.confirmed == 0:
                surf = globes.Globals.FONT.render("No", True,
                                                  globes.BLACK)
                globes.Globals.SCREEN.blit(surf, (530, 130))

    def update(self, time):
        self.blink = (self.blink + 1) % 10

    def event(self, event):
        if self.confirmation:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.confirmed = (self.confirmed - 1) % 2
                elif event.key == pygame.K_RIGHT:
                    self.confirmed = (self.confirmed + 1) % 2
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if self.confirmed:
                        globes.Globals.HIGHSCORES.clear_file()
                        self.confirmation = False
                    else:
                        self.confirmation = False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                globes.Globals.STATE = menu.Menu(True)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.option = (self.option - 1) % 4
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.option = (self.option + 1) % 4

            if event.type == pygame.KEYDOWN and \
                    (event.key == pygame.K_SPACE or
                     event.key == pygame.K_RETURN):
                if self.option == 0:
                    self.confirmation = True
                elif self.option == 1:
                    globes.Globals.STATE = joystick.Joystick()
                elif self.option == 2:
                    globes.Globals.STATE = volume.Volume(True)
                if self.option == 3:
                    globes.Globals.STATE = menu.Menu(True)
