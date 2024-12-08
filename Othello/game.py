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

# Initialiser la grille du plateau (0 = vide, 1 = noir, -1 = blanc)
plateau = [[0] * 8 for _ in range(8)]
plateau[3][3], plateau[3][4] = -1, 1  # Pions de départ
plateau[4][3], plateau[4][4] = 1, -1

joueur_actuel = 1  # 1 pour noir, -1 pour blanc

font = pygame.font.Font(None, 36)  # Police pour l'affichage du texte

def dessiner_plateau():
    """Dessine le plateau avec un fond vert et des lignes noires."""
    fenetre.fill(COULEUR_FOND)  # Remplir le fond avec la couleur du plateau

    # Dessiner les lignes horizontales et verticales
    for i in range(9):  # 9 lignes pour un plateau 8x8 (8 cases + bordures)
        pygame.draw.line(fenetre, COULEUR_LIGNE, (i * TAILLE_CASE, 0), (i * TAILLE_CASE, TAILLE_FENETRE), 2)
        pygame.draw.line(fenetre, COULEUR_LIGNE, (0, i * TAILLE_CASE), (TAILLE_FENETRE, i * TAILLE_CASE), 2)

def dessiner_pions():
    """Dessine les pions sur le plateau."""
    for y in range(8):
        for x in range(8):
            if plateau[y][x] == 1:
                fenetre.blit(pion_noir, (x * TAILLE_CASE, y * TAILLE_CASE))
            elif plateau[y][x] == -1:
                fenetre.blit(pion_blanc, (x * TAILLE_CASE, y * TAILLE_CASE))

def calculer_score():
    """Calcule le score des joueurs."""
    score_noir = sum(row.count(1) for row in plateau)
    score_blanc = sum(row.count(-1) for row in plateau)
    return score_noir, score_blanc

def afficher_score():
    """Affiche le score des deux joueurs avec un fond noir."""
    score_noir, score_blanc = calculer_score()
    texte_score = f"Noir: {score_noir} | Blanc: {score_blanc}"
    texte = font.render(texte_score, True, (255, 255, 255))
    
    # Dimensions du rectangle noir derrière le texte
    rect_largeur = texte.get_width() + 10
    rect_hauteur = texte.get_height() + 10
    rect_x = 5
    rect_y = 5

    # Dessiner le fond noir
    pygame.draw.rect(fenetre, (50, 50, 50), (rect_x, rect_y, rect_largeur, rect_hauteur))

    # Dessiner le texte
    fenetre.blit(texte, (rect_x + 5, rect_y + 5))


def est_mouvement_valide(x, y, couleur):
    """Vérifie si un mouvement est valide pour un joueur à une position donnée."""
    if plateau[y][x] != 0:
        return False  # La case n'est pas vide
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dx, dy in directions:
        i, j = x + dx, y + dy
        pions_a_retourner = []
        while 0 <= i < 8 and 0 <= j < 8 and plateau[j][i] == -couleur:
            pions_a_retourner.append((i, j))
            i += dx
            j += dy
        if 0 <= i < 8 and 0 <= j < 8 and plateau[j][i] == couleur and pions_a_retourner:
            return True
    return False

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

def jeu_fini():
    """Vérifie si le jeu est terminé."""
    for y in range(8):
        for x in range(8):
            if plateau[y][x] == 0 and (est_mouvement_valide(x, y, 1) or est_mouvement_valide(x, y, -1)):
                return False
    return True

def afficher_resultat_final():
    """Affiche le résultat final du jeu avec un fond noir."""
    score_noir, score_blanc = calculer_score()
    if score_noir > score_blanc:
        message = "Noir a gagné !"
    elif score_blanc > score_noir:
        message = "Blanc a gagné !"
    else:
        message = "Match nul !"
    texte = font.render(message, True, (255, 255, 255))

    # Dimensions du rectangle noir derrière le texte
    rect_largeur = texte.get_width() + 20
    rect_hauteur = texte.get_height() + 20
    rect_x = TAILLE_FENETRE // 2 - rect_largeur // 2
    rect_y = TAILLE_FENETRE // 2 - rect_hauteur // 2

    # Dessiner le fond noir
    pygame.draw.rect(fenetre, (0, 0, 0), (rect_x, rect_y, rect_largeur, rect_hauteur))

    # Dessiner le texte
    fenetre.blit(texte, (rect_x + 10, rect_y + 10))


def jouer_mouvement(x, y):
    """Permet au joueur actuel de jouer à la position (x, y) si le mouvement est valide."""
    global joueur_actuel
    if est_mouvement_valide(x, y, joueur_actuel):
        plateau[y][x] = joueur_actuel
        retourner_pions(x, y, joueur_actuel)
        joueur_actuel = -joueur_actuel  # Changer de joueur

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:  # Détection du clic de souris
            souris_x, souris_y = pygame.mouse.get_pos()
            grille_x = souris_x // TAILLE_CASE
            grille_y = souris_y // TAILLE_CASE
            jouer_mouvement(grille_x, grille_y)

    dessiner_plateau()
    dessiner_pions()
    afficher_score()

    if jeu_fini():
        afficher_resultat_final()

    pygame.display.flip()

pygame.quit()
sys.exit()
