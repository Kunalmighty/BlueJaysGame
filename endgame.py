""" Add-a-new-high-score state modularization. """


import pygame
import globes
import state
import score as S


class EndGame(state.State):
    """ #EmbraceTheS's interface for adding a new high score. """

    BACKGROUND = None
    LETTERS = None
    UNDERSCORE = None

    def __init__(self, score):
        state.State.__init__(self)
        self.font = pygame.font.Font(None, 50)
        globes.Globals.SCREEN.fill(globes.Globals.WHITE)
        globes.play_music("highscore.ogg")

        # Font variables
        self.blink = 0
        self.y_lvl = 200
        surf = self.font.render("WWWWWWWWWW", True, globes.Globals.BLACK)
        self.x_start = globes.hcenter(surf) - 5
        self.letter_width = int(surf.get_width() / 10)

        if EndGame.UNDERSCORE is None:
            EndGame.UNDERSCORE = self.font.render("_", True,
                                                  globes.Globals.BLACK)
        if EndGame.BACKGROUND is None:
            EndGame.BACKGROUND = pygame.image.load("bg/scroll.png").convert()
            highscore = pygame.image.load("imgs/highscore.png").convert_alpha()
            EndGame.BACKGROUND.blit(highscore, (0, 0))
        if EndGame.LETTERS is None:
            EndGame.LETTERS = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                               ' I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                               'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        self.score = int(score)
        # indices used to reference indices of LETTERS
        self.name_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # index (0-9) of letter in name being edited
        self.name_index = 0

    def render(self):
        """ Override State object's render method. """
        globes.Globals.SCREEN.blit(self.BACKGROUND, (0, 0))

        x_lvl = self.x_start
        for index in self.name_list:
            letter = self.font.render(EndGame.LETTERS[index], True,
                                      globes.Globals.BLACK)
            globes.Globals.SCREEN.blit(letter, (x_lvl, self.y_lvl))
            x_lvl += self.letter_width

        x_lvl = self.x_start + (self.name_index * self.letter_width)
        if (self.blink < 8):
            globes.Globals.SCREEN.blit(self.UNDERSCORE, (x_lvl, self.y_lvl))

    def update(self, time):
        """ Override State object's update method. """
        self.blink = (self.blink + 1) % 10

    def event(self, event):
        """ Override State object's event handler. """
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or
                    event.key == pygame.K_SPACE):  # save entry & change state
                name = ''
                for index in self.name_list:
                    if index == 9:
                        name += 'I'
                    else:
                        name += EndGame.LETTERS[index]
                globes.Globals.HIGHSCORES.add_score((name, self.score))
                globes.Globals.STATE = S.Score(True)
            self.update_name(event.key)

    def update_name(self, key):
        """ Change the name characters based on the key pressed. """
        if key == pygame.K_RIGHT:
            self.name_index = (self.name_index + 1) % 10
        elif key == pygame.K_LEFT:
            self.name_index = (self.name_index - 1) % 10
        elif key == pygame.K_UP:
            self.name_list[self.name_index] -= 1
            self.name_list[self.name_index] %= 27
        elif key == pygame.K_DOWN:
            self.name_list[self.name_index] += 1
            self.name_list[self.name_index] %= 27
