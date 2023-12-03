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



            if move == 'a':
                break

            if self.grille.deplacementAutorise(move):
                if move == 'g':
                    self.grille.deplacementGauche()
                elif move == 'd':
                    self.grille.deplacementDroite()
                elif move == 'h':
                    self.grille.deplacementHaut()
                elif move == 'b':
                    self.grille.deplacementBas()
                self.grille.afficher()
                t.sleep(0.2)

            else:
                if self.grille.deplacementAutorise('g') == False and self.grille.deplacementAutorise('d') == False and self.grille.deplacementAutorise('b') == False and self.grille.deplacementAutorise('h') == False:
                    print("Partie terminée, score final : ", self.grille.score)
                    break
            
        print("Score total : ", self.grille.score)
