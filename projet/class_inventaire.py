class Inventaire:

    def __init__(self, capacite=5):
        self.capacite = capacite
        self.objets = []

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
            self.objets.remove(objet)

    def utiliser(self, indice):
        """Utilise l'objet à l'indice donné ; le retire s'il est épuisé."""
        if not 0 <= indice < len(self.objets):
            return False
        objet = self.objets[indice]
        if objet.est_epuise():
            self.retirer(objet)
        return True

    def vider(self):
        self.objets.clear()