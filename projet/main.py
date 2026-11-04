import pygame
from contexte import *
from outils import *
from affichage import *
import affichage

"""
parcour profondeur
quel chemin le meilleur 
ajouter objet monstres et portes bloqués
"""

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

                elif evenement.key == pygame.K_DOWN:
                    if affichage.cord_y+50>=720:
                        affichage.cord_y=720
                    else:
                        affichage.cord_y+=50

                elif evenement.key == pygame.K_UP:
                    if affichage.cord_y-50<=370:
                        affichage.cord_y=370
                    else:
                        affichage.cord_y-=50

                elif evenement.key == pygame.K_LEFT:
                    if affichage.cord_x-50<=950:
                        affichage.cord_x=950
                    else:
                        affichage.cord_x-=50

                elif evenement.key == pygame.K_RIGHT:
                    if affichage.cord_x+50>=1350:
                        affichage.cord_x=1350
                    else:
                        affichage.cord_x+=50

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
                        if action == "parametres" and ecran_actuel=="labyrinthe":
                            ecran_actuel="parametres"
                        elif action == "retour" and ecran_actuel =="parametres":
                            ecran_actuel = "labyrinthe"
                        elif action == "autrelab" and ecran_actuel=="labyrinthe":
                            racine, salles = creer_labyrinthe(nombre)
                            actuelle = racine
                            passages_visites.clear()
                            passages_visites.append(5)
                            affichage.cord_x=1150
                            affichage.cord_y=550
                        elif action == "nvlab" and ecran_actuel=="labyrinthe":
                            racine, salles = creer_labyrinthe(demander_nombre_salles())
                            actuelle = racine
                            passages_visites.clear()
                            passages_visites.append(5)
                            affichage.cord_x=1150
                            affichage.cord_y=550
                        break
        
    if actuelle.get_type_fils() == 3 and ecran_actuel == "labyrinthe":
        afficher_gagne()

    elif ecran_actuel == "labyrinthe":
        afficher(actuelle, salles)

    elif ecran_actuel == "parametres":
        afficher_parametres()


    horloge.tick(60)

pygame.quit()
