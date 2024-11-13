import pygame
from pygame.locals import *
from balle import Balle
from random import randint

pygame.init()
pygame.key.set_repeat(400, 30)

fenetre = pygame.display.set_mode((640, 480))
fond = pygame.image.load("background.jpg").convert()
perso = pygame.image.load("Perso.png").convert_alpha()
persoRect = perso.get_rect()
persoRect.topleft = (270,380)
fenetre.blit(fond,(0,0))

continuer = True
listeBalles =[]

while continuer :
    if len(listeBalles)<10 and randint(1,500)<=10 :
        listeBalles.append(Balle('golfBall.png',(randint(25,455),-25)))
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
    for ball in listeBalles :
        ball.deplace()
        if ball.rect.top >= 480 :
            listeBalles.remove(ball)
        else :
            if ball.collision(persoRect) :
                continuer = False
            ball.affiche(fenetre)

    fenetre.blit(perso, persoRect)
    pygame.display.update()
    pygame.time.wait(10)
pygame.quit()