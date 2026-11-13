import pygame
from contexte import *
from outils import *



cord_x=1150   # 1150 base
cord_y=480    # 480 base 

#/!\/!\/!\/!\DEBUT IA /!\/!\/!\/!\ parce que c'est pas important juste pour synchro les item sur les slots 
# --- Cases de l'inventaire (mesurées sur inventaire.png) ---
INV_CENTRE = (1150, 180)        # où l'image est dessinée à l'écran
INV_TAILLE = (600, 188)         # taille d'affichage de l'image
INV_IMG = (2172, 724)           # taille réelle du fichier inventaire.png
# centre de chaque carré, en pixels dans le fichier inventaire.png
SLOTS_IMG = [(400, 365), (730, 365), (1082, 365), (1432, 365), (1764, 365)]
SLOT_COTE = 56                  # taille (à l'écran) de la zone où l'objet est dessiné
AFFICHER_SLOTS = False          # True : dessine le contour des cases pour vérifier

def _slot(cx, cy):
    x = INV_CENTRE[0] - INV_TAILLE[0] // 2 + cx * INV_TAILLE[0] / INV_IMG[0]
    y = INV_CENTRE[1] - INV_TAILLE[1] // 2 + cy * INV_TAILLE[1] / INV_IMG[1]
    rect = pygame.Rect(0, 0, SLOT_COTE, SLOT_COTE)
    rect.center = (round(x), round(y))
    return rect

SLOTS_INVENTAIRE = [_slot(cx, cy) for cx, cy in SLOTS_IMG]
#fin IA /!\ /!\ /!\ /!\ /!\ /!\ /!\



# Zones d'accès (au niveau du module pour être utilisables partout)
case_haut = pygame.Rect(1125, 345, 55, 55)
case_bas = pygame.Rect(1123, 700, 55, 55)
case_gauche = pygame.Rect(935, 520, 55, 55)
case_droite = pygame.Rect(1315, 520, 55, 55)
case_milieu = pygame.Rect(1125, 525, 50, 50)

def zone_aventurier(salle,racine):
    rect = pygame.Rect((cord_x - 10, cord_y - 10), (25, 25))
    types = salle.voir_suivant()
    if rect.colliderect(case_haut) and types[0]!= 0:
        return 1
    if rect.colliderect(case_droite)and types[1]!= 0:
        return 2
    if rect.colliderect(case_bas)and types[2]!= 0:
        return 3
    if rect.colliderect(case_gauche)and types[3]!= 0:
        return 4
    if rect.colliderect(case_milieu) and salle != racine:
        return 0
    return None

def afficher(actuelle, salles, racine,objets,inventaire):

    boutons.clear()
    boutons_salles.clear()
    boutond.clear()

    ecran.fill(FOND)

    texte("Information labyrinthe :",20, 125,BLANC,police)
    texte(f"Nombre de salles : {len(salles)}",20, 165,BLANC,petite_police)
    texte(f"Profondeur actuelle : {actuelle.get_profondeur()}", 20, 185,BLANC,petite_police)
    texte(f"Profondeur max : {profondeur_max(salles)}", 20, 205,BLANC,petite_police)
    texte_multiligne(f"Chemin enprunté : {historique()}", 20, 550,BLANC,petite_police,90)

    dessiner_salle(actuelle, salles,racine,objets,inventaire)

    pygame.display.flip()


def dessiner_salle(salle, salles,racine,objets,inventaire):
    global boutons_salles
    boutons.clear()
    boutond.clear()


    souris = pygame.mouse.get_pos()
    y_pere = 245
    positions_x = [195, 315, 435, 555] # des 4 fils sur la largeur 
    y_fils = 440

    types = salle.voir_suivant()

    #image salle 
    if salle==racine:
        image(ecran, "textures/terrain/salle_vide.png", (1150, 550), (700, 700))
    else:
        image(ecran, "textures/terrain/salle.png", (1150, 550), (700, 700))

    if types[0]==0:
        image(ecran, "textures/terrain/mur.png", (1150, 278), (100, 80)) #haut
    if types[2]==0:
        image(ecran, "textures/terrain/mur.png", (1152, 807), (100, 80), angle=180) #bas 
    if types[3]==0:
        image(ecran, "textures/terrain/mur.png", (880, 542), (100, 70), angle=90) #gauche 
    if types[1]==0:
        image(ecran, "textures/terrain/mur.png", (1420, 542), (100, 70), angle=90) #droite

    #images objets 
    for objet in objets:
        if objet.salle is salle and not objet.ramasse:
            if objet.image:
                image(ecran, objet.image, (objet.x, objet.y), objet.taille)
            else:
                pygame.draw.rect(ecran, JAUNE, objet.get_rect(), 2)   # carré temporaire

    #image personage

    image(ecran, "textures/personnage/aventurier.png", (cord_x, cord_y), (100, 100))
    rect_aventurier=pygame.Rect((cord_x-10, cord_y-10), (25, 25))
    #pygame.draw.rect(ecran, VERT, rect_aventurier, 2)

    #image inventaire
    image(ecran,"textures/hud/inventaire.png",(1150,180),(600,188))

    #objets rangés dans les cases de l'inventaire
    for i, slot in enumerate(SLOTS_INVENTAIRE):
        if AFFICHER_SLOTS:
            pygame.draw.rect(ecran, VERT, slot, 1)
        if inventaire.selection == i:
            pygame.draw.rect(ecran, JAUNE, slot.inflate(10, 10), 3, border_radius=6)
        if i < len(inventaire.objets):
            objet = inventaire.objets[i]
            if objet.image:
                image(ecran, objet.image, slot.center, (slot.width - 4, slot.height - 4))
            else:
                texte(objet.nom, slot.centerx, slot.centery, BLANC, petite_police, centrer=True)


    # Bouton rentrer
    rentrer = pygame.Rect(1050, 50, 130, 40)
    if zone_aventurier(salle,racine) is not None:
        couleur_rentrer = VERTH if rentrer.collidepoint(souris) else VERT
    else:
        couleur_rentrer = GRIS
    pygame.draw.rect(ecran, couleur_rentrer, rentrer, border_radius=10)
    texte("Entrer",rentrer.centerx,rentrer.centery,GRISF,petite_police,centrer=True)
    boutons.append((rentrer, "rentrer"))

    # Bouton récuperer
    recup = pygame.Rect(900, 50, 130, 40)
    sur_objet = any(objet.est_sous(rect_aventurier, salle) for objet in objets)
    if sur_objet:
        couleur_recuperer = VERTH if recup.collidepoint(souris) else VERT
    else:
        couleur_recuperer=GRIS
    pygame.draw.rect(ecran, couleur_recuperer, recup, border_radius=10)
    texte("Récuperer",recup.centerx,recup.centery,GRISF,petite_police,centrer=True)
    boutons.append((recup, "recuperer"))


    # Bouton utiliser
    use = pygame.Rect(750, 50, 130, 40)
    if inventaire.selection is not None:
        couleur_utiliser = VERTH if use.collidepoint(souris) else VERT
    else:
        couleur_utiliser = GRIS      # grisé tant qu'aucun objet n'est sélectionné
    pygame.draw.rect(ecran, couleur_utiliser, use, border_radius=10)
    texte("Utiliser", use.centerx, use.centery, GRISF, petite_police, centrer=True)
    boutons.append((use, "utiliser"))


    # Bouton paramètres
    settings = pygame.Rect(LARGEUR-150, 20, 130, 40)
    boutons.append((settings, "parametres"))
    boutond.append((settings, "parametres"))

    # Bouton autre lab
    autre_lab = pygame.Rect(20, 20, 145, 40)
    boutons.append((autre_lab, "autrelab"))
    boutond.append((autre_lab, "autrelab"))

    # Bouton nouveau lab
    nv_lab = pygame.Rect(185, 20, 176, 40)
    boutons.append((nv_lab, "nvlab"))
    boutond.append((nv_lab, "nvlab"))

    # Bouton clear
    reset = pygame.Rect(20, 70, 220, 40)
    boutons.append((reset, "reset"))
    boutond.append((reset, "reset"))


    # Dessin des boutons avec effet hover

    textes = {"recuperer": "Récuperer",
              "reset":"Réinitialiser l'historique",
              "utiliser": "Utiliser",
              "parametres": "Parametres",
              "autrelab": "Autre labyrinthe",
              "nvlab": "Nouveau labyrinthe"}

    for bouton, nom in boutond:
        if bouton.collidepoint(souris):
            couleur = BLEUH
        else:
            couleur = BLEU
        pygame.draw.rect(ecran, couleur, bouton, border_radius=10)
        texte(textes[nom],bouton.centerx,bouton.centery,GRISF,petite_police,centrer=True)


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


# --- Page paramètres : icônes de touches ---
_cache_icones = {}

def _icone(nom, hauteur):
    """Charge textures/key/<nom>.png, enlève les marges transparentes, garde les proportions."""
    cle = (nom, hauteur)
    if cle not in _cache_icones:
        img = pygame.image.load(f"textures/key/{nom}.png").convert_alpha()
        img = img.subsurface(img.get_bounding_rect()).copy()
        largeur = round(img.get_width() * hauteur / img.get_height())
        _cache_icones[cle] = pygame.transform.smoothscale(img, (largeur, hauteur))
    return _cache_icones[cle]

def _dessiner_touches(noms, x, y_centre, hauteur=46, espace=8): #IA
    for nom in noms:
        img = _icone(nom, hauteur)
        case = max(img.get_width(), hauteur)
        ecran.blit(img, (x + (case - img.get_width()) // 2, y_centre - img.get_height() // 2))
        x += case + espace

def afficher_parametres():
    ecran.fill(FOND)
    boutons.clear()
    souris = pygame.mouse.get_pos()

    texte("PARAMETRES", LARGEUR // 2, 50, BLEU, grande_police, centrer=True)
    texte("Touches et navigation", LARGEUR // 2, 95, GRIS, police, centrer=True)
    pygame.draw.line(ecran, GRIS, (LARGEUR // 2 - 120, 120), (LARGEUR // 2 + 120, 120), 2)

    # Bouton retour
    retour = pygame.Rect(LARGEUR - 150, 20, 130, 40)
    pygame.draw.rect(ecran, BLEUH if retour.collidepoint(souris) else BLEU, retour, border_radius=10)
    texte("Retour", retour.centerx, retour.centery, GRISF, petite_police, centrer=True)
    boutons.append((retour, "retour"))

    # (touches à afficher, description, couleur de la barre d'accent)
    # None à la place des touches = mini bouton "Utiliser" dessiné à la main
    #IA
    lignes = [
        (["1", "2", "3", "4"],                    "Accéder aux fils verts",                VERT),
        (["0"],                                   "Retourner à la salle père",             ORANGE),
        (["entrer"],                              "Entrer dans la salle (sur une porte)",  BLEU),
        (["haut", "gauche", "bas", "droite"],     "Déplacer l'aventurier dans la salle",   BLEU),
        (["5", "6", "7", "8", "9"],               "Sélectionner un objet de l'inventaire", JAUNE),
        (["e"],                                   "Ramasser l'objet sous l'aventurier",    JAUNE),
        (None,                                    "Utiliser l'objet sélectionné",          JAUNE),
        (["esc"],                                 "Quitter le jeu",                        ROUGE),
    ]

    x_carte, largeur_carte = 250, 1000
    hauteur_carte, pas = 64, 74
    y = 150
    for touches, description, accent in lignes:
        carte = pygame.Rect(x_carte, y, largeur_carte, hauteur_carte)
        pygame.draw.rect(ecran, (30, 41, 59), carte, border_radius=12)
        pygame.draw.rect(ecran, accent, (carte.x, carte.y + 10, 6, carte.height - 20), border_radius=3)

        if touches is None:
            bouton = pygame.Rect(carte.x + 30, carte.centery - 20, 130, 40)
            pygame.draw.rect(ecran, VERT, bouton, border_radius=10)
            texte("Utiliser", bouton.centerx, bouton.centery, GRISF, petite_police, centrer=True)
        else:
            _dessiner_touches(touches, carte.x + 30, carte.centery)

        img_txt = police.render(description, True, BLANC)
        ecran.blit(img_txt, (carte.x + 400, carte.centery - img_txt.get_height() // 2))
        y += pas

    texte("Le noeud du haut est la salle actuelle", LARGEUR // 2, y + 30, BLEU, police, centrer=True)

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