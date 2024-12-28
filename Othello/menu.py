import pygame
import subprocess
import os
import json

class Menu:
    def __init__(self, fenetre, taille_fenetre, taille_case):
        self.fenetre = fenetre
        self.taille_fenetre = taille_fenetre
        self.taille_case = taille_case
        self.police = pygame.font.Font(None, 36)
        self.police_petite = pygame.font.Font(None, 24)

        # Rectangles des boutons principaux
        self.bouton_joueur_vs_joueur = pygame.Rect(200, 150, 240, 50)
        self.bouton_joueur_vs_ia = pygame.Rect(200, 230, 240, 50)
        self.bouton_ia_vs_ia = pygame.Rect(200, 310, 240, 50)

        # Options IA
        self.mode_ia = "tout"  # "position", "mobilite", "absolu", "tout"
        self.profondeur = 2
        
        # Boutons pour les options IA
        self.boutons_mode = {
            "position": pygame.Rect(50, 400, 120, 30),
            "mobilite": pygame.Rect(180, 400, 120, 30),
            "absolu": pygame.Rect(310, 400, 120, 30),
            "tout": pygame.Rect(440, 400, 120, 30)
        }
        
        # Boutons pour la profondeur
        self.bouton_prof_minus = pygame.Rect(200, 450, 30, 30)
        self.bouton_prof_plus = pygame.Rect(300, 450, 30, 30)

        # Case à cocher
        self.case_a_cocher = pygame.Rect(200, 500, 20, 20)
        self.cochee = False

    def afficher(self):
        self.fenetre.fill((255, 255, 255))

        # Titre du menu
        titre = self.police.render("Menu Principal", True, (0, 0, 0))
        self.fenetre.blit(titre, (self.taille_fenetre // 2 - titre.get_width() // 2, 50))

        # Affichage des boutons principaux
        for bouton, texte in [
            (self.bouton_joueur_vs_joueur, "Joueur vs Joueur"),
            (self.bouton_joueur_vs_ia, "Joueur vs IA"),
            (self.bouton_ia_vs_ia, "IA vs IA")
        ]:
            pygame.draw.rect(self.fenetre, (0, 0, 255), bouton)
            texte_surface = self.police.render(texte, True, (255, 255, 255))
            self.fenetre.blit(texte_surface, (bouton.x + 10, bouton.y + 10))

        # Affichage des options IA
        titre_options = self.police.render("Options IA", True, (0, 0, 0))
        self.fenetre.blit(titre_options, (50, 360))

        # Affichage des boutons de mode
        for mode, bouton in self.boutons_mode.items():
            couleur = (0, 200, 0) if self.mode_ia == mode else (150, 150, 150)
            pygame.draw.rect(self.fenetre, couleur, bouton)
            texte = self.police_petite.render(mode, True, (255, 255, 255))
            self.fenetre.blit(texte, (bouton.x + 5, bouton.y + 5))

        # Affichage de la profondeur
        pygame.draw.rect(self.fenetre, (150, 150, 150), self.bouton_prof_minus)
        pygame.draw.rect(self.fenetre, (150, 150, 150), self.bouton_prof_plus)
        self.fenetre.blit(self.police.render("-", True, (0, 0, 0)), (self.bouton_prof_minus.x + 10, self.bouton_prof_minus.y))
        self.fenetre.blit(self.police.render("+", True, (0, 0, 0)), (self.bouton_prof_plus.x + 10, self.bouton_prof_plus.y))
        prof_texte = self.police.render(f"Profondeur: {self.profondeur}", True, (0, 0, 0))
        self.fenetre.blit(prof_texte, (240, 455))

        # Case à cocher et son texte
        pygame.draw.rect(self.fenetre, (0, 0, 0), self.case_a_cocher, 2)
        if self.cochee:
            pygame.draw.line(self.fenetre, (0, 0, 0), 
                           (self.case_a_cocher.x, self.case_a_cocher.y),
                           (self.case_a_cocher.x + 20, self.case_a_cocher.y + 20), 3)
            pygame.draw.line(self.fenetre, (0, 0, 0),
                           (self.case_a_cocher.x + 20, self.case_a_cocher.y),
                           (self.case_a_cocher.x, self.case_a_cocher.y + 20), 3)
        texte_case = self.police.render("Indications visuelles", True, (0, 0, 0))
        self.fenetre.blit(texte_case, (self.case_a_cocher.x + 30, self.case_a_cocher.y - 5))

    def sauvegarder_config_ia(self):
        config = {
            "mode": self.mode_ia,
            "profondeur": self.profondeur
        }
        with open("config_ia.json", "w") as f:
            json.dump(config, f)

    def gestion_clic(self, souris_x, souris_y):
        # Gestion des boutons de mode IA
        for mode, bouton in self.boutons_mode.items():
            if bouton.collidepoint(souris_x, souris_y):
                self.mode_ia = mode
                return None

        # Gestion des boutons de profondeur
        if self.bouton_prof_minus.collidepoint(souris_x, souris_y):
            self.profondeur = max(1, self.profondeur - 1)
            return None
        if self.bouton_prof_plus.collidepoint(souris_x, souris_y):
            self.profondeur = min(5, self.profondeur + 1)
            return None

        # Gestion des boutons principaux
        if self.bouton_joueur_vs_joueur.collidepoint(souris_x, souris_y):
            chemin_game = os.path.join(os.path.dirname(__file__), 'game.py')
            subprocess.Popen(['python', chemin_game])
            return "joueur_vs_joueur"
        if self.bouton_joueur_vs_ia.collidepoint(souris_x, souris_y):
            self.sauvegarder_config_ia()
            chemin_game = os.path.join(os.path.dirname(__file__), 'gameia.py')
            subprocess.Popen(['python', chemin_game])
            return "joueur_vs_ia"
        if self.bouton_ia_vs_ia.collidepoint(souris_x, souris_y):
            chemin_game = os.path.join(os.path.dirname(__file__), 'gameiavsia.py')
            subprocess.Popen(['python', chemin_game])
            return "ia_vs_ia"

        # Case à cocher
        if self.case_a_cocher.collidepoint(souris_x, souris_y):
            self.cochee = not self.cochee
        return None