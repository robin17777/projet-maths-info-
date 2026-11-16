<div align="center">

# 🏰 Labyrinthe quaternaire

**Un jeu d'exploration en pixel art où le labyrinthe est un arbre à quatre branches.**

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-34D399)
![Statut](https://img.shields.io/badge/statut-en%20d%C3%A9veloppement-F59E0B)

*Explorez les salles, ramassez des objets, trouvez la sortie.*

</div>

<!--
  💡 Ajoutez ici une capture d'écran du jeu :
  <p align="center"><img src="docs/capture.png" width="700" alt="Capture du jeu"></p>
-->

---

## ✨ Le principe

Chaque labyrinthe est généré aléatoirement sous la forme d'un **arbre quaternaire** : chaque salle possède **jusqu'à 4 fils** (haut, droite, bas, gauche). Un côté sans salle est un **mur**.

Vous commencez dans la salle de départ, vous explorez en descendant dans l'arbre, et vous gagnez en atteignant la **salle de sortie**.

Un panneau d'information vous indique en permanence :

- le **nombre de salles** du labyrinthe,
- la **profondeur actuelle** et la **profondeur maximale**,
- le **chemin emprunté** depuis le début.

Un schéma de l'arbre est affiché à gauche : le nœud du haut est votre salle actuelle, les quatre nœuds du bas sont ses fils (verts = salle, gris = mur, jaune = sortie).

---

## 🎮 Fonctionnalités

| | |
|---|---|
| 🌳 **Labyrinthes aléatoires** | Choisissez le nombre de salles, puis régénérez ou changez de labyrinthe à volonté |
| 🧍 **Aventurier déplaçable** | Déplacez-le dans la salle pour atteindre une porte ou un objet |
| 🎒 **Inventaire à 5 cases** | Ramassez, sélectionnez et utilisez des objets |
| 🗡️ **Objets** | Épée (3 usages), potion de soin, clé |
| 📊 **Barre de durabilité** | Les objets à plusieurs usages affichent ce qu'il leur reste |
| 🧭 **Historique du trajet** | Suivez votre chemin, ou repartez d'un nouveau point de départ |
| 🖱️ **Clavier ou souris** | Presque toutes les actions sont accessibles des deux façons |

---

## 🕹️ Commandes

| Touche | Action |
|:---:|---|
| `1` `2` `3` `4` | Aller dans le fils correspondant (uniquement les fils accessibles) |
| `0` | Retourner à la salle père |
| `↑` `←` `↓` `→` &nbsp;ou&nbsp; `Z` `Q` `S` `D` | Déplacer l'aventurier dans la salle |
| `Entrée` | Entrer dans la salle quand l'aventurier se tient sur une porte |
| `E` | Ramasser l'objet sous l'aventurier |
| `5` `6` `7` `8` `9` | Sélectionner la case 1 à 5 de l'inventaire (re-appuyer désélectionne) |
| `Échap` | Quitter |

**Boutons à l'écran :** `Entrer`, `Récupérer`, `Utiliser` (objet sélectionné), `Autre labyrinthe`, `Nouveau labyrinthe`, `Réinitialiser l'historique` et `Paramètres` (rappel des touches).

---

## 🗂️ Structure du projet

```
.
├── main.py              # Boucle principale, gestion des touches et des clics
├── affichage.py         # Dessin de la salle, de l'inventaire, des écrans (paramètres, victoire)
├── class_salle.py       # Classe Salle : un nœud de l'arbre à 4 fils
├── class_objet.py       # Classe Objet et placement aléatoire des objets
├── class_inventaire.py  # Classe Inventaire : ajout, sélection, utilisation
├── outils.py            # Génération du labyrinthe, saisie, texte, images, historique
├── contexte.py          # Fenêtre, polices et couleurs
└── textures/
    ├── terrain/         # Salles et murs
    ├── personnage/      # L'aventurier
    ├── objet/           # Épée, potion, clé
    ├── hud/             # Cadre de l'inventaire
    └── key/             # Icônes des touches
```

---

## 🧠 Comment ça marche

- **Arbre de salles :** chaque `Salle` garde un lien vers son père et ses quatre fils `f1` à `f4`. Le type d'un fils vaut `0` (mur), `1` (salle) ou `3` (sortie).
- **Génération :** à chaque étape, une place libre est choisie au hasard parmi toutes les salles déjà créées, ce qui donne des labyrinthes différents à chaque partie. La dernière salle créée est la sortie.
- **Objets :** ils sont placés au hasard dans les salles intermédiaires, jamais dans la salle de départ ni dans la sortie.
- **Durabilité :** chaque objet retient son nombre d'usages de départ, ce qui permet de dessiner la barre qui se vide à chaque utilisation.

---

## 🛣️ Pistes d'amélioration

- [ ] Donner un vrai effet aux objets (soin, ouverture de portes avec la clé…)
- [ ] Ajouter des ennemis à combattre avec l'épée
- [ ] Sauvegarder et recharger un labyrinthe
- [ ] Ajouter des sons et de la musique

---

<div align="center">

Fait avec 🐍 Python et Pygame

</div>
