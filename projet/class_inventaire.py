class Inventaire:

    def __init__(self, capacite=5):
        self.capacite = capacite
        self.objets = []
        self.selection = None   # indice de l'objet sélectionné (None = aucun)

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

    def selectionner(self, indice):
        """Sélectionne la case indice (si elle contient un objet). Re-appuyer désélectionne."""
        if 0 <= indice < len(self.objets):
            self.selection = None if self.selection == indice else indice

    def utiliser_selection(self):
        """Utilise l'objet sélectionné. Ne fait rien si rien n'est sélectionné."""
        if self.selection is None:
            return False
        return self.utiliser(self.selection)

    def utiliser(self, indice):
        """Utilise l'objet à l'indice donné ; le retire s'il est épuisé."""
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