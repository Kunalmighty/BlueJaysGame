import pygame
import sys
from pygame.locals import *

bif = "bluejay.png"
biftwo = "background2.png"
sif = "S.png"
siftwo = "goldenS.png"

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
backgroundtwo = pygame.image.load(biftwo).convert()
bj = pygame.image.load(bif).convert_alpha()
st = pygame.image.load(sif).convert_alpha()
sttwo = pygame.image.load(siftwo).convert_alpha()
bjscaled = pygame.transform.scale(bj, (12, 24))
stscaled = pygame.transform.scale(st, (3, 4))
bjflipped = pygame.transform.flip(bjscaled, True, False)

x = 430
y = 25
z = 300
a = 400
clock = pygame.time.Clock()
speed = 250

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(backgroundtwo, (0, 0))
        
    milli = clock.tick()
    seconds = milli/1000.
    dm = seconds*speed

    if x >= 340:
       y -= dm
       x -= dm/2
       screen.blit(stscaled, (x+7, y+3))
       screen.blit(bjscaled, (x,y))

    if x < 340 and x > 309:
        x -= dm/14
        screen.blit(bj, (x, y))
        screen.blit(st, (x-12, y+35))
        y += dm
        
    if x < 309 and x > 300:
       screen.blit(bj, (x, y))
       screen.blit(st,(x-12, y+35))
       y -= dm
       x -= dm
       screen.blit(bj, (x, y))
       screen.blit(sttwo, (306, 313))
       
    if x < 300:
       x -= dm
       y -= dm
       screen.blit(bj, (x, y))
       screen.blit(sttwo, (306, 313))
        

    pygame.display.update()
