import pygame
import sys
from menu import Menu  # Importer la classe Menu

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
TAILLE_FENETRE = 640
fenetre = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption("Othello")

# Créer une instance du menu
menu = Menu(fenetre, TAILLE_FENETRE, 80)

# Boucle principale du menu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            souris_x, souris_y = pygame.mouse.get_pos()
            choix = menu.gestion_clic(souris_x, souris_y)
            if choix:
                # Quitter la boucle du menu et démarrer le jeu
                running = False

    # Afficher le menu
    menu.afficher()

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter le menu et démarrer le jeu
pygame.quit()
sys.exit()
