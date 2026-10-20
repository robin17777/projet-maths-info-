# 🎮 Labyrinthe quaternaire

## 📌 Présentation

Ce projet consiste à créer un **labyrinthe quaternaire en Python**, représenté sous la forme d'un arbre dans lequel chaque salle peut posséder jusqu'à quatre salles filles.

L'utilisateur choisit le nombre de salles à générer, puis explore le labyrinthe grâce à une interface graphique réalisée avec **Pygame**. La navigation est possible au clavier ou à la souris.

## ✨ Fonctionnalités

- 🌳 **Génération aléatoire** : création d'un labyrinthe composé du nombre de salles choisi par l'utilisateur.
- 🧩 **Structure arborescente** : chaque salle peut avoir jusqu'à quatre salles filles.
- 🚪 **Gestion des murs** : les directions sans salle fille sont représentées par des murs.
- 🎮 **Navigation au clavier** : déplacement entre les salles à l'aide des touches `0`, `1`, `2`, `3` et `4`.
- 🖱️ **Interface interactive** : possibilité de cliquer sur les salles accessibles pour se déplacer.
- 🔙 **Retour à la salle précédente** : possibilité de remonter vers la salle parente.
- 🖥️ **Interface graphique** : affichage de la salle actuelle, des salles filles et des directions accessibles.

## 🛠️ Technologies utilisées

- **Python 3**
- **Pygame** : gestion de la fenêtre, des événements, des dessins et des interactions.
- **Random** : génération aléatoire de la structure du labyrinthe.

## 🎯 Utilisation

1. Lancez le programme.
2. Entrez le nombre de salles souhaité.
3. Appuyez sur `Entrée` pour générer le labyrinthe.
4. Explorez les salles à l'aide du clavier ou de la souris.

### Commandes

| Touche | Action |
|---|---|
| `0` | Retourner à la salle parente |
| `1` | Accéder à la salle fille 1 |
| `2` | Accéder à la salle fille 2 |
| `3` | Accéder à la salle fille 3 |
| `4` | Accéder à la salle fille 4 |
| `Échap` | Quitter le programme |

Les salles accessibles sont affichées en vert. Les directions sans salle fille sont représentées en gris.

## 🧠 Fonctionnement technique

### La classe `Salle`

Chaque salle est représentée par un objet de la classe `Salle`, qui contient :

- Un type de nœud : salle ou mur.
- Une référence vers sa salle parente.
- Quatre références vers ses salles filles (`f1`, `f2`, `f3` et `f4`).

Cette organisation permet de représenter le labyrinthe sous la forme d'un **arbre quaternaire**.

### La génération du labyrinthe

La fonction `creer_labyrinthe(nombre)` :

1. Crée une salle racine.
2. Recherche les emplacements disponibles parmi les salles existantes.
3. Choisit aléatoirement un emplacement libre.
4. Crée une nouvelle salle fille.
5. Répète ces étapes jusqu'à atteindre le nombre de salles demandé.

### La navigation

La méthode `acceder_salle(x)` permet de se déplacer dans l'arbre :

- `0` permet de remonter vers le parent.
- `1`, `2`, `3` et `4` permettent d'accéder aux salles filles correspondantes, lorsqu'elles existent.

Si le déplacement demandé est impossible, l'utilisateur reste dans la salle actuelle.

## 🚀 Améliorations possibles

- Ajouter un système de sortie et un objectif à atteindre.
- Afficher le chemin parcouru par le joueur.
- Ajouter une carte générale du labyrinthe.
- Permettre de recommencer une partie avec une nouvelle génération.
- Ajouter un compteur de déplacements.
- Améliorer la représentation graphique des salles et des murs.
- une sorte de menu principal avec des options
