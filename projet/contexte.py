import pygame

boutons_salles = []
boutons =[]


# =========================
# INITIALISATION DE PYGAME
# =========================

pygame.init()

LARGEUR = 1500
HAUTEUR = 900

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Labyrinthe quaternaire")


police = pygame.font.SysFont("Arial", 25)
petite_police = pygame.font.SysFont("Arial", 19)
grande_police = pygame.font.SysFont("Arial", 34)
horloge = pygame.time.Clock()


# COULEURS DU JEU

FOND = (17, 24, 39)
BLANC = (241, 245, 249)
GRIS = (100, 116, 139)
GRISF = (17, 24, 39)
VERT = (52, 211, 153)
BLEU = (56, 189, 248)
ROUGE = (251, 113, 133) 
ORANGE = (255,127,0)
JAUNE = (255,215,0)




