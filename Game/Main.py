from concurrent.futures import ProcessPoolExecutor
from GameIA import GameIA
from tqdm import tqdm
import argparse

def jouer_partie(_):
    game = GameIA()
    game.start()
    return game.grille.score, game.grille

def main(nb_parties_arg):
    if isinstance(nb_parties_arg, int) and nb_parties_arg > 0:
        nb_parties = nb_parties_arg
        print("Nombre de parties : ", nb_parties)
    else:
        nb_parties = 50
        print("Nombre de parties invalide, utilisation de la valeur par défaut (50)")

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jouer un nombre spécifié de parties.")
    parser.add_argument("nb_parties", type=int, nargs='?', default=50, help="Nombre de parties à jouer")
    args = parser.parse_args()
    main(args.nb_parties)