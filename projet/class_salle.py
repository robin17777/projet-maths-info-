passages_visites =[5]

class Salle:
    def __init__(self, pere=None, type_fils=1):
        self.type_fils = type_fils  # 1 = salle, 0 = mur , 2 = sortie
        self.pere = pere
        self.profondeur =0
        self.porte = None
        self.porte_ouverte = False


        self.f1 = None
        self.f2 = None
        self.f3 = None
        self.f4 = None

    def get_type_fils(self):
        return self.type_fils

    def set_fils(self, fils, type_fils):
        nouvelle_salle = Salle(self, type_fils)
        nouvelle_salle.set_profondeur(self.profondeur + 1)

        if fils == 1:
            self.f1 = nouvelle_salle
        elif fils == 2:
            self.f2 = nouvelle_salle
        elif fils == 3:
            self.f3 = nouvelle_salle
        elif fils == 4:
            self.f4 = nouvelle_salle

    def get_profondeur(self):
        return self.profondeur
    
    def set_profondeur(self, profondeur):
        self.profondeur = profondeur

    def get_fils(self, x):
        return {1: self.f1, 2: self.f2, 3: self.f3, 4: self.f4}.get(x)

    def set_porte(self, couleur):
        self.porte = couleur
        self.porte_ouverte = False

    def get_porte(self):
        return self.porte

    def porte_fermee(self, x):
        fils = self.get_fils(x)
        return fils is not None and fils.porte is not None and not fils.porte_ouverte

    def ouvrir_porte(self, x):
        fils = self.get_fils(x)
        if fils is not None:
            fils.porte_ouverte = True

    def voir_suivant(self):
        return tuple(
            0 if fils is None else fils.get_type_fils()
            for fils in (self.f1, self.f2, self.f3, self.f4)
        )

    def acceder_salle(self, x):
        fils = {1: self.f1,2: self.f2,3: self.f3,4: self.f4}

        if x == 0:
            if self.pere is None:
                return self

            passages_visites.append(0)
            return self.pere

        if x not in fils:
            return self

        cible = fils[x]

        if cible is not None and cible.get_type_fils() in (1, 2, 3) and not self.porte_fermee(x):
            passages_visites.append(x)
            return cible

        return self