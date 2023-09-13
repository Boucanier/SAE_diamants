import algo
import graph

# By default, the program start the graphical version
# If you want to start the CLI version, uncomment the line with : "version = "GRAPH" "

# Par défaut, le programme se lance dans le terminal
# Pour lancer la version graphique il faut décommenter la ligne : "version = "GRAPH" "

version = "CLI"
# version = "GRAPH"

if __name__ == "__main__" :
    if version == "CLI" :
        algo.game()
    elif version == "GRAPH" :
        graph.game_graph()
