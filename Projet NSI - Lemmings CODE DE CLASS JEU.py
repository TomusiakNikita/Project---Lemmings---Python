class Jeu:
    def __init__(self, Carte):
        self.grotte = []
        # Lecture du fichier carte et création de la grotte (tableau 2D)
        with open(Carte, "r") as file:
            for i in file:
                # Suppression du caractère de retour à la ligne si présent
                if i and i[-1]== '\n': # Vérifie si la ligne n'est pas vide et si le dernier caractère est un retour à la ligne
                    # Si oui, enlève le dernier caractère (le retour à la ligne) de la chaîne
                    i = i[:-1]
                self.grotte.append(list(i))
        self.lemmings = []

        # Recherche de la première colonne libre sur la première ligne
        for column in range(len(self.grotte[0])):
            if self.grotte[0][column] == ' ':
                self.start_column = column
                break
        col = self.start_column
        # Recherche de la première case libre dans cette colonne, sous le mur
        for row in range(len(self.grotte)):
            if self.grotte[row][col] == ' ':
                self.start_row = row
            if self.grotte[row][col] == '#':
                break

    def affiche(self):
        # Affiche la grotte ligne par ligne
        for ligne in self.grotte:
            ligne_str = ""
            for char in ligne:
                ligne_str+=char  # Ajoute chaque caractère à la chaîne de la ligne
            print(ligne_str)  # Affiche la ligne complète

    def tour(self):
        # Fait agir chaque lemming une fois et affiche le nouvel état du jeu
        for lemming in self.lemmings:
            lemming.action()
        self.affiche()

    def demarre(self):
        # Boucle principale du jeu : attend les commandes de l'utilisateur
        self.affiche()
        while 1:
            print("Saisirez 'l' pour ajouter un lemming, 'q' pour quitter et Entrée pour jouer un tour")
            commande = input()
            if commande == "l":
                # Ajoute un lemming à la position de départ détectée
                self.lemmings.append({'x': self.start_row, 'y': self.start_column})
                self.grotte[self.start_row][self.start_column] = 'L'  # Place le lemming sur la carte
                self.affiche()
            elif commande == "q":
                # Quitte la boucle et termine le jeu
                break
            else:
                # Joue un tour si l'utilisateur appuie sur Entrée
                self.tour()

# Création d'une instance du jeu et lancement de la boucle principale
first_play = Jeu("grotte.txt")
first_play.demarre()
