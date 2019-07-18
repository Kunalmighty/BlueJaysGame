""" #EmbraceTheS's main menu state.
    Interface to create/continue games, view high scores, navigate to
    options, or quit the game. """

import state
import score
import game
import options
import globes
import pygame
import cutscene1


class Menu(state.State):
    """ #EmbraceTheS's main menu state. See above for description. """

    TEXT = []
    BACKGROUND = None
    LEFT_MARGIN = None
    HEIGHTS = None

    def __init__(self, sound=False):
        """ @param sound True if title music is already playing """
        state.State.__init__(self)
        if not sound:
            globes.play_music("title.ogg")
        if (Menu.BACKGROUND is None):
            Menu.BACKGROUND = pygame.image.load("bg/titlescreen.png").convert()
        self.option = 0
        self.blink = 0  # cycle through 0-9, display if < 7
        if (len(Menu.TEXT) == 0):
            Menu.TEXT = [globes.Globals.FONT.render("New Game", True,
                                                    globes.BLACK),
                         globes.Globals.FONT.render("High Scores", True,
                                                    globes.BLACK),
                         globes.Globals.FONT.render("Options", True,
                                                    globes.BLACK),
                         globes.Globals.FONT.render("Quit", True,
                                                    globes.BLACK),
                         globes.Globals.FONT.render("Continue Game", True,
                                                    globes.BLACK)]
        if Menu.LEFT_MARGIN is None:
            Menu.LEFT_MARGIN = 2 * globes.Globals.WIDTH / 3
        if Menu.HEIGHTS is None:
            Menu.HEIGHTS = [
                (globes.Globals.HEIGHT / 2 - globes.Globals.HEIGHT / 8),
                (globes.Globals.HEIGHT / 2 - globes.Globals.HEIGHT / 16),
                (globes.Globals.HEIGHT / 2),
                (globes.Globals.HEIGHT / 2 + globes.Globals.HEIGHT / 16),
                (globes.Globals.HEIGHT / 2 - 3 * globes.Globals.HEIGHT / 16)
            ]
        self.num_options = 4
        if globes.Globals.GAME is not None:
            self.num_options = 5
            self.option = 4

    def render(self):
        globes.Globals.SCREEN.blit(Menu.BACKGROUND, (0, 0))
        for i in range(self.num_options):
            if ((not (self.option == i)) or self.blink < 7):
                globes.Globals.SCREEN.blit(Menu.TEXT[i], (Menu.LEFT_MARGIN,
                                           Menu.HEIGHTS[i]))

    def update(self, time):
        self.blink = (self.blink + 1) % 10

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            globes.Globals.RUNNING = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.option = (self.option - 1) % self.num_options
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.option = (self.option + 1) % self.num_options

        if event.type == pygame.KEYDOWN and \
                (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
            if self.option == 0:
                globes.stop_music()
                globes.play_music("angryTwain.ogg")
                globes.Globals.GAME = game.Game()
                globes.Globals.LVLS_UNLOCKED = 1
                globes.Globals.STATE = cutscene1.Hack()
            elif self.option == 1:
                globes.stop_music()
                globes.Globals.STATE = score.Score()
            elif self.option == 2:
                globes.Globals.STATE = options.Options(True)
            elif self.option == 3:
                globes.Globals.RUNNING = False
            elif self.option == 4:
                globes.stop_music()
                globes.play_music("game.ogg")
                if globes.Globals.MINIGAME is not None:
                    globes.Globals.STATE = globes.Globals.MINIGAME
                else:
                    globes.Globals.STATE = globes.Globals.GAME
