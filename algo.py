from tkinter import *
import time
import random
import os
import platform


class player :
    def __init__(self, name, is_ai) :
        '''
            Initialise l'objet player

            name (str) : nom du joueur
            total_gem (int) : nombre de gemmes du joueur au campement
            temp_gem (int) : nombre de gemmes temporaires du joueur pendant une manche
            in_game (boolean) : état du joueur (True = en jeu, False = au campement)
            nbr_relic (int) : nombre de reliques découvertes
            is_ai (bool) : indique si le joueur est une ia
        '''
        self.name = name
        self.total_gem = 0
        self.temp_gem = 0
        self.in_game = True
        self.nbr_relic = 0
        self.is_ai = is_ai

class Card :
    def __init__(self, danger, type_danger, treasure, nbr_gem, relic, version_graph) :
        '''
            Initialise l'objet Card

            danger (boolean) : indique si la carte est une carte danger
            type_danger (int) : indice du danger de la carte (0 si pas un danger, sinon de 1 à 5)
            treasure (boolean) : indique si la carte est une carte trésor
            nbr_gem (int) : nombre de gemmes de la carte (0 si pas un trésor, sinon 1, 2, 3, 4, 5, 7, 9, 11, 13, 14, 15 ou 17)
            relic (boolean) : indique si la carte est une relique

            Si la version du jeu est la version graphique (version_graph == True):
                Affecte à chaque carte une image de son type (trésor, relique, danger (une carte par type de danger))
        '''
        self.danger = danger
        self.type_danger = type_danger
        self.treasure = treasure
        self.nbr_gem = nbr_gem
        self.relic = relic
        self.graph = version_graph
        if self.graph :
            if self.type_danger :
                self.img = PhotoImage(file = "images/da" + str(self.type_danger) + "_card.png")
            elif self.treasure :
                self.img = PhotoImage(file = "images/tr_card.png")
            else :
                self.img = PhotoImage(file = "images/rel_card.png")

def create_deck(version_graph, round, list_player) :
    '''
        Crée le deck utilisé dans la partie pour piocher des cartes

        ENTREE
            version_graph (boolean) : indique si la version jouée est la version graphique (True si oui)
        
        SORTIE
            deck (list) : liste d'objets Card
    '''
    temp_relic = 0
    deck = []
    val_treasure = [1, 2, 3, 4, 5, 5, 7, 7, 9, 11, 11, 13, 14, 15, 17]
    for i in range (15) :
        deck.append(Card(False, 0, True, val_treasure[i], False, version_graph))

    for i in range (1, 6) :
        for j in range (3) :
            deck.append(Card(True, i, False, 0, False, version_graph))

    for i in range(len(list_player)):
        temp_relic += list_player[i].nbr_relic

    for i in range(round - temp_relic): # Ajoute une relique par manche : le nombre finale de relique est la différence entre le numéro de la manche et le nombre de reliques découvertes
        deck.append(Card(False, 0, False, 0, True, version_graph))
    random.shuffle(deck)
    return deck

def start_game():
    '''
        Prépare les liste des joueurs en demandant le nombre et le nom de chacun

        ENTREE
            ---

        SORTIE
            list_player (list) : liste des joueurs
    '''
    #Récupération du nombre de joueurs
    nb_player = int(input("Combien de joueurs êtes-vous ?"))
    while nb_player > 8 or nb_player < 3 :
        nb_player = int(input("Nombre de joueurs incorrects, il faut être entre 3 et 8 joueurs"))

    #Création de la liste des joueurs
    list_player = []
    for i in range (nb_player) :
        print("Joueur ",i+1,",entrez votre nom")
        name = str(input())
        list_player.append(player(name, False))
    
    return list_player

def draw(deck,deck_shown,list_player):
    '''
        Prend la première carte du deck mélangé et la met sur le plateau de jeu (dans le deck affiché)
        Réparti les diamants de la carte entre les joueurs encore en jeu

        ENTREE
            deck (list) : liste de cartes, deck_shown (list) : liste de cartes, list_player (list) : liste de joueurs

        SORTIE
            deck, deck_shown, list_player
    '''
    new_card = deck[0] # Tire la première carte du deck
    nbr_in_game = []
    if new_card.treasure :
        for i in range(len(list_player)):
            if list_player[i].in_game :
                nbr_in_game.append(i)

        for e in nbr_in_game: # Répartit les gemmes entre les joueurs en jeu
            list_player[e].temp_gem += (new_card.nbr_gem//len(nbr_in_game))

        new_card.nbr_gem -= (new_card.nbr_gem//len(nbr_in_game))*len(nbr_in_game)

    deck_shown.append(new_card)
    deck.remove(new_card)

    return deck, deck_shown, list_player

def trap_check(deck_shown):
    '''
        Détecte si un piège est présent deux fois sur le plateau
    
        ENTREE
            deck_shown (list) : liste de cartes tirées
        
        SORTIE
            trap_detected (boolean) : indique si un piège a été détecté
    '''
    trap_detected = False
    trap_in_game = []
    for i in range(len(deck_shown)):
        if deck_shown[i].type_danger != 0 :
            trap_in_game.append(deck_shown[i].type_danger)
    for i in range(1,6):
        if i in trap_in_game :
            trap_in_game.remove(i)
            if i in trap_in_game :
                trap_detected = True

    return trap_detected

def find_relic_val(list_player):
    '''
        Trouve la valeur de la prochaine relique qui va sortir (5, 5, 5, 10, 10)

        ENTREE
            list_player (list) : liste de joueurs
        
        SORTIE
            val_relic (int) : valeur de la prochaine relique sortie (5 ou 10)
    '''
    relic_sum = 0
    val_relic = 0
    for i in range (len(list_player)): # Détecte le nombre de reliques sorties
        relic_sum += list_player[i].nbr_relic
    if relic_sum < 3 :
        val_relic = 5
    elif relic_sum >= 3 :
        val_relic = 10
    return val_relic

def player_action(deck_shown,list_player):
    '''
        Demande au joueur s'il souhaite continuer à jouer ou rentrer au campement

        ENTREE
            deck_shown : liste de cartes, list_player : liste de joueurs
        
        SORTIE
            deck_shown, list_player
    '''
    player_out = []
    for i in range (len(list_player)):
        if list_player[i].in_game :
            is_out = ''
            while (is_out != 'O') and (is_out != 'N') :
                is_out = input(list_player[i].name + ' Sortir ? (O/N) ').upper() # Met la réponse en majuscule afin d'éviter de mettre trop de conditions après
            if is_out == 'O' :
                list_player[i].in_game = False
                player_out.append(i)
    return player_action_repart(deck_shown,list_player,player_out)

def player_action_repart(deck_shown, list_player, player_out):
    '''
        Réparti les gemmes encore sur le plateau entre les joueurs qui sortent (si elles ne peuvent pas toutes être partagées, le reste reste sur le plateau)

        ENTREE
            deck_shown (list) : liste de cartes, list_player (list) : liste de joueurs, player_out (list) : liste des joueurs qui viennent de sortir
        
        SORTIE
            deck_shown, list_player
    '''
    temp_relic = []
    temp_total = 0
    if len(player_out) != 0 : # Ne réparti pas les gemmes si aucun joueur ne veut sortir
        for i in range(len(deck_shown)):
            temp_total += deck_shown[i].nbr_gem
            if deck_shown[i].relic :
                temp_relic.append(i)

        for i in range(len(player_out)): # Transfert les gemmes des joueurs au camp et réparti les gemmes restantes
            list_player[player_out[i]].total_gem += list_player[player_out[i]].temp_gem
            list_player[player_out[i]].temp_gem = 0
            list_player[player_out[i]].total_gem += (temp_total // len(player_out))

        for i in range (len(deck_shown)):
            deck_shown[i].nbr_gem = 0

        for i in range (len(deck_shown)): # Stoque les gemmes restantes dans la dernière carte du plateau
            if deck_shown[i].treasure :
                deck_shown[i].nbr_gem = temp_total - ((temp_total // len(player_out)) * len(player_out))
                i = len(deck_shown)-1
                
        if len(temp_relic) > 0 and len(player_out) == 1: # Les reliques ne sortent pas si plusieurs personnes veulent sortir
                if len(player_out) == 1 :
                    for i in range (len(temp_relic)):
                        list_player[player_out[0]].total_gem += find_relic_val(list_player)
                        list_player[player_out[0]].nbr_relic += 1
                elif len(player_out) > 1 :
                    for i in range (len(temp_relic)):
                        list_player[player_out[0]].nbr_relic += 1
                for i in range (len(temp_relic)):
                    deck_shown[temp_relic[i]].relic = False
                    if deck_shown[temp_relic[i]].graph :
                        deck_shown[temp_relic[i]].img = PhotoImage(file = "") # Enlève les images de reliques pour qu'elles disparaissent du plateau
    return deck_shown, list_player


def check_end(list_player):
    '''
        Détecte les conditions de fin de manche :
            Détecte si tous les joueurs sont sortis
            Renvoie True si tous les joueurs sont sortis ou si un piège est présent deux fois sur le plateau

        ENTREE
            list_player (list) : liste de joueurs, trap_detected (boolean) : indique si un piège a été détecté
        
        SORTIE
            end_round (boolean) : indique si  la manche doit s'arrêter
    '''
    end_round = False
    player_out = 0
    for i in range(len(list_player)):
        if list_player[i].in_game == False :
            player_out += 1
    if player_out == len(list_player):
        end_round = True
    return end_round


def display(deck_shown,list_player,round):
    '''
        Affiche les cartes présentes sur le plateau :
            Les cartes trésor sont affichées avec le nombre de gemmes qu'il leur reste après la distribution
            Les cartes danger sont affichées avec leur type de danger (1 à 5)

        Affiche pour chaque joueur :
            Son nom
            Son statut dans le jeu (dans le temple / au camp)
            Le nombre de gemmes qu'il a avec lui dans le temple
            Le nombre de gemmes qu'il a au campement
        
        ENTREE
            deck_shown (list) : liste de cartes, list_player (list) : liste de joueurs
        
        SORTIE
            ---
    '''
    # détecte le système d'expoitation afin d'utiliser la bonne commande pour effacer le terminal
    if platform.system() == 'Linux':
        os.system('clear')
    elif platform.system() == 'Windows':
        os.system('cls')
    print('Manche',round,'/ 5','\n')
    temp_total = 0
    for i in range (len(deck_shown)):
        if deck_shown[i].danger :
            print('DANGER',deck_shown[i].type_danger)
        elif deck_shown[i].treasure :
            print('TRESOR')
            temp_total += deck_shown[i].nbr_gem
        elif deck_shown[i].relic :
            print('RELIQUE')
    print()
    print('Gemmes restantes :',temp_total)
    print()
    for i in range (len(list_player)):
        if list_player[i].in_game :
            position = '(dans le temple)'
        else :
            position = '(au campement) '
        print('{:>15s}{:>19s}{:>11s}{:>21s}'.format(str(list_player[i].name),position+' :',str(list_player[i].temp_gem)+' gemmes',str(list_player[i].total_gem)+' gemmes stockées'))
    print()


def round(list_player, round) :
    '''
        Fonction de tours, appelée à chaque manche, détecte si une manche doit s'arrêter, affiche les cartes, demande les choix des joueurs, réparti les gemmes

        ENTREE
            list_player (list) : liste de joueurs, round (int) : numéro de manche
        
        SORTIE
            list_player
    '''
    version_graph = False
    deck = create_deck(version_graph, round, list_player)
    deck_shown = []
    end_round = False
    while not end_round :
        if check_end(list_player) :
            end_round = True
        if not end_round :
            draw(deck, deck_shown, list_player)
        if trap_check(deck_shown) :
            end_round = True
            display(deck_shown, list_player, round)
            time.sleep(2)
        if not end_round :
            display(deck_shown, list_player, round)
            player_action(deck_shown, list_player)
            display(deck_shown, list_player, round)
    return list_player


def end_game(list_player):
    '''
        Classe les gemmes des joueurs

        ENTREE
            list_player (list) : liste de joueurs
        
        SORTIE
            temp_points (list) : liste des points des joueurs triée
    '''
    temp_points = []
    for i in range (len(list_player)):
        temp_points.append(list_player[i].total_gem)
    temp_points.sort()
    temp_points.reverse()
    return temp_points


def end_game_display(list_player):
    '''
        Affiche le classement des joueurs

        ENTREE
            list_player (list) : Liste des joueurs
        
        SORTIE
            ---
    '''
    temp_points = end_game(list_player)
    index_points = []
    for i in range(len(temp_points)):
        for j in range(len(list_player)):
            if (list_player[j].total_gem == temp_points[i]) and (j not in index_points) :
                index_points.append(j)
                j = len(list_player)-1
        print(i+1,':',list_player[index_points[i]].name + ',',temp_points[i],'gemmes')
        

def game():
    '''
        Fonction principale du jeu pour la version en lignes de commandes

        ENTREE
            ---
        
        SORTIE
            ---
    '''
    list_player = start_game()
    for i in range (5) :
        for j in range (len(list_player)): # Remet tous les joueurs dans la partie
            list_player[j].in_game = True
            list_player[j].temp_gem = 0
        list_player = round(list_player, i+1)
    end_game_display(list_player)