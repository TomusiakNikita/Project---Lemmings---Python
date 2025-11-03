class Lemmings :
    
    def __init__(self, ligne, colonne, direction = 1) :
        self.l = ligne
        self.c = colonne
        self.d = direction # si direction = 1 le lemmings va à droite si direction = -1 le lemmings va à gauche
        self.j = self.lemmings
        
    def __str__(self) :
        # Donne la direction du lemming
        if self.d == 1 :
            self.lemmings == ">"
            return self.lemmings
        elif self.d == -1 :
            self.lemmings == "<"
            return self.lemmings
        
    def action(self) :
        # Permet de changer la direction du lemming si il il y a un obstacle
        if self.lemmings[self.c][self.l+1] == "" :
            self.l = self.l + 1
        elif self.c+1 == "#" or "<" or ">":
            self.d = - 1
            print(__str__(self))
        elif self.c-1 == "#" or "<" or ">" :
            self.d = 1
            print(__str__(self))
        else :
            self.c = self.c + 1
        

    def sort(self) :
        #Fait sortir le lemming du jeu s'il atteint la sortie
        if self.lemmings[self.c][self.l] == 0 :
            self.lemmings == ""
            
            
    direction = 1
    print(__str__())

            

            
            

            
        