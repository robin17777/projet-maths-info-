import pygame
import class_objet
from class_salle import zone_porte


class Inventaire:

    def __init__(self, capacite=5):
        self.capacite = capacite
        self.objets = []
        self.selection = None

    def est_plein(self):
        return len(self.objets) >= self.capacite

    def ajouter(self, objet):
        if self.est_plein():
            return False
        objet.ramasser()
        self.objets.append(objet)
        return True

    def retirer(self, objet):
        if objet in self.objets:
            i = self.objets.index(objet)
            self.objets.remove(objet)
            # on garde la sélection cohérente après le retrait
            if self.selection is not None:
                if i == self.selection:
                    self.selection = None
                elif i < self.selection:
                    self.selection -= 1

    def objet_selectionne(self):
        if self.selection is None or not 0 <= self.selection < len(self.objets):
            return None
        return self.objets[self.selection]

    def lacher_selection(self):
        objet = self.objet_selectionne()
        if objet is not None:
            self.retirer(objet)
        return objet

    def selectionner(self, indice):
        if 0 <= indice < len(self.objets):
            self.selection = None if self.selection == indice else indice

    def utiliser_selection(self):
        if self.selection is None:
            return False
        return self.utiliser(self.selection)

    def utiliser(self, indice):
        if not 0 <= indice < len(self.objets):
            return False
        objet = self.objets[indice]
        objet.utiliser()
        if objet.est_epuise():
            self.retirer(objet)
        return True

    def vider(self):
        self.objets.clear()
        self.selection = None


# touches 5 à 9 (clavier principal ou pavé numérique) -> numéro de case de l'inventaire
TOUCHES_INVENTAIRE = {pygame.K_5: 0, pygame.K_KP5: 0,
                      pygame.K_6: 1, pygame.K_KP6: 1,
                      pygame.K_7: 2, pygame.K_KP7: 2,
                      pygame.K_8: 3, pygame.K_KP8: 3,
                      pygame.K_9: 4, pygame.K_KP9: 4,}

def indice_touche_inventaire(evenement):
    if evenement.key in TOUCHES_INVENTAIRE:
        return TOUCHES_INVENTAIRE[evenement.key]
    if evenement.unicode in ("5", "6", "7", "8", "9"):
        return int(evenement.unicode) - 5
    return None

def ramasser_objet(salle, inventaire, cord_x, cord_y):
    rect_av = pygame.Rect((cord_x - 10, cord_y - 10), (25, 25))
    for objet in class_objet.objets:
        if objet.est_sous(rect_av, salle):
            if inventaire.ajouter(objet):
                class_objet.objets.remove(objet)
            break

def utiliser_objet(salle, inventaire, cord_x, cord_y):
    numero = porte_a_ouvrir(salle, inventaire, cord_x, cord_y)
    if numero is not None:
        salle.ouvrir_porte(numero)
        inventaire.utiliser_selection()   # la clé est consommée

def lacher_objet(salle, inventaire, cord_x, cord_y):
    objet = inventaire.lacher_selection()
    if objet is not None:
        objet.placer(salle, cord_x, cord_y)



def porte_a_ouvrir(salle, inventaire, cord_x, cord_y):
    objet = inventaire.objet_selectionne()
    if objet is None or objet.couleur is None:
        return None
    numero = zone_porte(salle, cord_x, cord_y)
    if numero is not None and salle.porte_fermee(numero) and salle.get_fils(numero).porte == objet.couleur:
        return numero
    return None