import pygame
import sys
import json
import os
import time
from dataclasses import dataclass
from copy import deepcopy

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre et du plateau
TAILLE_FENETRE = 600
TAILLE_CASE = TAILLE_FENETRE // 8
COULEUR_FOND = (34, 139, 34)
COULEUR_LIGNE = (0, 0, 0)

# Liste pour historique des coups
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

@dataclass
class IAStats:
    """Classe pour stocker les statistiques de l'IA"""
    nodes_explored: int = 0
    total_time: float = 0
    moves_count: int = 0
    
    def average_time_per_move(self):
        return self.total_time / self.moves_count if self.moves_count > 0 else 0
    
    def average_nodes_per_move(self):
        return self.nodes_explored / self.moves_count if self.moves_count > 0 else 0
    
    def add_move_stats(self, nodes: int, time: float):
        """Ajoute les statistiques d'un coup"""
        self.nodes_explored += nodes
        self.total_time += time
        self.moves_count += 1

class NodeCounter:
    """Classe pour compter les nœuds explorés"""
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count += 1
        
    def get_count(self):
        return self.count

# Configuration de l'IA et stats
ia_stats = IAStats()

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

def est_mouvement_valide(x, y, joueur, plateau_jeu=None):
    """Vérifie si un mouvement est valide pour un joueur à une position donnée."""
    plateau_courant = plateau_jeu if plateau_jeu is not None else plateau
    
    if plateau_courant[x][y] != " ":
        return False
    autre_joueur = "noir" if joueur == "blanc" else "blanc"
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        trouvé_adverse = False
        while 0 <= nx < 8 and 0 <= ny < 8 and plateau_courant[nx][ny] == autre_joueur:
            trouvé_adverse = True
            nx += dx
            ny += dy
        if trouvé_adverse and 0 <= nx < 8 and 0 <= ny < 8 and plateau_courant[nx][ny] == joueur:
            return True
    return False

def retourner_pions(x, y, joueur, plateau_jeu=None):
    """Retourne les pions adverses après un coup valide."""
    plateau_courant = plateau_jeu if plateau_jeu is not None else plateau
    autre_joueur = "noir" if joueur == "blanc" else "blanc"
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        pions_a_retourner = []
        while 0 <= nx < 8 and 0 <= ny < 8 and plateau_courant[nx][ny] == autre_joueur:
            pions_a_retourner.append((nx, ny))
            nx += dx
            ny += dy
        if 0 <= nx < 8 and 0 <= ny < 8 and plateau_courant[nx][ny] == joueur:
            for (rx, ry) in pions_a_retourner:
                plateau_courant[rx][ry] = joueur

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

def jouer_mouvement(x, y, joueur, plateau_jeu=None):
    """Permet au joueur actuel de jouer un coup à la position (x, y) si le mouvement est valide.
    Si plateau_jeu est spécifié, joue le coup sur ce plateau. Sinon, utilise le plateau global."""
    plateau_courant = plateau_jeu if plateau_jeu is not None else plateau
    
    if est_mouvement_valide(x, y, joueur, plateau_courant):
        plateau_courant[x][y] = joueur
        retourner_pions(x, y, joueur, plateau_courant)
        # Ajouter le coup à l'historique seulement si on joue sur le plateau principal
        if plateau_jeu is None:
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
    """Version améliorée de la sauvegarde avec statistiques."""
    base_name = "partie_joueur_vs_ia"
    index = 1
    while os.path.exists(f"{base_name}_{index}.txt"):
        index += 1
    nom_fichier = f"{base_name}_{index}.txt"
    
    try:
        with open("config_ia.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {"mode": "all", "profondeur": 2}
    
    score_noir = sum(row.count("noir") for row in plateau)
    score_blanc = sum(row.count("blanc") for row in plateau)
    
    with open(nom_fichier, "w", encoding='utf-8') as f:
        f.write("Configuration de l'IA:\n")
        f.write(f"Stratégie: {config['mode']}\n")
        f.write(f"Profondeur de recherche: {config['profondeur']}\n\n")
        
        f.write("Statistiques de l'IA:\n")
        f.write(f"- Nœuds totaux explorés: {ia_stats.nodes_explored:,}\n")
        f.write(f"- Temps total de réflexion: {ia_stats.total_time:.2f} secondes\n")
        f.write(f"- Nombre de coups joués: {ia_stats.moves_count}\n")
        f.write(f"- Moyenne de nœuds par coup: {ia_stats.average_nodes_per_move():,.0f}\n")
        f.write(f"- Temps moyen par coup: {ia_stats.average_time_per_move():.3f} secondes\n\n")
        
        f.write("Historique des coups:\n")
        for i, coup in enumerate(historique, 1):
            joueur = "Joueur (Blanc)" if coup["joueur"] == "blanc" else "IA (Noir)"
            f.write(f"{i}. {joueur} a joué en {coup['position']}\n")
            
        f.write(f"\nScore final:\n")
        f.write(f"Noir (IA): {score_noir}\n")
        f.write(f"Blanc (Joueur): {score_blanc}\n")
        gagnant = "IA (Noir)" if score_noir > score_blanc else "Joueur (Blanc)" if score_blanc > score_noir else "Match nul"
        f.write(f"Gagnant: {gagnant}")

def afficher_stats_interface():
    """Affiche les statistiques de l'IA en temps réel."""
    y_offset = 300
    textes = [
        f"Statistiques IA:",
        f"Nœuds: {ia_stats.nodes_explored:,}",
        f"Temps total: {ia_stats.total_time:.1f}s",
        f"Coups: {ia_stats.moves_count}",
        f"Nœuds/coup: {ia_stats.average_nodes_per_move():,.0f}"
    ]
    
    for texte in textes:
        surface_texte = font.render(texte, True, (255, 255, 255))
        fenetre.blit(surface_texte, (10, y_offset))
        y_offset += 25

# Ajout de la stratégie d'évaluation
def evaluer_position(plateau):
    coins = [(0, 0), (0, 7), (7, 0), (7, 7)]
    bords = [(0,i) for i in range(1,7)] + [(7,i) for i in range(1,7)] + \
            [(i,0) for i in range(1,7)] + [(i,7) for i in range(1,7)]
    score = 0
    # Évaluation des coins
    for x, y in coins:
        if plateau[x][y] == "noir":
            score += 1
        elif plateau[x][y] == "blanc":
            score -= 1
            
    # Évaluation des bords
    for x, y in bords:
        if plateau[x][y] == "noir":
            score += 0
        elif plateau[x][y] == "blanc":
            score -= 0
            
    return score

def evaluer_mobilite(plateau, joueur):
    """Retourne une évaluation basée sur la mobilité du joueur."""
    coups_possibles_joueur = 0
    coups_possibles_adversaire = 0
    for x in range(8):
        for y in range(8):
            if plateau[x][y] == " ":
                if est_mouvement_valide(x, y, joueur):
                    coups_possibles_joueur += 1
                if est_mouvement_valide(x, y, "noir" if joueur == "blanc" else "blanc"):
                    coups_possibles_adversaire += 1
    return coups_possibles_joueur - coups_possibles_adversaire

def evaluer_diff_pions(plateau):
    """Retourne une évaluation basée sur la différence de nombre de pions."""
    score_noir = sum(row.count("noir") for row in plateau)
    score_blanc = sum(row.count("blanc") for row in plateau)
    return score_noir - score_blanc

def evaluation(plateau, joueur):
    """Combine plusieurs critères pour évaluer la position selon la configuration."""
    # Charger la configuration
    try:
        with open("config_ia.json", "r") as f:
            config = json.load(f)
    except:
        config = {"mode": "all", "profondeur": 2}  # Configuration par défaut
    
    score = 0
    if config["mode"] == "position" or config["mode"] == "all":
        score += evaluer_position(plateau) * 4
    
    if config["mode"] == "mobilite" or config["mode"] == "all":
        score += evaluer_mobilite(plateau, joueur) * 2
    
    if config["mode"] == "absolu" or config["mode"] == "all":
        score += evaluer_diff_pions(plateau)
    
    return score

# Implémentation de l'algorithme Min-Max avec élagage alpha-beta
def minimax(plateau, profondeur, alpha, beta, joueur, node_counter):
    """Version améliorée de Minimax avec comptage des nœuds."""
    node_counter.increment()
    
    if profondeur == 0 or jeu_fini():
        return evaluation(plateau, joueur)

    if joueur == "noir":
        max_eval = float("-inf")
        for x in range(8):
            for y in range(8):
                if est_mouvement_valide(x, y, joueur):
                    nouveau_plateau = deepcopy(plateau)
                    jouer_mouvement(x, y, joueur, nouveau_plateau)
                    eval = minimax(nouveau_plateau, profondeur - 1, alpha, beta, "blanc", node_counter)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float("inf")
        for x in range(8):
            for y in range(8):
                if est_mouvement_valide(x, y, joueur):
                    nouveau_plateau = deepcopy(plateau)
                    jouer_mouvement(x, y, joueur, nouveau_plateau)
                    eval = minimax(nouveau_plateau, profondeur - 1, alpha, beta, "noir", node_counter)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def trouver_meilleur_coup(plateau, profondeur, joueur):
    """Version améliorée de la recherche du meilleur coup avec stats."""
    node_counter = NodeCounter()
    debut_temps = time.time()
    
    meilleur_coup = None
    meilleur_score = float("-inf") if joueur == "noir" else float("inf")
    
    for x in range(8):
        for y in range(8):
            if est_mouvement_valide(x, y, joueur):
                nouveau_plateau = deepcopy(plateau)
                jouer_mouvement(x, y, joueur, nouveau_plateau)
                score = minimax(nouveau_plateau, profondeur - 1, float("-inf"), float("inf"),
                              "blanc" if joueur == "noir" else "noir", node_counter)
                
                if (joueur == "noir" and score > meilleur_score) or (joueur == "blanc" and score < meilleur_score):
                    meilleur_score = score
                    meilleur_coup = (x, y)
    
    temps_ecoule = time.time() - debut_temps
    ia_stats.add_move_stats(node_counter.get_count(), temps_ecoule)
    
    return meilleur_coup

def peut_jouer(joueur):
    """Vérifie si le joueur a au moins un coup valide possible."""
    for x in range(8):
        for y in range(8):
            if est_mouvement_valide(x, y, joueur):
                return True
    return False

def afficher_message_tour_passe(joueur):
    """Affiche un message quand un tour est passé."""
    message = f"Tour passé pour {joueur}"
    texte = font.render(message, True, (255, 255, 255))
    rect_largeur = texte.get_width() + 20
    rect_hauteur = texte.get_height() + 20
    pygame.draw.rect(fenetre, (0, 0, 0), 
                    (TAILLE_FENETRE // 2 - rect_largeur // 2, 
                     TAILLE_FENETRE // 2 - rect_hauteur // 2,
                     rect_largeur, rect_hauteur))
    fenetre.blit(texte, 
                (TAILLE_FENETRE // 2 - texte.get_width() // 2,
                 TAILLE_FENETRE // 2 - texte.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(1000)  # Afficher le message pendant 1 seconde

# Boucle principale du jeu
tour_actuel = "joueur"
coups_passes = 0  # Compteur pour suivre les passages de tour consécutifs
running = True
# Dans la boucle principale du jeu
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and tour_actuel == "joueur":
            if peut_jouer("blanc"):
                souris_x, souris_y = pygame.mouse.get_pos()
                grille_x = souris_y // TAILLE_CASE
                grille_y = souris_x // TAILLE_CASE
                if jouer_mouvement(grille_x, grille_y, "blanc"):
                    afficher_historique()
                    # Forcer l'affichage après le coup du joueur
                    dessiner_plateau()
                    dessiner_pions()
                    afficher_score()
                    afficher_historique_interface()
                    pygame.display.flip()
                    
                    coups_passes = 0
                    tour_actuel = "ia"
            else:
                print("Le joueur ne peut pas jouer - Tour passé")
                afficher_message_tour_passe("Joueur")
                coups_passes += 1
                tour_actuel = "ia"

    if tour_actuel == "ia":
        if peut_jouer("noir"):
            coup = trouver_meilleur_coup(plateau, 2, "noir")
            if coup:
                jouer_mouvement(coup[0], coup[1], "noir")
                # Forcer l'affichage après le coup de l'IA
                dessiner_plateau()
                dessiner_pions()
                afficher_score()
                afficher_historique_interface()
                pygame.display.flip()
                
                coups_passes = 0
        else:
            print("L'IA ne peut pas jouer - Tour passé")
            afficher_message_tour_passe("IA")
            coups_passes += 1
        tour_actuel = "joueur"

    # Si deux passages de tour consécutifs ou plateau plein
    if coups_passes >= 2 or jeu_fini():
        dessiner_plateau()
        dessiner_pions()
        afficher_score()
        afficher_historique_interface()
        afficher_resultat_final()
        pygame.display.flip()
        pygame.time.wait(3000)  # Attendre 3 secondes
        sauvegarder_historique()
        running = False
    else:
        # Mise à jour normale de l'affichage
        dessiner_plateau()
        dessiner_pions()
        afficher_score()
        afficher_historique_interface()
        pygame.display.flip()

# Avant de quitter, s'assurer que tout est bien affiché une dernière fois
dessiner_plateau()
dessiner_pions()
afficher_score()
afficher_historique_interface()
pygame.display.flip()
pygame.time.wait(1000)  # Attendre une seconde supplémentaire
pygame.quit()
sys.exit()
