import random

def mouvement_valide(plateau, x, y, joueur):
    """Vérifie si un mouvement est valide selon les règles d'Othello."""
    if plateau[x][y] != " ":
        return False  # Case déjà occupée

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
            return True  # Mouvement valide trouvé dans cette direction

    return False

#IA joue un coup valide aléatoire
def trouver_coup_valide(plateau, joueur):
    """Renvoie un coup valide pour le joueur."""
    coups_valides = []
    for x in range(8):
        for y in range(8):
            if mouvement_valide(plateau, x, y, joueur):
                coups_valides.append((x, y))

    return random.choice(coups_valides) if coups_valides else None
