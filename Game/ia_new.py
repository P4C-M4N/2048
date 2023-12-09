import math
import time
from Grille import Grille
import copy
from numpy import average

#coef
COEF_FIRST_CORNER_CASE = 200
COEF_BIGGER_MOVE_TO_CORNER_CASE = 400
COEF_SAME_BIGGER_CORNER_CASE = 200
COEF_NOT_SAME_BIGGER_CORNER_CASE = 25
COEF_EMPTY_CASES = 5

#depth
DEPTH = 2

class Ia:
    def __init__(self, grille):
        self.grille = grille
    
    def depth_test(self,thegrille, depth):
        list_move = self.enable_move()
        list_note = []

        for move in list_move:
            note_move = 0
            grilleCopie = copy.deepcopy(thegrille)
            grilleCopie.TryDeplacement(move)
            list_empty_cases = self.list_empty_cases()

            for empty_case in list_empty_cases:
                note_cases = []
                for val in [2, 4]:
                    grilleCopie.grille[empty_case[0]][empty_case[1]] = val
                    if val == 2:
                        note_cases.append(self.score_grille(grilleCopie) * 0.8)
                    else:
                        note_cases.append(self.score_grille(grilleCopie) * 0.2)
                note_move = average(note_cases)

            list_note.append((move, note_move))

        if depth == 1:
            best_move, _ = max(list_note, key=lambda x: x[1])
            return best_move
        else:
            # Recursively call depth_test with reduced depth
            sub_moves = []
            for move, _ in list_note:
                grilleCopie2 = copy.deepcopy(thegrille)
                grilleCopie2.TryDeplacement(move)
                sub_moves.append((move, self.depth_test(grilleCopie2, depth- 1)))

            # Choose the move with the maximum value
            best_move, _ = max(sub_moves, key=lambda x: x[1])
            print(best_move)
            return best_move

    def smoothness(self, grille: Grille):
        smoothness_score = 0
        for i in range(4):
            for j in range(4):
                if grille.grille[i][j] != 0:
                    # Value of the current tile
                    current_value = math.log(grille.grille[i][j], 2)

                    # Check right neighbor
                    for k in range(j + 1, 4):
                        if grille.grille[i][k] != 0:
                            right_value = math.log(grille.grille[i][k], 2)
                            smoothness_score -= abs(current_value - right_value)
                            break  # Break after finding the first non-zero right neighbor

                    # Check downward neighbor
                    for k in range(i + 1, 4):
                        if grille.grille[k][j] != 0:
                            down_value = math.log(grille.grille[k][j], 2)
                            smoothness_score -= abs(current_value - down_value)
                            break  # Break after finding the first non-zero downward neighbor

        return smoothness_score
        
    def monotonicity(self, grille: Grille):
        monotonicity = 0
        for i in range(4):
            for j in range(3):
                if grille.grille[i][j] > grille.grille[i][j + 1]:
                    monotonicity += grille.grille[i][j] - grille.grille[i][j + 1]
                else:
                    monotonicity += grille.grille[i][j + 1] - grille.grille[i][j]

                if grille.grille[j][i] > grille.grille[j + 1][i]:
                    monotonicity += grille.grille[j][i] - grille.grille[j + 1][i]
                else:
                    monotonicity += grille.grille[j + 1][i] - grille.grille[j][i]

        return monotonicity
            
    def free_tiles(self, grille: Grille):
        free = 0
        for i in range(4):
            for j in range(4):
                if grille.grille[i][j] == 0:
                    free += 1
        return free

    def score_grille(self, grille):
        smoothness_score = self.smoothness(grille)
        monotonicity_score = self.monotonicity(grille)
        free_tiles_score = self.free_tiles(grille)

        # Assign weights to each heuristic based on their importance
        smoothness_weight = 0.1
        monotonicity_weight = 1.0
        free_tiles_weight = 2.5

        score = (smoothness_score * smoothness_weight +
                 monotonicity_score * monotonicity_weight +
                 free_tiles_score * free_tiles_weight)

        return score
        
    """
    This méthode return a list of all possible move
    """
    def enable_move(self):
        list_move = {}
        for direction in ['d', 'g', 'b', 'h']:
            grilleCopie = Grille()
            grilleCopie.grille = copy.deepcopy(self.grille.grille)
            grilleCopie.score = copy.deepcopy(self.grille.score)
            if grilleCopie.TryDeplacement(direction):
                list_move[direction] = grilleCopie
        
        return list_move
    
    """
    This method return a list of the coordinates of empty cases
    """
    def list_empty_cases(self):
        list_empty_cases = []
        for i in range(4):
            for j in range(4):
                if self.grille.grille[i][j] == 0:
                    list_empty_cases.append([i, j])
        return list_empty_cases


    def calculMeilleurCoup(self):
        return self.depth_test(self.grille, DEPTH)
