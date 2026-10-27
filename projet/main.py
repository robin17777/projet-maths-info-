import pygame
from contexte import *
from outils import *
from affichage import *

# =========================
# LANCEMENT
# =========================

nombre = demander_nombre_salles()

if nombre is None:
    pygame.quit()
    raise SystemExit

racine, salles = creer_labyrinthe(nombre)
actuelle = racine

ecran_actuel = "labyrinthe"
actif = True

while actif:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            actif = False
        #pour les touches préssées au clavier 
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_ESCAPE:
                actif = False
            elif ecran_actuel == "labyrinthe":
                #pour acceder au salle avec les boutons_salles 1,2,3,4
                if evenement.key in (pygame.K_0, pygame.K_KP0):
                    actuelle = actuelle.acceder_salle(0)

                elif evenement.key in (pygame.K_1, pygame.K_KP1):
                    actuelle = actuelle.acceder_salle(1)

                elif evenement.key in (pygame.K_2, pygame.K_KP2):
                    actuelle = actuelle.acceder_salle(2)

                elif evenement.key in (pygame.K_3, pygame.K_KP3):
                    actuelle = actuelle.acceder_salle(3)

                elif evenement.key in (pygame.K_4, pygame.K_KP4):
                    actuelle = actuelle.acceder_salle(4)
        #   fait de  meme mais pour avoir la version clickable
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if evenement.button == 1: #voir si c'est le clic gauche 
                position = evenement.pos #position du clic coord x et y 
                if ecran_actuel == "labyrinthe":
                    for rectangle, numero in boutons_salles:
                        if rectangle.collidepoint(position): #verifie qu'on ai bien cliqué dans un recatngle 
                            if numero == 0:
                                actuelle = actuelle.acceder_salle(0)
                            else:
                                actuelle = actuelle.acceder_salle(numero)

                            break

                for rectangle, action in boutons:
                    if rectangle.collidepoint(position):
                        if action == "parametres":
                            ecran_actuel="parametres"
                        elif action == "retour":
                            ecran_actuel = "labyrinthe"
                            
                        break

    if ecran_actuel == "labyrinthe":
        afficher(actuelle, salles)

    elif ecran_actuel == "parametres":
        afficher_parametres()

    horloge.tick(60)

pygame.quit()