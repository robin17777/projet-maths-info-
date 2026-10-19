
import pygame
import random
boutons = []
# =========================
# CLASSE SALLE
# =========================

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


# =========================
# CREATION DU LABYRINTHE
# =========================

def creer_labyrinthe(nombre):
    racine = Salle(None, 1)
    salles = [racine]

    while len(salles) < nombre:
        possibles = []
        for salle in salles: # on vient ajouter tout les fils dans la liste des possibiklités
            for numero in range(1, 5):
                if numero == 1:
                    fils = salle.f1
                elif numero == 2:
                    fils = salle.f2
                elif numero == 3:
                  fils = salle.f3
                else:
                  fils = salle.f4
                if fils is None:
                    possibles.append((salle, numero))
        if not possibles: #si y'a pas de possibilité on stop mais ca devrait jamais arriver
            break
        parent, numero = random.choice(possibles) # parent prend le parent de la salle et numero son fils de dispo
        parent.set_fils(numero, 1)
        #cette partie ajouter a la liste salle l'enfant qui vient d'être créé 
        if numero == 1:
            enfant = parent.f1
        elif numero == 2:
            enfant = parent.f2
        elif numero == 3:
            enfant = parent.f3
        else:
            enfant = parent.f4

        salles.append(enfant)

    return racine, salles


# =========================
# INITIALISATION DE PYGAME
# =========================

pygame.init()

LARGEUR = 800
HAUTEUR = 600

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Labyrinthe quaternaire")

police = pygame.font.SysFont("Arial", 25)
petite_police = pygame.font.SysFont("Arial", 19)
horloge = pygame.time.Clock()

FOND = (30, 33, 45)
BLANC = (240, 240, 240)
GRIS = (150, 155, 165)
VERT = (50, 205, 130)
BLEU = (100, 170, 255)
ROUGE = (255, 100, 100)


# =========================
# SAISIE DU NOMBRE DE SALLES
# =========================

def demander_nombre_salles():
    nombre = ""
    message_erreur = ""

    while True:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return None

            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    return None

                elif evenement.key == pygame.K_RETURN:
                    if nombre.isdigit() and int(nombre) >= 1:
                        return int(nombre)
                    else:
                        message_erreur = "Entre un nombre entier positif."

                elif evenement.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                    message_erreur = ""
                #verifie que on tape bien un chiffre et que le nombre depasse pas 5 chiffre
                elif evenement.unicode.isdigit() and len(nombre) < 5:
                    nombre += evenement.unicode
                    message_erreur = ""

        ecran.fill(FOND)

        titre = police.render("LABYRINTHE QUATERNAIRE",True,BLEU)

        ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, 100)))

        question = police.render("Combien de salles veux-tu creer ?",True,BLANC)

        ecran.blit(question, question.get_rect(center=(LARGEUR // 2, 190)))

        # Champ de saisie
        champ = pygame.Rect(250, 240, 300, 55)
        pygame.draw.rect(ecran, BLANC, champ, 2, border_radius=5)

        contenu = police.render(nombre, True, BLANC)
        ecran.blit(contenu, contenu.get_rect(center=champ.center))

        aide = petite_police.render("Tape un nombre puis appuie sur Entree",True,GRIS)

        ecran.blit(aide, aide.get_rect(center=(LARGEUR // 2, 335)))

        sortie = petite_police.render("Echap : quitter",True,GRIS)

        ecran.blit(sortie, sortie.get_rect(center=(LARGEUR // 2, 375)))

        if message_erreur:
            erreur = petite_police.render(message_erreur, True, ROUGE)
            ecran.blit(erreur,erreur.get_rect(center=(LARGEUR // 2, 430)))

        pygame.display.flip() #pour afficher la chose 
        horloge.tick(30)


# =========================
# OUTILS D'AFFICHAGE
# =========================

def texte(message, x, y, couleur=BLANC, police_utilisee=None):
    #pour la police d'écriture
    if police_utilisee is None:
        police_utilisee = police
#pour transformer le texte en image a afficher
    image = police_utilisee.render(str(message), True, couleur)
    ecran.blit(image, (x, y))


# =========================
# DESSIN D'UNE SALLE
# =========================

    

def dessiner_salle(salle):
    global boutons

    centre_x = LARGEUR // 2
    y_pere = 155

    positions_x = [110, 303, 496, 689]
    y_fils = 340

    types = salle.voir_suivant()

    # Branches entre le pere et les fils
    for i in range(4):
        couleur = VERT if types[i] == 1 else GRIS

        pygame.draw.line(
            ecran,
            couleur,
            (centre_x, y_pere + 25),
            (positions_x[i], y_fils - 25),
            4
        )

    # Bouton du noeud pere
    rect_pere = pygame.Rect(
        centre_x - 75, y_pere - 25, 150, 50
    )

    pygame.draw.rect(
        ecran, BLEU, rect_pere, border_radius=10
    )

    identifiant = salles.index(salle) + 1
    nom = police.render(
        f"Salle {identifiant}", True, (20, 25, 35)
    )
    ecran.blit(nom, nom.get_rect(center=rect_pere.center))

    # Le clic sur le pere permet de remonter
    boutons.append((rect_pere, 0))

    # Les quatre boutons fils
    for i in range(4):
        x = positions_x[i]
        numero = i + 1

        accessible = types[i] == 1
        couleur = VERT if accessible else GRIS

        rect_fils = pygame.Rect(
            x - 55, y_fils - 25, 110, 50
        )

        pygame.draw.rect(
            ecran, couleur, rect_fils, border_radius=10
        )

        nom_fils = (
            f"Fils {numero}" if accessible else "Mur"
        )

        texte_fils = petite_police.render(
            nom_fils, True, (25, 30, 35)
        )

        ecran.blit(
            texte_fils,
            texte_fils.get_rect(center=rect_fils.center)
        )

        touche = petite_police.render(
            str(numero), True, BLANC
        )
        ecran.blit(
            touche,
            touche.get_rect(center=(x, y_fils + 45))
        )

        # Seules les salles accessibles sont cliquables
        if accessible:
            boutons.append((rect_fils, numero))


def afficher():
    ecran.fill(FOND)

    titre = police.render(
        "LABYRINTHE QUATERNAIRE", True, BLEU
    )
    ecran.blit(
        titre,
        titre.get_rect(center=(LARGEUR // 2, 35))
    )

    texte(
        f"Nombre de salles : {len(salles)}",
        20, 75
    )

    dessiner_salle(actuelle)

    texte(
        "Le noeud du haut est la salle actuelle",
        180, 420, BLANC, petite_police
    )

    texte(
        "Touches 1, 2, 3, 4 : acceder aux fils verts",
        145, 465, BLANC, petite_police
    )

    texte(
        "Touche 0 : retourner au pere",
        235, 500, BLANC, petite_police
    )

    texte(
        "Echap : quitter",
        320, 535, BLANC, petite_police
    )

    pygame.display.flip()



# =========================
# LANCEMENT
# =========================

nombre = demander_nombre_salles()

if nombre is None:
    pygame.quit()
    raise SystemExit

racine, salles = creer_labyrinthe(nombre)
actuelle = racine

actif = True

while actif:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            actif = False

        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_ESCAPE:
                actif = False
            #pour acceder au salle avec les boutons 1,2,3,4
            elif evenement.key in (pygame.K_0, pygame.K_KP0):
                actuelle = actuelle.acceder_salle(0)

            elif evenement.key in (pygame.K_1, pygame.K_KP1):
                actuelle = actuelle.acceder_salle(1)

            elif evenement.key in (pygame.K_2, pygame.K_KP2):
                actuelle = actuelle.acceder_salle(2)

            elif evenement.key in (pygame.K_3, pygame.K_KP3):
                actuelle = actuelle.acceder_salle(3)

            elif evenement.key in (pygame.K_4, pygame.K_KP4):
                actuelle = actuelle.acceder_salle(4)
        #c   fait de  meme mais pour avoir la version clickable
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if evenement.button == 1:
                position = evenement.pos

                for rectangle, numero in boutons:
                    if rectangle.collidepoint(position):
                        if numero == 0:
                               actuelle = actuelle.acceder_salle(0)
                        else:
                            actuelle = actuelle.acceder_salle(numero)

                        break
    afficher()
    horloge.tick(60)

pygame.quit()
