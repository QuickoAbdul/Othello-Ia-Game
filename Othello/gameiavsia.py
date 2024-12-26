import pygame
import sys
from ai import trouver_coup_valide

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre et du plateau
TAILLE_FENETRE = 600
TAILLE_CASE = TAILLE_FENETRE // 8
COULEUR_FOND = (34, 139, 34)
COULEUR_LIGNE = (0, 0, 0)

fenetre = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption("Othello - IA vs IA")

# Charger les images des pions
pion_noir = pygame.image.load("assets/BlackToken.png")
pion_blanc = pygame.image.load("assets/WhiteToken.png")
pion_noir = pygame.transform.scale(pion_noir, (TAILLE_CASE, TAILLE_CASE))
pion_blanc = pygame.transform.scale(pion_blanc, (TAILLE_CASE, TAILLE_CASE))

# Initialiser le plateau de jeu
plateau = [[" " for _ in range(8)] for _ in range(8)]
plateau[3][3] = plateau[4][4] = "blanc"
plateau[3][4] = plateau[4][3] = "noir"

# Initialiser la police pour l'affichage du score
font = pygame.font.Font(None, 36)

def dessiner_plateau():
    """Dessine le plateau avec un fond vert et des lignes noires."""
    fenetre.fill(COULEUR_FOND)
    for x in range(0, TAILLE_FENETRE, TAILLE_CASE):
        pygame.draw.line(fenetre, COULEUR_LIGNE, (x, 0), (x, TAILLE_FENETRE))
        pygame.draw.line(fenetre, COULEUR_LIGNE, (0, x), (TAILLE_FENETRE, x))

def dessiner_pions():
    """Dessine les pions sur le plateau."""
    for x in range(8):
        for y in range(8):
            if plateau[x][y] == "noir":
                fenetre.blit(pion_noir, (y * TAILLE_CASE, x * TAILLE_CASE))
            elif plateau[x][y] == "blanc":
                fenetre.blit(pion_blanc, (y * TAILLE_CASE, x * TAILLE_CASE))

def calculer_score():
    """Calcule le score des joueurs."""
    score_noir = sum(row.count("noir") for row in plateau)
    score_blanc = sum(row.count("blanc") for row in plateau)
    return score_noir, score_blanc

def afficher_score():
    """Affiche le score des deux joueurs."""
    score_noir, score_blanc = calculer_score()
    texte_score = f"Noir: {score_noir} | Blanc: {score_blanc}"
    texte = font.render(texte_score, True, (255, 255, 255))
    rect_largeur = texte.get_width() + 10
    rect_hauteur = texte.get_height() + 10
    pygame.draw.rect(fenetre, (0, 0, 0), (5, 5, rect_largeur, rect_hauteur))
    fenetre.blit(texte, (10, 10))

def retourner_pions(x, y, joueur):
    """Retourne les pions adverses après un coup valide."""
    autre_joueur = "noir" if joueur == "blanc" else "blanc"
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        pions_a_retourner = []
        while 0 <= nx < 8 and 0 <= ny < 8 and plateau[nx][ny] == autre_joueur:
            pions_a_retourner.append((nx, ny))
            nx += dx
            ny += dy
        if 0 <= nx < 8 and 0 <= ny < 8 and plateau[nx][ny] == joueur:
            for (rx, ry) in pions_a_retourner:
                plateau[rx][ry] = joueur

def jeu_fini():
    """Vérifie si le jeu est terminé."""
    for x in range(8):
        for y in range(8):
            if plateau[x][y] == " " and (trouver_coup_valide(plateau, "noir") or trouver_coup_valide(plateau, "blanc")):
                return False
    return True

def afficher_resultat_final():
    """Affiche le résultat final du jeu."""
    score_noir, score_blanc = calculer_score()
    if score_noir > score_blanc:
        message = "Noir a gagné !"
    elif score_blanc > score_noir:
        message = "Blanc a gagné !"
    else:
        message = "Match nul !"
    texte = font.render(message, True, (255, 255, 255))
    fenetre.blit(texte, (TAILLE_FENETRE // 2 - texte.get_width() // 2, TAILLE_FENETRE // 2 - texte.get_height() // 2))

# Boucle principale du jeu entre deux IA
tour_actuel = "noir"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dessiner_plateau()
    dessiner_pions()
    afficher_score()

    if not jeu_fini():
        coup = trouver_coup_valide(plateau, tour_actuel)
        if coup:
            x, y = coup
            plateau[x][y] = tour_actuel
            retourner_pions(x, y, tour_actuel)
            tour_actuel = "blanc" if tour_actuel == "noir" else "noir"
    else:
        afficher_resultat_final()
        pygame.display.flip()
        pygame.time.wait(5000)
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()