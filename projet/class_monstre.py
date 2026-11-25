import random


class Monstre:
    def __init__(self, nom, image, pv, degats):
        self.nom = nom
        self.image = image
        self.pv = pv
        self.pv_max = pv
        self.degats = degats

    def copie(self):
        return Monstre(self.nom, self.image, self.pv_max, self.degats)

    def est_mort(self):
        return self.pv <= 0

    def subir_degats(self, quantite):
        self.pv = max(0, self.pv - quantite)


# Les 4 monstres : (nom, image, PV, dégâts).
MONSTRES = [
    Monstre("Gobelin",   "textures/personnage/gobelin.png",   20, 4),
    Monstre("Araignée",  "textures/personnage/arraignee.png", 30, 6),
    Monstre("Squelette", "textures/personnage/squelette.png", 45, 8),
    Monstre("Zombie",    "textures/personnage/zombie.png",    70, 5),
]

PROBA_MONSTRE = 0.5   # chance qu'une salle (ni départ ni sortie) contienne un monstre


def placer_monstres(salles, proba=PROBA_MONSTRE):
    for salle in salles:
        salle.monstre = None
    for salle in salles[1:-1]:
        if random.random() < proba:
            salle.monstre = random.choice(MONSTRES).copie()