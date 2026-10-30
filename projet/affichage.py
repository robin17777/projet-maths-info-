import pygame
from contexte import *
from outils import *



def afficher(actuelle, salles):

    boutons.clear()
    boutons_salles.clear()

    ecran.fill(FOND)

    texte("Information labyrinthe :",20, 105,BLANC,police)
    texte(f"Nombre de salles : {len(salles)}",20, 145,BLANC,petite_police)
    texte(f"Profondeur actuelle : {actuelle.get_profondeur()}", 20, 165,BLANC,petite_police)
    texte(f"Profondeur max : {profondeur_max(salles)}", 20, 185,BLANC,petite_police)

    dessiner_salle(actuelle, salles)

    pygame.display.flip()


def dessiner_salle(salle, salles):
    global boutons_salles
    boutons.clear()

    y_pere = 245

    positions_x = [195, 315, 435, 555] # des 4 fils sur la largeur 
    y_fils = 440

    types = salle.voir_suivant()

    #bouton parametre
    settings=pygame.Rect(LARGEUR-150, 20, 130, 40)
    pygame.draw.rect(ecran, BLEU, settings, border_radius=10)
    texte("Parametres", settings.centerx, settings.centery, GRISF, petite_police, centrer=True)
    boutons.append((settings, "parametres"))

    #bouton autre lab
    autre_lab=pygame.Rect(20, 20, 145, 40)
    pygame.draw.rect(ecran, BLEU, autre_lab, border_radius=10)
    texte("Autre labyrinhte", autre_lab.centerx, autre_lab.centery, GRISF, petite_police, centrer=True)
    boutons.append((autre_lab, "autrelab"))

    #bouton nouveau lab
    nv_lab=pygame.Rect(185, 20, 176, 40)
    pygame.draw.rect(ecran, BLEU, nv_lab, border_radius=10)
    texte("Nouveau labyrinhte", nv_lab.centerx, nv_lab.centery, GRISF, petite_police, centrer=True)
    boutons.append((nv_lab, "nvlab"))

    # Branches entre le pere et les fils
    for i in range(4):
        couleur = VERT if types[i] == 1 else GRIS
                        #quel ecran , la couleur, coord x , cord y , epaisseur de la ligne
        pygame.draw.line(ecran,couleur,(LARGEUR//4, y_pere + 25),(positions_x[i], y_fils - 25),4)

    # Bouton du noeud pere
                      #rectangle(coord x,coord y,longueur,hauteur)
    rect_pere = pygame.Rect(LARGEUR//4 - 75, y_pere - 25, 150, 50)
                                            #arrondi sur les coin du rectangle de 10 pixel
    pygame.draw.rect(ecran, JAUNE if salle.get_type_fils()==3 else ORANGE, rect_pere, border_radius=10)
    if salle.get_type_fils()==3:
        text="Sortie"
    else:
        identifiant = salles.index(salle) + 1
        text=f"Salle {identifiant}"

    texte(text, rect_pere.centerx, rect_pere.centery, GRISF, police, centrer=True)
                    #pour avoir les coord du centre du rectangle
    """Ici jusqu'a la fin ca sert pour les boutons_salles"""               
    # Le clic sur le pere permet de remonter
    boutons_salles.append((rect_pere, 0))

    # Les quatre boutons_salles fils
    for i in range(4):
        x = positions_x[i]
        numero = i + 1

        accessible = types[i] == 1 or types[i]==3

        if types[i] == 1:
            couleur = VERT
        elif types[i]==3:
            couleur = JAUNE
        else:
            couleur=GRIS
                

        rect_fils = pygame.Rect(x - 55, y_fils - 25, 110, 50)

        pygame.draw.rect(ecran, couleur, rect_fils, border_radius=10)
        if types[i] == 1:
            nom_fils =f"Fils {numero}"
        elif types[i]==3:
            nom_fils = "Sortie"
        else:
            nom_fils ="Mur"
        texte(nom_fils, rect_fils.centerx, rect_fils.centery, GRISF, petite_police, centrer=True)

        #pour mettre le chiffre a taper sous chaque fils 
        texte(numero, x, y_fils + 45, BLANC, petite_police, centrer=True)

        # Seules les salles accessibles sont cliquables
        if accessible:
            boutons_salles.append((rect_fils, numero))


def afficher_parametres():
    ecran.fill(FOND)
    boutons.clear()

    texte("PARAMETRES", LARGEUR // 2, 80, BLEU, police, centrer=True)

    # Bouton retour
    retour = pygame.Rect(LARGEUR-150, 20, 130, 40)
    pygame.draw.rect(ecran, BLEU, retour, border_radius=10)
    texte("Retour", retour.centerx, retour.centery, GRISF, petite_police, centrer=True)
    boutons.append((retour, "retour"))

    texte("Touches et navigation :", LARGEUR // 2, 180, BLANC, grande_police, centrer=True)

    texte("Le noeud du haut est la salle actuelle",LARGEUR // 2, 220,BLEU,police, centrer=True)

    texte("Touches 1, 2, 3, 4 : acceder aux fils verts",LARGEUR // 2,250, VERT,police, centrer=True)

    texte("Touche 0 : retourner au pere",LARGEUR // 2, 280, ORANGE,police, centrer=True)

    texte("Echap : quitter",LARGEUR // 2, 310, BLANC,police, centrer=True)

    pygame.display.flip()

def afficher_gagne():
    ecran.fill(FOND)
    boutons.clear()

    texte("VOUS AVEZ GAGNÉ", LARGEUR // 2, 80, JAUNE, grande_police, centrer=True)

    autre_lab = pygame.Rect(LARGEUR//2 - 100, HAUTEUR//2 - 50, 200, 40)
    pygame.draw.rect(ecran, BLEU, autre_lab, border_radius=10)
    texte("Autre labyrinthe", autre_lab.centerx, autre_lab.centery, GRISF, petite_police, centrer=True)
    boutons.append((autre_lab, "autrelab"))


    nv_lab = pygame.Rect(LARGEUR//2 - 100, HAUTEUR//2 + 20, 200, 40)
    pygame.draw.rect(ecran, BLEU, nv_lab, border_radius=10)
    texte("Nouveau labyrinthe", nv_lab.centerx, nv_lab.centery, GRISF, petite_police, centrer=True)
    boutons.append((nv_lab, "nvlab"))

    pygame.display.flip()