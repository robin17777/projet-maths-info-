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

    def copie(self): #cree des copies pour en avoir plusieur du meme type
        return Objet(self.nom, self.description, self.image, x=self.x, y=self.y,
                     usages=self.usages_max, taille=self.taille, couleur=self.couleur)

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
potion_soin = Objet("Potion de soin", "Soigne un peu", "textures/objet/potion_soin.png",usages=1, x=1270, y=400)
potion_degat = Objet("Potion de dégât", "fais des degats", "textures/objet/potion_degat.png",usages=1, x=1075, y=580)
cle_b = Objet("Clé bleue", "Ouvre la porte bleue","textures/objet/clef_bleu.png", usages=1, x=1330, y=670, couleur="bleu")
cle_j = Objet("Clé jaune", "Ouvre la porte jaune","textures/objet/clef_jaune.png", usages=1, x=1000, y=420, couleur="jaune")
cle_r = Objet("Clé rouge", "Ouvre la porte rouge","textures/objet/clef_rouge.png", usages=1, x=1200, y=690, couleur="rouge")

TOUS_LES_OBJETS = [epee, potion_soin, cle_b, cle_r, cle_j,potion_degat]
OBJETS_MENU = [epee, potion_soin, potion_degat]   # objets qui apparairon dans le menu de creation 

def est_ancetre_ou_egal(a, b):
    while b is not None:
        if b is a:
            return True
        b = b.pere
    return False

def _position_libre(salle):
    x, y = 1150, 560
    for _ in range(40):
        x = random.randrange(1000, 1301, 25)
        y = random.randrange(420, 671, 25)
        if abs(x - 1150) < 70 and abs(y - 480) < 70:
            continue
        if all(abs(o.x - x) >= 60 or abs(o.y - y) >= 60 for o in objets if o.salle is salle):
            break
    return x, y


#ia
def placer_portes_et_cles(salles, cles=None, sortie_bloquee=False):
    for salle in salles:
        salle.porte = None
        salle.porte_ouverte = False

    if cles is None:
        cles = [cle_b, cle_j, cle_r]
    candidates_cles = salles[1:-1]
    portes_possibles = salles[1:]
    cles_placees = []
    # salles par lesquelles on doit forcément passer pour atteindre la sortie (la sortie comprise)
    chemin_sortie = [s for s in salles[1:] if est_ancetre_ou_egal(s, salles[-1])]

    for cle in cles:
        choix = [s for s in portes_possibles if s.porte is None and not any(est_ancetre_ou_egal(s, k) for k in cles_placees)]
        if sortie_bloquee and not cles_placees:
            # 1re clé : sa porte barre la route de la sortie. Sa clé est placée hors de la zone
            # derrière cette porte (voir 'endroits'), donc le labyrinthe reste faisable.
            choix = [s for s in choix if s in chemin_sortie]
        random.shuffle(choix)
        for salle_porte in choix:
            endroits = [s for s in candidates_cles if not est_ancetre_ou_egal(salle_porte, s)]
            if endroits:
                salle_porte.set_porte(cle.couleur)
                salle_cle = random.choice(endroits)
                x, y = _position_libre(salle_cle)
                cle.placer(salle_cle, x, y)
                cles_placees.append(cle.salle)
                break
        else:
            break

#ia
def placer_objets(salles, options=None):
    """options = None -> un de chaque objet et toutes les portes. Sinon
    {"portes": {"bleu", ...}, "objets": {"Épée": 2, "Potion de soin": 0, ...}}
    (portes = couleurs des portes voulues, leur clé est placée avec elles ; objets = quantité de chaque).
    La salle ET la position dans la salle sont toujours tirées au hasard."""
    objets.clear()
    for obj in TOUS_LES_OBJETS:
        obj.reinitialiser()

    if options is None:
        quantites = {obj.nom: 1 for obj in OBJETS_MENU}
        couleurs = {"bleu", "jaune", "rouge"}
        sortie_bloquee = False
    else:
        quantites = options["objets"]
        couleurs = options["portes"]
        sortie_bloquee = bool(options.get("sortie_bloquee", False))

    candidates = salles[1:-1]
    if not candidates:
        return

    for obj in OBJETS_MENU:
        for k in range(quantites.get(obj.nom, 0)):
            salle = random.choice(candidates)
            x, y = _position_libre(salle)
            exemplaire = obj if k == 0 else obj.copie()   # le 1er est l'objet d'origine, les autres des copies
            exemplaire.placer(salle, x, y)

    cles = [c for c in (cle_b, cle_j, cle_r) if c.couleur in couleurs]
    if sortie_bloquee and not cles:
        cles = [cle_b]   # il faut au moins une porte pour bloquer la sortie
    placer_portes_et_cles(salles, cles, sortie_bloquee)