import random
from Grille import Grille
import copy
import neat


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
            move = ['g', 'h', 'd', 'b'][output.index(max(output))]

            if grille.TryDeplacement(move):
                genome.fitness += 20


                grille.ajoutNombreAleatoire()
            else:
                genome.fitness -= 50
                # play a random move
                move = random.choice(['g', 'h', 'd', 'b'])
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
