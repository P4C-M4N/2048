from concurrent.futures import ProcessPoolExecutor
from GameIA import GameIA
from tqdm import tqdm

def jouer_partie(_):
    game = GameIA()
    game.start()
    return game.grille.score, game.grille

if __name__ == "__main__":
    nb_parties = 100000

    with ProcessPoolExecutor() as executor:
        resultats = list(tqdm(executor.map(jouer_partie, range(nb_parties)), total=nb_parties, desc="Simulation Progress"))

    scores = [resultat[0] for resultat in resultats]
    grilles = [resultat[1] for resultat in resultats]

    print("\n#########################################\nMoyenne des scores : ", sum(scores) / len(scores), "\nMeilleur score : ", max(scores), "\nMin score :", min(scores), "\n#########################################")
    grilles[scores.index(max(scores))].afficher()

    #Affichage du nombre de parties gagnées
    nb_parties_gagnees = 0
    #rechercher dans chacune des grilles le nombre 2048
    for grille in grilles:
        for ligne in grille.grille:
            if 2048 in ligne:
                nb_parties_gagnees += 1
                break

    print("Nombre de parties gagnées : ", nb_parties_gagnees)
