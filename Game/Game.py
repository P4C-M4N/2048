import random as r
import keyboard as k
 

def afficherGrille(grille):
    global score
    print("Score total ", score)
    for ligne in range(0, 4):
        for colonne in range(0, 4):
            print(grille[ligne][colonne], end=" ")
        print()

def ajoutNombreAleatoire(grille):
    ajoute = False
    nombreListe = [2, 2, 2, 4]
    nombre = r.choice(nombreListe)
    while not ajoute:
        ligne = r.randint(0, 3)
        colonne = r.randint(0, 3)
        if grille[ligne][colonne] == 0:
            grille[ligne][colonne] = nombre
            ajoute = True
    return grille

def creerGrilleTempo():
    grilleTempo = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1],[-1, -1, -1, -1]]
    return grilleTempo



def remplirZero(grille):
  for ligne in range(0, 4):
    for colonne in range(0, 4):
      if grille[ligne][colonne] < 0:
        grille[ligne][colonne] = 0
  return grille

def retirerZeroDroite(grille):
  grilleTempo = creerGrilleTempo()
  for ligne in range(0, 4):
      idColonne = 3
      for colonne in range(3, -1, -1):
          if grille[ligne][colonne] != 0:
              grilleTempo[ligne][idColonne] = grille[ligne][colonne]
              idColonne -= 1
  return grilleTempo

def deplacementDroite(grille):
    global score
    grille = retirerZeroDroite(grille)
    for ligne in range(0, 4):
        for colonne in range(3, 0, -1):
            if grille[ligne][colonne] == grille[ligne][colonne - 1] and grille[ligne][colonne]!=-1:
                grille[ligne][colonne] = grille[ligne][colonne] * 2
                score = score + grille[ligne][colonne]
                grille[ligne][colonne - 1] = 0
    grille = retirerZeroDroite(grille)
    grille = remplirZero(grille)
    return grille

def retirerZeroHaut(grille):
  grilleTempo = creerGrilleTempo()
  for colonne in range(0, 4):
      idLigne = 0
      for ligne in range(0, 4):
          if grille[ligne][colonne] != 0:
              grilleTempo[idLigne][colonne] = grille[ligne][colonne]
              idLigne += 1
  return grilleTempo

def deplacementHaut(grille):
    global score
    grille = retirerZeroHaut(grille)
    for colonne in range(0, 4):
        for ligne in range(0, 3):
            if grille[ligne][colonne] == grille[ligne + 1][colonne] and grille[ligne][colonne]!=-1:
                grille[ligne][colonne] = grille[ligne][colonne] * 2
                score = score + grille[ligne][colonne]
                grille[ligne + 1][colonne] = 0
    grille = retirerZeroHaut(grille)
    grille = remplirZero(grille)
    return grille


def retirerZeroBas(grille):
  grilleTempo = creerGrilleTempo()
  for colonne in range(0, 4):
      idLigne = 3
      for ligne in range(3, -1, -1):
          if grille[ligne][colonne] != 0:
              grilleTempo[idLigne][colonne] = grille[ligne][colonne]
              idLigne -= 1
  return grilleTempo

def deplacementBas(grille):
    global score
    grille = retirerZeroBas(grille)
    for colonne in range(0, 4):
        for ligne in range(3, 0, -1):
            if grille[ligne][colonne] == grille[ligne - 1][colonne] and grille[ligne][colonne]!=-1:
                grille[ligne][colonne] = grille[ligne][colonne] * 2
                score = score + grille[ligne][colonne]
                grille[ligne - 1][colonne] = 0
    grille = retirerZeroBas(grille)
    grille = remplirZero(grille)
    return grille

def retirerZeroGauche(grille):
    grilleTempo = creerGrilleTempo()
    for ligne in range(0, 4):
        idColonne = 0
        for colonne in range(0, 4):
            if grille[ligne][colonne] != 0:
                grilleTempo[ligne][idColonne] = grille[ligne][colonne]
                idColonne += 1
    return grilleTempo

def deplacementGauche(grille):
    global score
    grille = retirerZeroGauche(grille)
    for ligne in range(0, 4):
        for colonne in range(0, 3):
            if grille[ligne][colonne] == grille[ligne][colonne+1] and grille[ligne][colonne]!=-1:
                grille[ligne][colonne] = grille[ligne][colonne] * 2
                score = score + grille[ligne][colonne]
                grille[ligne][colonne+1] = 0
    grille = retirerZeroGauche(grille)
    grille = remplirZero(grille)
    return grille

def lancerJeu():
    global score
    grille = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    grille = ajoutNombreAleatoire(grille)
    grille = ajoutNombreAleatoire(grille)
    print("Jeu du 2048 : ")
    print("Utiliser les touches 'g' (gauche), 'h' (haut), 'd' (droite), 'b' (bas) pour jouer")
    print("Appuyer sur 'a' pour quitter")

    afficherGrille(grille)

    while True:
        saisie = input("Entrez votre choix: ")

        if saisie == 'a':
            print("Fin du jeu.")
            break
        elif saisie == 'g':
            grille = deplacementGauche(grille)
            grille = ajoutNombreAleatoire(grille)
            afficherGrille(grille)
        elif saisie == 'd':
            grille = deplacementDroite(grille)
            grille = ajoutNombreAleatoire(grille)
            afficherGrille(grille)
        elif saisie == 'h':
            grille = deplacementHaut(grille)
            grille = ajoutNombreAleatoire(grille)
            afficherGrille(grille)
        elif saisie == 'b':
            grille = deplacementBas(grille)
            grille = ajoutNombreAleatoire(grille)
            afficherGrille(grille)
score = 0
lancerJeu()