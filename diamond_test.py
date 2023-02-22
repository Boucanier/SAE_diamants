from main import *

def test_create_deck() :
    list_player = []
    for i in range (3):
        list_player.append(player("p " + str(i),False))

    deck = create_deck(False, 1, list_player)
    assert len(deck) == 31, "Erreur de taille de deck"

    deck = create_deck(False, 4, list_player)
    assert len(deck) == 34, "Erreur de taille de deck"


def test_draw():
    list_player = []
    deck_shown = []
    for i in range (3):
        list_player.append(player("p " + str(i),False))
    deck = create_deck(False, 1, list_player)
    
    for i in range (6):
        deck, deck_shown, list_player = draw(deck, deck_shown, list_player)

    assert len(deck_shown) == 6, "Erreur de taille pendant draw"
    assert len(deck) + len(deck_shown) == 31, "Erreur de taille pendant draw"

    for i in range (17):
        deck, deck_shown, list_player = draw(deck, deck_shown, list_player)

    assert len(deck_shown) == 23, "Erreur de taille pendant draw"
    assert len(deck) + len(deck_shown) == 31, "Erreur de taille pendant draw"


def test_trap_check():
    deck_shown = [Card(True, 2, False, 0, False, False), Card(True, 2, False, 0, False, False)]
    assert trap_check(deck_shown) == True, "Erreur de détection de piège"

    deck_shown = [Card(True, 1, False, 0, False, False), Card(True, 2, False, 0, False, False)]
    assert trap_check(deck_shown) == False, "Erreur de détection de piège"

    deck_shown = [Card(True, 2, False, 0, False, False), Card(True, 2, False, 0, False, False), Card(True, 2, False, 0, False, False)]
    assert trap_check(deck_shown) == True, "Erreur de détection de piège"


def test_find_relic_val():
    list_player = []
    for i in range (3):
        list_player.append(player("p " + str(i),False))
    
    for i in range(2):
        list_player[i].nbr_relic = 1
    assert find_relic_val(list_player) == 5, "Erreur de détection de relique"

    list_player[-1].nbr_relic = 1
    assert find_relic_val(list_player) == 10, "Erreur de détection de relique"

    for i in range(3):
        list_player[i].nbr_relic = 0

    list_player[0].nbr_relic = 0
    list_player[1].nbr_relic = 3
    list_player[2].nbr_relic = 1
    assert find_relic_val(list_player) == 10, "Erreur de détection de relique"


def test_check_end():
    list_player = []
    for i in range (4):
        list_player.append(player("p " + str(i),False))
        list_player[i].in_game = True
    assert check_end(list_player) == False, "Erreur de détection de l'état des joueurs"

    list_player[3].in_game = False
    assert check_end(list_player) == False, "Erreur de détection de l'état des joueurs"

    for i in range(len(list_player)):
        list_player[i].in_game = False
    assert check_end(list_player) == True, "Erreur de détection de l'état des joueurs"


def test_player_action_repart():
    list_player = []
    for i in range (4):
        list_player.append(player("p " + str(i),False))
    
    deck_shown = [Card(False, 0, True, 3, False, False)]

    player_out = [0, 1]
    player_action_repart(deck_shown, list_player, player_out)
    assert list_player[0].total_gem == 1, "Erreur de répartition des gemmes"
    assert list_player[2].total_gem == 0, "Erreur de répartition des gemmes"

    deck_shown = [Card(False, 0, True, 8, False, False)]
    player_out = [0, 1, 2, 3]
    for i in range(4):
        list_player[i].total_gem = 0
    player_action_repart(deck_shown, list_player, player_out)
    assert list_player[1].total_gem == 2, "Erreur de répartition des gemmes"

    player_out = [0, 1, 3]
    deck_shown = [Card(False, 0, True, 8, False, False)]
    for i in range(4):
        list_player[i].total_gem = 0
    player_action_repart(deck_shown, list_player, player_out)
    assert list_player[2].total_gem == 0, "Erreur de répartition des gemmes"
    assert list_player[0].total_gem == 2, "Erreur de répartition des gemmes"


test_draw()

test_create_deck()

test_trap_check()

test_find_relic_val()

test_check_end()

test_player_action_repart()