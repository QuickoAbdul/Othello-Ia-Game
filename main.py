import pygame
from pygame.locals import *

pygame.init()

fenetre = pygame.display.set_mode((640, 480))

continuer = True
while continuer :
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False

pygame.quit()

