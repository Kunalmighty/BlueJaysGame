import pygame
import globes
import state
import menu
import endgame


class GameOver(state.State):

    BACKGROUND = None
    LETTERS = None

    def __init__(self, score, timeremaining, lives):
        state.State.__init__(self)
        self.score = score + timeremaining
        if lives > 0:
            self.score += 50 * lives
        globes.Globals.SCREEN.fill(globes.Globals.BLACK)
        if GameOver.BACKGROUND is None:
            GameOver.BACKGROUND = pygame.image.load("imgs/highscore.png")\
                .convert()
        self.newHighscore = True

    def render(self):
        if not self.newHighscore:
            font = pygame.font.Font(None, 50)
            surf = font.render("GAME OVER", True, (255, 0, 0))
            globes.Globals.SCREEN.blit(surf, (globes.Globals.WIDTH / 2 -
                                              surf.get_width() / 2, 100))
            #globes.Globals.SCREEN.blit(self.BACKGROUND, (0, 0))

    def update(self, time):
        if globes.Globals.HIGHSCORES.should_add(self.score):
            globes.Globals.STATE = endgame.EndGame(self.score)
        else:
            self.newHighscore = False

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                globes.Globals.STATE = menu.Menu()
