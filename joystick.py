import pygame as PY
import pygame.event as EV
import globes as G
import state
import options


class Joystick(state.State):

    BGS = None
    TEXT = None
    PROMPTS = None
    EVENTS = None

    def __init__(self):
        state.State.__init__(self)
        if Joystick.BGS is None:
            self.build_bg()
            self.prompt_init()
        self.sequence = -1  # set up sequence up, down, left, right,
                           # space, escape
        self.time = 0

    def render(self):
        if self.sequence == -1 or self.sequence == 0:
            G.Globals.SCREEN.blit(Joystick.BGS[0], (0, 0))
        else:
            G.Globals.SCREEN.blit(Joystick.BGS[1], (0, 0))

        if not G.Globals.CONTROLLER:
            G.Globals.SCREEN.blit(Joystick.TEXT[1], (610, 67))
            return
        G.Globals.SCREEN.blit(Joystick.TEXT[0], (610, 67))
        if self.sequence == -1:
            return

        G.Globals.SCREEN.blit(Joystick.PROMPTS[self.sequence], (270, 117))

    def update(self, dt):
        if G.Globals.CONTROLLER and self.sequence == -1:
            self.time += dt
        if G.Globals.CONTROLLER and self.sequence == -1 and self.time >= 1.0:
            self.sequence = 0
            self.time = 0

    def event(self, event):
        if event.type == PY.KEYDOWN:
            if event.key == PY.K_ESCAPE and self.sequence != 11:
                if (self.sequence != 0 and self.sequence !=
                        (len(Joystick.PROMPTS) - 1)):
                    self.sequence = -1
                    G.Globals.CONTROLLER = False
                elif self.sequence == (len(Joystick.PROMPTS) - 1):
                    self.sequence = -1
                G.Globals.STATE = options.Options(True, 1)
            if ((event.key == PY.K_RETURN or event.key == PY.K_SPACE) and
                    (self.sequence < 0 or self.sequence > 11)):
                G.Globals.CONTROLLER = not G.Globals.CONTROLLER
                if G.Globals.CONTROLLER:
                    PY.joystick.init()
                    G.Globals.JOYSTICK = PY.joystick.Joystick(0)
                    G.Globals.JOYSTICK.init()
                    self.event_maps_init()

        if (self.sequence < 12 and self.event_validator(event)):
            G.Globals.EVENTS[self.sequence] = event
            self.sequence += 1
        if (self.sequence >= 12 and self.new_event_validator(event)):
            G.Globals.EVENT_MAP[self.sequence % 12] = event
            self.sequence += 1
            if self.sequence >= 24:
                self.sequence = -1
                G.Globals.STATE = options.Options(True, 1)

    def event_validator(self, event):
        if self.sequence < 0 or self.sequence > 23:
            return False
        elif self.sequence == 0:
            if event.type == PY.KEYDOWN and event.key == PY.K_UP:
                return True
        elif self.sequence == 1:
            if event.type == PY.KEYUP and event.key == PY.K_UP:
                return True
        elif self.sequence == 2:
            if event.type == PY.KEYDOWN and event.key == PY.K_DOWN:
                return True
        elif self.sequence == 3:
            if event.type == PY.KEYUP and event.key == PY.K_DOWN:
                return True
        elif self.sequence == 4:
            if event.type == PY.KEYDOWN and event.key == PY.K_LEFT:
                return True
        elif self.sequence == 5:
            if event.type == PY.KEYUP and event.key == PY.K_LEFT:
                return True
        elif self.sequence == 6:
            if event.type == PY.KEYDOWN and event.key == PY.K_RIGHT:
                return True
        elif self.sequence == 7:
            if event.type == PY.KEYUP and event.key == PY.K_RIGHT:
                return True
        elif self.sequence == 8:
            if event.type == PY.KEYDOWN and event.key == PY.K_SPACE:
                return True
        elif self.sequence == 9:
            if event.type == PY.KEYDOWN and event.key == PY.K_RETURN:
                return True
        elif self.sequence == 10:
            if event.type == PY.KEYDOWN and event.key == PY.K_m:
                return True
        elif self.sequence == 11:
            if event.type == PY.KEYDOWN and event.key == PY.K_ESCAPE:
                return True

        return False

    def new_event_validator(self, event):
        if self.sequence == 12:  # up motion
            if event.type == PY.JOYHATMOTION and event.value == (0, 1):
                return True
            elif (event.type == PY.JOYAXISMOTION and
                  G.significant_magnitude(event.value)
                  and event.value < 0 and event.axis == 1):
                return True
        elif self.sequence == 13:  # up release
            if event.type == PY.JOYHATMOTION and event.value == (0, 0):
                return True
            elif (event.type == PY.JOYAXISMOTION and event.axis == 1 and not
                  G.significant_magnitude(event.value) and event.value < 0):
                return True
        elif self.sequence == 14:  # down motion:
            if event.type == PY.JOYHATMOTION and event.value == (0, -1):
                return True
            elif (event.type == PY.JOYAXISMOTION and event.value > 0 and
                  event.axis == 1 and G.significant_magnitude(event.value)):
                return True
        elif self.sequence == 15:  # down release:
            if event.type == PY.JOYHATMOTION and event.value == (0, 0):
                return True
            elif (event.type == PY.JOYAXISMOTION and event.axis == 1 and not
                  G.significant_magnitude(event.value) and event.value > 0):
                return True
        elif self.sequence == 16:  # left motion
            if event.type == PY.JOYHATMOTION and event.value == (1, 0):
                return True
            elif (event.type == PY.JOYAXISMOTION and event.axis == 0 and
                  event.value < 0 and G.significant_magnitude(event.value)):
                return True
        elif self.sequence == 17:  # left release:
            if event.type == PY.JOYHATMOTION and event.value == (0, 0):
                return True
            elif (event.type == PY.JOYAXISMOTION and event.axis == 0 and
                  not G.significant_magnitude(event.value)
                  and event.value < 0):
                return True
        elif self.sequence == 18:  # right motion
            if event.type == PY.JOYHATMOTION and event.value == (-1, 0):
                return True
            elif (event.type == PY.JOYAXISMOTION and event.axis == 0 and
                  event.value > 0 and
                  G.significant_magnitude(event.value)):
                return True
        elif self.sequence == 19:  # right release:
            if event.type == PY.JOYHATMOTION and event.value == (0, 0):
                return True
            elif (event.type == PY.JOYAXISMOTION and event.axis == 0 and not
                  G.significant_magnitude(event.value)
                  and event.value > 0):
                return True
        elif (self.sequence == 20 or self.sequence == 21 or self.sequence ==
                22 or self.sequence == 23):  # space, return, mute, escape
            if event.type == PY.JOYBUTTONDOWN:
                return True

        return False

    def event_maps_init(self):
        G.Globals.EVENT_MAP = []
        G.Globals.EVENTS = []
        for count in range(len(Joystick.PROMPTS) / 2):
            G.Globals.EVENT_MAP.append(None)
            G.Globals.EVENTS.append(None)

    def build_bg(self):
        Joystick.BGS = []
        Joystick.BGS.append(PY.image.load("bg/titlescreen.png").convert())
        Joystick.BGS.append(Joystick.BGS[0])

        font = PY.font.Font(None, 35)
        surf = font.render("Use USB game controller?", True, G.BLACK)
        Joystick.BGS[0].blit(surf, (250, 67))

        Joystick.TEXT = []
        Joystick.TEXT.append(font.render("Yes", True, G.BLACK))
        Joystick.TEXT.append(font.render("No", True, G.BLACK))

    def prompt_init(self):
        font = PY.font.Font(None, 35)
        Joystick.PROMPTS = []
        words = ['Press and hold the up arrow',
                 'Release the up arrow',
                 'Press and hold the down arrow',
                 'Release the down arrow',
                 'Press and hold the left arrow',
                 'Release the left arrow',
                 'Press and hold the right arrow',
                 'Release the right arrow',
                 'Press the spacebar',
                 'Press enter',
                 "Press the 'm' key",
                 'Press the escape key']

        for text in words:
            surf = font.render(text, True, G.BLACK)
            Joystick.PROMPTS.append(surf)

        words = ['Press and hold the desired up movement.',
                 'Release the desired up movement control.',
                 'Press and hold the desired down movement.',
                 'Release the desired down movement.',
                 'Press and hold the desired left movement.',
                 'Release the desired left movement control.',
                 'Press and hold the desired right movement.',
                 'Release the desired right movement.',
                 'Press the desired spacebar equivalent.',
                 'Press the desired enter equivalent.',
                 'Press the desired mute button.',
                 'Press the desired escape key equivalent']

        for text in words:
            surf = font.render(text, True, G.BLACK)
            Joystick.PROMPTS.append(surf)
        return
