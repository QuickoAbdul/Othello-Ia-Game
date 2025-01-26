import pygame
import sys
import json
import os
from copy import deepcopy
# Ajout des imports nécessaires
import time
from dataclasses import dataclass
from typing import Tuple, Dict
# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre et du plateau
TAILLE_FENETRE = 600
TAILLE_CASE = TAILLE_FENETRE // 8
COULEUR_FOND = (34, 139, 34)
COULEUR_LIGNE = (0, 0, 0)

# Liste pour historique des coups
historique = []

# Chemin actuel du fichier
current_path = os.path.dirname(__file__)

fenetre = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption("Othello - IA vs IA")


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

# Charger les images des pions
pion_noir = pygame.image.load(os.path.join(current_path, "assets/BlackToken.png"))
pion_blanc = pygame.image.load(os.path.join(current_path, "assets/WhiteToken.png"))
pion_noir = pygame.transform.scale(pion_noir, (TAILLE_CASE, TAILLE_CASE))
pion_blanc = pygame.transform.scale(pion_blanc, (TAILLE_CASE, TAILLE_CASE))

# Initialiser le plateau de jeu
plateau = [[" " for _ in range(8)] for _ in range(8)]
plateau[3][3] = plateau[4][4] = "blanc"
plateau[3][4] = plateau[4][3] = "noir"

# Initialiser la police pour l'affichage du score
font = pygame.font.Font(None, 36)

    # Dictionnaire pour stocker les stats pour chaque IA
ia_stats = {
    "noir": IAStats(),
    "blanc": IAStats()
}

# Configuration des IAs
configs_ia = {
    "noir": {"mode": "position", "profondeur": 2},
    "blanc": {"mode": "tout", "profondeur": 2}
}

def charger_configs_ia():
    """Charge les configurations des deux IAs depuis les fichiers."""
    try:
        with open("config_ia_noir.json", "r") as f:
            configs_ia["noir"] = json.load(f)
        with open("config_ia_blanc.json", "r") as f:
            configs_ia["blanc"] = json.load(f)
    except FileNotFoundError:
        # Configurations par défaut si les fichiers n'existent pas
        configs_ia["noir"] = {"mode": "tout", "profondeur": 2}
        configs_ia["blanc"] = {"mode": "tout", "profondeur": 2}

def evaluer_position(plateau, joueur):
    coins = [(0, 0), (0, 7), (7, 0), (7, 7)]
    bords = [(0,i) for i in range(1,7)] + [(7,i) for i in range(1,7)] + \
            [(i,0) for i in range(1,7)] + [(i,7) for i in range(1,7)]
    score = 0
    autre_joueur = "blanc" if joueur == "noir" else "noir"
    
    for x, y in coins:
        if plateau[x][y] == joueur:
            score += 10
        elif plateau[x][y] == autre_joueur:
            score -= 10
            
    for x, y in bords:
        if plateau[x][y] == joueur:
            score += 2
        elif plateau[x][y] == autre_joueur:
            score -= 2
            
    return score

def evaluer_mobilite(plateau, joueur):
    coups_possibles_joueur = sum(1 for x in range(8) for y in range(8) 
                                if plateau[x][y] == " " and est_mouvement_valide(x, y, joueur))
    autre_joueur = "blanc" if joueur == "noir" else "noir"
    coups_possibles_adversaire = sum(1 for x in range(8) for y in range(8) 
                                   if plateau[x][y] == " " and est_mouvement_valide(x, y, autre_joueur))
    return coups_possibles_joueur - coups_possibles_adversaire

def evaluer_diff_pions(plateau, joueur):
    autre_joueur = "blanc" if joueur == "noir" else "noir"
    score_joueur = sum(row.count(joueur) for row in plateau)
    score_adversaire = sum(row.count(autre_joueur) for row in plateau)
    return score_joueur - score_adversaire

def evaluation(plateau, joueur, config):
    """Évalue la position selon la configuration de l'IA spécifique."""
    score = 0
    if config["mode"] == "position" or config["mode"] == "tout":
        score += evaluer_position(plateau, joueur) * 4
    if config["mode"] == "mobilite" or config["mode"] == "tout":
        score += evaluer_mobilite(plateau, joueur) * 2
    if config["mode"] == "absolu" or config["mode"] == "tout":
        score += evaluer_diff_pions(plateau, joueur)
    return score

def minimax(plateau, profondeur, alpha, beta, joueur, config, node_counter):
    """Version modifiée de Minimax avec compteur de nœuds correct."""
    node_counter.increment()
    
    if profondeur == 0 or jeu_fini():
        return evaluation(plateau, joueur, config)

    coups_possibles = [(x, y) for x in range(8) for y in range(8)
                      if plateau[x][y] == " " and est_mouvement_valide(x, y, joueur)]
    
    if not coups_possibles:
        if any(est_mouvement_valide(x, y, "blanc" if joueur == "noir" else "noir")
               for x in range(8) for y in range(8)):
            return minimax(plateau, profondeur - 1, alpha, beta,
                         "blanc" if joueur == "noir" else "noir", config, node_counter)
        return evaluation(plateau, joueur, config)

    if joueur == "noir":
        max_eval = float("-inf")
        for x, y in coups_possibles:
            nouveau_plateau = deepcopy(plateau)
            jouer_mouvement(x, y, joueur, nouveau_plateau)
            eval = minimax(nouveau_plateau, profondeur - 1, alpha, beta, "blanc", config, node_counter)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for x, y in coups_possibles:
            nouveau_plateau = deepcopy(plateau)
            jouer_mouvement(x, y, joueur, nouveau_plateau)
            eval = minimax(nouveau_plateau, profondeur - 1, alpha, beta, "noir", config, node_counter)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def trouver_meilleur_coup(plateau, joueur):
    """Version modifiée avec mesure correcte des nœuds explorés."""
    config = configs_ia[joueur]
    node_counter = NodeCounter()
    debut_temps = time.time()
    
    meilleur_coup = None
    meilleur_score = float("-inf") if joueur == "noir" else float("inf")
    
    for x in range(8):
        for y in range(8):
            if est_mouvement_valide(x, y, joueur):
                nouveau_plateau = deepcopy(plateau)
                jouer_mouvement(x, y, joueur, nouveau_plateau)
                score = minimax(nouveau_plateau, config["profondeur"] - 1,
                              float("-inf"), float("inf"),
                              "blanc" if joueur == "noir" else "noir",
                              config, node_counter)
                
                if ((joueur == "noir" and score > meilleur_score) or 
                    (joueur == "blanc" and score < meilleur_score)):
                    meilleur_score = score
                    meilleur_coup = (x, y)
    
    temps_ecoule = time.time() - debut_temps
    ia_stats[joueur].add_move_stats(node_counter.get_count(), temps_ecoule)
    
    return meilleur_coup

def est_mouvement_valide(x, y, joueur, plateau_test=None):
    """Vérifie si un mouvement est valide pour un joueur à une position donnée."""
    if plateau_test is None:
        plateau_test = plateau
        
    if plateau_test[x][y] != " ":
        return False
    
    autre_joueur = "noir" if joueur == "blanc" else "blanc"
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        trouve_adverse = False
        while 0 <= nx < 8 and 0 <= ny < 8 and plateau_test[nx][ny] == autre_joueur:
            trouve_adverse = True
            nx += dx
            ny += dy
        if trouve_adverse and 0 <= nx < 8 and 0 <= ny < 8 and plateau_test[nx][ny] == joueur:
            return True
    return False

def retourner_pions(x, y, joueur, plateau_test=None):
    """Retourne les pions adverses après un coup valide."""
    if plateau_test is None:
        plateau_test = plateau
        
    autre_joueur = "noir" if joueur == "blanc" else "blanc"
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        pions_a_retourner = []
        while 0 <= nx < 8 and 0 <= ny < 8 and plateau_test[nx][ny] == autre_joueur:
            pions_a_retourner.append((nx, ny))
            nx += dx
            ny += dy
        if 0 <= nx < 8 and 0 <= ny < 8 and plateau_test[nx][ny] == joueur:
            for rx, ry in pions_a_retourner:
                plateau_test[rx][ry] = joueur

def jouer_mouvement(x, y, joueur, plateau_test=None):
    """Joue un mouvement et retourne les pions."""
    if plateau_test is None:
        plateau_test = plateau
    if est_mouvement_valide(x, y, joueur, plateau_test):
        plateau_test[x][y] = joueur
        retourner_pions(x, y, joueur, plateau_test)
        historique.append({"joueur": joueur, "position": (x, y)})
        return True
    return False

def jeu_fini():
    """Vérifie si le jeu est terminé."""
    return not any(plateau[x][y] == " " and 
                  (est_mouvement_valide(x, y, "noir") or est_mouvement_valide(x, y, "blanc"))
                  for x in range(8) for y in range(8))

def peut_jouer(joueur):
    """Vérifie si le joueur a au moins un coup valide possible."""
    return any(est_mouvement_valide(x, y, joueur) for x in range(8) for y in range(8))

def afficher_plateau():
    """Dessine le plateau et les pions."""
    fenetre.fill(COULEUR_FOND)
    for x in range(0, TAILLE_FENETRE, TAILLE_CASE):
        pygame.draw.line(fenetre, COULEUR_LIGNE, (x, 0), (x, TAILLE_FENETRE))
        pygame.draw.line(fenetre, COULEUR_LIGNE, (0, x), (TAILLE_FENETRE, x))
    
    for x in range(8):
        for y in range(8):
            if plateau[x][y] == "noir":
                fenetre.blit(pion_noir, (y * TAILLE_CASE, x * TAILLE_CASE))
            elif plateau[x][y] == "blanc":
                fenetre.blit(pion_blanc, (y * TAILLE_CASE, x * TAILLE_CASE))

def afficher_score():
    """Affiche le score des deux joueurs."""
    score_noir = sum(row.count("noir") for row in plateau)
    score_blanc = sum(row.count("blanc") for row in plateau)
    texte = f"Noir: {score_noir} | Blanc: {score_blanc}"
    surface_texte = font.render(texte, True, (255, 255, 255))
 # Dimensions du rectangle noir derrière le texte
    rect_largeur = surface_texte.get_width() + 10
    rect_hauteur = surface_texte.get_height() + 10
    rect_x = 5
    rect_y = 5

    # Dessiner le fond noir
    pygame.draw.rect(fenetre, (50, 50, 50), (rect_x, rect_y, rect_largeur, rect_hauteur))

    # Dessiner le texte
    fenetre.blit(surface_texte, (rect_x + 5, rect_y + 5))
   

def afficher_historique():
    """Met à jour l'historique affiché dans l'interface."""
    y_offset = 50
    for index, coup in enumerate(historique[-10:]):
        joueur = coup["joueur"]
        position = coup["position"]
        texte = f"{index + 1}. {joueur} : {position}"
        surface_texte = font.render(texte, True, (255, 255, 255))
        fenetre.blit(surface_texte, (10, y_offset))
        y_offset += 30

def sauvegarder_partie():
    """Version modifiée avec sauvegarde des statistiques."""
    base_name = "partie_ia_vs_ia"
    index = 1
    while os.path.exists(f"{base_name}_{index}.txt"):
        index += 1
    nom_fichier = f"{base_name}_{index}.txt"
    
    score_noir = sum(row.count("noir") for row in plateau)
    score_blanc = sum(row.count("blanc") for row in plateau)
    
    with open(nom_fichier, "w", encoding='utf-8') as f:
        f.write("Configuration des IAs:\n")
        f.write(f"IA Noir: {configs_ia['noir']}\n")
        f.write(f"IA Blanc: {configs_ia['blanc']}\n\n")
        
        f.write("Statistiques des IAs:\n")
        for couleur in ['noir', 'blanc']:
            stats = ia_stats[couleur]
            f.write(f"\nIA {couleur.capitalize()}:\n")
            f.write(f"- Nœuds totaux explorés: {stats.nodes_explored:,}\n")
            f.write(f"- Temps total de réflexion: {stats.total_time:.2f} secondes\n")
            f.write(f"- Nombre de coups joués: {stats.moves_count}\n")
            f.write(f"- Moyenne de nœuds par coup: {stats.average_nodes_per_move():,.0f}\n")
            f.write(f"- Temps moyen par coup: {stats.average_time_per_move():.3f} secondes\n")
        
        f.write("\nHistorique des coups:\n")
        for i, coup in enumerate(historique, 1):
            f.write(f"{i}. {coup['joueur']} a joué en {coup['position']}\n")
            
        f.write(f"\nScore final:\n")
        f.write(f"Noir: {score_noir}\n")
        f.write(f"Blanc: {score_blanc}\n")
        f.write(f"Gagnant: {'Noir' if score_noir > score_blanc else 'Blanc' if score_blanc > score_noir else 'Match nul'}")

def afficher_stats_en_cours():
    """Affiche les statistiques en cours de partie."""
    y_offset = 300  # Position verticale de départ pour les stats
    
    for couleur in ['noir', 'blanc']:
        stats = ia_stats[couleur]
        textes = [
            f"IA {couleur.capitalize()}:",
            f"Nœuds: {stats.nodes_explored:,}",
            f"Temps total: {stats.total_time:.1f}s",
            f"Coups: {stats.moves_count}",
            f"Nœuds/coup: {stats.average_nodes_per_move():,.0f}"
        ]
        
        for texte in textes:
            surface_texte = font.render(texte, True, (255, 255, 255))
            fenetre.blit(surface_texte, (10, y_offset))
            y_offset += 25
        
        y_offset += 10  # Espace entre les stats des deux IAs

def main():
    charger_configs_ia()
    clock = pygame.time.Clock()
    tour_actuel = "noir" 
    running = True
    temps_attente = 500  # Temps d'attente entre les coups en millisecondes

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not jeu_fini():
            if peut_jouer(tour_actuel):
                # Faire jouer l'IA
                coup = trouver_meilleur_coup(plateau, tour_actuel)
                if coup:
                    jouer_mouvement(coup[0], coup[1], tour_actuel)
                    # Mise à jour de l'affichage
                    afficher_plateau()
                    afficher_score()
                    #afficher_historique()
                    pygame.display.flip()
                    
                # Attendre avant le prochain coup
                pygame.time.wait(temps_attente)
                # Changer de joueur
                tour_actuel = "blanc" if tour_actuel == "noir" else "noir"
            else:
                # Si le joueur actuel ne peut pas jouer, passer au joueur suivant
                tour_actuel = "blanc" if tour_actuel == "noir" else "noir"
        else:
            # Le jeu est terminé
            sauvegarder_partie()
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()