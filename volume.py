""" #EmbraceTheS's options menu state. """

import state
import options
import globes as G
import pygame
import soundwave
import game
import enemy
import player
import items


class Volume(state.State):
    """ Volume menu state with the option to change volume """

    BACKGROUND = None
    NOTCH = None
    STEP = 0.1

    def __init__(self, sound=False):
        state.State.__init__(self)
        if not sound:
            G.play_music("title.ogg")
        if (Volume.BACKGROUND is None):
            self.build_bg()
            Volume.NOTCH = pygame.image.load("bg/notch.png")\
                .convert_alpha()
        self.option = True  # True for volume, False for brightness

    def render(self):
        G.Globals.SCREEN.blit(Volume.BACKGROUND, (0, 0))
        G.Globals.SCREEN.blit(Volume.NOTCH, (537 + 200 * G.Globals.VOLUME,
                                             233))
        G.Globals.SCREEN.blit(Volume.NOTCH, (537 + 200 * G.Globals.BRIGHTNESS,
                                             313))

    def update(self, time):
        pass

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                G.Globals.STATE = options.Options(True)
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.option = not self.option
            elif event.key == pygame.K_LEFT:
                if self.option:
                    self.change_volume(-Volume.STEP)
                else:
                    self.change_brightness(-Volume.STEP)
            elif event.key == pygame.K_RIGHT:
                if self.option:
                    self.change_volume(Volume.STEP)
                else:
                    self.change_brightness(Volume.STEP)

    def build_bg(self):
        # G.Globals.FONT is size 30
        font = pygame.font.Font(None, 35)
        Volume.BACKGROUND = pygame.image.load("bg/titlescreen.png")\
            .convert()
        surf = pygame.image.load("bg/bar.png").convert_alpha()
        Volume.BACKGROUND.blit(surf, (532, 230))
        Volume.BACKGROUND.blit(surf, (532, 310))
        surf = font.render("Brightness", True, G.BLACK)
        Volume.BACKGROUND.blit(surf, (532, 280))
        surf = font.render("Volume", True, G.BLACK)
        Volume.BACKGROUND.blit(surf, (532, 165))
        surf = G.Globals.FONT.render("Hit 'm' to mute/unmute",
                                     True, G.BLACK)
        Volume.BACKGROUND.blit(surf, (532, 200))

    def change_volume(self, change):
        if ((change < 0 and G.Globals.VOLUME <= 0) or (change > 0 and
                                                       G.Globals.VOLUME
                                                       >= 1)):
            return

        G.Globals.VOLUME += change
        set_volume_levels()

    def change_brightness(self, change):
        if ((change < 0 and G.Globals.BRIGHTNESS <= 0) or (change > 0 and
                                                           G.Globals.BRIGHTNESS
                                                           >= 1)):
            return

        G.Globals.BRIGHTNESS += change
        pygame.display.set_gamma(G.Globals.BRIGHTNESS,
                                 G.Globals.BRIGHTNESS,
                                 G.Globals.BRIGHTNESS)


def set_volume_levels():
    if G.Globals.MUTE:
        level = 0
    else:
        level = G.Globals.VOLUME

    G.Globals.SOUND.set_volume(level)
    if soundwave.Soundwave.SOUND is not None:
        soundwave.Soundwave.SOUND.set_volume(level)
    if game.Game.ENEMY_BOUNCE is not None:
        game.Game.ENEMY_BOUNCE.set_volume(level)
    if game.Game.EVIL_LAUGH is not None:
        game.Game.EVIL_LAUGH.set_volume(level)
    if player.Player.WALLSOUND is not None:
        player.Player.WALLSOUND.set_volume(level)
    if items.Airplane.SOUND is not None:
        items.Airplane.SOUND.set_volume(level)
#    items.Twain.SOUND.set_volume(level)
