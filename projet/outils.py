import textwrap
import random
import pygame
from class_salle import *
from contexte import *



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
        # curseur clignotant
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            largeur_texte = grande_police.size(nombre)[0] if nombre else 0
            x_curseur = champ.centerx + largeur_texte // 2 + 4
            pygame.draw.line(ecran, BLEU, (x_curseur, champ.centery - 16), (x_curseur, champ.centery + 16), 2)

        texte("Tape un nombre puis appuie sur Entree", LARGEUR // 2, 385, GRIS, petite_police, centrer=True)

        # Message d'erreur
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

        # On ajoute tous les fils disponibles dans la liste des possibilités
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

        # S'il n'y a plus de possibilité, on arrête
        if not possibles:
            break

        parent, numero = random.choice(possibles)
        if i ==nombre-2:
            parent.set_fils(numero,3)
        else:
            parent.set_fils(numero, 1)

        # On récupère l'enfant qui vient d'être créé
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

#IA
# ---------------------------------------------------------------------------
# Petits outils de dessin pour avoir une interface plus jolie
# ---------------------------------------------------------------------------
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
#fin ia 

def texte_multiligne(contenu, x, y, couleur, police, largeur=40):
    lignes = textwrap.wrap(contenu, width=largeur)

    for ligne in lignes:
        texte(ligne, x, y, couleur, police)
        y += 25


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

def historique():
    directions = {0: "Salle précédente",1: "1",2: "2",3: "3",4: "4",5: "Début labyrinthe",6:"Nouveau point de départ"}
    hist=""
    for passage in passages_visites:
        if passage ==5 or passage==6:
            hist+=directions[passage]
        else:
            hist= hist+" -> "+directions[passage]
    return hist