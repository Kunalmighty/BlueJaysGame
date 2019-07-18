import sys
import time
import pygame


FADE_IN_TIME = 5
FADE_OUT_TIME = 5
FADE_IN_EASING = lambda x: x  # Linear
FADE_OUT_EASING = lambda x: x  # Linear
PLAYING = True


pygame.init()
clock = pygame.time.Clock()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont('sans-serif', 20, True)
fps_font = pygame.font.SysFont('monospace', 20, True)

rendered_text1 = font.render("The public is sensitive to little things" +
                             " and they wouldn't have full confidence in" +
                             " a college",
                             True, (255, 255, 255))
rendered_text2 = font.render("        that didn't know how to spell the name" +
                             " John." +
                             "   - Mark Twain", True, (255, 255, 255))
text_rect = rendered_text1.get_rect(center=(width / 2, height / 2))

ST_FADEIN = 0
ST_FADEOUT = 1

state = ST_FADEIN
last_state_change = time.time()

while PLAYING:
    ## Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Exit the main loop
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            PLAYING = False

    ## Update the state
    state_time = time.time() - last_state_change

    if state == ST_FADEIN:
        if state_time >= FADE_IN_TIME:
            state = ST_FADEOUT
            #state_time = max(0, min(state_time - FADE_IN_TIME, 1))
            state_time -= FADE_IN_TIME
            last_state_change = time.time() - state_time

    elif state == ST_FADEOUT:
        if state_time >= FADE_OUT_TIME:
            state = ST_FADEIN
            #state_time = max(0, min(state_time - FADE_OUT_TIME, 1))
            state_time -= FADE_OUT_TIME
            last_state_change = time.time() - state_time

    else:
        raise ValueError()

    if state == ST_FADEIN:
        alpha = FADE_IN_EASING(1.0 * state_time / FADE_IN_TIME)
        rt = rendered_text1
    elif state == ST_FADEOUT:
        alpha = 1. - FADE_OUT_EASING(1.0 * state_time / FADE_OUT_TIME)
        rt = rendered_text2
    else:
        raise ValueError()

    surf2 = pygame.surface.Surface((text_rect.width, text_rect.height))
    surf2.set_alpha(255 * alpha)

    screen.fill((0, 0, 0))
    surf2.blit(rt, (0, 0))
    screen.blit(surf2, text_rect)

    fps = clock.get_fps()
    fpslabel = fps_font.render(str(int(fps)), True, (255, 255, 255))
    rec = fpslabel.get_rect(top=5, right=width - 5)

    pygame.display.flip()
    clock.tick(50)
##
##
