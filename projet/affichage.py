import math
import random
import textwrap
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

# Position / taille / angle des 4 murs (1 = haut, 2 = droite, 3 = bas, 4 = gauche)
POS_MURS = {
    1: ((1150, 278), (100, 80), 0),
    2: ((1424, 540), (100, 80), 90),
    3: ((1152, 811), (100, 80), 180),
    4: ((880, 541),  (100, 80), 90),
}
# Les portes (et le trésor de la sortie) se placent dans le trou des murs :
# même centre que le mur, boîte de même taille (une fois le mur remis à l'endroit),
# image mise à l'échelle pour y entrer ENTIÈREMENT sans être déformée.
# Rotation des portes (sens trigonométrique de pygame) : le BAS de la porte est toujours
# du côté de l'intérieur de la salle -> haut 0°, droite 90° horaire (=270), bas 180°, gauche 90°
ANGLES_PORTES = {1: 0, 2: 270, 3: 180, 4: 90}

MARGE_TROU = 0   # pixels laissés libres autour de l'image (0 = bord à bord)

def boite_trou(numero):
    pos, (w, h), angle = POS_MURS[numero]
    if angle in (90, 270):      # les murs de côté sont tournés : on remet largeur/hauteur à l'endroit
        w, h = h, w
    return pos, (w - 2 * MARGE_TROU, h - 2 * MARGE_TROU)

_cache_trous = {}

def image_dans_trou(chemin, numero, angle=0):
    """Dessine l'image dans le trou du mur n° numero, tournée de angle, entière et non déformée."""
    pos, (bw, bh) = boite_trou(numero)            # taille du trou À L'ÉCRAN
    cle = (chemin, bw, bh, angle)
    if cle not in _cache_trous:
        img = pygame.image.load(chemin).convert_alpha()
        img = img.subsurface(img.get_bounding_rect()).copy()      # enlève les marges transparentes
        # avant rotation, la boîte est tournée quand l'angle est de 90° / 270°
        av_w, av_h = (bh, bw) if angle in (90, 270) else (bw, bh)
        echelle = min(av_w / img.get_width(), av_h / img.get_height())
        taille = (max(1, round(img.get_width() * echelle)), max(1, round(img.get_height() * echelle)))
        img = pygame.transform.scale(img, taille)                 # scale = pixels nets (pixel art)
        if angle:
            img = pygame.transform.rotate(img, angle)
        _cache_trous[cle] = img
    img = _cache_trous[cle]
    ecran.blit(img, img.get_rect(center=pos))

COULEURS_PORTES = {"bleu": BLEU, "jaune": JAUNE, "rouge": ROUGE}
NOMS_PORTES = {"bleu": "bleue", "jaune": "jaune", "rouge": "rouge"}

# Zones d'accès (au niveau du module pour être utilisables partout)
case_haut = pygame.Rect(1125, 345, 55, 55)
case_bas = pygame.Rect(1123, 700, 55, 55)
case_gauche = pygame.Rect(935, 520, 55, 55)
case_droite = pygame.Rect(1315, 520, 55, 55)
case_milieu = pygame.Rect(1125, 525, 50, 50)

def zone_porte(salle):
    """Numéro (1-4) du passage devant lequel est l'aventurier, même si la porte est fermée."""
    rect = pygame.Rect((cord_x - 10, cord_y - 10), (25, 25))
    types = salle.voir_suivant()
    for numero, case in ((1, case_haut), (2, case_droite), (3, case_bas), (4, case_gauche)):
        if rect.colliderect(case) and types[numero - 1] != 0:
            return numero
    return None
#fin ia 

def zone_aventurier(salle,racine):
    rect = pygame.Rect((cord_x - 10, cord_y - 10), (25, 25))
    numero = zone_porte(salle)
    if numero is not None and not salle.porte_fermee(numero):
        return numero
    if rect.colliderect(case_milieu) and salle != racine:
        return 0
    return None

def porte_a_ouvrir(salle, inventaire):
    """Numéro de la porte fermée devant l'aventurier que la clé sélectionnée peut ouvrir (sinon None)."""
    objet = inventaire.objet_selectionne()
    if objet is None or objet.couleur is None:
        return None
    numero = zone_porte(salle)
    if numero is not None and salle.porte_fermee(numero) and salle.get_fils(numero).porte == objet.couleur:
        return numero
    return None
#IA
def ombre_sol(centre, largeur, hauteur, alpha=70):
    """Petite ellipse sombre sous un objet / l'aventurier pour donner du relief."""
    cle = (largeur, hauteur, alpha)
    if cle not in _cache_ombres_sol:
        surface = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, (0, 0, 0, alpha), surface.get_rect())
        _cache_ombres_sol[cle] = surface
    ecran.blit(_cache_ombres_sol[cle], _cache_ombres_sol[cle].get_rect(center=centre))

_cache_ombres_sol = {}


def lignes_historique(largeur=68, max_lignes=5):
    """Historique du chemin coupé en lignes ; on garde les dernières si c'est trop long."""
    lignes = textwrap.wrap(historique(), width=largeur)
    if len(lignes) > max_lignes:
        lignes = ["..."] + lignes[-(max_lignes - 1):]
    return lignes


def afficher(actuelle, salles, racine,objets,inventaire):

    boutons.clear()
    boutons_salles.clear()
    boutond.clear()

    ecran.blit(FOND_DEGRADE, (0, 0))

    # --- carte "Arbre du labyrinthe" : infos + arbre (l'arbre est dessiné dans dessiner_salle) ---
    panneau(pygame.Rect(20, 125, 725, 385), "Arbre du labyrinthe")
    infos = [("Nombre de salles : ", len(salles)),
             ("Profondeur actuelle : ", actuelle.get_profondeur()),
             ("Profondeur max : ", profondeur_max(salles))]
    y_info = 190
    for libelle, valeur in infos:
        texte(libelle, 40, y_info, GRIS, petite_police)
        texte(valeur, 40 + petite_police.size(libelle)[0], y_info, BLANC, petite_police)
        y_info += 25

    # --- carte "Chemin emprunté" ---
    panneau(pygame.Rect(20, 525, 725, 200), "Chemin emprunté")
    y_hist = 587
    for ligne in lignes_historique():
        texte(ligne, 40, y_hist, BLANC, petite_police)
        y_hist += 25

    # --- carte "Objet sélectionné" ---
    panneau(pygame.Rect(20, 740, 725, 125), "Objet sélectionné")
    objet_sel = inventaire.objet_selectionne()
    if objet_sel is None:
        texte("Aucun objet sélectionné (touches 5 à 9 ou clic sur une case)", 40, 805, GRIS, petite_police)
    else:
        texte(objet_sel.nom, 40, 797, JAUNE, police)
        usages = f"Usages : {objet_sel.usages}/{objet_sel.usages_max}"
        texte(usages, 725 - petite_police.size(usages)[0], 801, BLANC, petite_police)
        texte(objet_sel.description, 40, 832, GRIS, petite_police)

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
    temps = pygame.time.get_ticks()

    types = salle.voir_suivant()

    rect_aventurier=pygame.Rect((cord_x-10, cord_y-10), (25, 25))

    #image salle 
    if salle==racine:
        image(ecran, "textures/terrain/salle_vide.png", (1150, 550), (700, 700))
    else:
        image(ecran, "textures/terrain/salle.png", (1150, 550), (700, 700))

    # murs ; portes fermées (une porte ouverte n'est plus dessinée) ; trésor devant la sortie
    for numero in range(1, 5):
        if types[numero - 1] == 0:
            pos, taille, angle = POS_MURS[numero]
            image(ecran, "textures/terrain/mur.png", pos, taille, angle=angle)
        elif salle.porte_fermee(numero):
            image_dans_trou(f"textures/terrain/porte_{salle.get_fils(numero).porte}.png", numero, ANGLES_PORTES[numero])
        elif types[numero - 1] == 3:
            image_dans_trou("textures/terrain/tresor.png", numero)

    #images objets (ombre au sol, petit flottement, halo quand l'aventurier est dessus)
    for objet in objets:
        if objet.salle is salle and not objet.ramasse:
            if objet.est_sous(rect_aventurier, salle):
                lueur(objet.get_rect(), JAUNE, 14, 12)
            ombre_sol((objet.x, objet.y + objet.taille[1] // 2 - 4), 40, 12, 80)
            flottement = round(math.sin(temps / 350 + objet.x) * 3)
            if objet.image:
                image(ecran, objet.image, (objet.x, objet.y + flottement), objet.taille)
            else:
                pygame.draw.rect(ecran, JAUNE, objet.get_rect().move(0, flottement), 2)   # carré temporaire

    #image personage
    ombre_sol((cord_x, cord_y + 38), 56, 16, 80)
    image(ecran, "textures/personnage/aventurier.png", (cord_x, cord_y), (100, 100))
    #pygame.draw.rect(ecran, VERT, rect_aventurier, 2)

    #image inventaire
    image(ecran,"textures/hud/inventaire.png",(1150,180),(600,188))

    #objets rangés dans les cases de l'inventaire
    for i, slot in enumerate(SLOTS_INVENTAIRE):
        if AFFICHER_SLOTS:
            pygame.draw.rect(ecran, VERT, slot, 1)
        if inventaire.selection == i:
            cadre = slot.inflate(10, 10)
            lueur(cadre, JAUNE, 8, 12)
            pygame.draw.rect(ecran, JAUNE, cadre, 3, border_radius=6)
        if i < len(inventaire.objets):
            objet = inventaire.objets[i]
            if objet.image:
                image(ecran, objet.image, slot.center, (slot.width - 4, slot.height - 4))
            else:
                texte(objet.nom, slot.centerx, slot.centery, BLANC, petite_police, centrer=True)


    # Bouton rentrer
    rentrer = pygame.Rect(1050, 50, 130, 40)
    bouton(rentrer, "Entrer", VERT, actif=zone_aventurier(salle,racine) is not None)
    boutons.append((rentrer, "rentrer"))

    # Bouton récuperer
    recup = pygame.Rect(900, 50, 130, 40)
    sur_objet = any(objet.est_sous(rect_aventurier, salle) for objet in objets)
    bouton(recup, "Récupérer", VERT, actif=sur_objet)
    boutons.append((recup, "recuperer"))

    # Bouton utiliser (grisé tant qu'on n'est pas devant une porte avec la bonne clé)
    use = pygame.Rect(750, 50, 130, 40)
    bouton(use, "Utiliser", VERT, actif=porte_a_ouvrir(salle, inventaire) is not None)
    boutons.append((use, "utiliser"))

    # Bouton lâcher
    lacher = pygame.Rect(600, 50, 130, 40)
    bouton(lacher, "Lâcher", VERT, actif=inventaire.selection is not None)
    boutons.append((lacher, "lacher"))


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


    # Dessin des boutons du haut (effet de survol géré par bouton())
    textes = {"reset":"Réinitialiser l'historique",
              "parametres": "Parametres",
              "autrelab": "Autre labyrinthe",
              "nvlab": "Nouveau labyrinthe"}

    for rect_b, nom in boutond:
        bouton(rect_b, textes[nom], BLEU)


    # Couleur de chaque fils (et de sa branche)
    infos_fils = []
    for i in range(4):
        numero = i + 1
        verrouille = salle.porte_fermee(numero)
        accessible = (types[i] == 1 or types[i] == 3) and not verrouille
        if verrouille:
            couleur = COULEURS_PORTES[salle.get_fils(numero).porte]
        elif types[i] == 1:
            couleur = VERT
        elif types[i] == 3:
            couleur = JAUNE
        else:
            couleur = (71, 85, 105)
        infos_fils.append((verrouille, accessible, couleur))

    # Branches entre le pere et les fils
    for i in range(4):
        couleur = infos_fils[i][2]
        debut = (LARGEUR//4, y_pere + 25)
        fin = (positions_x[i], y_fils - 25)
        pygame.draw.line(ecran, couleur, debut, fin, 4)
        pygame.draw.circle(ecran, couleur, debut, 5)
        pygame.draw.circle(ecran, couleur, fin, 5)

    # Noeud du pere (la salle actuelle)
    rect_pere = pygame.Rect(LARGEUR//4 - 75, y_pere - 25, 150, 50)
    couleur_pere = JAUNE if salle.get_type_fils()==3 else ORANGE
    if salle.get_type_fils()==3:
        text="Sortie"
    else:
        identifiant = salles.index(salle) + 1
        text=f"Salle {identifiant}"
    lueur(rect_pere, couleur_pere, 12, 14)
    bouton(rect_pere, text, couleur_pere, cliquable=salle.pere is not None, police_utilisee=police)
    if salle.pere is not None:
        badge_touche((rect_pere.left - 28, rect_pere.centery), "0")
    """Ici jusqu'a la fin ca sert pour les boutons_salles"""               
    # Le clic sur le pere permet de remonter
    boutons_salles.append((rect_pere, 0))

    # Les quatre boutons_salles fils
    for i in range(4):
        x = positions_x[i]
        numero = i + 1
        verrouille, accessible, couleur = infos_fils[i]

        rect_fils = pygame.Rect(x - 55, y_fils - 25, 110, 50)

        if verrouille:
            nom_fils = f"Porte {NOMS_PORTES[salle.get_fils(numero).porte]}"
        elif types[i] == 1:
            nom_fils =f"Fils {numero}"
        elif types[i]==3:
            nom_fils = "Sortie"
        else:
            nom_fils ="Mur"
        bouton(rect_fils, nom_fils, couleur, actif=types[i] != 0, cliquable=accessible)

        #pour mettre le chiffre a taper sous chaque fils 
        badge_touche((x, y_fils + 45), numero)

        # Seules les salles accessibles sont cliquables
        if accessible:
            boutons_salles.append((rect_fils, numero))


# --- Page paramètres : icônes de touches ---
_cache_icones = {}
SEUIL_TOUCHE_LARGE = 1.3   # largeur/hauteur au-delà de laquelle une touche est considérée "large"

def _icone(nom, hauteur):
    """Charge textures/key/<nom>.png, enlève les marges transparentes, garde les proportions."""
    cle = (nom, hauteur)
    if cle not in _cache_icones:
        try:
            img = pygame.image.load(f"textures/key/{nom}.png").convert_alpha()
            img = img.subsurface(img.get_bounding_rect()).copy()
        except (FileNotFoundError, pygame.error):
            # image absente : on dessine une touche avec la lettre
            img = pygame.Surface((hauteur, hauteur), pygame.SRCALPHA)
            pygame.draw.rect(img, (226, 232, 240), img.get_rect(), border_radius=8)
            pygame.draw.rect(img, GRIS, img.get_rect(), 3, border_radius=8)
            lettre = grande_police.render(nom.upper(), True, GRISF)
            img.blit(lettre, lettre.get_rect(center=img.get_rect().center))
        # même hauteur pour toutes ; les touches "normales" (à peu près carrées) sont toutes
        # exactement hauteur x hauteur, les touches larges (entrer, esc...) gardent leurs proportions
        ratio = img.get_width() / img.get_height()
        largeur = hauteur if ratio <= SEUIL_TOUCHE_LARGE else round(hauteur * ratio)
        _cache_icones[cle] = pygame.transform.smoothscale(img, (largeur, hauteur))
    return _cache_icones[cle]

def _dessiner_touches(noms, x, y_centre, hauteur=46, espace=8): #IA
    for nom in noms:
        img = _icone(nom, hauteur)
        ecran.blit(img, (x, y_centre - hauteur // 2))
        x += img.get_width() + espace

def afficher_parametres():
    ecran.blit(FOND_DEGRADE, (0, 0))
    boutons.clear()
    souris = pygame.mouse.get_pos()

    texte("PARAMETRES", LARGEUR // 2, 50, BLEU, grande_police, centrer=True)
    texte("Touches et navigation", LARGEUR // 2, 95, GRIS, police, centrer=True)
    pygame.draw.line(ecran, GRIS, (LARGEUR // 2 - 120, 120), (LARGEUR // 2 + 120, 120), 2)

    # Bouton retour
    retour = pygame.Rect(LARGEUR - 150, 20, 130, 40)
    bouton(retour, "Retour", BLEU)
    boutons.append((retour, "retour"))

    # (touches à afficher, description, couleur de la barre d'accent)
    # 4e élément optionnel = mini bouton dessiné à la main, affiché avant les touches
    #IA
    lignes = [
        (["1", "2", "3", "4"],                    "Accéder aux fils verts",                VERT),
        (["0"],                                   "Retourner à la salle père",             ORANGE),
        (["entrer"],                              "Entrer dans la salle (sur une porte)",  BLEU),
        (["haut", "gauche", "bas", "droite"],     "Déplacer l'aventurier dans la salle",   BLEU),
        (["5", "6", "7", "8", "9"],               "Sélectionner un objet (touche ou clic)", JAUNE),
        (["f"],                                   "Ramasser l'objet sous l'aventurier",    JAUNE, "Récupérer"),
        (["e"],                                   "Ouvrir une porte (clé sélectionnée)",   JAUNE, "Utiliser"),
        (["a"],                                   "Lâcher l'objet sélectionné",            JAUNE, "Lâcher"),
        (["esc"],                                 "Quitter le jeu",                        ROUGE),
    ]

    x_carte, largeur_carte = 250, 1000
    hauteur_carte, pas = 64, 74
    y = 150
    for touches, description, accent, *reste in lignes:
        bouton_txt = reste[0] if reste else None
        carte = pygame.Rect(x_carte, y, largeur_carte, hauteur_carte)
        ombre(carte, 12, decalage=4, alpha=70)
        pygame.draw.rect(ecran, CARTE, carte, border_radius=12)
        pygame.draw.rect(ecran, accent, (carte.x, carte.y + 10, 6, carte.height - 20), border_radius=3)

        x_touches = carte.x + 30
        if bouton_txt is not None:
            rect_mini = pygame.Rect(carte.x + 30, carte.centery - 20, 130, 40)
            bouton(rect_mini, bouton_txt, VERT, cliquable=False)
            x_touches = rect_mini.right + 20
        _dessiner_touches(touches, x_touches, carte.centery)

        img_txt = police.render(description, True, BLANC)
        ecran.blit(img_txt, (carte.x + 400, carte.centery - img_txt.get_height() // 2))
        y += pas

    texte("Le noeud du haut est la salle actuelle", LARGEUR // 2, y + 30, BLEU, police, centrer=True)

    pygame.display.flip()

_confettis = []
COULEURS_CONFETTIS = [BLEU, VERT, JAUNE, ROUGE, ORANGE]

def _maj_confettis():
    """Fait tomber des confettis (un peu au hasard) derrière la carte de victoire."""
    if len(_confettis) < 140 and random.random() < 0.7:
        _confettis.append({"x": random.uniform(0, LARGEUR), "y": -10.0,
                           "vy": random.uniform(2, 5), "vx": random.uniform(-1, 1),
                           "t": random.randint(6, 12), "c": random.choice(COULEURS_CONFETTIS),
                           "ph": random.uniform(0, 6.28)})
    for c in _confettis[:]:
        c["y"] += c["vy"]
        c["x"] += c["vx"] + math.sin(c["y"] / 30 + c["ph"])
        if c["y"] > HAUTEUR + 10:
            _confettis.remove(c)
        else:
            pygame.draw.rect(ecran, c["c"], (c["x"], c["y"], c["t"], c["t"] * 0.6))

def afficher_gagne():
    ecran.blit(FOND_DEGRADE, (0, 0))
    boutons.clear()
    _maj_confettis()

    carte = pygame.Rect(LARGEUR // 2 - 350, 200, 700, 420)
    lueur(carte, JAUNE, 24, 14)
    panneau(carte, rayon=24)

    flottement = math.sin(pygame.time.get_ticks() / 400) * 6
    texte("VOUS AVEZ GAGNÉ", LARGEUR // 2, 290 + flottement, JAUNE, titre_police, centrer=True)
    texte("Tu as trouvé la sortie du labyrinthe !", LARGEUR // 2, 365, BLANC, police, centrer=True)
    pygame.draw.line(ecran, CARTE_BORD, (LARGEUR // 2 - 200, 410), (LARGEUR // 2 + 200, 410), 2)

    autre_lab = pygame.Rect(LARGEUR // 2 - 140, 450, 280, 52)
    bouton(autre_lab, "Autre labyrinthe", BLEU, police_utilisee=police)
    boutons.append((autre_lab, "autrelab"))

    nv_lab = pygame.Rect(LARGEUR // 2 - 140, 525, 280, 52)
    bouton(nv_lab, "Nouveau labyrinthe", BLEU, police_utilisee=police)
    boutons.append((nv_lab, "nvlab"))

    pygame.display.flip()