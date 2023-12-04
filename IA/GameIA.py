from Grille import Grille

class Game:
    grille = Grille()
    Ia = Ia(grille)
    
    def __init__(self):
        self.grille.ajoutNombreAleatoire()
        self.grille.ajoutNombreAleatoire()
    
    
    def start(self):
        print("Jeu du 2048 : ")
        print("IA Jeux")
        self.grille.afficher()
        while self.grille.isNotFull():
            move = self.ia.MeilleurCoup()
            if self.grille.TryDeplacement(move):
                self.grille.ajoutNombreAleatoire()
                self.grille.afficher()
        print("Game Over")
        self.grille.afficher()
        print("Score total : ", self.grille.score)