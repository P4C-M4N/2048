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
        print("Appuyer sur 'a' pour quitter")
        self.grille.afficher()
        while True:
            move = input("Entrez la direction (g, h, d, b) ou 'a' pour quitter: ")

            if move == 'g':
                self.grille.deplacementGauche()
            elif move == 'd':
                self.grille.deplacementDroite()
            elif move == 'h':
                self.grille.deplacementHaut()
            elif move == 'b':
                self.grille.deplacementBas()
            elif move == 'a':
                break
            else:
                print("Direction invalide. Utilisez 'g', 'h', 'd' ou 'b'.")
                continue
            self.grille.afficher()
            t.sleep(0.2)
        print("Game Over")
        print("Score total : ", self.grille.score)
    