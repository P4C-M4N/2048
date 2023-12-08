import math
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
                scoreProximite = (tailleGrille - i) * (tailleGrille - j)
                scoreEvaluation += valeurCase * scoreProximite

                if j < tailleGrille - 1:
                    scoreEvaluation -= abs(valeurCase - grille[i][j + 1])
                if i < tailleGrille - 1:
                    scoreEvaluation -= abs(valeurCase - grille[i + 1][j])
        
        monotonicite = self.calc_monotonicite(grille)
        return scoreEvaluation + monotonicite

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
                pointsSmoothness = self.calc_smoothness(grilleCopie)
                pointMonotonicite = self.calc_monotonicite(grilleCopie.grille)
                scoreTotal = grilleCopie.score + scoreFutur + scoreEvaluation + pointsCoin + pointsCaseVide + pointsSmoothness + pointMonotonicite
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

    # 2D array, rotates by 90 degrees
    @staticmethod
    def rotate_clockwise(arr, iteration=1):
        n = len(arr)
        for _ in range(iteration):
            for x in range(n // 2):
                for y in range(x, n - x - 1):
                    temp = arr[x][y]
                    arr[x][y] = arr[n - y - 1][x]
                    arr[n - y - 1][x] = arr[n - x - 1][n - y - 1]
                    arr[n - x - 1][n - y - 1] = arr[y][n - x - 1]
                    arr[y][n - x - 1] = temp
        return arr

    def calc_smoothness(self, grille):
        board = copy.deepcopy(grille.grille)
        smoothness = 0
        # Only rotate twice to avoid double counting
        # Ignore 0 tiles
        for rotation in range(2):
            for i in range(0, len(board)):
                for j in range(0, len(board[i])):
                    if board[i][j] != 0 and j + 1 < len(board[i]) and board[i][j + 1] != 0:
                        current_smoothness = math.fabs(math.log2(board[i][j]) - math.log2(board[i][j + 1]))
                        smoothness = smoothness - current_smoothness
            self.rotate_clockwise(board)

        return smoothness
    
    def calc_monotonicite(self, grille):
       scores = [0, 0, 0, 0]  # Haut/Bas, Bas/Haut, Gauche/Droite, Droite/Gauche
       for i in range(4):
           current = 0
           next = current + 1
           while next < 4:
               while next < 4 and grille[i][next] == 0:
                   next += 1
               if next >= 4: next -= 1
               currentValue = math.log(grille[i][current], 2) if grille[i][current] != 0 else 0
               nextValue = math.log(grille[i][next], 2) if grille[i][next] != 0 else 0
               if currentValue > nextValue:
                   scores[0] += nextValue - currentValue
               elif nextValue > currentValue:
                   scores[1] += currentValue - nextValue
               current = next
               next += 1
       for j in range(4):
           current = 0
           next = current + 1
           while next < 4:
               while next < 4 and grille[next][j] == 0:
                   next += 1
               if next >= 4: next -= 1
               currentValue = math.log(grille[current][j], 2) if grille[current][j] != 0 else 0
               nextValue = math.log(grille[next][j], 2) if grille[next][j] != 0 else 0
               if currentValue > nextValue:
                   scores[2] += nextValue - currentValue
               elif nextValue > currentValue:
                   scores[3] += currentValue - nextValue
               current = next
               next += 1
       return max(scores)

    def meilleurSituation(self, grilles):
        scores = {}
        for direction, grille in grilles.items():
            scoreBase = grille.score
            scoreEvaluation = self.evaluationGrille(grille.grille)
            pointsCoin = self.pointsPourCoin(grille.grille)
            scoreProfondeur = self.calculMeilleurCoupProfondeur(grille, 3)
            pointsCaseVide = self.pointsPourCasesVides(grille.grille)
            pointsSmoothness = self.calc_smoothness(grille)
            pointsMonotonicite = self.calc_monotonicite(grille.grille)
            scoreTotal = scoreBase + scoreEvaluation + pointsCoin + scoreProfondeur + pointsCaseVide + pointsSmoothness + pointsMonotonicite
            scores[direction] = scoreTotal

        return max(scores, key=scores.get) if scores else None
