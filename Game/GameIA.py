from Grille import Grille
from ia import Ia

class GameIA:
    grille = Grille()
    
    def __init__(self):
        self.grille = Grille()
        self.grille.ajoutNombreAleatoire()
        self.grille.ajoutNombreAleatoire()
        self.ia = Ia(self.grille)
    
    
    def start(self):
        #print("Jeu du 2048 : ")
        #print("IA Jeux")
        #self.grille.afficher()
        while self.grille.isNotFull():
            move = self.ia.calculMeilleurCoup()
            #print(move)
            if self.grille.TryDeplacement(move):
                self.grille.ajoutNombreAleatoire()
                #self.grille.afficher()
        #print("Game Over")
        #self.grille.afficher()
        #print("Score total : ", self.grille.score)