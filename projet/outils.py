
import random
import pygame
from class_salle import *
from contexte import *


def creer_labyrinthe(nombre):
    racine = Salle(None, 1)
    salles = [racine]

    for i in range(nombre-1):
        possibles = []

        # On ajoute tous les fils disponibles dans la liste des possibilités
        for salle in salles:
            for numero in range(1, 5):
                if numero == 1:
                    fils = salle.f1
                elif numero == 2:
                    fils = salle.f2
                elif numero == 3:
                    fils = salle.f3
                else:
                    fils = salle.f4

                if fils is None:
                    possibles.append((salle, numero))

        # S'il n'y a plus de possibilité, on arrête
        if not possibles:
            break

        parent, numero = random.choice(possibles)
        if i ==nombre-2:
            parent.set_fils(numero,3)
        else:
            parent.set_fils(numero, 1)

        # On récupère l'enfant qui vient d'être créé
        if numero == 1:
            enfant = parent.f1
        elif numero == 2:
            enfant = parent.f2
        elif numero == 3:
            enfant = parent.f3
        else:
            enfant = parent.f4

        salles.append(enfant)

    return racine, salles


def demander_nombre_salles():
    nombre = ""
    message_erreur = ""

    while True:
        for evenement in pygame.event.get():

            if evenement.type == pygame.QUIT:
                return None

            if evenement.type == pygame.KEYDOWN:

                if evenement.key == pygame.K_ESCAPE:
                    return None

                elif evenement.key == pygame.K_RETURN:
                    if nombre.isdigit() and int(nombre) >= 1:
                        return int(nombre)
                    else:
                        message_erreur = "Entre un nombre entier positif."

                elif evenement.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                    message_erreur = ""

                # Vérifie qu'on tape un chiffre et que le nombre ne dépasse pas 5 chiffres
                elif evenement.unicode.isdigit() and len(nombre) < 5:
                    nombre += evenement.unicode
                    message_erreur = ""

        # Fond de l'écran
        ecran.fill(FOND)

        # Titre du jeu
        texte("LABYRINTHE QUATERNAIRE", LARGEUR // 2, 100, BLEU, police, centrer=True)

        # Question
        texte("Combien de salles veux-tu creer ?", LARGEUR // 2, 190, BLANC, police, centrer=True)

        # Champ de saisie
        champ = pygame.Rect(LARGEUR // 2 - 150, 240, 300, 55)
        pygame.draw.rect(ecran, BLANC, champ, 2, border_radius=5)

        # Nombre écrit dans le champ
        texte(nombre, champ.centerx, champ.centery, BLANC, police, centrer=True)

        # Indication
        texte("Tape un nombre puis appuie sur Entree", LARGEUR // 2, 335, GRIS, petite_police, centrer=True)

        # Quitter
        texte("Echap : quitter", LARGEUR // 2, 375, GRIS, petite_police, centrer=True)

        # Message d'erreur
        if message_erreur:
            texte(message_erreur, LARGEUR // 2, 430, ROUGE, petite_police, centrer=True)

        pygame.display.flip()
        horloge.tick(30)


def texte(message, x, y, couleur=BLANC, police_utilisee=None, centrer=False):

    # Choisit la police par défaut
    if police_utilisee is None:
        police_utilisee = police

    # Transforme le texte en image
    image = police_utilisee.render(str(message), True, couleur)

    # Affiche le texte centré ou normalement
    if centrer:
        rectangle = image.get_rect(center=(x, y))
        ecran.blit(image, rectangle)
    else:
        ecran.blit(image, (x, y))
