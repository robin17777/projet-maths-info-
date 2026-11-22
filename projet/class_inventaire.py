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