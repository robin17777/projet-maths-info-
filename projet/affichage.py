import pygame
from contexte import *
from outils import *

def afficher_parametres():
    ecran.fill(FOND)

    titre = police.render("PARAMETRES", True, BLEU)
    ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, 80)))

    # Bouton retour
    retour = pygame.Rect(20, 20, 120, 40)
    pygame.draw.rect(ecran, BLEU, retour, border_radius=10)
    txt_retour = petite_police.render("Retour", True, GRISF)
    ecran.blit(txt_retour, txt_retour.get_rect(center=retour.center))
    boutons.append((retour, "retour"))

    texte("Le noeud du haut est la salle actuelle",20, 490, BLANC, petite_police)

    texte("Touches 1, 2, 3, 4 : acceder aux fils verts",20, 510, BLANC, petite_police)

    texte("Touche 0 : retourner au pere",20, 530, BLANC, petite_police)

    texte("Echap : quitter",20, 550, BLANC, petite_police)

    pygame.display.flip()

def dessiner_salle(salle, salles):
    global boutons_salles

    centre_x = LARGEUR // 2
    y_pere = 155

    positions_x = [110, 303, 496, 689] # des 4 fils sur la largeur 
    y_fils = 340

    types = salle.voir_suivant()



    #bouton parametre
    settings=pygame.Rect(650, 20, 130, 40)
    pygame.draw.rect(ecran, BLEU, settings, border_radius=10)
    txt_para=petite_police.render("Parametres",True,GRISF)
    ecran.blit(txt_para, txt_para.get_rect(center=settings.center))
    boutons.append((settings, "parametres"))



    # Branches entre le pere et les fils
    for i in range(4):
        couleur = VERT if types[i] == 1 else GRIS
                        #quel ecran , la couleur, coord x , cord y , epaisseur de la ligne
        pygame.draw.line(ecran,couleur,(centre_x, y_pere + 25),(positions_x[i], y_fils - 25),4)

    # Bouton du noeud pere
                      #rectangle(coord x,coord y,longueur,hauteur)
    rect_pere = pygame.Rect(centre_x - 75, y_pere - 25, 150, 50)
                                            #arrondi sur les coin du rectangle de 10 pixel
    pygame.draw.rect(ecran, BLEU, rect_pere, border_radius=10)

    identifiant = salles.index(salle) + 1 #pour avoir le num de la salle avec son indexe dans la liste
    nom = police.render(f"Salle {identifiant}", True, GRISF)
    ecran.blit(nom, nom.get_rect(center=rect_pere.center))
                    #pour avoir les coord du centre du rectangle
    """Ici jusqu'a la fin ca sert pour les boutons_salles"""               
    # Le clic sur le pere permet de remonter
    boutons_salles.append((rect_pere, 0))

    # Les quatre boutons_salles fils
    for i in range(4):
        x = positions_x[i]
        numero = i + 1

        accessible = types[i] == 1
        couleur = VERT if accessible else GRIS

        rect_fils = pygame.Rect(x - 55, y_fils - 25, 110, 50)

        pygame.draw.rect(ecran, couleur, rect_fils, border_radius=10)

        nom_fils = (f"Fils {numero}" if accessible else "Mur")

        texte_fils = petite_police.render(nom_fils, True, GRISF)

        ecran.blit(texte_fils,texte_fils.get_rect(center=rect_fils.center))
        #pour mettre le chiffre a taper sous chaque fils 
        touche = petite_police.render(str(numero), True, BLANC)

        ecran.blit(touche,touche.get_rect(center=(x, y_fils + 45)))

        # Seules les salles accessibles sont cliquables
        if accessible:
            boutons_salles.append((rect_fils, numero))


def afficher(actuelle, salles):

    boutons.clear()
    boutons_salles.clear()

    ecran.fill(FOND)

    titre = police.render("LABYRINTHE QUATERNAIRE", True, BLEU)

    ecran.blit(titre,titre.get_rect(center=(LARGEUR // 2, 35)))

    texte(f"Nombre de salles : {len(salles)}",20, 75)

    dessiner_salle(actuelle, salles)



    pygame.display.flip()


