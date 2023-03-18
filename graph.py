from algo import *
from tkinter import *
import time
import random

def game_graph():
    '''
        Fonction principale du jeu pour la version graphique

        ENTREE
            ---
        
        SORTIE
            ---
    '''
    # Création de la fenêtre
    window = Tk()
    window.geometry('1400x800')
    window.resizable(False,False) # La taille de la fenêtre ne peut pas être modifié à la main pour éviter les erreurs d'affichage
    window.title('Diamant')
    nb_player = menu(window) # Appelle de la fonction menu
    list_player = start_game_graph(window,nb_player) # Création des joueurs
    for i in range (5) : # Boucle du jeu : 5 manches
        for j in range (len(list_player)): # Remet tous les joueurs dans la partie et leurs gemmes temporaires à 0
            list_player[j].in_game = True
            list_player[j].temp_gem = 0
        list_player = round_graph(window, list_player, i+1) # Lance une manche de la partie
    end_game_display_graph(list_player, window)
    window.destroy()
    window.mainloop()
    ask_continue()


def display_rules(win):
    '''
        Affiche les règles dans le menu

        ENTREE
            win (Frame tkinter) : Fenêtre du jeu
        
        SORTIE
            ---
    '''
    rules_win = Frame(win, highlightbackground="black", highlightthickness=5)
    rules_win.place(x = 50, y = 40)

    with open('regles.txt', 'r', encoding = "utf-8") as rules_file : # Copie les règles qui se trouve dans le fichier "regles.txt"
        rules = rules_file.read()
    Label(rules_win, text = rules, justify='left').pack(side = TOP, padx = 5, pady = 5)
    close_but = Button(rules_win, text = "Fermer", command = lambda : rules_win.destroy(), activebackground = 'SteelBlue2')
    close_but.pack(side = BOTTOM, pady = 15)


def menu(window):
    '''
        Fonction du menu, permet d'afficher les règles, de choisir le nombre de joueurs et de lancer la partie
    
        ENTREE
            window (tkinter window) : frame du menu
        
        SORTIE
            window, nb_player (int) : Nombre de joueurs sélectionné
    '''
    win = Frame(window) # Création d'un cadre dans la fenêtre tkinter pour le menu
    win.pack(expand = True, fill = "both") # Le cadre prend l'entièreté de la fenêtre
    nb_player = 0
    okvar = IntVar() # Création d'une variable tkinter qui détermine la fin de la fonction
    Label(win, text = "Diamant", font = "Purisa 90 bold underline").pack(side = LEFT, padx = 100)

    def set_nb_player(nb_p):
        '''
            Fonction interne qui permet de changer le nombre de joueurs (entry qui n'apparaît pas)

            ENTREE
                nb_p (int) : nombre de joueurs défini pour chaque bouton
            
            SORTIE
                ---
        '''
        nonlocal nb_player
        nb_player = int(nb_p)
        Label(win, text = str(nb_player) + " joueurs", font = 'Arial 16 bold').place(relx = 0.79, rely = 0.337)
    
    def confirm():
        '''
            Fonction interne qui permet de vérifier et valider le nombre de joueurs et lancer la partie

            ENTREE
                --- (les variables contenues dans set_nb_player() sont accessibles)
            
            SORTIE
                --- (modifie okvar)
        '''
        if 2<nb_player<9 : # Si le nombre de joueur est entre 2 et 9 exclus (si un bouton a été utilisé), okvar passe à 1
            okvar.set(1)

    Label(win, text="Sélectionner le nombre de joueur :",font = 'Arial 14 bold').place(relx= 0.715,rely=0.3)

    but_list = button_creation_menu(win, set_nb_player) # Crée la liste des boutons qui vont s'afficher

    global loadimage
    loadimage = PhotoImage(file="images/Start-Button.png")

    start_button = Button(win, command = lambda : confirm(), cursor='hand2', image = loadimage, activebackground = 'black')
    start_button.place(relx = 0.785, rely = 0.65)

    Button(win, text = 'Règles', font = 'Arial 20 bold', command = lambda : display_rules(win), activebackground = 'SteelBlue1').place(relx = 0.8, rely = 0.9)

    for i in range(3) : # Affiche les boutons créés précédemment
        but_list[i].place(relx = 0.75 + i*0.05, rely = 0.4)
        but_list[i+3].place(relx = 0.75 + i*0.05, rely = 0.5)

    start_button.wait_variable(okvar) # Si start_button est pressé et que okvar == 1 : la fonction continue vers sa fin
    win.destroy() # Destruction du Frame du menu (inutile désormais)
    return nb_player


def button_creation_menu(win, set_nb_player):
    '''
        Crée les boutons qui apparaissent dans le menu

        ENTREE
            win (Frame tkinter) : Frame du menu, set_nb_player (function)
        
        SORTIE
            but_list (list) : Liste comprenant les boutons
    '''
    but_list = []
    but_list.append(Button(win, text = '3', command = lambda : set_nb_player(3), activebackground = 'SteelBlue1', cursor='hand2',font='Arial 11 bold', bg='gray65', height = 3, width = 4))
    but_list.append(Button(win, text = '4', command = lambda : set_nb_player(4), activebackground = 'SteelBlue1', cursor='hand2',font='Arial 11 bold', bg='gray65', height = 3, width = 4))
    but_list.append(Button(win, text = '5', command = lambda : set_nb_player(5), activebackground = 'SteelBlue1', cursor='hand2',font='Arial 11 bold', bg='gray65', height = 3, width = 4))
    but_list.append(Button(win, text = '6', command = lambda : set_nb_player(6), activebackground = 'SteelBlue1', cursor='hand2',font='Arial 11 bold', bg='gray65', height = 3, width = 4))
    but_list.append(Button(win, text = '7', command = lambda : set_nb_player(7), activebackground = 'SteelBlue1', cursor='hand2',font='Arial 11 bold', bg='gray65', height = 3, width = 4))
    but_list.append(Button(win, text = '8', command = lambda : set_nb_player(8), activebackground = 'SteelBlue1', cursor='hand2',font='Arial 11 bold', bg='gray65', height = 3, width = 4))
    return but_list


def start_game_graph(window,nb_player):
    '''
        Permet aux joueurs de choisir leur pseudo (maximum 8 caractères)

        ENTREE
            window (Fenêtre tkinter) : Fenêtre principale du jeu, nb_player (int) ; nombre de joueurs
        
        SORTIE
            list_player (list) : Liste d'objet contenant les joueurs
    '''
    name_win = Frame(window)
    name_win.pack(expand=True, fill = "both")
    list_player = []
    name_ent_list = []
    okvar = IntVar()

    def check_list():
        '''
            Permet de vérifier que tous les joueurs ont un nom

            ENTREE
                --- (les variables contenues dans start_game_graph() sont accessibles)
            
            SORTIE
                --- (modifie okvar)
        '''
        for i in range(len(list_player)):
            if list_player[i] != '': # Vérifie si le nom n'est pas vide
                okvar.set(1)

    def add_name(i) :
        '''
            Ajoute un joueur dans la liste des joueurs avec son pseudo

            ENTREE
                i (int) : indice dans la liste des joueurs du joueur à modifier
            
            SORTIE
                --- (modifie list_player)
        '''
        temp_name = name_ent_list[i].get()[:8] # Limite du nombre de caractères à 8 pour éviter des problèmes lors de l'affichage
        if temp_name != '':
            list_player[i] = player(temp_name, False)
            name_but_list[i].destroy() # Détruit le bouton pour confirmer le nom, on ne peut pas changer son pseudo
            name_ent_list[i].destroy()
            Label(name_win, text = temp_name, font='Arial 20').place(relx = 0.42, rely = 0.05 + i*0.11)
            ia_list[i].destroy()
    
    def add_ai(i) :
        '''
            Ajoute une ia dans dans la liste des joueurs

            ENTREE
                i (int) : indice dans la liste des joueurs du joueur à modifier
            
            SORTIE
                --- (modifie list_player)
        '''
        list_player[i] = player("IA " + str(i+1), True)
        name_but_list[i].destroy()
        ia_list[i].destroy()
        name_ent_list[i].destroy()
        Label(name_win, text = "IA " + str(i+1), font='Arial 20').place(relx = 0.42, rely = 0.05 + i*0.11)

    name_but_list, ia_list = button_creation_name(name_win, add_name, add_ai) # Crée la liste des boutons qui vont s'afficher

    for i in range(nb_player):
        Label(name_win,text = "Nom joueur " + str(i+1) + " :",font='Arial 20 bold').place(relx = 0.27, rely = 0.11*i+0.05)
        list_player.append('') # Ajuste la taille de list_player afin de pouvoir changer la partie voulue
        name_ent_list.append(Entry(name_win, font='Arial 20'))
        name_ent_list[i].place(relx = 0.42, rely = 0.05 + i*0.11)
        name_ent_list[i].insert(0,"joueur " + str(i+1)) # Le nomde base d'un joueur est 'joueur n'
        name_but_list[i].place(relx = 0.65, rely = 0.05 + i*0.11)
        ia_list[i].place(relx = 0.73, rely = 0.05 + i*0.11)
    
    launch_button = Button(name_win, text = "Commencer", font =' Arial 15 bold', activebackground = 'green', command = lambda : check_list(), cursor = 'hand2',height=2,width=12)
    launch_button.pack(side='bottom',pady=25)
    
    launch_button.wait_variable(okvar)
    name_win.destroy()
    return list_player


def button_creation_name(name_win, add_name, add_ai):
    '''
        Crée les boutons qui apparaissent dans la page de choix des pseudo

        ENTREE
            name_win (Frame tkinter) : Frame de la page des pseudos, add_name (function)
        
        SORTIE
            name_but_list (list) : Liste comprenant les boutons pour confirmer un nom, ia_list (list) : liste comprenant les boutons pour ajouter des ia
    '''
    name_but_list = []
    name_but_list.append(Button(name_win,text = "Confirmer", font='Arial 14',command = lambda : add_name(0), activebackground = 'SteelBlue1', cursor='hand2'))
    name_but_list.append(Button(name_win,text = "Confirmer", font='Arial 14',command = lambda : add_name(1), activebackground = 'SteelBlue1', cursor='hand2'))
    name_but_list.append(Button(name_win,text = "Confirmer", font='Arial 14',command = lambda : add_name(2), activebackground = 'SteelBlue1', cursor='hand2'))
    name_but_list.append(Button(name_win,text = "Confirmer", font='Arial 14',command = lambda : add_name(3), activebackground = 'SteelBlue1', cursor='hand2'))
    name_but_list.append(Button(name_win,text = "Confirmer", font='Arial 14',command = lambda : add_name(4), activebackground = 'SteelBlue1', cursor='hand2'))
    name_but_list.append(Button(name_win,text = "Confirmer", font='Arial 14',command = lambda : add_name(5), activebackground = 'SteelBlue1', cursor='hand2'))
    name_but_list.append(Button(name_win,text = "Confirmer", font='Arial 14',command = lambda : add_name(6), activebackground = 'SteelBlue1', cursor='hand2'))
    name_but_list.append(Button(name_win,text = "Confirmer", font='Arial 14',command = lambda : add_name(7), activebackground = 'SteelBlue1', cursor='hand2'))

    ia_list = []
    ia_list.append(Button(name_win,text = "IA", font='Arial 14',command = lambda : add_ai(0), activebackground = 'SteelBlue1', cursor='hand2'))
    ia_list.append(Button(name_win,text = "IA", font='Arial 14',command = lambda : add_ai(1), activebackground = 'SteelBlue1', cursor='hand2'))
    ia_list.append(Button(name_win,text = "IA", font='Arial 14',command = lambda : add_ai(2), activebackground = 'SteelBlue1', cursor='hand2'))
    ia_list.append(Button(name_win,text = "IA", font='Arial 14',command = lambda : add_ai(3), activebackground = 'SteelBlue1', cursor='hand2'))
    ia_list.append(Button(name_win,text = "IA", font='Arial 14',command = lambda : add_ai(4), activebackground = 'SteelBlue1', cursor='hand2'))
    ia_list.append(Button(name_win,text = "IA", font='Arial 14',command = lambda : add_ai(5), activebackground = 'SteelBlue1', cursor='hand2'))
    ia_list.append(Button(name_win,text = "IA", font='Arial 14',command = lambda : add_ai(6), activebackground = 'SteelBlue1', cursor='hand2'))
    ia_list.append(Button(name_win,text = "IA", font='Arial 14',command = lambda : add_ai(7), activebackground = 'SteelBlue1', cursor='hand2'))

    return name_but_list, ia_list


def round_graph(window, list_player, round):
    '''
        Fonction de tours pour la version graphique, appelée à chaque manche, détecte si une manche doit s'arrêter, affiche les cartes, demande les choix des joueurs, réparti les gemmes

        ENTREE
            window (tkinter window) : Fenêtre principale du jeu, list_player (list) : liste de joueurs, round (int) : numéro de manche
        
        SORTIE
            list_player
    '''
    version_graph = True # La version jouée est la version graphique
    deck = create_deck(version_graph, round, list_player)
    deck_shown = []
    end_round = False
    
    dis_win = Frame(window, background = "khaki3") # Création du cadre pour le plateau
    dis_win.pack(side="top", expand=True, fill="both")
    dis_win.grid_propagate(False) # Le cadre ne va pas s'étendre quand on rajoutera de éléments dedans

    player_win = Frame(window, highlightbackground="gray", highlightthickness=3, background = "wheat3") # Création du cadre pour l'affichage des joueurs
    player_win.pack(side="top", expand=True, fill="both")

    init_player_graph(player_win,list_player,round)

    while not end_round :
        if check_end(list_player) :
            end_round = True
        if not end_round :
            draw(deck, deck_shown, list_player)
        if trap_check(deck_shown) :
            end_round = True
            display_graph(dis_win,player_win,deck_shown, list_player)
            dis_win.update()
            time.sleep(2) # Courte pause avant de changer de manche
        if not end_round :
            display_graph(dis_win,player_win,deck_shown, list_player)
            deck_shown, list_player = player_action_graph(player_win,deck_shown, list_player)
    dis_win.destroy()
    player_win.destroy()

    return list_player


def init_player_graph(player_win, list_player, round):
    '''
        Fonction qui affiche le numéro de la manche en cours et les noms des joueurs, ces valeurs ne changent pas entre chaque tour

        ENTREE
            player_win (Frame tkinter) : Frame de l'affichage des joueurs, list_player (list) : liste de joueurs, round (int) : numéro de la manche
        
        SORTIE
            ---
    '''
    Label(player_win, text = "Manche n°" + str(round), font='Arial 12 bold', bg = "wheat3").place(relx = 0.1, rely = 0.01)
    for i in range(len(list_player)):
        Label(player_win, text = list_player[i].name, font='Arial 16 bold', bg = "wheat3").place(relx = 0.04 + i*0.12, rely = 0.25)


def player_display(player_win, list_player):
    '''
        Affiche les informations pour chaque joueur, gemmes, état et le nombre de gemmes restantes sur le plateau

        ENTREE
            player_win (Frame tkinter) : Frame de l'affichage des joueurs, list_player (list) : liste de joueurs
        
        SORTIE
            ---
    '''
    for i in range(len(list_player)):
        Label(player_win, text = list_player[i].name, font = 'Purisa 16 bold underline', bg = "wheat3").place(relx = 0.04 + i*0.12, rely = 0.25)
        if list_player[i].in_game : # Vérifie si le joueur est en jeu ou au campement
            Label(player_win,text = "en jeu", font = 'Arial 14 bold', fg = "blue", bg = "wheat3").place(relx = 0.04 + i*0.12, rely = 0.35)
        else :
            Label(player_win,text = "au camp", font = 'Arial 14 bold', fg = "red2", bg = "wheat3").place(relx = 0.04 + i*0.12, rely = 0.35)
        Label(player_win,text = str(list_player[i].temp_gem) + " gemmes", font = 'Arial 14 bold', bg = "wheat3").place(relx = 0.04 + i*0.12, rely = 0.50)
        Label(player_win,text = str(list_player[i].total_gem) + " gemmes \n stockées", font = 'Arial 14 bold', bg = "wheat3").place(relx = 0.04 + i*0.12, rely = 0.58)


def display_graph(dis_win, player_win, deck_shown, list_player):
    '''
        Affiche les cartes tirées sur le plateau et appelle player_display() pour afficher les informations des joueur

        ENTREE
            dis_win (Frame tkinter) : Frame du plateau, player_win (Frame tkinter) : Frame de l'affichage des joueurs, deck_shown (list) : liste des cartes sur le plateau, list_player (list) : liste de joueurs
        
        SORTIE
            ---
    '''
    temp_total = 0
    for i in range (len(deck_shown)): # Calcul du nombre de gemmes encore sur le plateau
        if deck_shown[i].treasure :
            temp_total += deck_shown[i].nbr_gem
    Label(player_win, text = "Gemmes restantes : " + str(temp_total) + '  ', font='Arial 12 bold', bg = "wheat3").place(relx = 0.3, rely = 0.01)

    if len(deck_shown) < 16: # À partir de 16 cartes, les cartes sont affichées sur une nouvelle ligne
        Label(dis_win, image = deck_shown[-1].img, bg = "wheat3").grid(row = 0, column = len(deck_shown), sticky = N, padx = 10, pady= 15)
    else :
        Label(dis_win, image = deck_shown[-1].img, bg = "wheat3").grid(row = 1, column = len(deck_shown) - 15, sticky = N, padx = 10, pady= 15)

    player_display(player_win,list_player)


def player_action_graph(player_win, deck_shown, list_player):
    '''
        Fonction qui demande aux joueurs s'ils reste dans la grotte ou s'ils veulent partir avec deux boutons et appelle player_action_repart() pour répartir les gemmes

        ENTREE
            player_win (Frame tkinter) : Frame de l'affichage des joueurs, deck_shown (list) : liste des cartes sur le plateau, list_player (list) : liste de joueurs
        
        SORTIE
            deck_shown, list_player
    '''
    okvar = IntVar()
    player_out = [] # Liste des indices des joueurs qui sortent
    cpt = [] # Compteur de joueur qui ont joué
    verif = 0

    for i in range(len(list_player)): # Nombre de joueurs encore en jeu
        if list_player[i].in_game :
            verif += 1

    def set_state(state, i):
        '''
            Fonction interne qui change l'attribut in_game pour chaque joueur qui joue

            ENTREE
                state (boolean) : décision du joueur (True = Rester, False = Partir), i (int) : indice du joueur qui prend une décision dans list_player
            
            SORTIE
                --- (modifie list_player)
        '''
        list_player[i].in_game = state
        # Supprime les boutons "Rester" et "Sortir", ils sont inutiles maintenant
        stay_list[i].destroy()
        quit_list[i].destroy()
        cpt.append(i)
        if not state :
            player_out.append(i)
    
    def set_ok():
        '''
            Fonction interne qui vérifie si tous les joueurs ont pris une décision

            ENTREE
                --- (les variables contenues dans start_game_graph() sont accessibles)

            SORTIE
                --- (modifie okvar)
        '''
        if len(cpt) == verif : # Vérifie si il y autant de joueurs qui ont joué que de joueurs encore en jeu
            okvar.set(1)

    stay_list, quit_list = button_creation_action(player_win,set_state)

    bt_ok = Button(player_win, text = "Continuer", font = 'Arial 15', activebackground = 'green', command = lambda: set_ok(), cursor = 'hand2')
    bt_ok.place(relx = 0.8, rely = 0.01)

    for i in range(len(list_player)):
        if list_player[i].in_game and not list_player[i].is_ai: # Vérifie que les joueurs sont bien réels et dans la partie pour leur afficher les choix
            stay_list[i].place(relx = 0.041 + i * 0.12, rely = 0.72)
            quit_list[i].place(relx = 0.046 + i * 0.12, rely = 0.81)
        elif list_player[i].in_game and list_player[i].is_ai: # Vérifie que les ia sont bien dans la partie afin qu'elle fasse un choix
            set_state(ai_choice(deck_shown),i)

    bt_ok.wait_variable(okvar)

    return player_action_repart(deck_shown, list_player, player_out)


def ai_choice(deck_shown):
    '''
        Détermine les choix que feront les ia, plus il y a des dangers, plus elles ont des chances de sortir :
            Quand il n'y a pas de danger, elles ont une chance sur quatorze de sortir
            Quand un danger apparaît, les chances de sortir augmentent

        ENTREE
            deck_shown (list) : 
        
        SORTIE
            choice (bool) : Choix de sortir (False) ou de rester (True)
    '''
    choice_list = [True, True, True, True, True, True, True, True, True, True, True, True, True, False] # 1 chance sur 14 de sortir si aucune danger n'est découvert
    cpt_danger = 0

    for i in range(len(deck_shown)):
        if deck_shown[i].danger : # Augmente les chances de sortir si des dangers apparaîssent
            choice_list.append(False)
            choice_list.append(False)
            choice_list.append(False)
            cpt_danger += 1
        else :
            choice_list.append(True)
            choice_list.append(True)
            choice_list.append(False)
    
    if cpt_danger == 0: # Si il n'y a aucun danger sur le plateau, les ia ne sortent pas
        choice_list = [True]

    choice = random.choice(choice_list)

    return choice


def button_creation_action(player_win,set_state):
    '''
        Crée les boutons qui "Rester" et "Sortir" pour que les joueurs prennent une décision

        ENTREE
            player_win (Frame tkinter) : Frame de l'affichage des joueurs, set_state (function)
        
        SORTIE
            stay_list (list) : liste comprenant les boutons "Rester", stay_list (list) : liste comprenant les boutons "Sortir"
    '''
    stay_list = []
    quit_list = []

    stay_list.append(Button(player_win, text = "Rester", font='Arial 12', command = lambda: set_state(True, 0), activebackground = 'SteelBlue1', cursor='hand2'))
    stay_list.append(Button(player_win, text = "Rester", font='Arial 12', command = lambda: set_state(True, 1), activebackground = 'SteelBlue1', cursor='hand2'))
    stay_list.append(Button(player_win, text = "Rester", font='Arial 12', command = lambda: set_state(True, 2), activebackground = 'SteelBlue1', cursor='hand2'))
    stay_list.append(Button(player_win, text = "Rester", font='Arial 12', command = lambda: set_state(True, 3), activebackground = 'SteelBlue1', cursor='hand2'))
    stay_list.append(Button(player_win, text = "Rester", font='Arial 12', command = lambda: set_state(True, 4), activebackground = 'SteelBlue1', cursor='hand2'))
    stay_list.append(Button(player_win, text = "Rester", font='Arial 12', command = lambda: set_state(True, 5), activebackground = 'SteelBlue1', cursor='hand2'))
    stay_list.append(Button(player_win, text = "Rester", font='Arial 12', command = lambda: set_state(True, 6), activebackground = 'SteelBlue1', cursor='hand2'))
    stay_list.append(Button(player_win, text = "Rester", font='Arial 12', command = lambda: set_state(True, 7), activebackground = 'SteelBlue1', cursor='hand2'))

    quit_list.append(Button(player_win, text = "Sortir", command = lambda: set_state(False, 0), activebackground = 'red2', cursor='hand2'))
    quit_list.append(Button(player_win, text = "Sortir", command = lambda: set_state(False, 1), activebackground = 'red2', cursor='hand2'))
    quit_list.append(Button(player_win, text = "Sortir", command = lambda: set_state(False, 2), activebackground = 'red2', cursor='hand2'))
    quit_list.append(Button(player_win, text = "Sortir", command = lambda: set_state(False, 3), activebackground = 'red2', cursor='hand2'))
    quit_list.append(Button(player_win, text = "Sortir", command = lambda: set_state(False, 4), activebackground = 'red2', cursor='hand2'))
    quit_list.append(Button(player_win, text = "Sortir", command = lambda: set_state(False, 5), activebackground = 'red2', cursor='hand2'))
    quit_list.append(Button(player_win, text = "Sortir", command = lambda: set_state(False, 6), activebackground = 'red2', cursor='hand2'))
    quit_list.append(Button(player_win, text = "Sortir", command = lambda: set_state(False, 7), activebackground = 'red2', cursor='hand2'))
    return stay_list, quit_list


def ask_continue():
    '''
        Crée une nouvelle fenêtre qui demande au joueur s'il veut rejouer ou s'il veut quitter le jeu

        ENTREE
            ---

        SORTIE
            ---
    '''
    end_window = Tk()
    end_window.geometry('500x350')
    end_window.resizable(False,False)
    end_window.title("Diamant - Fin de partie")
    Label(end_window, text = "Partie terminée", font = "Purisa 30 bold").pack(side = TOP, pady = 10)

    def play_again():
        '''
            Fonction interne qui ferme la fenêtre et relance la fonction principale du jeu

            ENTREE
                --- (les variables contenues dans play_again() sont accessibles)
            
            SORTIE
                ---
        '''
        end_window.destroy()
        game_graph()
    
    Button(end_window, text = "Nouvelle partie", command = lambda : play_again(), font = 'Arial 20 bold', activebackground = 'SteelBlue1', cursor = 'hand2', height = 3, width = 15).pack(side = TOP, pady = 8)
    Button(end_window, text = "Quitter", command = lambda : end_window.destroy(), font = 'Arial 20 bold', activebackground = 'red2', cursor = 'hand2', height = 3, width = 15).pack(side = TOP, pady = 8)

    end_window.mainloop()


def end_game_display_graph(list_player, window):
    '''
        Affiche le classement des joueurs

        ENTREE
            list_player (list) : Liste des joueurs
        
        SORTIE
            ---
    '''
    dis_points = Frame(window)
    dis_points.pack(side="top", expand=True, fill="both")
    temp_points = end_game(list_player)
    index_points = []
    okvar = IntVar()

    Label(dis_points, text = 'Classement :', font = 'Arial 25 bold underline').pack(side = TOP, pady = 10)

    for i in range(len(temp_points)):
        for j in range(len(list_player)):
            if (list_player[j].total_gem == temp_points[i]) and (j not in index_points) :
                index_points.append(j)
                j = len(list_player)-1
        Label(dis_points, text = str(i+1) + ' : ' + list_player[index_points[i]].name + ', ' + str(temp_points[i]) + ' gemmes', font = 'Arial 22 bold').pack(side = TOP, pady = 20)
    
    conf_but = Button(dis_points, text = 'Sortir', font = 'Arial 35 bold', cursor = 'hand2', command = lambda : okvar.set(1), activebackground = 'green')
    conf_but.pack(side = BOTTOM, pady = 20)
    conf_but.wait_variable(okvar)
    dis_points.destroy()