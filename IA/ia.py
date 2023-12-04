from Game.Grille import Grille
import copy

class Ia:
    grille = Grille()

    def __init__(self, grille):
        self.grille == grille


    def calculMeilleurCoup(self, nbRecursion, compt=0):
        if compt == nbRecursion:
            return self.meilleurSitutation(grilleDroite, grilleGauche, grilleBas, grilleHaut)
        grilleDroite = Grille()
        grilleDroite.grille = copy.deepcopy(self.grille)
        grilleGauche = Grille()
        grilleGauche.grille = copy.deepcopy(self.grille)
        grilleBas = Grille()
        grilleBas.grille = copy.deepcopy(self.grille)
        grilleHaut = Grille()
        grilleHaut.grille = copy.deepcopy(self.grille)
        
        

    def meilleurSituation(self, grilleDroite, grilleGauche, grilleBas, grilleHaut):
        scores = {
            "droite": grilleDroite.score(),
            "gauche": grilleGauche.score(),
            "bas": grilleBas.score(),
            "haut": grilleHaut.score()
        }
        meilleure_direction = max(scores, key=scores.get)
        if meilleure_direction == "droite":
            return grilleDroite
        elif meilleure_direction == "gauche":
            return grilleGauche
        elif meilleure_direction == "bas":
            return grilleBas
        elif meilleure_direction == "haut":
            return grilleHaut

        
        






