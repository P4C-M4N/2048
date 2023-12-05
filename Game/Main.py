from Game import Game
from GameIA import GameIA
from tqdm import tqdm

if __name__ == "__main__":
    scores = []
    grilles = []

    # Use tqdm to create a progress bar
    for i in tqdm(range(100000), desc="Simulation Progress"):
        game = GameIA()
        game.start()
        scores.append(game.grille.score)
        grilles.append(game.grille)

    print("\n#########################################\nMoyenne des scores : ", sum(scores)/len(scores), "\nMeilleur score : ", max(scores), "\nMin score :", min(scores), "\n#########################################")
    grilles[scores.index(max(scores))].afficher()
