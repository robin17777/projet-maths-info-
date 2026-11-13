import pygame
from contexte import *
from outils import *
from affichage import *
from class_inventaire import *
import affichage
import class_objet


# touches 5 à 9 (clavier principal ou pavé numérique) -> numéro de case de l'inventaire
TOUCHES_INVENTAIRE = {
    pygame.K_5: 0, pygame.K_KP5: 0,
    pygame.K_6: 1, pygame.K_KP6: 1,
    pygame.K_7: 2, pygame.K_KP7: 2,
    pygame.K_8: 3, pygame.K_KP8: 3,
    pygame.K_9: 4, pygame.K_KP9: 4,
}

def indice_touche_inventaire(evenement):
    if evenement.key in TOUCHES_INVENTAIRE:
        return TOUCHES_INVENTAIRE[evenement.key]
    # clavier AZERTY : chiffre tapé avec Maj, pygame renvoie alors le caractère
    if evenement.unicode in ("5", "6", "7", "8", "9"):
        return int(evenement.unicode) - 5
    return None

def ramasser_objet(salle):
    """Ramasse l'objet qui est sous l'aventurier (bouton Récupérer ou touche E)."""
    rect_av = pygame.Rect((affichage.cord_x - 10, affichage.cord_y - 10), (25, 25))
    for objet in class_objet.objets:
        if objet.est_sous(rect_av, salle):
            if inventaire.ajouter(objet):
                class_objet.objets.remove(objet)
            break

nombre = demander_nombre_salles()

if nombre is None:
    pygame.quit()
    raise SystemExit

racine, salles = creer_labyrinthe(nombre)
class_objet.placer_objets(salles)
inventaire = Inventaire()
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

                elif evenement.key in (pygame.K_s,pygame.K_DOWN):
                    if affichage.cord_y+25>=720:
                        affichage.cord_y=720
                    else:
                        affichage.cord_y+=25

                elif evenement.key in (pygame.K_z,pygame.K_UP):
                    if affichage.cord_y-25<=370:
                        affichage.cord_y=370
                    else:
                        affichage.cord_y-=25

                elif evenement.key in (pygame.K_q,pygame.K_LEFT):
                    if affichage.cord_x-25<=950:
                        affichage.cord_x=950
                    else:
                        affichage.cord_x-=25

                elif evenement.key in (pygame.K_d,pygame.K_RIGHT):
                    if affichage.cord_x+25>=1350:
                        affichage.cord_x=1350
                    else:
                        affichage.cord_x+=25

                elif evenement.key == pygame.K_e:
                    ramasser_objet(actuelle)

                elif indice_touche_inventaire(evenement) is not None:
                    inventaire.selectionner(indice_touche_inventaire(evenement))

                if evenement.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                                        zone = affichage.zone_aventurier(actuelle,racine)
                                        if zone is not None:
                                            nouvelle = actuelle.acceder_salle(zone)
                                            if nouvelle is not actuelle:
                                                actuelle = nouvelle
                                                affichage.cord_x = 1150
                                                affichage.cord_y = 480

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
                            class_objet.placer_objets(salles)
                            inventaire.vider()
                            actuelle = racine
                            passages_visites.clear()
                            passages_visites.append(5)
                            affichage.cord_x=1150
                            affichage.cord_y=480
                        elif action == "nvlab" and ecran_actuel=="labyrinthe":
                            nouveau_nombre = demander_nombre_salles()
                            if nouveau_nombre is not None:
                                nombre = nouveau_nombre
                                racine, salles = creer_labyrinthe(nombre)
                                class_objet.placer_objets(salles)
                                inventaire.vider()
                                actuelle = racine
                                passages_visites.clear()
                                passages_visites.append(5)
                                affichage.cord_x=1150
                                affichage.cord_y=480
                        elif action=="reset" and ecran_actuel=="labyrinthe":
                            passages_visites.clear()
                            passages_visites.append(6)
                        elif action == "rentrer" and ecran_actuel == "labyrinthe":
                            zone = affichage.zone_aventurier(actuelle,racine)
                            if zone is not None:
                                nouvelle = actuelle.acceder_salle(zone)
                                if nouvelle is not actuelle:
                                    actuelle = nouvelle
                                    affichage.cord_x = 1150
                                    affichage.cord_y = 480
                        elif action == "utiliser" and ecran_actuel == "labyrinthe":
                            inventaire.utiliser_selection()
                        elif action == "recuperer" and ecran_actuel == "labyrinthe":
                            ramasser_objet(actuelle)
                        break
        
        
    if actuelle.get_type_fils() == 3 and ecran_actuel == "labyrinthe":
        afficher_gagne()

    elif ecran_actuel == "labyrinthe":
        afficher(actuelle, salles, racine,class_objet.objets,inventaire)

    elif ecran_actuel == "parametres":
        afficher_parametres()


    


    horloge.tick(60)

pygame.quit()