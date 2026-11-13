import pygame
import random

objets=[]
class Objet:

    def __init__(self, nom, description="", image=None, x=1150, y=480,usages=1, effet=None, taille=(50, 50)):
        self.nom = nom
        self.description = description
        self.image = image
        self.x = x
        self.y = y
        self.taille = taille
        self.usages = usages
        self.ramasse = False
        self.salle=None
    def get_nom(self):
        return self.nom

    def get_description(self):
        return self.description

    def get_usages(self):
        return self.usages

    def est_ramasse(self):
        return self.ramasse

    def get_rect(self):
        rect = pygame.Rect((0, 0), self.taille)
        rect.center = (self.x, self.y)
        return rect
    
    def placer(self, salle, x=None, y=None):
        self.salle = salle
        self.ramasse = False
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if self not in objets:
            objets.append(self)

    def est_sous(self, rect_aventurier, salle_actuelle):
        return (not self.ramasse and self.salle is salle_actuelle and self.get_rect().colliderect(rect_aventurier))

    def ramasser(self):
        self.ramasse = True

    def utiliser(self):
        """Utilise l'objet. Renvoie True si l'utilisation a eu lieu."""
        if self.usages <= 0:
            return False
        self.usages -= 1
        return True

    def est_epuise(self):
        return self.usages <= 0

    def __str__(self):
        return f"{self.nom} ({self.usages} usage(s))"

epee = Objet("Épée", "Une vieille épée", "textures/objet/epee.png",usages=3, x=960, y=650)
potion_soin = Objet("Potion", "Soigne un peu", "textures/objet/potion_soin.png",usages=1, x=1270, y=400)
cle = Objet("Clé", "Ouvre quelque chose","textures/objet/clef_bleu.png", usages=1, x=1330, y=670)

TOUS_LES_OBJETS = [epee, potion_soin, cle]


def placer_objets(salles):
    objets.clear()
    for obj in TOUS_LES_OBJETS:
        obj.salle = None
        obj.ramasse = False

    candidates = salles[1:-1]
    if not candidates:
        return
    for obj in TOUS_LES_OBJETS:
        obj.placer(random.choice(candidates))