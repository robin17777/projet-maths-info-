import random
import pygame
from class_salle import *
from contexte import *
from rendu import *


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

        ecran.blit(FOND_DEGRADE, (0, 0))

        texte("LABYRINTHE QUATERNAIRE", LARGEUR // 2, 100, BLEU, titre_police, centrer=True)
        pygame.draw.line(ecran, GRIS, (LARGEUR // 2 - 120, 150), (LARGEUR // 2 + 120, 150), 2)

        carte = pygame.Rect(LARGEUR // 2 - 300, 190, 600, 330)
        panneau(carte)

        texte("Combien de salles veux-tu creer ?", LARGEUR // 2, 245, BLANC, police, centrer=True)

        champ = pygame.Rect(LARGEUR // 2 - 150, 285, 300, 60)
        lueur(champ, BLEU, 10, 10)
        pygame.draw.rect(ecran, FOND, champ, border_radius=10)
        pygame.draw.rect(ecran, BLEU, champ, 2, border_radius=10)

        texte(nombre, champ.centerx, champ.centery, BLANC, grande_police, centrer=True)
        
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            largeur_texte = grande_police.size(nombre)[0] if nombre else 0
            x_curseur = champ.centerx + largeur_texte // 2 + 4
            pygame.draw.line(ecran, BLEU, (x_curseur, champ.centery - 16), (x_curseur, champ.centery + 16), 2)
        texte("Tape un nombre puis appuie sur Entree", LARGEUR // 2, 385, GRIS, petite_police, centrer=True)
        if message_erreur:
            texte(message_erreur, LARGEUR // 2, 430, ROUGE, petite_police, centrer=True)

        texte("Echap pour quitter", LARGEUR // 2, 490, GRIS, petite_police, centrer=True)

        pygame.display.flip()
        horloge.tick(30)



def creer_labyrinthe(nombre):
    racine = Salle(None, 1)
    salles = [racine]
    for i in range(nombre-1):
        possibles = []
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
        if not possibles:
            break
        parent, numero = random.choice(possibles)
        if i ==nombre-2:
            parent.set_fils(numero,3)
        else:
            parent.set_fils(numero, 1)
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



def image(ecran, chemin, position, taille=None, angle=0):
    img = pygame.image.load(chemin).convert_alpha()

    if taille is not None:
        img = pygame.transform.scale(img, taille)

    if angle != 0:
        img = pygame.transform.rotate(img, angle)

    rect = img.get_rect(center=position)
    ecran.blit(img, rect)


def profondeur_max(salles):
    maximum = 0

    for salle in salles:
        if salle.get_profondeur() > maximum:
            maximum = salle.get_profondeur()
    return maximum