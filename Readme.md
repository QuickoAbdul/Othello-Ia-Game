# Othello - Jeu en Python avec PyGame

## 📌 Présentation

Ce projet est une implémentation du jeu **Othello (Reversi)** en Python en utilisant **PyGame**. Il propose plusieurs modes de jeu :

- **Joueur vs Joueur** 👥
- **Joueur vs IA** 🤖
- **IA vs IA** 🤖🤖 (avec algorithme Min-Max et élagage alpha-bêta)

Le projet inclut également un système d'historique des coups et enregistre les statistiques des parties jouées dans un fichier `.txt`.

---

## 🛠️ Fonctionnalités

- 🎮 **Interface graphique avec PyGame**
- 🔄 **Modes de jeu :** Joueur contre Joueur, Joueur contre IA, IA contre IA
- 🧠 **Intelligence Artificielle avec Min-Max et élagage alpha-bêta**
- 📝 **Historique des coups joués**
- 📊 **Enregistrement des statistiques de l'IA** après chaque partie
- 🎯 **Indication des coups possibles (option activable)**

---

## 📥 Installation

### Prérequis

- Python **3.x**
- Bibliothèques nécessaires :
  ```bash
  pip install pygame
  ```

### Exécution du jeu

Cloner le dépôt et lancer le jeu :

```bash
git clone <(https://github.com/QuickoAbdul/Othello-Ia-Game)>
cd Othello_PyGame
python main.py
```

---

## 🎲 Règles du jeu Othello

1. Le plateau est un carré **8×8**.
2. Deux joueurs s'affrontent : **Noir** et **Blanc**.
3. Chaque joueur pose un pion par tour.
4. Un pion doit être placé de manière à **encadrer** une ou plusieurs pièces adverses (horizontalement, verticalement ou diagonalement).
5. Les pièces encadrées sont retournées pour devenir celles du joueur actif.
6. La partie se termine lorsque **plus aucun coup n'est possible** ou lorsque le plateau est **rempli**.
7. Le joueur ayant le **plus de pions** sur le plateau remporte la partie.

---

## 🤖 Intelligence Artificielle

L'IA repose sur l'algorithme **Min-Max avec élagage alpha-bêta**, optimisé par différentes stratégies d'évaluation :

- **Positionnelle** : Utilisation d'une grille de poids pour donner de l'importance aux coins et aux bords.
- **Mobilité** : Privilégier les coups qui maximisent les mouvements possibles et limitent ceux de l'adversaire.
- **Différence de pions** : Calculer la différence entre les pions de l'IA et ceux de l'adversaire.

L'IA peut jouer avec différentes profondeurs de recherche pour ajuster son niveau de difficulté.

---

## 📜 Historique des coups

Un historique des coups est sauvegardé dans un fichier `.txt` après chaque partie. Il permet de :

- Consulter les coups joués dans l'ordre chronologique
- Analyser les décisions prises par l'IA
- Rejouer une partie à partir des données sauvegardées

---

## 📊 Statistiques

À la fin de chaque partie, un fichier `.txt` enregistre des statistiques telles que :

- Nombre total de parties jouées
- Victoires/défaites de l'IA
- Score final de chaque partie
- Nombre moyen de coups par partie

Ces statistiques permettent d'évaluer les performances de l'IA sur le long terme.

---

## 📌 Améliorations futures

- 🔍 **Optimisation de l'IA** (ajout de nouvelles heuristiques)
- 📈 **Interface plus avancée** avec animations et effets visuels
- ☁️ **Sauvegarde des parties en base de données**
- 🕹️ **Mode multijoueur en ligne**

---

## 📝 Auteurs

Projet réalisé par **[Shahzad Abdul Rahman]** dans le cadre d'un apprentissage sur l'IA et le jeu Othello.

📧 Contact : [shd.abdul29@example.com]

---

## 🏆 Licence

Ce projet est sous licence MIT - Vous êtes libre de l'utiliser et de le modifier à votre convenance.
