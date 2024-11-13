import pygame
import sys
import os

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre et du plateau
TAILLE_FENETRE = 640  # Taille de la fenêtre (640x640)
TAILLE_CASE = TAILLE_FENETRE // 8  # Taille d'une case pour un plateau 8x8
COULEUR_FOND = (34, 139, 34)  # Couleur verte pour le fond du plateau
COULEUR_LIGNE = (0, 0, 0)  # Couleur noire pour les lignes

current_path = os.path.dirname(__file__)

# Charger les images des pions
pion_noir = pygame.image.load(os.path.join(current_path, "assets/BlackToken.png"))
pion_blanc = pygame.image.load(os.path.join(current_path, "assets/WhiteToken.png"))

# Créer la fenêtre
fenetre = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption("Othello")

# Redimensionner les pions pour qu'ils s'adaptent aux cases
pion_noir = pygame.transform.scale(pion_noir, (TAILLE_CASE, TAILLE_CASE))
pion_blanc = pygame.transform.scale(pion_blanc, (TAILLE_CASE, TAILLE_CASE))


# Positions initiales des pions
# Centre du plateau pour un jeu 8x8
positions_depart = [
    (3, 3, pion_blanc),
    (3, 4, pion_noir),
    (4, 3, pion_noir),
    (4, 4, pion_blanc)
]

# Initialiser la grille du plateau (0 = vide, 1 = noir, -1 = blanc)
plateau = [[0] * 8 for _ in range(8)]
plateau[3][3], plateau[3][4] = -1, 1  # Pions de départ
plateau[4][3], plateau[4][4] = 1, -1

joueur_actuel = 1  # 1 pour noir, -1 pour blanc


def dessiner_pions():
    """Dessine tous les pions placés sur le plateau en fonction de la grille."""
    for y in range(8):
        for x in range(8):
            if plateau[y][x] == 1:  # Pion noir
                fenetre.blit(pion_noir, (x * TAILLE_CASE, y * TAILLE_CASE))
            elif plateau[y][x] == -1:  # Pion blanc
                fenetre.blit(pion_blanc, (x * TAILLE_CASE, y * TAILLE_CASE))

def dessiner_plateau():
    """Dessine le plateau avec un fond vert et des lignes noires."""
    fenetre.fill(COULEUR_FOND)  # Fond vert

    # Dessiner les lignes horizontales et verticales
    for i in range(9):  # 9 lignes pour un plateau 8x8 (8 cases + bordures)
        pygame.draw.line(fenetre, COULEUR_LIGNE, (i * TAILLE_CASE, 0), (i * TAILLE_CASE, TAILLE_FENETRE), 2)
        pygame.draw.line(fenetre, COULEUR_LIGNE, (0, i * TAILLE_CASE), (TAILLE_FENETRE, i * TAILLE_CASE), 2)

def est_mouvement_valide(x, y, couleur):
    """Vérifie si un mouvement est valide pour un joueur à une position donnée."""
    if plateau[y][x] != 0:
        return False  # La case n'est pas vide
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    valide = False
    for dx, dy in directions:
        i, j = x + dx, y + dy
        pions_a_retourner = []
        while 0 <= i < 8 and 0 <= j < 8 and plateau[j][i] == -couleur:
            pions_a_retourner.append((i, j))
            i += dx
            j += dy
        if 0 <= i < 8 and 0 <= j < 8 and plateau[j][i] == couleur and pions_a_retourner:
            valide = True
            break
    return valide

def retourner_pions(x, y, couleur):
    """Retourne les pions selon les règles après un mouvement valide."""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dx, dy in directions:
        i, j = x + dx, y + dy
        pions_a_retourner = []
        while 0 <= i < 8 and 0 <= j < 8 and plateau[j][i] == -couleur:
            pions_a_retourner.append((i, j))
            i += dx
            j += dy
        if 0 <= i < 8 and 0 <= j < 8 and plateau[j][i] == couleur:
            for (rx, ry) in pions_a_retourner:
                plateau[ry][rx] = couleur

def jouer_mouvement(x, y):
    """Permet au joueur actuel de jouer à la position (x, y) si le mouvement est valide."""
    global joueur_actuel
    if est_mouvement_valide(x, y, joueur_actuel):
        plateau[y][x] = joueur_actuel
        retourner_pions(x, y, joueur_actuel)
        joueur_actuel = -joueur_actuel
        return True
    return False
        
# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:  # Détection du clic de souris
            # Obtenir les coordonnées de la souris
            souris_x, souris_y = pygame.mouse.get_pos()

            # Convertir les coordonnées de la souris en indices de la grille
            grille_x = souris_x // TAILLE_CASE
            grille_y = souris_y // TAILLE_CASE

            # Jouer le mouvement si possible
            if jouer_mouvement(grille_x, grille_y):
                # Redessiner le plateau pour montrer le coup
                dessiner_plateau()
                dessiner_pions()
                pygame.display.flip()  # Mettre à jour l'affichage

    # Dessiner le plateau et les pions
    dessiner_plateau()
    dessiner_pions()

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()

