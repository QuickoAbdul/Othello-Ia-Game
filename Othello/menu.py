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
        self.bouton_joueur_vs_joueur = pygame.Rect(200, 100, 240, 50)
        self.bouton_joueur_vs_ia = pygame.Rect(200, 160, 240, 50)
        self.bouton_ia_vs_ia = pygame.Rect(200, 220, 240, 50)

        # Options pour l'IA Noire
        self.mode_ia_noir = "tout"
        self.profondeur_noir = 2
        self.boutons_mode_noir = {
            "position": pygame.Rect(50, 320, 120, 30),
            "mobilite": pygame.Rect(180, 320, 120, 30),
            "absolu": pygame.Rect(310, 320, 120, 30),
            "mixte": pygame.Rect(440, 320, 120, 30)
        }
        self.bouton_prof_minus_noir = pygame.Rect(200, 370, 30, 30)
        self.bouton_prof_plus_noir = pygame.Rect(300, 370, 30, 30)

        # Options pour l'IA Blanche
        self.mode_ia_blanc = "tout"
        self.profondeur_blanc = 2
        self.boutons_mode_blanc = {
            "position": pygame.Rect(50, 450, 120, 30),
            "mobilite": pygame.Rect(180, 450, 120, 30),
            "absolu": pygame.Rect(310, 450, 120, 30),
            "mixte": pygame.Rect(440, 450, 120, 30)
        }
        self.bouton_prof_minus_blanc = pygame.Rect(200, 500, 30, 30)
        self.bouton_prof_plus_blanc = pygame.Rect(300, 500, 30, 30)

        # Case à cocher pour les indications visuelles
        self.case_a_cocher = pygame.Rect(200, 550, 20, 20)
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

        # Titre options IA Noire
        titre_options_noir = self.police.render("Options IA Noire", True, (0, 0, 0))
        self.fenetre.blit(titre_options_noir, (50, 280))

        # Affichage des boutons de mode IA Noire
        for mode, bouton in self.boutons_mode_noir.items():
            couleur = (0, 200, 0) if self.mode_ia_noir == mode else (150, 150, 150)
            pygame.draw.rect(self.fenetre, couleur, bouton)
            texte = self.police_petite.render(mode, True, (255, 255, 255))
            self.fenetre.blit(texte, (bouton.x + 5, bouton.y + 5))

        # Profondeur IA Noire
        pygame.draw.rect(self.fenetre, (150, 150, 150), self.bouton_prof_minus_noir)
        pygame.draw.rect(self.fenetre, (150, 150, 150), self.bouton_prof_plus_noir)
        self.fenetre.blit(self.police.render("-", True, (0, 0, 0)), (self.bouton_prof_minus_noir.x + 10, self.bouton_prof_minus_noir.y))
        self.fenetre.blit(self.police.render("+", True, (0, 0, 0)), (self.bouton_prof_plus_noir.x + 10, self.bouton_prof_plus_noir.y))
        prof_texte_noir = self.police.render(f"Profondeur: {self.profondeur_noir}", True, (0, 0, 0))
        self.fenetre.blit(prof_texte_noir, (350, 375))

        # Titre options IA Blanche
        titre_options_blanc = self.police.render("Options IA Blanche", True, (0, 0, 0))
        self.fenetre.blit(titre_options_blanc, (50, 410))

        # Affichage des boutons de mode IA Blanche
        for mode, bouton in self.boutons_mode_blanc.items():
            couleur = (0, 200, 0) if self.mode_ia_blanc == mode else (150, 150, 150)
            pygame.draw.rect(self.fenetre, couleur, bouton)
            texte = self.police_petite.render(mode, True, (255, 255, 255))
            self.fenetre.blit(texte, (bouton.x + 5, bouton.y + 5))

        # Profondeur IA Blanche
        pygame.draw.rect(self.fenetre, (150, 150, 150), self.bouton_prof_minus_blanc)
        pygame.draw.rect(self.fenetre, (150, 150, 150), self.bouton_prof_plus_blanc)
        self.fenetre.blit(self.police.render("-", True, (0, 0, 0)), (self.bouton_prof_minus_blanc.x + 10, self.bouton_prof_minus_blanc.y))
        self.fenetre.blit(self.police.render("+", True, (0, 0, 0)), (self.bouton_prof_plus_blanc.x + 10, self.bouton_prof_plus_blanc.y))
        prof_texte_blanc = self.police.render(f"Profondeur: {self.profondeur_blanc}", True, (0, 0, 0))
        self.fenetre.blit(prof_texte_blanc, (350, 505))

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

    def sauvegarder_configs_ia(self):
        config_noir = {
            "mode": self.mode_ia_noir,
            "profondeur": self.profondeur_noir
        }
        config_blanc = {
            "mode": self.mode_ia_blanc,
            "profondeur": self.profondeur_blanc
        }
        with open("config_ia_noir.json", "w") as f:
            json.dump(config_noir, f)
        with open("config_ia_blanc.json", "w") as f:
            json.dump(config_blanc, f)

    def gestion_clic(self, souris_x, souris_y):
        # Gestion des boutons de mode IA Noire
        for mode, bouton in self.boutons_mode_noir.items():
            if bouton.collidepoint(souris_x, souris_y):
                self.mode_ia_noir = mode
                return None

        # Gestion des boutons de mode IA Blanche
        for mode, bouton in self.boutons_mode_blanc.items():
            if bouton.collidepoint(souris_x, souris_y):
                self.mode_ia_blanc = mode
                return None

        # Gestion des boutons de profondeur IA Noire
        if self.bouton_prof_minus_noir.collidepoint(souris_x, souris_y):
            self.profondeur_noir = max(1, self.profondeur_noir - 1)
            return None
        if self.bouton_prof_plus_noir.collidepoint(souris_x, souris_y):
            self.profondeur_noir = min(5, self.profondeur_noir + 1)
            return None

        # Gestion des boutons de profondeur IA Blanche
        if self.bouton_prof_minus_blanc.collidepoint(souris_x, souris_y):
            self.profondeur_blanc = max(1, self.profondeur_blanc - 1)
            return None
        if self.bouton_prof_plus_blanc.collidepoint(souris_x, souris_y):
            self.profondeur_blanc = min(5, self.profondeur_blanc + 1)
            return None

        # Gestion des boutons principaux
        if self.bouton_joueur_vs_joueur.collidepoint(souris_x, souris_y):
            chemin_game = os.path.join(os.path.dirname(__file__), 'game.py')
            subprocess.Popen(['python', chemin_game])
            return "joueur_vs_joueur"
        if self.bouton_joueur_vs_ia.collidepoint(souris_x, souris_y):
            self.sauvegarder_configs_ia()
            chemin_game = os.path.join(os.path.dirname(__file__), 'gameia.py')
            subprocess.Popen(['python', chemin_game])
            return "joueur_vs_ia"
        if self.bouton_ia_vs_ia.collidepoint(souris_x, souris_y):
            self.sauvegarder_configs_ia()
            chemin_game = os.path.join(os.path.dirname(__file__), 'gameiavsia.py')
            subprocess.Popen(['python', chemin_game])
            return "ia_vs_ia"

        # Case à cocher
        if self.case_a_cocher.collidepoint(souris_x, souris_y):
            self.cochee = not self.cochee
        return None