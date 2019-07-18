import state
import pygame
import globes
import introduction


class Hack(state.State):  # Hack for levelOneCutscene integration.

    def __init__(self):
        state.State.__init__(self)
        mif = "imgs/marktwain.png"
        biftwo = "bg/background2.png"
        sif = "imgs/S.png"
        self.backgroundtwo = pygame.image.load(biftwo).convert()
        self.mt = pygame.image.load(mif).convert()
        key = self.mt.get_at((0, 0))
        self.mt.set_colorkey(key)
        self.st = pygame.image.load(sif).convert_alpha()
        self.mtscaled = pygame.transform.scale(self.mt, (16, 30))
        self.stscaled = pygame.transform.scale(self.st, (3, 4))
        self.mtflipped = pygame.transform.flip(self.mtscaled, True, False)
        self.x = 600
        self.y = 160
        self.z = 0
        self.clock = pygame.time.Clock()
        self.speed = 250

    def render(self):
        globes.Globals.SCREEN.blit(self.backgroundtwo, (0, 0))
        globes.Globals.SCREEN.blit(self.mt, (self.x, self.y))

        milli = self.clock.tick()
        seconds = milli / 1000.
        dm = seconds * self.speed

        if self.x >= 320:
            self.x -= dm
            globes.Globals.SCREEN.blit(self.st, (300, 315))

        if self.x < 320:
            self.x -= 0
            globes.Globals.SCREEN.blit(self.mt, (self.x, self.y))
            globes.Globals.SCREEN.blit(self.st, (self.x - 10, self.y + 200))
            self.x -= dm / 2
            self.y -= dm
        if self.y < -274 and self.x > 100:
            self.x += dm / 2
            globes.Globals.SCREEN.blit(self.mtflipped, (self.x + 150, self.z))
            globes.Globals.SCREEN.blit(self.stscaled, (self.x + 147,
                                                       self.z + 23))
            if self.z < 45:
                self.z += dm / 2

    def update(self, time):
        pass  # static state

    def event(self, event):
        if (event.type == pygame.KEYDOWN):
            globes.stop_music()
            globes.play_music("game.ogg")
            globes.Globals.GAME.initialize_lvl(0)
            globes.Globals.STATE = introduction.Intro(1)
