from Game import Game
from GameIA import GameIA



if __name__ == "__main__":
    scores = []
    for i in range(100):
        print("Partie ", i)
        game = GameIA()
        game.start()
        scores.append(game.grille.score)
        
    print ("\n#########################################\nMoyenne des scores : ", sum(scores)/len(scores))
    



