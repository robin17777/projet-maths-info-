import pygame

boutons_salles = []
boutons =[]


# =========================
# INITIALISATION DE PYGAME
# =========================

pygame.init()

LARGEUR = 800
HAUTEUR = 600

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Labyrinthe quaternaire")


police = pygame.font.SysFont("Arial", 25)
petite_police = pygame.font.SysFont("Arial", 19)
horloge = pygame.time.Clock()

FOND = (30, 33, 45)
BLANC = (240, 240, 240)
GRIS = (150, 155, 165)
GRISF = (20, 25, 35)
VERT = (50, 205, 130)
BLEU = (100, 170, 255)
ROUGE = (255, 100, 100)



