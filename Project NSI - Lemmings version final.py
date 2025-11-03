class Jeu:
    def __init__(self, Carte):
        self.grotte = []  # La grotte est une matrice de cases (Case)
        # Lecture du fichier carte et création de la grotte
        with open(Carte, "r") as file:
            for i in file:
                # Supprime le retour à la ligne à la fin de chaque ligne
                if i and i[-1]== '\n':
                    i = i[:-1]
                ligne = []  # Liste pour la ligne courante
                # Pour chaque caractère de la ligne, crée une Case
                for char in i:
                    ligne.append(Case(char))
                self.grotte.append(ligne)  # Ajoute la ligne à la grotte
        self.lemmings = []  # Liste des lemmings en jeu
        self.lemmings_total = 0  # Compteur de lemmings créés
        self.lemmings_sortis = 0  # Compteur de lemmings sortis
        self.tours = 0  # Compteur de tours joués

        # Recherche de la première colonne libre sur la première ligne pour le départ
        for column in range(len(self.grotte[0])):
            if self.grotte[0][column].libre():
                self.start_column = column  # Sauvegarde la colonne de départ
                break
        col = self.start_column
        # Recherche de la première case libre dans cette colonne, sous le mur
        for row in range(len(self.grotte)):
            if self.grotte[row][col].libre():
                self.start_row = row  # Sauvegarde la ligne de départ
            if self.grotte[row][col].terrain == '#':
                break  # Arrête la recherche si on rencontre un mur

    def affiche(self):
        # Affiche la grotte ligne par ligne
        for ligne in self.grotte:
            ligne_str = ""
            # Construit la chaîne de caractères de la ligne à afficher
            for case in ligne:
                ligne_str += str(case)  # Utilise __str__ de Case
            print(ligne_str)  # Affiche la ligne complète

    def tour(self):
        # Fait agir chaque lemming une fois (copie pour éviter modification pendant la boucle)
        for lemming in self.lemmings[:]:
            lemming.action()
        self.tours += 1  # Incrémente le nombre de tours joués
        self.affiche()  # Affiche l'état actuel de la grotte

    def demarre(self):
        self.affiche()  # Affiche la grotte au début
        while 1:
            # Affiche les commandes disponibles à l'utilisateur
            print("Saisirez 'l' pour ajouter un lemming, 'q' pour quitter et Entrée pour jouer un tour")
            commande = input()
            if commande == "l":
                # Crée un nouveau lemming à la position de départ détectée
                lem = Lemming(self.start_row, self.start_column, 1, self)
                self.lemmings.append(lem)  # Ajoute le lemming à la liste
                self.grotte[self.start_row][self.start_column].arrivee(lem)  # Place le lemming sur la case
                self.lemmings_total += 1  # Incrémente le compteur de lemmings créés
                self.affiche()  # Affiche la grotte après ajout
            elif commande == "q":
                # Affiche les statistiques et quitte la boucle
                print("Nombre de lemmings créés :", self.lemmings_total)
                print("Nombre de lemmings sortis :", self.lemmings_sortis)
                print("Nombre de tours joués :", self.tours)
                break
            else:
                # Joue un tour si l'utilisateur appuie sur Entrée
                self.tour()

class Lemming:
    def __init__(self, l, c, d, j):
        self.l = l  # Ligne occupée par le lemming
        self.c = c  # Colonne occupée par le lemming
        self.d = d  # Direction (1 = droite, -1 = gauche)
        self.j = j  # Référence vers l'objet Jeu

    def __str__(self):
        # Renvoie le caractère selon la direction du lemming
        return '>' if self.d == 1 else '<'

    def action(self):
        # Tombe tant que la case en dessous est libre
        while self.l + 1 < len(self.j.grotte) and self.j.grotte[self.l + 1][self.c].libre():
            self.j.grotte[self.l][self.c].depart()  # Retire le lemming de la case actuelle
            self.l += 1  # Avance d'une ligne (tombe)
            self.j.grotte[self.l][self.c].arrivee(self)  # Place le lemming sur la nouvelle case
            # Vérifie si la case actuelle est une sortie après la chute
            if self.j.grotte[self.l][self.c].terrain == 'O':
                self.j.grotte[self.l][self.c].depart()  # Retire le lemming de la case de sortie
                self.j.lemmings_sortis += 1  # Incrémente le compteur de lemmings sortis
                if self in self.j.lemmings:  # Vérifie que le lemming est dans la liste
                    self.j.lemmings.remove(self)  # Retire le lemming de la liste
                return  # Termine l'action

        # Vérifie si la case en dessous est la sortie
        if self.l + 1 < len(self.j.grotte) and self.j.grotte[self.l + 1][self.c].terrain == 'O':
            self.j.grotte[self.l][self.c].depart()  # Retire le lemming de la case actuelle
            self.j.lemmings_sortis += 1  # Incrémente le compteur de lemmings sortis
            if self in self.j.lemmings:  # Vérifie que le lemming est dans la liste
                self.j.lemmings.remove(self)  # Retire le lemming de la liste
            return  # Termine l'action

        # Déplacement horizontal si possible (après la chute)
        next_c = self.c + self.d  # Calcule la prochaine colonne selon la direction
        # Vérifie si la case suivante dans la direction du déplacement est libre
        if 0 <= next_c < len(self.j.grotte[self.l]) and self.j.grotte[self.l][next_c].libre():
            self.j.grotte[self.l][self.c].depart()  # Retire le lemming de la case actuelle
            self.c = next_c  # Met à jour la colonne
            self.j.grotte[self.l][self.c].arrivee(self)  # Place le lemming sur la nouvelle case
            # Vérifie si la case actuelle est une sortie après le déplacement horizontal
            if self.j.grotte[self.l][self.c].terrain == 'O':
                self.j.grotte[self.l][self.c].depart()  # Retire le lemming de la case de sortie
                self.j.lemmings_sortis += 1  # Incrémente le compteur de lemmings sortis
                if self in self.j.lemmings:  # Vérifie que le lemming est dans la liste
                    self.j.lemmings.remove(self)  # Retire le lemming de la liste
                return  # Termine l'action
        # Si la case suivante dans la direction du déplacement est une sortie
        elif 0 <= next_c < len(self.j.grotte[self.l]) and self.j.grotte[self.l][next_c].terrain == 'O':
            self.j.grotte[self.l][self.c].depart()  # Retire le lemming de la case actuelle
            self.c = next_c  # Met à jour la colonne
            self.j.lemmings_sortis += 1  # Incrémente le compteur de lemmings sortis
            if self in self.j.lemmings:  # Vérifie que le lemming est dans la liste
                self.j.lemmings.remove(self)  # Retire le lemming de la liste
            return  # Termine l'action
        else:
            self.d = -self.d  # Change de direction si bloqué

    def sort(self):
        # Fait sortir le lemming du jeu
        self.j.grotte[self.l][self.c].depart()  # Retire le lemming de la case
        if self in self.j.lemmings:            # Vérifie qu'il est bien dans la liste
            self.j.lemmings.remove(self)       # Retire le lemming de la liste

class Case:
    """Représente une case de la grotte.
    terrain : '#'(mur), ' ' (vide), 'O' (sortie)
    lemming : objet Lemming présent sur la case, ou None si libre"""

    def __init__(self, terrain):
    
        self.terrain = terrain
        self.lemming = None

    def __str__(self):
        """role : Affiche le lemming s'il est présent, sinon le terrain."""
        if self.lemming is not None:
            return str(self.lemming)
        return self.terrain

    def libre(self):
        """role :True si la case n'est pas un mur ET n'est pas occupée."""
        return self.terrain != '#' and self.lemming is None

    def depart(self):
        """Retire le lemming présent (si présent)."""
        self.lemming = None

    def arrivee(self, lem):
        """role : Place le lemming sur la case, ou le fait sortir si c’est la sortie."""
    
        # Si c’est une sortie
        if self.terrain == 'O':
            lem.sort()   # on fait sortir le lemming
            return True

        # Si la case n’est pas libre, on ne peut pas poser le lemming
        if not self.libre():
            return False

        # Sinon, on met le lemming sur la case
        self.lemming = lem
        return True

        # Sinon, il faut que la case soit libre
        if not self.libre():
            return False

        self.lemming = lem
        return True
    
# Création d'une instance du jeu et lancement de la boucle principale
first_play = Jeu("c:\\NSI Documents\\2025-2026\\Projets\\grotte.txt")
first_play.demarre()