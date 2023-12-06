import random
from Grille import Grille
import copy
import neat


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
            

def eval_genomes(genomes, config):
    scores = []
    end_grille = []
    for genome_id, genome in genomes:
        genome.fitness = 0.0
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
            
        grille.ajoutNombreAleatoire()
        end_grille.append(grille)
        genome.fitness = genome.fitness + grille.score
        scores.append(genome.fitness)


    best_grille = end_grille[scores.index(max(scores))]
    best_case = max([max(i) for i in best_grille.grille])

    print(f"Generation: {p.generation}")
    print(f'Best genome: {genome.fitness} ; Best score: {max(scores)} ; Best case: {best_case}')
    best_grille.afficher()


if __name__ == "__main__":
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward.txt')

    p = neat.Population(config)

    p.run(eval_genomes, 100000)

    winner = p.best_genome
