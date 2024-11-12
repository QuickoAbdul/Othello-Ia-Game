import pygame
from pygame.locals import *

pygame.init()

fenetre = pygame.display.set_mode((640, 480))
fond = pygame.image.load("background.jpg").convert()
perso = pygame.image.load("Perso.png").convert_alpha() # convert_alpha pour rendre le png invisible autour du perso
fenetre.blit(fond,(0,0)) # on colle le fond sur la fenetre
fenetre.blit(perso, (270,380)) # on colle le perso au centre comme position 
continuer = True
while continuer :
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False

    pygame.display.update()
pygame.quit()