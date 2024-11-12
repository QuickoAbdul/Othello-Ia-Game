import pygame
from pygame.locals import *

pygame.init()
pygame.key.set_repeat(400, 30)

fenetre = pygame.display.set_mode((640, 480))
fond = pygame.image.load("background.jpg").convert()
perso = pygame.image.load("Perso.png").convert_alpha()
persoRect = perso.get_rect()
persoRect.topleft = (270,380)

fenetre.blit(fond,(0,0))
continuer = True
while continuer :
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        if event.type == KEYDOWN  :
                if event.key == K_LEFT :
                    if persoRect.left>=10 :
                        persoRect = persoRect.move(-10,0)
                if event.key == K_RIGHT :
                    if persoRect.right<=630 :
                        persoRect = persoRect.move(10,0)
    fenetre.blit(fond, (0,0))
    fenetre.blit(perso, persoRect)
    pygame.display.update()
pygame.quit()