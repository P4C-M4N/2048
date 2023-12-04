from Grille import Grille
import copy

class Ia:
    grille = Grille()
    def __init__(self, grille):
        self.grille = grille


    def calculMeilleurCoup(self):
        grilleDroite = Grille()
        grilleDroite.grille = copy.deepcopy(self.grille.grille)
        grilleDroite.score = copy.deepcopy(self.grille.score)
        verifDroite = grilleDroite.TryDeplacement('d')

        grilleGauche = Grille()
        grilleGauche.grille = copy.deepcopy(self.grille.grille)
        grilleGauche.score = copy.deepcopy(self.grille.score)
        verifGauche = grilleGauche.TryDeplacement('g')

        grilleBas = Grille()
        grilleBas.grille = copy.deepcopy(self.grille.grille)
        grilleBas.score = copy.deepcopy(self.grille.score)
        verifBas = grilleBas.TryDeplacement('b')

        grilleHaut = Grille()
        grilleHaut.grille = copy.deepcopy(self.grille.grille)
        grilleHaut.score = copy.deepcopy(self.grille.score)
        verifHaut = grilleHaut.TryDeplacement('h')

        return self.meilleurSituation((grilleDroite,verifDroite), (grilleGauche,verifGauche), (grilleBas,verifBas), (grilleHaut,verifHaut))
        
        

    def meilleurSituation(self, EnsemblegrilleDroite, EnsemblegrilleGauche, EnsemblegrilleBas, EnsemblegrilleHaut):
        scores = {
            "d": EnsemblegrilleDroite[0].score if EnsemblegrilleDroite[1] else -1,
            "g": EnsemblegrilleGauche[0].score if EnsemblegrilleGauche[1] else -1,
            "b": EnsemblegrilleBas[0].score if EnsemblegrilleBas[1] else -1,
            "h": EnsemblegrilleHaut[0].score if EnsemblegrilleHaut[1] else -1,
        }
        return max(scores, key=scores.get)
        



        
        






