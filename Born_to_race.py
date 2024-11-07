import pyxel
import random, time

mode_de_diff = 2
nb_joueur = 1
LARGEUR_FENETRE = 120
LONGUEUR_FENETRE = 120
TAILLE_JOUEURS = 10
VITESSE_APPARITION = 30
nombre_de_vehicule = 3
LARGEUR_VOIE = LARGEUR_FENETRE // 4
SOIN = {
    "vitesse": LARGEUR_FENETRE // 30,
    "rayon": 3
}
SHIELD = {
    "vitesse": LARGEUR_FENETRE // 40,
    "rayon": 3
}
VOITURE = {
    "longueur": 15,
    "largeur": 10,
    "vitesse": LONGUEUR_FENETRE // 50 * mode_de_diff
}
MOTO = {
    "longueur": 10,
    "largeur": 5,
    "vitesse": LONGUEUR_FENETRE // 50 * mode_de_diff
}
CAMION = {
    "longueur": 20,
    "largeur": 10,
    "vitesse": LONGUEUR_FENETRE // 55 * mode_de_diff
}


class Jeu:
    def __init__(self, type):
        self.joueur1 = Joueur1()
        self.liste_vehicule = []
        self.liste_explosion = []
        self.liste_bonus = []
        self.type = type
        self.last_numbr = 0
        self.vitesse_apparition = VITESSE_APPARITION
        pyxel.load("sprites.pyxres")
        pyxel.run(self.draw, self.update)

    def colonne_deplacement(self, vehicule):
        largeur_vehicule = 0
        if vehicule == "voiture":
            largeur_vehicule = VOITURE["largeur"]
        if vehicule == "moto":
            largeur_vehicule == MOTO["largeur"]
        if vehicule == "camion":
            largeur_vehicule = CAMION["largeur"]

        nb_voie = 6

        nombre = random.randint(0, nb_voie - 1)
        if nombre == 0:
            return (LARGEUR_VOIE - largeur_vehicule) // 2
        if nombre == 1:
            return LARGEUR_FENETRE // nb_voie + ((LARGEUR_VOIE - largeur_vehicule) // 2)
        if nombre == 2:
            return LARGEUR_FENETRE // nb_voie * 2 + ((LARGEUR_VOIE - largeur_vehicule) // 2)
        if nombre == 3:
            return LARGEUR_FENETRE // nb_voie * 3 + ((LARGEUR_VOIE - largeur_vehicule) // 2)
        if nombre == 4:
            return LARGEUR_FENETRE // nb_voie * 4 + ((LARGEUR_VOIE - largeur_vehicule) // 2)
        if nombre == 5:
            return LARGEUR_FENETRE // nb_voie * 5 + ((LARGEUR_VOIE - largeur_vehicule) // 2)
        if nombre == 6:
            return LARGEUR_FENETRE // nb_voie * 6 + ((LARGEUR_VOIE - largeur_vehicule) // 2)

    def creation_vehicule(self):
        vehicule_apparait = random.randint(0, nombre_de_vehicule - 1)
        if vehicule_apparait == 0:
            if (pyxel.frame_count % self.vitesse_apparition == 0):
                self.liste_vehicule.append(Voiture(self.colonne_deplacement("voiture")))
        if vehicule_apparait == 1:
            if (pyxel.frame_count % self.vitesse_apparition == 0):
                self.liste_vehicule.append(Moto(self.colonne_deplacement("moto")))
        if vehicule_apparait == 2:
            if (pyxel.frame_count % self.vitesse_apparition == 0):
                self.liste_vehicule.append(Camion(self.colonne_deplacement("camion")))

    def creation_bonus(self):
        nb_aleatoire = random.randint(1, 20)
        if nb_aleatoire == 2 and (pyxel.frame_count % self.vitesse_apparition == 0):
            self.liste_bonus.append(Soin(random.randint(0, LARGEUR_FENETRE - SOIN["rayon"] - 2)))

    def creation_explosion(self, x, y):
        self.liste_explosion.append(Explosion(x, y))

    def suppression_vehicule(self):
        for vehicule in self.liste_vehicule:
            if vehicule.y == LONGUEUR_FENETRE:
                self.liste_vehicule.remove(vehicule)
                self.joueur1.score += 1

    def suppression_bonus(self):
        for bonus in self.liste_bonus:

            if isinstance(bonus, Soin):
                if bonus.x <= self.joueur1.x + SOIN[
                    "rayon"] * 2 and bonus.y <= self.joueur1.y + TAILLE_JOUEURS and bonus.x + SOIN[
                    "rayon"] * 2 >= self.joueur1.x and bonus.y + SOIN["rayon"] * 2 >= self.joueur1.y:
                    self.joueur1.vie += 1
                    self.liste_bonus.remove(bonus)
                    pyxel.playm((1))
            if bonus.y == LONGUEUR_FENETRE:
                self.liste_bonus.remove(bonus)

    def suppression_joueur(self):
        for vehicule in self.liste_vehicule:

            if isinstance(vehicule, Camion):
                if vehicule.x <= self.joueur1.x + CAMION[
                    "largeur"] and vehicule.y <= self.joueur1.y + TAILLE_JOUEURS and vehicule.x + CAMION[
                    "largeur"] >= self.joueur1.x and vehicule.y + CAMION["longueur"] >= self.joueur1.y:
                    pyxel.playm(2)
                    self.joueur1.vie -= 1
                    self.liste_vehicule.remove(vehicule)
                    self.creation_explosion(self.joueur1.x, self.joueur1.y)

            if isinstance(vehicule, Moto):
                if vehicule.x <= self.joueur1.x + MOTO[
                    "largeur"] and vehicule.y <= self.joueur1.y + TAILLE_JOUEURS and vehicule.x + MOTO[
                    "largeur"] >= self.joueur1.x and vehicule.y + MOTO["longueur"] >= self.joueur1.y:
                    pyxel.playm(2)
                    self.joueur1.vie -= 1
                    self.liste_vehicule.remove(vehicule)
                    self.creation_explosion(self.joueur1.x, self.joueur1.y)

            if isinstance(vehicule, Voiture):
                if vehicule.x <= self.joueur1.x + VOITURE[
                    "largeur"] and vehicule.y <= self.joueur1.y + TAILLE_JOUEURS and vehicule.x + VOITURE[
                    "largeur"] >= self.joueur1.x and vehicule.y + VOITURE["longueur"] >= self.joueur1.y:
                    pyxel.playm(2)
                    self.joueur1.vie -= 1
                    self.liste_vehicule.remove(vehicule)
                    self.creation_explosion(self.joueur1.x, self.joueur1.y)

    def animation_explosion(self):
        for explosion in self.liste_explosion:
            explosion.couleur += 1
            if explosion.couleur == 12:
                self.liste_explosion.remove(explosion)

    def update(self):

        if self.joueur1.vie > 0:
            self.joueur1.deplacement_j1()
            self.creation_vehicule()
            self.creation_bonus()
            self.suppression_bonus()
            self.suppression_joueur()
            self.suppression_vehicule()
            self.animation_explosion()

            for vehicule in self.liste_vehicule:

                if isinstance(vehicule, Voiture):
                    vehicule.mvt_voiture()

                if isinstance(vehicule, Moto):
                    vehicule.mvt_moto()

                if isinstance(vehicule, Camion):
                    vehicule.mvt_camion()

            for explosion in self.liste_explosion:
                explosion.dessin_explosion()

            for bonus in self.liste_bonus:
                if isinstance(bonus, Soin):
                    bonus.mvt_soin()

            if self.type == "hard" and self.joueur1.score % 10 == 0 and self.joueur1.score != self.last_numbr and self.vitesse_apparition != 0:
                self.last_numbr += 10
                self.vitesse_apparition = self.vitesse_apparition - 1

    def draw(self):
        pyxel.cls(0)

        if self.joueur1.vie > 0:

            self.joueur1.dessin_joueur1()
            pyxel.text(LARGEUR_FENETRE // 20, LONGUEUR_FENETRE // 24, f"vies : {self.joueur1.vie}", 7)
            pyxel.text(LARGEUR_FENETRE // 20, (LONGUEUR_FENETRE // 24 + 10), f"score : {self.joueur1.score}", 7)
            for vehicule in self.liste_vehicule:

                if isinstance(vehicule, Voiture):
                    vehicule.dessin_voiture()

                if isinstance(vehicule, Moto):
                    vehicule.dessin_moto()

                if isinstance(vehicule, Camion):
                    vehicule.dessin_camion()

            for bonus in self.liste_bonus:
                if isinstance(bonus, Soin):
                    bonus.dessin_soin()

        else:
            pyxel.cls(0)
            pyxel.text(LARGEUR_FENETRE // 2 - len("game over") / 2 * 4, LONGUEUR_FENETRE // 2, 'GAME OVER', 7)
            pyxel.text(LARGEUR_FENETRE // 2 - len(f"votre score est de {self.joueur1.score}") / 2 * 4,
                       LONGUEUR_FENETRE // 2 + 10, f"VOTRE SCORE EST DE {self.joueur1.score}", 7)


class Joueur1:
    def __init__(self):
        self.x = LARGEUR_FENETRE // 2
        self.y = LONGUEUR_FENETRE // 2 + LONGUEUR_FENETRE // 6
        self.score = 0
        self.vie = 3

    def dessin_joueur1(self):
        pyxel.blt(self.x, self.y, 0, 0, 16, 11, 16)

    def deplacement_j1(self):
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < LARGEUR_FENETRE - TAILLE_JOUEURS - 2:
            self.x = self.x + LARGEUR_FENETRE // 40
        if nb_joueur == 1:
            if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
                self.x = self.x - LARGEUR_FENETRE // 40
        elif nb_joueur == 2:
            if pyxel.btn(pyxel.KEY_LEFT) and self.x > LARGEUR_FENETRE // 2:
                self.x = self.x - LARGEUR_FENETRE // 40


class Voiture:
    def __init__(self, x):
        self.x = x
        self.y = 0

    def mvt_voiture(self):
        self.y = self.y + VOITURE["vitesse"]

    def dessin_voiture(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 11, 16)


class Moto:
    def __init__(self, x):
        self.x = x
        self.y = 0

    def mvt_moto(self):
        self.y = self.y + MOTO["vitesse"]

    def dessin_moto(self):
        pyxel.blt(self.x, self.y, 0, 16, 0, 5, 11)


class Camion:

    def __init__(self, x):
        self.x = x
        self.y = 0

    def mvt_camion(self):
        self.y = self.y + CAMION["vitesse"]

    def dessin_camion(self):
        pyxel.blt(self.x, self.y, 0, 24, 0, 11, 21)


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.couleur = 0

    def dessin_explosion(self):
        pyxel.circb(self.x + TAILLE_JOUEURS // 2, self.y, 8 * (self.couleur // 4), 8 + self.couleur % 3)


class Soin:
    def __init__(self, x):
        self.x = x
        self.y = 0

    def mvt_soin(self):
        self.y = self.y + SOIN["vitesse"]

    def dessin_soin(self):
        pyxel.blt(self.x, self.y, 0, 16, 16, 7, 7)


import pyxel

TAILLE_POINT = 8
LARGEUR_FENETRE = 120
LONGUEUR_FENETRE = 120


class Menu:
    def __init__(self):
        pyxel.init(LARGEUR_FENETRE, LONGUEUR_FENETRE, title="born to race")
        self.point = Point()
        pyxel.load("sprites.pyxres")
        pyxel.playm(0, loop=True)
        pyxel.run(self.draw, self.update)

    def update(self):
        self.point.deplacement_point()
        if self.point.y == LARGEUR_FENETRE // 2 - 2:
            if pyxel.btnp(pyxel.KEY_RETURN):
                Jeu("easy")
        if self.point.y == LARGEUR_FENETRE // 2 + TAILLE_POINT:
            if pyxel.btnp(pyxel.KEY_RETURN):
                Jeu("hard")
        if self.point.y == LARGEUR_FENETRE // 2 + TAILLE_POINT + 10:
            if pyxel.btnp(pyxel.KEY_RETURN):
                quit()

    def draw(self):
        pyxel.cls(1)
        pyxel.text(LARGEUR_FENETRE // 2 - len('BORN TO RACE') / 2 * 4, LONGUEUR_FENETRE // 4, "BORN TO RACE", 10)
        pyxel.text(LARGEUR_FENETRE // 2 - len('UP FOR THE CHALLENGE') / 2 * 4, LONGUEUR_FENETRE // 4 + 10,
                   "up for the challenge ?", 10)
        pyxel.text(TAILLE_POINT + 4, LONGUEUR_FENETRE // 2, "EASY MODE", 13)
        pyxel.text(TAILLE_POINT + 4, LONGUEUR_FENETRE // 2 + 10, "HARD MODE", 13)
        pyxel.text(TAILLE_POINT + 4, LONGUEUR_FENETRE // 2 + 20, "EXIT", 13)

        self.point.dessiner_point()


class Point:
    def __init__(self):
        self.x = 2
        self.y = LONGUEUR_FENETRE // 2 - 2
        self.haut = True
        self.bas = False

    def deplacement_point(self):
        if self.haut is False and pyxel.btnp(pyxel.KEY_UP):
            if self.bas is True:
                self.bas = False
            self.y = self.y - (TAILLE_POINT + 2)

        if self.bas is False and pyxel.btnp(pyxel.KEY_DOWN):
            if self.haut is True:
                self.haut = False
            self.y = self.y + (TAILLE_POINT + 2)

        if self.y == LONGUEUR_FENETRE // 2 - 2:
            self.haut = True

        if self.y == LONGUEUR_FENETRE // 2 + (TAILLE_POINT - 2) * 3:
            self.bas = True

    def dessiner_point(self):
        pyxel.rect(self.x, self.y, TAILLE_POINT, TAILLE_POINT, 8)
        if pyxel.btnp(pyxel.KEY_RETURN):
            pyxel.rect(self.x, self.y, TAILLE_POINT, TAILLE_POINT, 5)


Menu()
