""" Score state modularization """


import state
import pygame
import globes
import menu


class Score(state.State):
    """ Score state: high score display """

    BACKGROUND = None

    def __init__(self, music=False):
        state.State.__init__(self)

        if Score.BACKGROUND is None:
            Score.BACKGROUND = pygame.image.load("bg/scroll.png").convert()
            highscore = pygame.image.load("imgs/highscore.png").convert_alpha()
            Score.BACKGROUND.blit(highscore, (0, 0))
        if not music:
            globes.play_music("highscore.ogg")
        globes.Globals.SCREEN.fill(pygame.color.Color("black"))

        self.blit_scores()

    def render(self):
        pass  # static state

    def update(self, time):
        pass  # static state

    def event(self, event):
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or \
           (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
           (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
            globes.stop_music()
            globes.Globals.STATE = menu.Menu()

    def blit_scores(self):
        font = pygame.font.Font(None, 40)
        entry = ''
        globes.Globals.SCREEN.blit(Score.BACKGROUND, (0, 0))
        y_lvl = 150
        if globes.Globals.HIGHSCORES.get_length() > 9:
            y_lvl -= 15

        for i in range(0, globes.Globals.HIGHSCORES.get_length()):
            entry = globes.Globals.HIGHSCORES.entry_to_str(i)
            surf = font.render(entry, True, globes.Globals.BLACK)
            globes.Globals.SCREEN.blit(surf,
                                       (globes.hcenter(surf) - 10, y_lvl))
            y_lvl += surf.get_height() + 10
