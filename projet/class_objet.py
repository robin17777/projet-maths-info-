import pygame


class Objet:
    """Un objet posé dans une salle, ramassable puis utilisable."""

    def __init__(self, nom, description="", image=None, x=1150, y=480,usages=1, effet=None, taille=(50, 50)):
        self.nom = nom
        self.description = description
        self.image = image
        self.x = x
        self.y = y
        self.taille = taille
        self.usages = usages
        self.ramasse = False

    # ---------- getters ----------
    def get_nom(self):
        return self.nom

    def get_description(self):
        return self.description

    def get_usages(self):
        return self.usages

    def est_ramasse(self):
        return self.ramasse

    def get_rect(self):
        """Rectangle de l'objet dans la salle (pour savoir si l'aventurier est dessus)."""
        rect = pygame.Rect((0, 0), self.taille)
        rect.center = (self.x, self.y)
        return rect

    def est_sous(self, rect_aventurier):
        return not self.ramasse and self.get_rect().colliderect(rect_aventurier)


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

