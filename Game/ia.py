import random
from Grille import Grille
import copy
import neat

def caluculate_monoticity(grille):
    """
    This heuristic tries to ensure that the values of the tiles are all either
    increasing or decreasing along both the left/right and up/down directions.
    This heuristic alone captures the intuition that many others have mentioned,
    that higher valued tiles should be clustered in a corner. It will typically
    prevent smaller valued tiles from getting orphaned and will keep the board
    very organized, with smaller tiles cascading in and filling up into the larger tiles.

    Here's a screenshot of a perfectly monotonic grid. I obtained this by running the
    algorithm with the eval function set to disregard the other heuristics and only
    consider monotonicity.
    :param grille:
    :return:
    """


    # left/right
    left_right = 0
    for i in range(4):
        for j in range(3):
            if grille[i][j] > grille[i][j + 1]:
                left_right += 1
            elif grille[i][j] < grille[i][j + 1]:
                left_right -= 1

    # up/down
    up_down = 0
    for j in range(4):
        for i in range(3):
            if grille[i][j] > grille[i + 1][j]:
                up_down += 1
            elif grille[i][j] < grille[i + 1][j]:
                up_down -= 1

    return max(left_right, up_down)





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
                genome.fitness += caluculate_monoticity(grille.grille)*2


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

    p.run(eval_genomes, 500)

    winner = p.best_genome

        






