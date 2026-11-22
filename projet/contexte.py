import pygame

boutons_salles = []
boutons =[]
boutond=[]


pygame.init()

# ECRAN
LARGEUR = 1500
HAUTEUR = 900
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Labyrinthe quaternaire")

# POLICES
police = pygame.font.SysFont("Arial", 25)
petite_police = pygame.font.SysFont("Arial", 19)
grande_police = pygame.font.SysFont("Arial", 34)
titre_police = pygame.font.SysFont("Arial", 64, bold=True)
horloge = pygame.time.Clock()


# COULEURS DU JEU

FOND = (17, 24, 39)
BLANC = (241, 245, 249)
GRIS = (100, 116, 139)
GRISF = (17, 24, 39)
VERT = (52, 211, 153)
VERTH = (30, 160, 110)
BLEU = (56, 189, 248)
BLEUH = (80, 130, 200)
ROUGE = (251, 113, 133) 
ORANGE = (255,127,0)
JAUNE = (255,215,0)

#IA
# Couleurs de l'interface (cartes, boutons grisés...)
CARTE = (30, 41, 59)
CARTE_BORD = (51, 65, 85)
BOUTON_OFF = (51, 65, 85)
TEXTE_OFF = (148, 163, 184)


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