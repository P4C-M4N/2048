import pygame
import sys
from Game import Grille
from ia import Ia

# Initialiser Pygame
pygame.init()

# Méthode pour centrer un bouton sur l'écran
def centrer_bouton(x, y, largeur_ecran, hauteur_ecran, largeur_bouton, hauteur_bouton):
    return (largeur_ecran * x - largeur_bouton / 2, hauteur_ecran * y - hauteur_bouton / 2)

# Constantes pour l'interface
TAILLE_CASE = 100
MARGE = 10
TAILLE_BOUTON = (200, 50)
TAILLE_ECRAN = (TAILLE_CASE * 4 + MARGE * 5, TAILLE_CASE * 4 + MARGE * 6 + TAILLE_BOUTON[1] * 2)  # Augmentation de la hauteur
COULEURS = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121), 
            16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114), 
            256: (237, 204, 97), 512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46)}

POSITION_BOUTON_MANUEL = centrer_bouton(0.5, 0.7, TAILLE_ECRAN[0], TAILLE_ECRAN[1], TAILLE_BOUTON[0], TAILLE_BOUTON[1])
POSITION_BOUTON_IA = centrer_bouton(0.5, 0.8, TAILLE_ECRAN[0], TAILLE_ECRAN[1], TAILLE_BOUTON[0], TAILLE_BOUTON[1])
POSITION_BOUTON_ARRET = centrer_bouton(0.5, 0.9, TAILLE_ECRAN[0], TAILLE_ECRAN[1], TAILLE_BOUTON[0], TAILLE_BOUTON[1])

COULEUR_BOUTON = (100, 100, 100)
COULEUR_TEXTE = (255, 255, 255)

mode_IA = None  # Pour gérer le mode de jeu

# Créer une fenêtre
ecran = pygame.display.set_mode(TAILLE_ECRAN)
pygame.display.set_caption('2048')

# Créer une instance de Grille
grille = Grille()
ia = Ia(grille)

# Fonction dessiner_boutons
def dessiner_boutons():
    ecran.fill((128, 128, 128))  # Changer la couleur de fond en gris pour une meilleure visibilité
    font = pygame.font.Font(None, 40)
    pygame.draw.rect(ecran, COULEUR_BOUTON, (*POSITION_BOUTON_MANUEL, *TAILLE_BOUTON))
    pygame.draw.rect(ecran, COULEUR_BOUTON, (*POSITION_BOUTON_IA, *TAILLE_BOUTON))
    pygame.draw.rect(ecran, COULEUR_BOUTON, (*POSITION_BOUTON_ARRET, *TAILLE_BOUTON))
    
    texte_manuel = font.render('Mode Manuel', True, COULEUR_TEXTE)
    texte_IA = font.render('Mode IA', True, COULEUR_TEXTE)
    texte_arret = font.render('Quitter', True, COULEUR_TEXTE)

    ecran.blit(texte_manuel, (POSITION_BOUTON_MANUEL[0] + 20, POSITION_BOUTON_MANUEL[1] + 10))
    ecran.blit(texte_IA, (POSITION_BOUTON_IA[0] + 40, POSITION_BOUTON_IA[1] + 10))
    ecran.blit(texte_arret, (POSITION_BOUTON_ARRET[0] + 50, POSITION_BOUTON_ARRET[1] + 10))

def dessiner_grille():
    ecran.fill((187, 173, 160))
    
    # Dessiner la grille
    for i in range(4):
        for j in range(4):
            valeur = grille.grille[i][j]
            couleur = COULEURS[valeur]
            pygame.draw.rect(ecran, couleur, (j * TAILLE_CASE + (j + 1) * MARGE, 
                                              i * TAILLE_CASE + (i + 1) * MARGE, 
                                              TAILLE_CASE, TAILLE_CASE))
            if valeur != 0:
                font = pygame.font.Font(None, 50)
                texte = font.render(str(valeur), True, (0, 0, 0))
                ecran.blit(texte, (j * TAILLE_CASE + (j + 1) * MARGE + 30, 
                                   i * TAILLE_CASE + (i + 1) * MARGE + 30))
    # Dessiner le bouton "Quitter"
    font = pygame.font.Font(None, 40)
    pygame.draw.rect(ecran, COULEUR_BOUTON, (*POSITION_BOUTON_ARRET, *TAILLE_BOUTON))
    texte_arret = font.render('Quitter', True, COULEUR_TEXTE)
    ecran.blit(texte_arret, (POSITION_BOUTON_ARRET[0] + 50, POSITION_BOUTON_ARRET[1] + 10))
                
def bouton_clique(pos, pos_bouton):
    x, y = pos
    bx, by, bw, bh = pos_bouton[0], pos_bouton[1], TAILLE_BOUTON[0], TAILLE_BOUTON[1]
    return bx <= x <= bx + bw and by <= y <= by + bh

# Afficher les boutons initiaux
dessiner_boutons()
pygame.display.update()

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Gérer la sélection du mode de jeu
        if mode_IA is None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_clique(event.pos, (*POSITION_BOUTON_MANUEL, *TAILLE_BOUTON)):
                    mode_IA = False
                    grille = Grille()  # Réinitialiser la grille
                elif bouton_clique(event.pos, (*POSITION_BOUTON_IA, *TAILLE_BOUTON)):
                    mode_IA = True
                    grille = Grille()  # Réinitialiser la grille
                elif bouton_clique(event.pos, (*POSITION_BOUTON_ARRET, *TAILLE_BOUTON)):
                    if mode_IA is None:
                        pygame.quit()
                        sys.exit()
        elif mode_IA:
            # Exécuter l'IA pour faire un mouvement
            move = ia.calculMeilleurCoup()
            if grille.TryDeplacement(move):
                grille.ajoutNombreAleatoire()
        else:
            # Gérer les entrées utilisateur pour le mode manuel
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    grille.TryDeplacement('g')
                    grille.ajoutNombreAleatoire()
                elif event.key == pygame.K_RIGHT:
                    grille.TryDeplacement('d')
                    grille.ajoutNombreAleatoire()
                elif event.key == pygame.K_UP:
                    grille.TryDeplacement('h')
                    grille.ajoutNombreAleatoire()
                elif event.key == pygame.K_DOWN:
                    grille.TryDeplacement('b')
                    grille.ajoutNombreAleatoire()
                
        if mode_IA is not None and event.type == pygame.MOUSEBUTTONDOWN:
            # Gérer le clic sur le bouton d'arrêt pendant le jeu
            if bouton_clique(event.pos, (*POSITION_BOUTON_ARRET, *TAILLE_BOUTON)):
                mode_IA = None
                dessiner_boutons()

    # Dessiner la grille ou les boutons selon le mode
    if mode_IA is None:
        dessiner_boutons()
    else:
        dessiner_grille()

    pygame.display.update()