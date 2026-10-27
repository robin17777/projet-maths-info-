

class Salle:
    def __init__(self, pere=None, type_fils=1):
        self.type_fils = type_fils  # 1 = salle, 0 = mur
        self.pere = pere

        self.f1 = None
        self.f2 = None
        self.f3 = None
        self.f4 = None

    def get_type_fils(self):
        return self.type_fils

    def set_fils(self, fils, type_fils):
        nouvelle_salle = Salle(self, type_fils)

        if fils == 1:
            self.f1 = nouvelle_salle
        elif fils == 2:
            self.f2 = nouvelle_salle
        elif fils == 3:
            self.f3 = nouvelle_salle
        elif fils == 4:
            self.f4 = nouvelle_salle

    def voir_suivant(self):
        return tuple(
            0 if fils is None else fils.get_type_fils()
            for fils in (self.f1, self.f2, self.f3, self.f4)
        )

    def acceder_salle(self, x):
        fils = {1: self.f1,2: self.f2,3: self.f3,4: self.f4}

        if x == 0:
            return self if self.pere is None else self.pere

        if x not in fils:
            return self

        cible = fils[x]

        if cible is not None and cible.get_type_fils() == 1:
            return cible

        return self