def calculMeilleurCoup(grille, score):
    grilleGauche, grilleDroite, grilleHaut, grilleBas = grille,grille,grille,grille
    scoreGauche, scoreDroite, scoreHaut, scoreBas = score,score,score,score
    grilleGauche, scoreGauche = deplacementGauche(grilleGauche, scoreGauche)
    grilleDroite, scoreDroite = deplacementDroite(grilleDroite, scoreDroite)
    grilleBas, scoreBas = deplacementBas(grilleBas, scoreBas)
    grilleHaut, scoreHaut = deplacementHaut(grilleHaut, scoreHaut)
    meilleurCoup = max(scoreGauche, scoreDroite, scoreHaut, scoreBas)
    print("Le meilleur coup est : ", meilleurCoup)
    if scoreDroite == meilleurCoup:
        return 'droite'
    elif scoreGauche == meilleurCoup:
        return 'gauche'
    elif scoreBas == meilleurCoup:
        return 'bas'
    elif scoreHaut == meilleurCoup:
        return 'haut'
    return 'haut'




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
            prochainCoup = calculMeilleurCoup(grille, score)
            if prochainCoup == 'droite':
                grille, score = deplacementDroite(grille, score)
                ajoutNombreAleatoire(grille)
            elif prochainCoup == 'gauche':
                grille, score = deplacementGauche(grille, score)
                ajoutNombreAleatoire(grille)
            elif prochainCoup == 'bas':
                grille, score = deplacementBas(grille, score)
                ajoutNombreAleatoire(grille)
            elif prochainCoup == 'haut':
                grille, score = deplacementHaut(grille, score)
                ajoutNombreAleatoire(grille)
            afficherGrille(grille)
            t.sleep(0.2)

