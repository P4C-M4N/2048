import threading
import time
import tkinter as tk
from ia import Ia
from Grille import Grille

# Initialisation de Tkinter
root = tk.Tk()
root.title("2048")

# Définition des dimensions de la fenêtre
TAILLE_ECRAN = (500, 600)  # Ajustez selon vos besoins
root.geometry(f"{TAILLE_ECRAN[0]}x{TAILLE_ECRAN[1]}")

# Couleurs pour les cases
COULEURS = {
    0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200), 
    8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95), 
    64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97), 
    512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46)
}
COULEUR_TEXTE = (50, 50, 50)

# Fonction pour convertir RGB en Hex
def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

# Fonction pour centrer les boutons
def centrer_bouton(x, y, largeur_bouton, hauteur_bouton):
    return (TAILLE_ECRAN[0] * x - largeur_bouton / 2, TAILLE_ECRAN[1] * y - hauteur_bouton / 2)

# Taille des boutons
TAILLE_BOUTON = (200, 50)

# Position des boutons
POSITION_BOUTON_MANUEL = centrer_bouton(0.5, 0.7, TAILLE_BOUTON[0], TAILLE_BOUTON[1])
POSITION_BOUTON_IA = centrer_bouton(0.5, 0.8, TAILLE_BOUTON[0], TAILLE_BOUTON[1])
POSITION_BOUTON_ARRET = centrer_bouton(0.5, 0.9, TAILLE_BOUTON[0], TAILLE_BOUTON[1])

def mode_ia():
    for widget in root.winfo_children():
        widget.destroy()

    frame_jeu = tk.Frame(root)
    frame_jeu.pack()

    global grille
    grille = Grille()
    global ia
    ia = Ia(grille)
    global ia_running

    # Créez les labels une seule fois et mettez-les à jour ensuite
    labels = [[None for _ in range(4)] for _ in range(4)]

    def update_interface():
        try:
            for i in range(4):
                for j in range(4):
                    valeur = grille.grille[i][j]
                    couleur_fond = rgb_to_hex(COULEURS[valeur])
                    couleur_texte = rgb_to_hex(COULEUR_TEXTE)
                    if labels[i][j] is None:
                        label = tk.Label(frame_jeu, bg=couleur_fond, fg=couleur_texte, width=4, height=2, borderwidth=1, relief="solid", font=("Helvetica", 40, "bold"))
                        label.grid(row=i, column=j, padx=5, pady=5)
                        labels[i][j] = label
                    else:
                        label = labels[i][j]
                        label.config(bg=couleur_fond, fg=couleur_texte, text=str(valeur) if valeur != 0 else '')
        except tk.TclError:
            return
    
    print("Jeu du 2048 : ")
    update_interface()

    def ia_process():
        global ia_running
        ia_running = True
        global grille
        global ia
        i = 0
        while grille.isNotFull() and ia_running :
            print("Tour de caca", i)
            i += 1
            move = ia.calculMeilleurCoup()
            if grille.TryDeplacement(move):
                grille.ajoutNombreAleatoire()
                root.after(0, update_interface)
            time.sleep(0.01)  # Une petite pause pour éviter de bloquer l'interface

        # grille = Grille()
        # ia = Ia(grille) 
        # ia_process()  # Relance l'IA

    threading.Thread(target=ia_process, name='ia').start()  # Lance l'IA dans un thread séparé

    bouton_retour = tk.Button(root, text="Retour au Menu", command=retour_menu)
    bouton_retour.pack()




def quitter():
    global ia_running
    ia_running = False
    root.quit()

def mode_manuel():
    # Nettoyer la fenêtre des anciens widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Création de l'interface du jeu
    frame_jeu = tk.Frame(root)
    frame_jeu.pack()

    # Initialisation du jeu 2048
    grille = Grille()

    # Mise à jour de l'interface graphique pour afficher la grille
    def update_interface():
        for i in range(4):
            for j in range(4):
                valeur = grille.grille[i][j]
                couleur_fond = rgb_to_hex(COULEURS[valeur])
                couleur_texte = rgb_to_hex(COULEUR_TEXTE)
                label = tk.Label(frame_jeu, text=str(valeur) if valeur != 0 else '', bg=couleur_fond, fg=couleur_texte ,width=4, height=2, borderwidth=1, relief="solid", font=("Helvetica", 40, "bold"))
                label.grid(row=i, column=j, padx=5, pady=5)

    update_interface()

    # Gestion des entrées clavier pour les mouvements
    def handle_keypress(event):
        key = event.keysym.lower()
        if key in ['left', 'up', 'right', 'down']:
            move = {'left': 'g', 'up': 'h', 'right': 'd', 'down': 'b'}[key]
            if grille.TryDeplacement(move):
                grille.ajoutNombreAleatoire()
                update_interface()

    root.bind("<Key>", handle_keypress)

    # Bouton pour retourner au menu principal
    bouton_retour = tk.Button(root, text="Retour au Menu", command=retour_menu)
    bouton_retour.pack()

def retour_menu():
    global ia_running
    ia_running = False
    
    # Stopper l'IA si elle est en cours``
    for thread in threading.enumerate():
        if thread.name == 'ia':
            thread.join()

    # Nettoyer la fenêtre et recréer l'interface du menu principal
    for widget in root.winfo_children():
        widget.destroy()

    # Recréation des boutons du menu principal
    bouton_manuel = tk.Button(root, text="Mode Manuel", command=mode_manuel, width=20, height=2)
    bouton_manuel.place(x=POSITION_BOUTON_MANUEL[0], y=POSITION_BOUTON_MANUEL[1])

    bouton_ia = tk.Button(root, text="Mode IA", command=mode_ia, width=20, height=2)
    bouton_ia.place(x=POSITION_BOUTON_IA[0], y=POSITION_BOUTON_IA[1])

    bouton_arret = tk.Button(root, text="Quitter", command=quitter, width=20, height=2)
    bouton_arret.place(x=POSITION_BOUTON_ARRET[0], y=POSITION_BOUTON_ARRET[1])

# Création des boutons du menu principal
retour_menu()

# Démarrage de la boucle principale de Tkinter
root.mainloop()
