import random as r
import time as t
from Grille import Grille

class Game:
    grille = Grille()
    
    def __init__(self):
        self.grille.ajoutNombreAleatoire()
        self.grille.ajoutNombreAleatoire()
    
    
    def start(self):
        print("Jeu du 2048 : ")
        print("Utiliser les touches 'g' (gauche), 'h' (haut), 'd' (droite), 'b' (bas) pour jouer")
        print("Appuyer sur 'q' pour quitter")
        self.grille.afficher()
        while self.grille.isNotFull():
            move = input("Entrez la direction (g, h, d, b) ou 'a' pour quitter: ")
            if move == 'q':
                break
            if self.grille.TryDeplacement(move):
                self.grille.ajoutNombreAleatoire()
                self.grille.afficher()
        print("Game Over")
        self.grille.afficher()
        print("Score total : ", self.grille.score)
