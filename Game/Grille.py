import random

class Grille:
    
    grille = []
    score = 0
    
    def __init__(self):
        self.grille = self.grilleVide()
        
    def grilleVide(self):
        grille = [
            [0, 0, 0, 0], 
            [0, 0, 0, 0], 
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        return grille
    
    def afficher(self):
        print("Score total ", self.score)
        for ligne in range(0, 4):
            for colonne in range(0, 4):
                print(self.grille[ligne][colonne], end=' ')
            print()
    
    def ajoutNombreAleatoire(self):
        celluleVide = [(i, j) for i in range(4) for j in range(4) if self.grille[i][j] == 0]
        if celluleVide:
            i, j = random.choice(celluleVide)
            self.grille[i][j] = random.choice([2, 2, 2, 4])
    
    def ecrasementCellules(self, ligne):
        temp_ligne = [val for val in ligne if val != 0]
        for i in range(len(temp_ligne) - 1):
            if temp_ligne[i] == temp_ligne[i + 1]:
                temp_ligne[i] *= 2
                self.score += temp_ligne[i]
                temp_ligne[i + 1] = 0
        temp_ligne = [val for val in temp_ligne if val != 0] + [0] * (4 - len(temp_ligne))
        return temp_ligne
    
    def deplacementHaut(self):
        for j in range(4):
            col = [self.grille[i][j] for i in range(4)]
            colEcrase = self.ecrasementCellules(col)
            for i in range(len(colEcrase)):
                self.grille[i][j] = colEcrase[i]
        self.ajoutNombreAleatoire()
    
    def deplacementBas(self):
        for j in range(4):
            col = [self.grille[i][j] for i in range(4)][::-1]
            colEcrase = self.ecrasementCellules(col)
            for i in range(len(colEcrase)):
                self.grille[3 - i][j] = colEcrase[i]
        self.ajoutNombreAleatoire()

    
    def deplacementGauche(self):
        for i in range(4):
            ligne = self.grille[i]
            ligneEcrasee = self.ecrasementCellules(ligne)
            for j in range(len(ligneEcrasee)):
                self.grille[i][j] = ligneEcrasee[j]
        self.ajoutNombreAleatoire()

    
    def deplacementDroite(self):
        for i in range(4):
            ligne = self.grille[i][::-1]
            ligneEcrasee = self.ecrasementCellules(ligne)
            for j in range(len(ligneEcrasee)):
                self.grille[i][3 - j] = ligneEcrasee[j]
        self.ajoutNombreAleatoire()
            
    
    def deplacementAutorise(self, move):
        print("Mouvement envisagé :", move)
        grilleTempo = [row[:] for row in self.grille]
        
        if move == 'g':
            self.deplacementGauche()
        elif move == 'd':
            self.deplacementDroite()
        elif move == 'h':
            self.deplacementHaut()
        elif move == 'b':
            self.deplacementBas()
        else:
            print("Mouvement interdit")
            self.grille = [row[:] for row in grilleTempo]
            return False
        
        if grilleTempo == self.grille:
            print("Mouvement interdit")
            self.grille = [row[:] for row in grilleTempo]
            return False
        
        print("Mouvement autorisé")
        return True