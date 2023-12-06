import random
import copy
import neat
from Grille import Grille
from neat.parallel import ParallelEvaluator
from neat import StdOutReporter, StatisticsReporter
from math import log2

import math

def rotate_clockwise(arr, iteration = 1):
    if iteration <= 0:
        return

    l = len(arr)
    for i in range(0, iteration):
        for s in range(0, int(l / 2)):
            for j in range(0, l - (2 * s) - 1):
                temp = arr[s][s + j]
                arr[s][s + j] = arr[l - s - j - 1][s]
                arr[l - s - j - 1][s] = arr[l - s - 1][l - s - j - 1]
                arr[l - s - 1][l - s - j - 1] = arr[s + j][l - s - 1]
                arr[s + j][l - s - 1] = temp

    return arr

def calc_smoothness(grille):
    board = grille.grille
    smoothness = 0
    # Only rotate twice to avoid double counting
    # Ignore 0 tiles
    for rotation in range(2):
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if board[i][j] != 0 and j + 1 < len(board[i]) and board[i][j + 1] != 0:
                    current_smoothness = math.fabs(log2(board[i][j]) - log2(board[i][j + 1]))
                    smoothness = smoothness - current_smoothness
        rotate_clockwise(board)

    return smoothness


def CoupPossible(grille):
        dirf = []
        for direction in ['d', 'g', 'b', 'h']:
            grilleCopie = Grille()
            grilleCopie.grille = copy.deepcopy(grille.grille)
            grilleCopie.score = copy.deepcopy(grille.score)
            if grilleCopie.TryDeplacement(direction):
                dirf.append(direction)
        while len(dirf) < 4 :
            dirf.append(dirf[0])

        return dirf

score_w = 1.0
smoothness_w = 1.0
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    grille = Grille()
    while grille.isNotFull():
        #if genome.fitness < -100:
        #    break
        grid_flat = [item for sublist in grille.grille for item in sublist]
        # move is max index of output
        output = net.activate(grid_flat)
        move = CoupPossible(grille)[output.index(max(output))]
        grille.TryDeplacement(move)
        grille.ajoutNombreAleatoire()

    bestCase = grille.bestCase()
    print(f"Score: {grille.score}, BestCase: {bestCase}")
    grille.ajoutNombreAleatoire()
    score = grille.score
    smoothness = calc_smoothness(grille)
    return (grille.score * score_w / (smoothness * smoothness_w)) * log2(bestCase) * -1  # Renvoie le score comme fitness

def print_generation_info(population):
    print(f"Generation: {population.generation}")
    print(f"Meilleur fitness de cette génération: {max([c.fitness for c in population.population.values()])}")

if __name__ == "__main__":
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward.txt')

    p = neat.Population(config)

    # Ajoutez StdOutReporter pour des informations de base
    p.add_reporter(StdOutReporter(True))

    # Ajoutez StatisticsReporter pour des statistiques détaillées
    stats = StatisticsReporter()
    p.add_reporter(stats)

    # Utilisez ParallelEvaluator pour l'évaluation parallèle
    pe = ParallelEvaluator(10, eval_genome)
    winner = p.run(pe.evaluate, 100000)

    # Affichez les statistiques à la fin de l'exécution
    print(stats)