import math
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
            
    """
    This method return a bigger score to prioritize to have a big number in the corner.
    """
    def point_for_corner(self, grille: Grille):
        if not grille.grilleOld:
            return max(grille.grille[0][0], grille.grille[3][3], grille.grille[0][3], grille.grille[3][0]) * COEF_FIRST_CORNER_CASE

        list_place_olde_bigger_number = grille.getPlaceAncienPlusGrandNombre()
        list_place_bigger_number = grille.getPlacePlusGrandNombre()

        for place in list_place_bigger_number:
            for place_olde in list_place_olde_bigger_number:
                if place == place_olde and place in [[0, 0], [3, 3], [0, 3], [3, 0]]:
                    return grille.grille[place[0]][place[1]] * COEF_SAME_BIGGER_CORNER_CASE

        for place in list_place_bigger_number:
            if place in [[0, 0], [3, 3], [0, 3], [3, 0]]:
                return grille.grille[place[0]][place[1]] * COEF_BIGGER_MOVE_TO_CORNER_CASE

        return -1000000


    """
    This methode return a bigger score to prioritize to have more empty cases.
    """
    def pointsPourCasesVides(self, grille):
        #Get the number of empty cases
        emptyCases = sum(1 for ligne in grille.grille for case in ligne if case == 0)

        return emptyCases * COEF_EMPTY_CASES
    
    """
    This method return a rotated array of 90 degrees.
    """
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

    def smoothness(self, grille):
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
        

            

    def score_grille(self, grille):
        score = self.point_for_corner(grille)
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
