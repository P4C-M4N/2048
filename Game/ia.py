from Grille import Grille
import copy

class Ia:
    def __init__(self, grille):
        self.grille = grille

    def pointsPourCasesVides(self, grille):
        # Encourage a additionner un max de tuiles
        casesVides = sum(1 for ligne in grille for case in ligne if case == 0)
        return casesVides * 10

    def pointsPourCoin(self, grille):
        # Encourage à garder les valeurs élevées dans un coin spécifique, par exemple le coin supérieur gauche
        return grille[0][0] * 50

    def evaluationGrille(self, grille):
        scoreEvaluation = 0
        tailleGrille = len(grille)
        for i in range(tailleGrille):
            for j in range(tailleGrille):
                valeurCase = grille[i][j]
                # Plus la valeur est élevée et proche du coin, plus le score est élevé
                scoreProximite = (tailleGrille - i) * (tailleGrille - j)
                scoreEvaluation += valeurCase * scoreProximite

                # Encourage les valeurs adjacentes similaires
                if j < tailleGrille - 1:
                    scoreEvaluation -= abs(valeurCase - grille[i][j + 1])
                if i < tailleGrille - 1:
                    scoreEvaluation -= abs(valeurCase - grille[i + 1][j])
        return scoreEvaluation

    def calculMeilleurCoupProfondeur(self, grille, profondeur):
        if profondeur == 0:
            return self.evaluationGrille(grille.grille) + self.pointsPourCoin(grille.grille) + self.pointsPourCasesVides(grille.grille)

        meilleursScores = []
        for direction in ['d', 'g', 'b', 'h']:
            grilleCopie = Grille()
            grilleCopie.grille = copy.deepcopy(grille.grille)
            grilleCopie.score = copy.deepcopy(grille.score)

            if grilleCopie.TryDeplacement(direction):
                scoreFutur = self.calculMeilleurCoupProfondeur(grilleCopie, profondeur - 1)
                scoreEvaluation = self.evaluationGrille(grilleCopie.grille)
                pointsCoin = self.pointsPourCoin(grilleCopie.grille)
                pointsCaseVide = self.pointsPourCasesVides(grilleCopie.grille)
                scoreTotal = grilleCopie.score + scoreFutur + scoreEvaluation + pointsCoin + pointsCaseVide
                meilleursScores.append(scoreTotal)

        return max(meilleursScores) if meilleursScores else -1


    def calculMeilleurCoup(self):
        grilles = {}
        for direction in ['d', 'g', 'b', 'h']:
            grilleCopie = Grille()
            grilleCopie.grille = copy.deepcopy(self.grille.grille)
            grilleCopie.score = copy.deepcopy(self.grille.score)
            if grilleCopie.TryDeplacement(direction):
                grilles[direction] = grilleCopie

        return self.meilleurSituation(grilles)

    def meilleurSituation(self, grilles):
        scores = {}
        for direction, grille in grilles.items():
            scoreBase = grille.score
            scoreEvaluation = self.evaluationGrille(grille.grille)
            pointsCoin = self.pointsPourCoin(grille.grille)
            scoreProfondeur = self.calculMeilleurCoupProfondeur(grille, 2)
            pointsCaseVide = self.pointsPourCasesVides(grille.grille)
            scoreTotal = scoreBase + scoreEvaluation + pointsCoin + scoreProfondeur + pointsCaseVide
            scores[direction] = scoreTotal

        return max(scores, key=scores.get) if scores else None
