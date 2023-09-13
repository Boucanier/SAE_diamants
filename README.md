# SAÉ 1.01 : jeu Diamants

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Création du jeu Diamants en python

## Lancement du jeu

Version graphique :
    Pour lancer la version graphique, il faut lancer [_main.py_](main.py)

Version lignes de commandes :
    Pour lancer le version en lignes de commandes, il faut commenter la ligne "version = "GRAPH" " dans le fichier [_main.py_](main.py).
    Il faut ensuite lancer [_main.py_](main.py)


## Présentation du jeu

Nous avons été jusqu'au niveau 3 dans la réalisation du jeu. Nous avons aussi réalisé le bonus en créant des ia.
Nous avons utilisé tkinter pour créer l'interface graphique car nous voulions utilisé le type 'Button' de cette librairie.


## Problèmes rencontrés

Dans tkinter, nous n'avons pas trouver comment créer plusieurs boutons ayant des valeurs différentes avec une boucle.
Nous avons donc créer des fonctions qui créent des listes de boutons afin de réduire les tailles des fonctions principales.


## Bugs connus

Quand la version graphique est lancée et que le jeu est fermé "de force" (avec la croix), le programme tourne encore dans le terminal.
Pour bien quitter le jeu, il faut finir la partie et quitter.


## Idées

- Les ia que nous avons créées ont un pourcentage de chance de sortir du jeu qui est adaptatif.
En effet, quand aucun danger n'est présent sur le plateau, elles ne sortent pas.
Quand une carte qui n'est pas un danger est posée sur le plateau, elles ont un peu plus de chance de sortir.
Enfin, quand un danger est posé sur le plateau, elles ont encore plus de chances de sortir.
    
- Afin d'éviter des problèmes d'affichage liés aux dimensions de la fenêtre, nous avons bloqué la posibilité de pouvoir les déformer


## Remarque

Les fonctions de test pour les fonctions importantes se trouvent dans [_diamond_test.py_](diamond_test.py)

---

Projet réalisé dans le cadre de la SAÉ 1.01 du premier semestre de BUT Informatique à l'IUT de Vélizy

Décembre 2022
