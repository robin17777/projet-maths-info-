import math
import textwrap
import pygame
from contexte import *
from outils import *
from rendu import *
from class_salle import zone_aventurier, zone_porte
from class_inventaire import porte_a_ouvrir
from rendu import _maj_confettis, _dessiner_touches, _image_menu   # les noms en _ ne passent pas avec 'import *'


cord_x=1150   # 1150 base
cord_y=480    # 480 base 
MONSTRE_POS = (1150, 630)   # où le monstre de la salle est dessiné


def afficher(actuelle, salles, racine,objets,inventaire):

    boutons.clear()
    boutons_salles.clear()
    boutond.clear()

    ecran.blit(FOND_DEGRADE, (0, 0))

    #carte du lab
    panneau(pygame.Rect(20, 125, 725, 385), "Arbre du labyrinthe")
    infos = [("Nombre de salles : ", len(salles)),
             ("Profondeur actuelle : ", actuelle.get_profondeur()),
             ("Profondeur max : ", profondeur_max(salles))]
    y_info = 190
    for libelle, valeur in infos:
        texte(libelle, 40, y_info, GRIS, petite_police)
        texte(valeur, 40 + petite_police.size(libelle)[0], y_info, BLANC, petite_police)
        y_info += 25

    #carte historique
    panneau(pygame.Rect(20, 525, 725, 200), "Chemin emprunté")
    y_hist = 587
    for ligne in lignes_historique():
        texte(ligne, 40, y_hist, BLANC, petite_police)
        y_hist += 25

    # carte objet 
    panneau(pygame.Rect(20, 740, 370, 125), "Objet sélectionné")
    objet_sel = inventaire.objet_selectionne()
    if objet_sel is None:
        texte("Aucun objet sélectionné", 40, 795, GRIS, petite_police)
        texte("(touches 5 à 9 ou clic sur une case)", 40, 822, GRIS, petite_police)
    else:
        texte(objet_sel.nom, 40, 797, JAUNE, police)
        usages = f"Usages : {objet_sel.usages}/{objet_sel.usages_max}"
        texte(usages, 370 - petite_police.size(usages)[0], 801, BLANC, petite_police)
        texte(objet_sel.description, 40, 832, GRIS, petite_police)

    # pancarte du monstre de la salle, à côté de la carte objet
    panneau(pygame.Rect(400, 740, 345, 125), "Monstre de la salle")
    monstre = actuelle.monstre
    if monstre is None:
        texte("Aucun monstre ici", 420, 805, GRIS, petite_police)
    else:
        texte(monstre.nom, 420, 797, ROUGE, police)
        degats = f"Dégâts : {monstre.degats}"
        texte(degats, 725 - petite_police.size(degats)[0], 801, BLANC, petite_police)
        # barre de PV
        ratio = monstre.pv / monstre.pv_max
        couleur_pv = VERT if ratio > 0.5 else (ORANGE if ratio > 0.25 else ROUGE)
        barre = pygame.Rect(420, 838, 170, 16)
        pygame.draw.rect(ecran, FOND, barre, border_radius=6)
        if monstre.pv > 0:
            pygame.draw.rect(ecran, couleur_pv, (barre.x, barre.y, max(8, round(barre.width * ratio)), barre.height), border_radius=6)
        pygame.draw.rect(ecran, GRIS, barre, 2, border_radius=6)
        texte(f"PV : {monstre.pv}/{monstre.pv_max}", barre.right + 12, 833, BLANC, petite_police)

    dessiner_salle(actuelle, salles,racine,objets,inventaire)

    pygame.display.flip()


def dessiner_salle(salle, salles,racine,objets,inventaire):
    boutons.clear()
    boutond.clear()


    y_pere = 245
    positions_x = [195, 315, 435, 555] # des 4 fils sur la largeur 
    y_fils = 440
    temps = pygame.time.get_ticks()

    types = salle.voir_suivant()

    rect_aventurier=pygame.Rect((cord_x-10, cord_y-10), (25, 25))

    #image salle 
    if salle==racine:
        image(ecran, "textures/terrain/salle_vide.png", (1150, 550), (700, 700))
    else:
        image(ecran, "textures/terrain/salle.png", (1150, 550), (700, 700))

    # murs , portes fermées 
    for numero in range(1, 5):
        if types[numero - 1] == 0:
            pos, taille, angle = POS_MURS[numero]
            image(ecran, "textures/terrain/mur.png", pos, taille, angle=angle)
        elif salle.porte_fermee(numero):
            image_dans_trou(f"textures/terrain/porte_{salle.get_fils(numero).porte}.png", numero, ANGLES_PORTES[numero])
        elif types[numero - 1] == 3:
            image_dans_trou("textures/terrain/tresor.png", numero)

    #monstre de la salle (dessiné sous les objets et l'aventurier)
    if salle.monstre is not None:
        mx, my = MONSTRE_POS
        ombre_sol((mx, my + 62), 100, 26, 80)
        flottement_m = round(math.sin(temps / 500) * 3)
        img_monstre = _image_menu(salle.monstre.image, 130)
        if img_monstre is not None:
            ecran.blit(img_monstre, img_monstre.get_rect(center=(mx, my + flottement_m)))
        else:   # image absente : carré rouge temporaire
            pygame.draw.rect(ecran, ROUGE, pygame.Rect(mx - 50, my - 50 + flottement_m, 100, 100), 3, border_radius=10)
            texte("?", mx, my + flottement_m, ROUGE, grande_police, centrer=True)

    #images objets
    for objet in objets:
        if objet.salle is salle and not objet.ramasse:
            if objet.est_sous(rect_aventurier, salle):
                lueur(objet.get_rect(), JAUNE, 14, 12)
            ombre_sol((objet.x, objet.y + objet.taille[1] // 2 - 4), 40, 12, 80)
            flottement = round(math.sin(temps / 350 + objet.x) * 3)
            if objet.image:
                image(ecran, objet.image, (objet.x, objet.y + flottement), objet.taille)
            else:
                pygame.draw.rect(ecran, JAUNE, objet.get_rect().move(0, flottement), 2)   # carré temporaire

    #image personage
    ombre_sol((cord_x, cord_y + 38), 56, 16, 80)
    image(ecran, "textures/personnage/aventurier.png", (cord_x, cord_y + 13), (100, 100))
    #pygame.draw.rect(ecran, VERT, rect_aventurier, 2)

    #image inventaire
    image(ecran,"textures/hud/inventaire.png",(1150,180),(600,188))

    #objets rangés dans les cases de l'inventaire
    for i, slot in enumerate(SLOTS_INVENTAIRE):
        if AFFICHER_SLOTS:
            pygame.draw.rect(ecran, VERT, slot, 1)
        if inventaire.selection == i:
            cadre = slot.inflate(10, 10)
            lueur(cadre, JAUNE, 8, 12)
            pygame.draw.rect(ecran, JAUNE, cadre, 3, border_radius=6)
        if i < len(inventaire.objets):
            objet = inventaire.objets[i]
            if objet.image:
                image(ecran, objet.image, slot.center, (slot.width - 4, slot.height - 4))
            else:
                texte(objet.nom, slot.centerx, slot.centery, BLANC, petite_police, centrer=True)


    # Bouton rentrer
    rentrer = pygame.Rect(1050, 50, 130, 40)
    bouton(rentrer, "Entrer", VERT, actif=zone_aventurier(salle, racine, cord_x, cord_y) is not None)
    boutons.append((rentrer, "rentrer"))

    # Bouton récuperer
    recup = pygame.Rect(900, 50, 130, 40)
    sur_objet = any(objet.est_sous(rect_aventurier, salle) for objet in objets)
    bouton(recup, "Récupérer", VERT, actif=sur_objet)
    boutons.append((recup, "recuperer"))

    # Bouton utiliser (grisé tant qu'on n'est pas devant une porte avec la bonne clé)
    use = pygame.Rect(750, 50, 130, 40)
    bouton(use, "Utiliser", VERT, actif=porte_a_ouvrir(salle, inventaire, cord_x, cord_y) is not None)
    boutons.append((use, "utiliser"))

    # Bouton lâcher
    lacher = pygame.Rect(600, 50, 130, 40)
    bouton(lacher, "Lâcher", VERT, actif=inventaire.selection is not None)
    boutons.append((lacher, "lacher"))


    # Bouton paramètres
    settings = pygame.Rect(LARGEUR-150, 20, 130, 40)
    boutons.append((settings, "parametres"))
    boutond.append((settings, "parametres"))

    # Bouton comment jouer (juste à gauche de Paramètres)
    aide = pygame.Rect(LARGEUR-310, 20, 150, 40)
    boutons.append((aide, "aide"))
    boutond.append((aide, "aide"))

    # Bouton autre lab
    autre_lab = pygame.Rect(20, 20, 145, 40)
    boutons.append((autre_lab, "autrelab"))
    boutond.append((autre_lab, "autrelab"))

    # Bouton nouveau lab
    nv_lab = pygame.Rect(185, 20, 176, 40)
    boutons.append((nv_lab, "nvlab"))
    boutond.append((nv_lab, "nvlab"))

    # Bouton clear
    reset = pygame.Rect(20, 70, 220, 40)
    boutons.append((reset, "reset"))
    boutond.append((reset, "reset"))


    # Dessin des boutons du haut (effet de survol géré par bouton())
    textes = {"reset":"Réinitialiser l'historique",
              "parametres": "Parametres",
              "aide": "Comment jouer",
              "autrelab": "Autre labyrinthe",
              "nvlab": "Nouveau labyrinthe"}

    for rect_b, nom in boutond:
        bouton(rect_b, textes[nom], BLEU)


    # Couleur de chaque fils (et de sa branche)
    infos_fils = []
    for i in range(4):
        numero = i + 1
        verrouille = salle.porte_fermee(numero)
        accessible = (types[i] == 1 or types[i] == 3) and not verrouille
        if verrouille:
            couleur = COULEURS_PORTES[salle.get_fils(numero).porte]
        elif types[i] == 1:
            couleur = VERT
        elif types[i] == 3:
            couleur = JAUNE
        else:
            couleur = (71, 85, 105)
        infos_fils.append((verrouille, accessible, couleur))

    # Branches entre le pere et les fils
    for i in range(4):
        couleur = infos_fils[i][2]
        debut = (LARGEUR//4, y_pere + 25)
        fin = (positions_x[i], y_fils - 25)
        pygame.draw.line(ecran, couleur, debut, fin, 4)

    # Noeud du pere (la salle actuelle)
    rect_pere = pygame.Rect(LARGEUR//4 - 75, y_pere - 25, 150, 50)
    couleur_pere = JAUNE if salle.get_type_fils()==3 else ORANGE
    if salle.get_type_fils()==3:
        text="Sortie"
    else:
        identifiant = salles.index(salle) + 1
        text=f"Salle {identifiant}"
    pere_survole = salle.pere is not None and rect_pere.collidepoint(pygame.mouse.get_pos())
    aventurier_au_milieu = zone_aventurier(salle, racine, cord_x, cord_y) == 0
    lueur_noeud(rect_pere, couleur_pere, intense=pere_survole or aventurier_au_milieu)
    bouton(rect_pere, text, couleur_pere, cliquable=salle.pere is not None, police_utilisee=police)
    if salle.pere is not None:
        badge_touche((rect_pere.left - 28, rect_pere.centery), "0")
    """Ici jusqu'a la fin ca sert pour les boutons_salles"""               
    # Le clic sur le pere permet de remonter
    boutons_salles.append((rect_pere, 0))

    # Les quatre boutons_salles fils
    for i in range(4):
        x = positions_x[i]
        numero = i + 1
        verrouille, accessible, couleur = infos_fils[i]

        rect_fils = pygame.Rect(x - 55, y_fils - 25, 110, 50)

        if types[i] != 0:      # pas de lueur sur un mur
            fils_survole = accessible and rect_fils.collidepoint(pygame.mouse.get_pos())
            aventurier_sur_porte = zone_porte(salle, cord_x, cord_y) == numero
            lueur_noeud(rect_fils, couleur, intense=fils_survole or aventurier_sur_porte, rayon=10, etendue=12)

        if verrouille:
            nom_fils = f"Porte {NOMS_PORTES[salle.get_fils(numero).porte]}"
        elif types[i] == 1:
            nom_fils =f"Fils {numero}"
        elif types[i]==3:
            nom_fils = "Sortie"
        else:
            nom_fils ="Mur"
        bouton(rect_fils, nom_fils, couleur, actif=types[i] != 0, cliquable=accessible)

        #pour mettre le chiffre a taper sous chaque fils 
        badge_touche((x, y_fils + 45), numero)

        # Seules les salles accessibles sont cliquables
        if accessible:
            boutons_salles.append((rect_fils, numero))

def afficher_parametres():
    ecran.blit(FOND_DEGRADE, (0, 0))
    boutons.clear()

    texte("PARAMETRES", LARGEUR // 2, 50, BLEU, grande_police, centrer=True)
    texte("Touches et navigation", LARGEUR // 2, 95, GRIS, police, centrer=True)
    pygame.draw.line(ecran, GRIS, (LARGEUR // 2 - 120, 120), (LARGEUR // 2 + 120, 120), 2)

    # Bouton retour
    retour = pygame.Rect(LARGEUR - 150, 20, 130, 40)
    bouton(retour, "Retour", BLEU)
    boutons.append((retour, "retour"))

    # (touches à afficher, description, couleur de la barre d'accent)
    # 4e élément optionnel = mini bouton dessiné à la main, affiché avant les touches
    #IA
    lignes = [
        (["1", "2", "3", "4"],                    "Accéder aux fils verts",                VERT),
        (["0"],                                   "Retourner à la salle père",             ORANGE),
        (["entrer"],                              "Entrer dans la salle (sur une porte)",  BLEU),
        (["haut", "gauche", "bas", "droite"],     "Déplacer l'aventurier dans la salle",   BLEU),
        (["5", "6", "7", "8", "9"],               "Sélectionner un objet (touche ou clic)", JAUNE),
        (["f"],                                   "Ramasser l'objet sous l'aventurier",    JAUNE, "Récupérer"),
        (["e"],                                   "Ouvrir une porte (clé sélectionnée)",   JAUNE, "Utiliser"),
        (["a"],                                   "Lâcher l'objet sélectionné",            JAUNE, "Lâcher"),
        (["esc"],                                 "Quitter le jeu",                        ROUGE),
    ]

    x_carte, largeur_carte = 250, 1000
    hauteur_carte, pas = 64, 74
    y = 150
    for touches, description, accent, *reste in lignes:
        bouton_txt = reste[0] if reste else None
        carte = pygame.Rect(x_carte, y, largeur_carte, hauteur_carte)
        ombre(carte, 12, decalage=4, alpha=70)
        pygame.draw.rect(ecran, CARTE, carte, border_radius=12)
        pygame.draw.rect(ecran, accent, (carte.x, carte.y + 10, 6, carte.height - 20), border_radius=3)

        x_touches = carte.x + 30
        if bouton_txt is not None:
            rect_mini = pygame.Rect(carte.x + 30, carte.centery - 20, 130, 40)
            bouton(rect_mini, bouton_txt, VERT, cliquable=False)
            x_touches = rect_mini.right + 20
        _dessiner_touches(touches, x_touches, carte.centery)

        img_txt = police.render(description, True, BLANC)
        ecran.blit(img_txt, (carte.x + 400, carte.centery - img_txt.get_height() // 2))
        y += pas

    texte("Le noeud du haut est la salle actuelle", LARGEUR // 2, y + 30, BLEU, police, centrer=True)

    pygame.display.flip()


def afficher_aide():
    """Page « Comment jouer » : 6 cartes qui expliquent les règles et les touches."""
    ecran.blit(FOND_DEGRADE, (0, 0))
    boutons.clear()

    texte("COMMENT JOUER", LARGEUR // 2, 50, BLEU, grande_police, centrer=True)
    texte("Trouve la sortie du labyrinthe", LARGEUR // 2, 95, GRIS, police, centrer=True)
    pygame.draw.line(ecran, GRIS, (LARGEUR // 2 - 120, 120), (LARGEUR // 2 + 120, 120), 2)

    # Bouton retour
    retour = pygame.Rect(LARGEUR - 150, 20, 130, 40)
    bouton(retour, "Retour", BLEU)
    boutons.append((retour, "retour"))

    # (titre, couleur d'accent, explication)
    rubriques = [
        ("Le but", VERT,
         "Atteins la sortie du labyrinthe. Dans l'arbre à gauche, le nœud du haut est ta salle "
         "actuelle et les 4 nœuds du bas sont ses fils : vert = salle, gris = mur, jaune = sortie."),
        ("Se déplacer", BLEU,
         "Déplace l'aventurier avec les flèches ou ZQSD. Place-toi sur une porte ou au milieu de la "
         "salle puis appuie sur Entrée. Les touches 1 à 4 vont directement vers un fils, 0 revient à la salle père."),
        ("Les objets", JAUNE,
         "Marche sur un objet et appuie sur F pour le ramasser. L'inventaire a 5 cases : touches 5 à 9 "
         "ou clic pour sélectionner, A pour lâcher l'objet choisi."),
        ("Portes et clés", ROUGE,
         "Une porte colorée bloque le passage. Trouve la clé de la même couleur, sélectionne-la, "
         "mets-toi devant la porte et appuie sur E. La clé est consommée."),
        ("Le chemin emprunté", ORANGE,
         "Le panneau « Chemin emprunté » garde la trace de tes déplacements. Le bouton "
         "« Réinitialiser l'historique » l'efface sans changer de salle."),
        ("Les labyrinthes", VERT,
         "« Autre labyrinthe » en génère un nouveau avec les mêmes options. « Nouveau labyrinthe » te laisse "
         "choisir le nombre de salles, les portes, les objets et une sortie verrouillée."),
    ]

    largeur_carte, hauteur_carte = 680, 190
    colonnes_x = (60, 760)
    y_depart, pas = 150, 205

    for i, (titre, accent, description) in enumerate(rubriques):
        carte = pygame.Rect(colonnes_x[i % 2], y_depart + (i // 2) * pas, largeur_carte, hauteur_carte)
        ombre(carte, 12, decalage=4, alpha=70)
        pygame.draw.rect(ecran, CARTE, carte, border_radius=12)
        pygame.draw.rect(ecran, CARTE_BORD, carte, 2, border_radius=12)
        pygame.draw.rect(ecran, accent, (carte.x, carte.y + 14, 6, carte.height - 28), border_radius=3)

        # pastille numérotée + titre
        centre = (carte.x + 50, carte.y + 40)
        pygame.draw.circle(ecran, accent, centre, 22)
        texte(i + 1, centre[0], centre[1], GRISF, police, centrer=True)
        texte(titre, carte.x + 90, carte.y + 24, accent, police)
        pygame.draw.line(ecran, CARTE_BORD, (carte.x + 25, carte.y + 72), (carte.right - 25, carte.y + 72), 2)

        # texte d'explication, coupé en lignes
        for n, ligne in enumerate(textwrap.wrap(description, width=62)[:4]):
            texte(ligne, carte.x + 30, carte.y + 84 + n * 26, TEXTE_OFF, petite_police)

    texte("Échap pour quitter le jeu", LARGEUR // 2, 825, GRIS, petite_police, centrer=True)

    pygame.display.flip()


def afficher_gagne():
    ecran.blit(FOND_DEGRADE, (0, 0))
    boutons.clear()
    _maj_confettis()

    carte = pygame.Rect(LARGEUR // 2 - 350, 200, 700, 420)
    lueur(carte, JAUNE, 24, 14)
    panneau(carte, rayon=24)

    flottement = math.sin(pygame.time.get_ticks() / 400) * 6
    texte("VOUS AVEZ GAGNÉ", LARGEUR // 2, 290 + flottement, JAUNE, titre_police, centrer=True)
    texte("Tu as trouvé la sortie du labyrinthe !", LARGEUR // 2, 365, BLANC, police, centrer=True)
    pygame.draw.line(ecran, CARTE_BORD, (LARGEUR // 2 - 200, 410), (LARGEUR // 2 + 200, 410), 2)

    autre_lab = pygame.Rect(LARGEUR // 2 - 140, 450, 280, 52)
    bouton(autre_lab, "Autre labyrinthe", BLEU, police_utilisee=police)
    boutons.append((autre_lab, "autrelab"))

    nv_lab = pygame.Rect(LARGEUR // 2 - 140, 525, 280, 52)
    bouton(nv_lab, "Nouveau labyrinthe", BLEU, police_utilisee=police)
    boutons.append((nv_lab, "nvlab"))

    pygame.display.flip()