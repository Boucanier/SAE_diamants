import algo
import graph

# By default, the program start the graphical version
# If you want to start the CLI version, comment the line with : "version = "GRAPH" "

version = "CLI"
# version = "GRAPH"

if __name__ == "__main__" :
    if version == "CLI" :
        algo.game()
    elif version == "GRAPH" :
        graph.game_graph()