""" Modularization of Intro state object """


import pygame
import globes
import state


class Intro(state.State):
    """ Intro state displays backstory and instructional text """

    TEXTSCREENS = None
    HIT_ENTER = None
    BACKGROUND = None
    ARROWS = None

    def __init__(self, intro_id):
        state.State.__init__(self)

        if Intro.ARROWS is None:
            Intro.ARROWS = pygame.image.load("imgs/arrows.png").convert_alpha()
            Intro.BACKGROUND = pygame.image.load("bg/scroll.png").convert()

        if intro_id == 1:
            self.build_txt_scrns()
            self.num_screens = 3

        self.screen = 0

    def render(self):
        globes.Globals.SCREEN.blit(Intro.BACKGROUND, (0, 0))
        globes.Globals.SCREEN.blit(Intro.TEXTSCREENS[self.screen], (0, 0))
        globes.Globals.SCREEN.blit(Intro.HIT_ENTER, (0, 0))

    def update(self, delta_t=1):
        pass

    def event(self, event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or
                    (self.screen == (self.num_screens - 1) and
                     event.key != pygame.K_LEFT)):
                globes.Globals.STATE = globes.Globals.GAME
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or
                    event.key == pygame.K_SPACE):
                self.screen += 1
            elif ((event.key == pygame.K_LEFT or event.key == pygame.K_UP) and
                    self.screen > 0):
                self.screen -= 1

    def build_txt_scrns(self):
        """ Build text for first level introduction """
        Intro.TEXTSCREENS = []

        image = pygame.image.load("imgs/introtxt1.png").convert_alpha()
        image.blit(Intro.ARROWS, (535, 460), (30, 0, 30, 36))
        Intro.TEXTSCREENS.append(image)
        image = pygame.image.load("imgs/introtxt2.png").convert_alpha()
        image.blit(Intro.ARROWS, (256, 460), (0, 0, 30, 36))
        image.blit(Intro.ARROWS, (535, 460), (30, 0, 30, 36))
        Intro.TEXTSCREENS.append(image)
        image = pygame.image.load("imgs/introtxt3.png").convert_alpha()
        image.blit(Intro.ARROWS, (256, 460), (0, 0, 30, 36))
        Intro.TEXTSCREENS.append(image)

        Intro.HIT_ENTER = pygame.image.load("imgs/introtxt" +
                                            ".png").convert_alpha()
