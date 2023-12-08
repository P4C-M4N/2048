import copy
import random

class Grille:
    
    grille = []
    score = 0
    grilleOld = []
    
    def __init__(self):
        self.grille = self.grilleVide()
        self.grilleOld
        self.ajoutNombreAleatoire()
        self.ajoutNombreAleatoire()
        
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
            val = random.choice([2, 2, 2, 4])
            self.grille[i][j] = val
    
    def ecrasementCellules(self, ligne):
        temp_ligne = [val for val in ligne if val != 0]

        for i in range(len(temp_ligne) - 1):
            if temp_ligne[i] == temp_ligne[i + 1]:
                temp_ligne[i] *= 2
                self.score += temp_ligne[i]
                temp_ligne[i + 1] = 0

        # Filtrez à nouveau les zéros après l'écrasement
        temp_ligne = [val for val in temp_ligne if val != 0]

        # Ajoutez des zéros pour compléter la ligne
        temp_ligne += [0] * (4 - len(temp_ligne))

        return temp_ligne

    
    def deplacementHaut(self):
        for j in range(4):
            col = [self.grille[i][j] for i in range(4)]
            colEcrase = self.ecrasementCellules(col)
            for i in range(len(colEcrase)):
                self.grille[i][j] = colEcrase[i]
        
    
    def deplacementBas(self):
        for j in range(4):
            col = [self.grille[i][j] for i in range(4)][::-1]
            colEcrase = self.ecrasementCellules(col)
            for i in range(len(colEcrase)):
                self.grille[3 - i][j] = colEcrase[i]
        

    
    def deplacementGauche(self):
        for i in range(4):
            ligne = self.grille[i]
            ligneEcrasee = self.ecrasementCellules(ligne)
            for j in range(len(ligneEcrasee)):
                self.grille[i][j] = ligneEcrasee[j]
        

    
    def deplacementDroite(self):
        for i in range(4):
            ligne = self.grille[i][::-1]
            ligneEcrasee = self.ecrasementCellules(ligne)
            for j in range(len(ligneEcrasee)):
                self.grille[i][3 - j] = ligneEcrasee[j]
        
        
    def TryDeplacement(self, move):
        #Save the old grid
        self.grilleOld = copy.deepcopy(self.grille)
        #print("Mouvement envisagé :", move)
        if self.deplacementAutorise(move):
            #print("mouvement ok")
            if move == 'g':
                self.deplacementGauche()
            elif move == 'd':
                self.deplacementDroite()
            elif move == 'h':
                self.deplacementHaut()
            elif move == 'b':
                self.deplacementBas()
            return True
        else :
            #print("mouvement interdit")  
            return False
    
    def deplacementAutorise(self, move):
        grilleTempo = Grille()
        grilleTempo.grille = copy.deepcopy(self.grille)

        if move == 'g':
            grilleTempo.deplacementGauche()
        elif move == 'd':
            grilleTempo.deplacementDroite()
        elif move == 'h':
            grilleTempo.deplacementHaut()
        elif move == 'b':
            grilleTempo.deplacementBas()
        else:
            return False

        return grilleTempo.grille != self.grille  
    
    def getPlusGrandNombre(self):
        return max(max(self.grille))
    
    def getAncienPlusGrandNombre(self):
        return max(max(self.grilleOld))
    
    def getPlacePlusGrandNombre(self):
        list_place = []
        for i in range(4):
            for j in range(4):
                if self.grille[i][j] == self.getPlusGrandNombre():
                    list_place.append([i, j])
        return list_place

    def getPlaceAncienPlusGrandNombre(self):
        list_place = []
        for i in range(4):
            for j in range(4):
                if self.grilleOld[i][j] == self.getAncienPlusGrandNombre():
                    list_place.append([i, j])
        return list_place

    def isNotFull(self):
       return (self.deplacementAutorise('g') or self.deplacementAutorise('d') or self.deplacementAutorise('h') or self.deplacementAutorise('b'))
