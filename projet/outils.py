import random
import pygame
from class_salle import *
from contexte import *

def creer_labyrinthe(nombre):
    racine = Salle(None, 1)
    salles = [racine]

    while len(salles) < nombre:
        possibles = []
        for salle in salles: # on vient ajouter tout les fils dans la liste des possibilités
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
        if not possibles: #si y'a pas de possibilité on stop mais ca devrait jamais arriver
            break
        parent, numero = random.choice(possibles) # parent prend le parent de la salle et numero son fils de dispo
        parent.set_fils(numero, 1)
        #cette partie ajouter a la liste salle l'enfant qui vient d'être créé 
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
                #verifie que on tape bien un chiffre et que le nombre depasse pas 5 chiffre
                elif evenement.unicode.isdigit() and len(nombre) < 5:
                    nombre += evenement.unicode
                    message_erreur = ""

        ecran.fill(FOND)

        titre = police.render("LABYRINTHE QUATERNAIRE",True,BLEU)

        ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, 100)))

        question = police.render("Combien de salles veux-tu creer ?",True,BLANC)

        ecran.blit(question, question.get_rect(center=(LARGEUR // 2, 190)))

        # Champ de saisie
        champ = pygame.Rect(250, 240, 300, 55)
        pygame.draw.rect(ecran, BLANC, champ, 2, border_radius=5)

        contenu = police.render(nombre, True, BLANC)
        ecran.blit(contenu, contenu.get_rect(center=champ.center))

        aide = petite_police.render("Tape un nombre puis appuie sur Entree",True,GRIS)

        ecran.blit(aide, aide.get_rect(center=(LARGEUR // 2, 335)))

        sortie = petite_police.render("Echap : quitter",True,GRIS)

        ecran.blit(sortie, sortie.get_rect(center=(LARGEUR // 2, 375)))

        if message_erreur:
            erreur = petite_police.render(message_erreur, True, ROUGE)
            ecran.blit(erreur,erreur.get_rect(center=(LARGEUR // 2, 430)))

        pygame.display.flip() #pour afficher la chose 
        horloge.tick(30)

def texte(message, x, y, couleur=BLANC, police_utilisee=None):
    #pour la police d'écriture
    if police_utilisee is None:
        police_utilisee = police
    #pour transformer le texte en image a afficher
    image = police_utilisee.render(str(message), True, couleur) #true pour rendre le texte plus lissible 
    ecran.blit(image, (x, y))