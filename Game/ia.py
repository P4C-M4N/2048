import random
import copy
import neat
from Grille import Grille
from neat.parallel import ParallelEvaluator
from neat import StdOutReporter, StatisticsReporter

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
    return grille.score  # Renvoie le score comme fitness

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