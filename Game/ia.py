from concurrent.futures import ProcessPoolExecutor, as_completed
import random
import copy
import neat
from Grille import Grille


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
            

def eval_genome(genome_id, genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    grille = Grille()
    while grille.isNotFull():
        grid_flat = [item for sublist in grille.grille for item in sublist]
        output = net.activate(grid_flat)
        move = CoupPossible(grille)[output.index(max(output))]
        grille.TryDeplacement(move)
        grille.ajoutNombreAleatoire()
    
    grille.ajoutNombreAleatoire()
    return genome_id, grille.score, grille

def parallel_eval_genomes(genomes, config):
    # Créer un dictionnaire pour mapper les id de génome aux objets génome
    genome_dict = {genome_id: genome for genome_id, genome in genomes}

    with ProcessPoolExecutor() as executor:
        # Soumettre les tâches
        futures = {executor.submit(eval_genome, genome_id, genome, config): genome_id for genome_id, genome in genomes}

        for future in as_completed(futures):
            # Obtenir l'id du génome à partir de la future
            genome_id = futures[future]
            score, _, grille = future.result()

            # Mettre à jour le fitness du génome
            genome_dict[genome_id].fitness = score

            # Affichage des résultats
            print(f'Genome ID: {genome_id} ; Fitness: {score}')
            grille.afficher()


if __name__ == "__main__":
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward.txt')

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    p.run(parallel_eval_genomes, 100000)

    winner = p.best_genome
    print("\nBest Genome:\n{!s}".format(winner))