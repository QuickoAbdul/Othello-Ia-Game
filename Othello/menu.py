import pygame
import subprocess
import os

class Menu:
    def __init__(self, fenetre, taille_fenetre, taille_case):
        self.fenetre = fenetre
        self.taille_fenetre = taille_fenetre
        self.taille_case = taille_case
        self.police = pygame.font.Font(None, 36)

        # Rectangles des boutons
        self.bouton_joueur_vs_joueur = pygame.Rect(200, 150, 240, 50)
        self.bouton_joueur_vs_ia = pygame.Rect(200, 230, 240, 50)
        self.bouton_ia_vs_ia = pygame.Rect(200, 310, 240, 50)

        # Case à cocher
        self.case_a_cocher = pygame.Rect(200, 390, 20, 20)
        self.cochee = False

    def afficher(self):
        self.fenetre.fill((255, 255, 255))  # Fond blanc

        # Titre du menu
        titre = self.police.render("Menu Principal", True, (0, 0, 0))
        self.fenetre.blit(titre, (self.taille_fenetre // 2 - titre.get_width() // 2, 50))

        # Affichage des boutons
        pygame.draw.rect(self.fenetre, (0, 0, 255), self.bouton_joueur_vs_joueur)
        pygame.draw.rect(self.fenetre, (0, 0, 255), self.bouton_joueur_vs_ia)
        pygame.draw.rect(self.fenetre, (0, 0, 255), self.bouton_ia_vs_ia)

        texte_joueur_vs_joueur = self.police.render("Joueur vs Joueur", True, (255, 255, 255))
        texte_joueur_vs_ia = self.police.render("Joueur vs IA", True, (255, 255, 255))
        texte_ia_vs_ia = self.police.render("IA vs IA", True, (255, 255, 255))

        self.fenetre.blit(texte_joueur_vs_joueur, (self.bouton_joueur_vs_joueur.x + 10, self.bouton_joueur_vs_joueur.y + 10))
        self.fenetre.blit(texte_joueur_vs_ia, (self.bouton_joueur_vs_ia.x + 10, self.bouton_joueur_vs_ia.y + 10))
        self.fenetre.blit(texte_ia_vs_ia, (self.bouton_ia_vs_ia.x + 10, self.bouton_ia_vs_ia.y + 10))

        # Affichage de la case à cocher
        pygame.draw.rect(self.fenetre, (0, 0, 0), self.case_a_cocher, 2)  # Bordure de la case
        if self.cochee:
            pygame.draw.line(self.fenetre, (0, 0, 0), (self.case_a_cocher.x, self.case_a_cocher.y),
                             (self.case_a_cocher.x + self.case_a_cocher.width, self.case_a_cocher.y + self.case_a_cocher.height), 3)
            pygame.draw.line(self.fenetre, (0, 0, 0), (self.case_a_cocher.x + self.case_a_cocher.width, self.case_a_cocher.y),
                             (self.case_a_cocher.x, self.case_a_cocher.y + self.case_a_cocher.height), 3)

        # Afficher "Indications visuelles"
        texte_case = self.police.render("Indications visuelles", True, (0, 0, 0))
        self.fenetre.blit(texte_case, (self.case_a_cocher.x + 30, self.case_a_cocher.y - 5))

    def gestion_clic(self, souris_x, souris_y):
        """Gère les clics de souris sur les différents boutons et la case à cocher."""
        if self.bouton_joueur_vs_joueur.collidepoint(souris_x, souris_y):
            # Utiliser le chemin absolu pour game.py
            chemin_game = os.path.join(os.path.dirname(__file__), 'game.py')
            subprocess.Popen(['python', chemin_game])
            return "joueur_vs_joueur"
        if self.bouton_joueur_vs_ia.collidepoint(souris_x, souris_y):
            chemin_game = os.path.join(os.path.dirname(__file__), 'gameia.py')
            subprocess.Popen(['python', chemin_game])
            return "joueur_vs_ia"
        if self.bouton_ia_vs_ia.collidepoint(souris_x, souris_y):
            chemin_game = os.path.join(os.path.dirname(__file__), 'game.py')
            subprocess.Popen(['python', chemin_game])
            return "ia_vs_ia"

        # Vérifier les clics sur la case à cocher
        if self.case_a_cocher.collidepoint(souris_x, souris_y):
            self.cochee = not self.cochee
        return None
