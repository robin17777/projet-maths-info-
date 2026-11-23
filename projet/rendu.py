import math
import random
import textwrap
import pygame
import class_objet
from contexte import *
from class_salle import historique

"""TOUT CE QUI SE TROUVE DANS SE FICHIER EST GENERE PAR IA ET NE SERT QUE A RENDRE PLUS JOLI LE JEU"""


def _creer_fond():
    """Fond dégradé (haut sombre -> bas un peu plus clair) avec une grille de petits points."""
    fond = pygame.Surface((LARGEUR, HAUTEUR))
    haut, bas = (10, 15, 30), (28, 38, 70)
    for y in range(HAUTEUR):
        t = y / (HAUTEUR - 1)
        couleur = tuple(int(haut[i] + (bas[i] - haut[i]) * t) for i in range(3))
        pygame.draw.line(fond, couleur, (0, y), (LARGEUR, y))
    for x in range(20, LARGEUR, 40):
        for y in range(20, HAUTEUR, 40):
            fond.set_at((x, y), (46, 58, 94))
    return fond

FOND_DEGRADE = _creer_fond()


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



# ===========================================================================
# Outils de dessin : ombres, lueurs, panneaux, boutons
# ===========================================================================

_cache_ombres = {}
_cache_lueurs = {}


def eclaircir(couleur, quantite=25):
    """Retourne la couleur un peu plus claire (sert pour l'effet de survol)."""
    return tuple(min(255, v + quantite) for v in couleur)


def ombre(rect, rayon=12, decalage=5, alpha=90):
    """Ombre douce sous un rectangle arrondi."""
    cle = (rect.width, rect.height, rayon, alpha)
    if cle not in _cache_ombres:
        surface = pygame.Surface((rect.width + 16, rect.height + 16), pygame.SRCALPHA)
        for marge, a in ((8, alpha // 4), (4, alpha // 3), (0, alpha // 2)):
            zone = pygame.Rect(8 - marge, 8 - marge, rect.width + 2 * marge, rect.height + 2 * marge)
            pygame.draw.rect(surface, (0, 0, 0, a), zone, border_radius=rayon + marge)
        _cache_ombres[cle] = surface
    ecran.blit(_cache_ombres[cle], (rect.x - 8, rect.y - 8 + decalage))


def lueur(rect, couleur, rayon=10, etendue=12):
    """Halo lumineux autour d'un rectangle arrondi."""
    cle = (rect.width, rect.height, couleur, rayon, etendue)
    if cle not in _cache_lueurs:
        surface = pygame.Surface((rect.width + 2 * etendue, rect.height + 2 * etendue), pygame.SRCALPHA)
        for i in range(etendue, 0, -2):
            a = int(70 * (1 - i / etendue)) + 8
            zone = pygame.Rect(etendue - i, etendue - i, rect.width + 2 * i, rect.height + 2 * i)
            pygame.draw.rect(surface, (*couleur, a), zone, border_radius=rayon + i)
        _cache_lueurs[cle] = surface
    ecran.blit(_cache_lueurs[cle], (rect.x - etendue, rect.y - etendue))


def panneau(rect, titre=None, rayon=16):
    """Carte arrondie avec ombre, bordure et titre optionnel (comme dans les paramètres)."""
    ombre(rect, rayon)
    pygame.draw.rect(ecran, CARTE, rect, border_radius=rayon)
    pygame.draw.rect(ecran, CARTE_BORD, rect, 2, border_radius=rayon)
    if titre:
        texte(titre, rect.x + 20, rect.y + 12, BLEU, police)
        pygame.draw.line(ecran, CARTE_BORD, (rect.x + 20, rect.y + 48), (rect.right - 20, rect.y + 48), 2)


def bouton(rect, message, couleur, actif=True, cliquable=True, police_utilisee=None, rayon=10):
    """Bouton arrondi avec ombre, bordure claire et effet de survol (le bouton se soulève).

    actif=False      -> bouton grisé
    cliquable=False  -> couleur normale mais pas d'effet de survol
    """
    if police_utilisee is None:
        police_utilisee = petite_police
    survol = actif and cliquable and rect.collidepoint(pygame.mouse.get_pos())

    if not actif:
        fond, couleur_texte = BOUTON_OFF, TEXTE_OFF
    else:
        fond, couleur_texte = (eclaircir(couleur, 22) if survol else couleur), GRISF

    dessin = rect.move(0, -2) if survol else rect
    ombre(dessin, rayon, decalage=4 if survol else 3, alpha=100 if actif else 50)
    pygame.draw.rect(ecran, fond, dessin, border_radius=rayon)
    pygame.draw.rect(ecran, eclaircir(fond, 35) if actif else CARTE_BORD, dessin, 2, border_radius=rayon)
    texte(message, dessin.centerx, dessin.centery, couleur_texte, police_utilisee, centrer=True)


def badge_touche(centre, message, cote=30):
    """Petit carré qui rappelle la touche du clavier à utiliser."""
    rect = pygame.Rect(0, 0, cote, cote)
    rect.center = centre
    pygame.draw.rect(ecran, FOND, rect, border_radius=7)
    pygame.draw.rect(ecran, GRIS, rect, 2, border_radius=7)
    texte(message, rect.centerx, rect.centery, BLANC, petite_police, centrer=True)


_cache_ombres_sol = {}

def ombre_sol(centre, largeur, hauteur, alpha=70):
    """Petite ellipse sombre sous un objet / l'aventurier pour donner du relief."""
    cle = (largeur, hauteur, alpha)
    if cle not in _cache_ombres_sol:
        surface = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, (0, 0, 0, alpha), surface.get_rect())
        _cache_ombres_sol[cle] = surface
    ecran.blit(_cache_ombres_sol[cle], _cache_ombres_sol[cle].get_rect(center=centre))


# ===========================================================================
# Inventaire, murs et portes : positions et dessin
# ===========================================================================

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


def lignes_historique(largeur=68, max_lignes=5):
    """Historique du chemin coupé en lignes ; on garde les dernières si c'est trop long."""
    lignes = textwrap.wrap(historique(), width=largeur)
    if len(lignes) > max_lignes:
        lignes = ["..."] + lignes[-(max_lignes - 1):]
    return lignes


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


# ===========================================================================
# Menu "Nouveau labyrinthe" : options avancées (salles, portes, objets)
# ===========================================================================

_cache_images_menu = {}

def _image_menu(chemin, cote):
    """Image chargée, rognée et mise à l'échelle pour tenir dans cote x cote (None si absente)."""
    cle = (chemin, cote)
    if cle not in _cache_images_menu:
        try:
            img = pygame.image.load(chemin).convert_alpha()
            img = img.subsurface(img.get_bounding_rect()).copy()
            echelle = min(cote / img.get_width(), cote / img.get_height())
            taille = (max(1, round(img.get_width() * echelle)), max(1, round(img.get_height() * echelle)))
            _cache_images_menu[cle] = pygame.transform.scale(img, taille)
        except (FileNotFoundError, pygame.error):
            _cache_images_menu[cle] = None
    return _cache_images_menu[cle]


def case_a_cocher(rect, coche, couleur=VERT):
    """Case à cocher arrondie avec une coche quand elle est cochée."""
    pygame.draw.rect(ecran, FOND, rect, border_radius=8)
    pygame.draw.rect(ecran, couleur if coche else GRIS, rect, 2, border_radius=8)
    if coche:
        x, y, w, h = rect
        points = [(x + w * 0.22, y + h * 0.52), (x + w * 0.43, y + h * 0.74), (x + w * 0.80, y + h * 0.28)]
        pygame.draw.lines(ecran, couleur, False, points, 4)


def _ligne_option(rect, coche, couleur):
    """Fond d'une ligne cliquable du menu (bordure colorée si cochée, léger survol)."""
    survol = rect.collidepoint(pygame.mouse.get_pos())
    fond = eclaircir(CARTE, 10) if survol else CARTE
    pygame.draw.rect(ecran, fond, rect, border_radius=12)
    pygame.draw.rect(ecran, couleur if coche else CARTE_BORD, rect, 2, border_radius=12)
    case = pygame.Rect(0, 0, 36, 36)
    case.center = (rect.x + 36, rect.centery)
    case_a_cocher(case, coche, couleur)


def _dessiner_image_menu(chemin, centre, cote, coche=True):
    img = _image_menu(chemin, cote)
    if img is None:
        return
    if not coche:                       # option décochée : image un peu grisée
        img = img.copy()
        img.set_alpha(110)
    ecran.blit(img, img.get_rect(center=centre))


MAX_PAR_TYPE = 9   # nombre maximum d'exemplaires d'un même objet
NB_EMPLACEMENTS_OBJETS = 4   # lignes d'objets prévues dans le menu (augmente si tu en ajoutes plus)


def options_par_defaut():
    return {"portes": {"bleu", "jaune", "rouge"},
            "objets": {objet.nom: 1 for objet in class_objet.OBJETS_MENU}}


def demander_options_labyrinthe(nombre_defaut, options_defaut=None):
    """Menu du 'Nouveau labyrinthe' : nombre de salles, portes (avec leur clé) et objets (quantité de chacun).

    Retourne (nombre_de_salles, options) ou None si on annule.
    options = {"portes": {"bleu", "jaune", "rouge"}, "objets": {"Épée": 2, "Potion de soin": 1, "Potion de dégât": 0}}
    """
    defaut = options_defaut or options_par_defaut()
    portes = set(defaut["portes"])
    quantites = dict(defaut["objets"])
    nombre = str(nombre_defaut)
    message_erreur = ""

    cles_portes = {"bleu": class_objet.cle_b, "jaune": class_objet.cle_j, "rouge": class_objet.cle_r}
    objets_menu = class_objet.OBJETS_MENU
    for objet in objets_menu:
        quantites.setdefault(objet.nom, 0)

    # --- positions (calculées une seule fois) ---
    hauteur_ligne_objet, pas_objets = 80, 92     # lignes d'objets compactes pour en loger NB_EMPLACEMENTS_OBJETS
    hauteur_panneaux = max(400, 62 + (NB_EMPLACEMENTS_OBJETS - 1) * pas_objets + hauteur_ligne_objet + 20)
    carte = pygame.Rect(LARGEUR // 2 - 550, 100, 1100, 160 + hauteur_panneaux + 170)
    p_salles = pygame.Rect(carte.x + 30, carte.y + 30, carte.width - 60, 110)
    champ = pygame.Rect(p_salles.x + 20, p_salles.y + 58, 160, 40)
    p_portes = pygame.Rect(carte.x + 30, carte.y + 160, 500, hauteur_panneaux)
    p_objets = pygame.Rect(p_portes.right + 20, carte.y + 160, carte.right - 30 - (p_portes.right + 20), hauteur_panneaux)
    lignes_portes = [(couleur, pygame.Rect(p_portes.x + 15, p_portes.y + 62 + i * 108, p_portes.width - 30, 96))
                     for i, couleur in enumerate(("bleu", "jaune", "rouge"))]
    lignes_objets = []
    for i, objet in enumerate(objets_menu):
        rect = pygame.Rect(p_objets.x + 15, p_objets.y + 62 + i * pas_objets, p_objets.width - 30, hauteur_ligne_objet)
        moins = pygame.Rect(rect.x + 140, rect.centery + 3, 32, 32)
        plus = pygame.Rect(rect.x + 238, rect.centery + 3, 32, 32)
        lignes_objets.append((objet, rect, moins, plus))
    btn_annuler = pygame.Rect(carte.centerx - 220, carte.bottom - 75, 200, 48)
    btn_creer = pygame.Rect(carte.centerx + 20, carte.bottom - 75, 200, 48)

    def valider():
        if nombre.isdigit() and int(nombre) >= 1:
            return int(nombre), {"portes": set(portes), "objets": dict(quantites)}
        return None

    while True:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return None

            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    return None
                elif evenement.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    resultat = valider()
                    if resultat is not None:
                        return resultat
                    message_erreur = "Entre un nombre de salles entier positif."
                elif evenement.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                    message_erreur = ""
                elif evenement.unicode.isdigit() and len(nombre) < 5:
                    nombre += evenement.unicode
                    message_erreur = ""

            elif evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                pos = evenement.pos
                for couleur, rect in lignes_portes:
                    if rect.collidepoint(pos):
                        portes.symmetric_difference_update({couleur})   # coche / décoche
                for objet, rect, moins, plus in lignes_objets:
                    if moins.collidepoint(pos):
                        quantites[objet.nom] = max(0, quantites[objet.nom] - 1)
                    elif plus.collidepoint(pos):
                        quantites[objet.nom] = min(MAX_PAR_TYPE, quantites[objet.nom] + 1)
                    elif rect.collidepoint(pos):                      # la case : 0 <-> 1
                        quantites[objet.nom] = 0 if quantites[objet.nom] > 0 else 1
                if btn_annuler.collidepoint(pos):
                    return None
                if btn_creer.collidepoint(pos):
                    resultat = valider()
                    if resultat is not None:
                        return resultat
                    message_erreur = "Entre un nombre de salles entier positif."

        # ------------------------------ dessin ------------------------------
        total_objets = sum(quantites.values())
        ecran.blit(FOND_DEGRADE, (0, 0))
        texte("NOUVEAU LABYRINTHE", LARGEUR // 2, 55, BLEU, titre_police, centrer=True)
        panneau(carte)

        # nombre de salles
        panneau(p_salles, "Nombre de salles")
        lueur(champ, BLEU, 10, 10)
        pygame.draw.rect(ecran, FOND, champ, border_radius=10)
        pygame.draw.rect(ecran, BLEU, champ, 2, border_radius=10)
        texte(nombre, champ.centerx, champ.centery, BLANC, police, centrer=True)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            largeur_texte = police.size(nombre)[0] if nombre else 0
            x_curseur = champ.centerx + largeur_texte // 2 + 4
            pygame.draw.line(ecran, BLEU, (x_curseur, champ.centery - 14), (x_curseur, champ.centery + 14), 2)
        texte("Tape un nombre (la sortie est toujours la dernière salle créée)", champ.right + 25,
              champ.centery - 10, GRIS, petite_police)

        # portes + clés
        panneau(p_portes, "Portes et clés")
        for couleur, rect in lignes_portes:
            coche = couleur in portes
            _ligne_option(rect, coche, COULEURS_PORTES[couleur])
            _dessiner_image_menu(f"textures/terrain/porte_{couleur}.png", (rect.x + 115, rect.centery), 76, coche)
            texte(f"Porte {NOMS_PORTES[couleur]}", rect.x + 175, rect.centery - 24, BLANC if coche else GRIS, police)
            texte("ouverte par sa clé  >", rect.x + 175, rect.centery + 8, GRIS, petite_police)
            _dessiner_image_menu(cles_portes[couleur].image, (rect.right - 45, rect.centery), 60, coche)

        # objets (case + image + nom + quantité avec - et +)
        panneau(p_objets, "Objets")
        for objet, rect, moins, plus in lignes_objets:
            quantite = quantites[objet.nom]
            coche = quantite > 0
            _ligne_option(rect, coche, JAUNE)
            _dessiner_image_menu(objet.image, (rect.x + 95, rect.centery), 60, coche)
            texte(objet.nom, rect.x + 140, rect.centery - 31, BLANC if coche else GRIS, police)
            bouton(moins, "-", BLEU, actif=quantite > 0, police_utilisee=police)
            texte(f"x{quantite}", (moins.right + plus.left) // 2, moins.centery,
                  JAUNE if coche else GRIS, police, centrer=True)
            bouton(plus, "+", BLEU, actif=quantite < MAX_PAR_TYPE, police_utilisee=police)

        # résumé
        resume = f"Salles : {nombre or '?'}   |   Portes : {len(portes)}   |   Objets : {total_objets}"
        texte(resume, carte.centerx, p_portes.bottom + 30, BLANC, petite_police, centrer=True)
        if message_erreur:
            texte(message_erreur, carte.centerx, p_portes.bottom + 58, ROUGE, petite_police, centrer=True)
        elif nombre.isdigit() and int(nombre) < 3 and (portes or total_objets):
            texte("Avec moins de 3 salles, les portes et les objets ne seront pas placés.",
                  carte.centerx, p_portes.bottom + 58, ORANGE, petite_police, centrer=True)

        bouton(btn_annuler, "Annuler", ROUGE, police_utilisee=police)
        bouton(btn_creer, "Créer", VERT, police_utilisee=police)

        pygame.display.flip()
        horloge.tick(30)