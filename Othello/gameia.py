import pygame, os
import sys
from ai import trouver_coup_valide, mouvement_valide

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre et du plateau
TAILLE_FENETRE = 600
TAILLE_CASE = TAILLE_FENETRE // 8
COULEUR_FOND = (34, 139, 34)
COULEUR_LIGNE = (0, 0, 0)

#Liste pour historique des coups
historique = []

fenetre = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption("Othello - Joueur vs IA")

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

def est_mouvement_valide(x, y, joueur):
    """Vérifie si un mouvement est valide pour un joueur à une position donnée."""
    if plateau[x][y] != " ":
        return False
    autre_joueur = "noir" if joueur == "blanc" else "blanc"
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        trouvé_adverse = False
        while 0 <= nx < 8 and 0 <= ny < 8 and plateau[nx][ny] == autre_joueur:
            trouvé_adverse = True
            nx += dx
            ny += dy
        if trouvé_adverse and 0 <= nx < 8 and 0 <= ny < 8 and plateau[nx][ny] == joueur:
            return True
    return False

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
            if plateau[x][y] == " " and (est_mouvement_valide(x, y, "noir") or est_mouvement_valide(x, y, "blanc")):
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
    rect_largeur = texte.get_width() + 20
    rect_hauteur = texte.get_height() + 20
    pygame.draw.rect(fenetre, (0, 0, 0), (TAILLE_FENETRE // 2 - rect_largeur // 2, TAILLE_FENETRE // 2 - rect_hauteur // 2, rect_largeur, rect_hauteur))
    fenetre.blit(texte, (TAILLE_FENETRE // 2 - texte.get_width() // 2, TAILLE_FENETRE // 2 - texte.get_height() // 2))

def jouer_mouvement(x, y, joueur):
    """Permet au joueur actuel de jouer un coup à la position (x, y) si le mouvement est valide."""
    if est_mouvement_valide(x, y, joueur):
        plateau[x][y] = joueur
        retourner_pions(x, y, joueur)
         # Ajouter le coup à l'historique
        historique.append({"joueur": joueur, "position": (x, y)})
        return True
    return False

def afficher_historique():
    """Affiche l'historique des coups joués."""
    print("\nHistorique des coups :")
    for index, coup in enumerate(historique, start=1):
        joueur = "Joueur (Blanc)" if coup["joueur"] == "blanc" else "IA (Noir)"
        position = coup["position"]
        print(f"{index}. {joueur} a joué en position {position}")

def afficher_historique_interface():
    """Met à jour l'historique affiché dans l'interface."""
    y_offset = 10
    for index, coup in enumerate(historique[-10:], start=1):  # Afficher les 10 derniers coups
        joueur = "Blanc" if coup["joueur"] == "blanc" else "Noir"
        position = coup["position"]
        texte = f"{(index)}. {joueur} : {position}"
        texte_surface = pygame.font.SysFont(None, 24).render(texte, True, (255, 255, 255))
        fenetre.blit(texte_surface, (475, y_offset))
        y_offset += 25

def sauvegarder_historique():
    """Sauvegarde l'historique des coups dans un fichier unique."""
    base_name = "historique_coups"
    extension = ".txt"
    index = 1

    # Créer un nom de fichier unique
    while os.path.exists(f"{base_name}_{index}{extension}"):
        index += 1

    file_name = f"{base_name}_{index}{extension}"

    # Écrire dans le fichier
    with open(file_name, "w") as f:
        f.write("Historique des coups joues :\n")
        for idx, coup in enumerate(historique, start=1):
            joueur = "Joueur (Blanc)" if coup["joueur"] == "blanc" else "IA (Noir)"
            position = coup["position"]
            f.write(f"{idx}. {joueur} a joue en position {position}\n")

    print(f"Historique sauvegard dans le fichier : {file_name}")

# Boucle principale du jeu
tour_actuel = "joueur"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and tour_actuel == "joueur":
            souris_x, souris_y = pygame.mouse.get_pos()
            grille_x = souris_y // TAILLE_CASE
            grille_y = souris_x // TAILLE_CASE
            if jouer_mouvement(grille_x, grille_y, "blanc"):
                afficher_historique()  # Afficher l'historique
                tour_actuel = "ia"

    if tour_actuel == "ia":
        coup = trouver_coup_valide(plateau, "noir")
        if coup:
            jouer_mouvement(coup[0], coup[1], "noir")
        tour_actuel = "joueur"
        continue

    dessiner_plateau()
    dessiner_pions()
    afficher_score()
    afficher_historique_interface()

    if jeu_fini():
        afficher_resultat_final()
        pygame.time.wait(8000)
        sauvegarder_historique()
        running = False

    pygame.display.flip() # Mettre à jour l'affichage

pygame.quit()
sys.exit()
