import pygame
import random

objets=[]
class Objet:

    def __init__(self, nom, description="", image=None, x=1150, y=480,usages=1, effet=None, taille=(50, 50), couleur=None):
        self.nom = nom
        self.description = description
        self.image = image
        self.x = x
        self.y = y
        self.taille = taille
        self.usages = usages
        self.usages_max = usages
        self.couleur = couleur   # pour les clés : couleur de la porte qu'elles ouvrent
        self.ramasse = False
        self.salle=None
    def reinitialiser(self):
        self.usages = self.usages_max
        self.ramasse = False
        self.salle = None

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
        if self.usages <= 0:
            return False
        self.usages -= 1
        return True

    def est_epuise(self):
        return self.usages <= 0

    def __str__(self):
        return f"{self.nom} ({self.usages} usage(s))"

epee = Objet("Épée", "Une vieille épée", "textures/objet/epee.png",usages=4, x=960, y=650)
potion_soin = Objet("Potion", "Soigne un peu", "textures/objet/potion_soin.png",usages=1, x=1270, y=400)
cle_b = Objet("Clé bleue", "Ouvre la porte bleue","textures/objet/clef_bleu.png", usages=1, x=1330, y=670, couleur="bleu")
cle_j = Objet("Clé jaune", "Ouvre la porte jaune","textures/objet/clef_jaune.png", usages=1, x=1000, y=420, couleur="jaune")
cle_r = Objet("Clé rouge", "Ouvre la porte rouge","textures/objet/clef_rouge.png", usages=1, x=1200, y=690, couleur="rouge")

TOUS_LES_OBJETS = [epee, potion_soin, cle_b, cle_r, cle_j]


def est_ancetre_ou_egal(a, b):
    while b is not None:
        if b is a:
            return True
        b = b.pere
    return False


def placer_portes_et_cles(salles):
    for salle in salles:
        salle.porte = None
        salle.porte_ouverte = False

    cles = [cle_b, cle_j, cle_r]
    candidates_cles = salles[1:-1]
    portes_possibles = salles[1:]
    cles_placees = []

    for cle in cles:
        choix = [s for s in portes_possibles if s.porte is None and not any(est_ancetre_ou_egal(s, k) for k in cles_placees)]
        random.shuffle(choix)
        for salle_porte in choix:
            endroits = [s for s in candidates_cles if not est_ancetre_ou_egal(salle_porte, s)]
            if endroits:
                salle_porte.set_porte(cle.couleur)
                cle.placer(random.choice(endroits))
                cles_placees.append(cle.salle)
                break
        else:
            break


def placer_objets(salles):
    objets.clear()
    for obj in TOUS_LES_OBJETS:
        obj.reinitialiser()

    candidates = salles[1:-1]
    if not candidates:
        return
    for obj in (epee, potion_soin):
        obj.placer(random.choice(candidates))

    placer_portes_et_cles(salles)