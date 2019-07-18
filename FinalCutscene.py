import state
import pygame
import globes
import introduction
import gameover


class HackFinal(state.State):  # Hack for FinalCutscene integration.

    def __init__(self):
        state.State.__init__(self)
        bif = "imgs/jumpleft1.png"
        biftwo = "bg/background2.png"
        sif = "imgs/S.png"
        siftwo = "imgs/goldenS.png"
        self.backgroundtwo = pygame.image.load(biftwo).convert()
        self.bj = pygame.image.load(bif).convert()
        key = self.bj.get_at((0, 0))
        self.bj.set_colorkey(key)
        self.st = pygame.image.load(sif).convert_alpha()
        self.sttwo = pygame.image.load(siftwo).convert_alpha()
        self.bjscaled = pygame.transform.scale(self.bj, (16, 30))
        self.stscaled = pygame.transform.scale(self.st, (3, 4))
        self.bjflipped = pygame.transform.flip(self.bjscaled, True, False)
        self.x = 430
        self.y = 25
        self.z = 0
        self.clock = pygame.time.Clock()
        self.speed = 250

    def render(self):
        globes.Globals.SCREEN.blit(self.backgroundtwo, (0, 0))

        milli = self.clock.tick()
        seconds = milli / 1000.
        dm = seconds * self.speed

        if self.x >= 340:
            self.y -= dm
            self.x -= dm / 2
            globes.Globals.SCREEN.blit(self.stscaled, (self.x + 7, self.y + 3))
            globes.Globals.SCREEN.blit(self.bjscaled, (self.x, self.y))

        if self.x < 340 and self.x > 309:
            self.x -= dm / 14
            globes.Globals.SCREEN.blit(self.bj, (self.x, self.y))
            globes.Globals.SCREEN.blit(self.st, (self.x - 12, self.y + 35))
            self.y += dm

        if self.x < 309 and self.x > 300:
            globes.Globals.SCREEN.blit(self.bj, (self.x, self.y))
            globes.Globals.SCREEN.blit(self.st, (self.x - 12, self.y + 35))
            self.y -= dm
            self.x -= dm
            globes.Globals.SCREEN.blit(self.bj, (self.x, self.y))
            globes.Globals.SCREEN.blit(self.sttwo, (306, 313))

        if self.x < 300:
            self.x -= dm
            self.y -= dm
            globes.Globals.SCREEN.blit(self.bj, (self.x, self.y))
            globes.Globals.SCREEN.blit(self.sttwo, (306, 313))

    def update(self, time):
        pass  # static state

    def event(self, event):
        if (event.type == pygame.KEYDOWN):
            globes.stop_music()
            globes.play_music("game.ogg")
            score = globes.Globals.GAME.score
            timeremaining = globes.Globals.GAME.timeremaining
            lives = globes.Globals.GAME.lives
            globes.Globals.STATE = gameover.GameOver(score,
                                                     timeremaining,
                                                     lives)
            globes.Globals.GAME.initialize_lvl(0)
