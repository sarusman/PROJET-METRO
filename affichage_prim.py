import networkx as nx
import matplotlib.pyplot as plt
import main
import prim

#listes
sommets = [] 
arretes = []
sommets_visites = []
arbre_couvrant = []
#remplissage des listes
main.parse_metro(sommets, arretes)
prim.prim_algo(sommets, arretes, arbre_couvrant, sommets_visites)
# Créer un graphe vide
graphe = nx.Graph()


def creation_graph(sommets_visites, arbre_couvrant, graphe) :
    for s in sommets :
        graphe.add_node(s['numSommet'])
    for a in arbre_couvrant :
        graphe.add_edge(a['S1'], a['S2'])

def afficher_graphe(graphe) :
    # Tracer le graphe
    plt.figure(figsize=(10, 10))
    pos = nx.kamada_kawai_layout(graphe)
    nx.draw(graphe, pos, with_labels=True, node_color="grey", edge_color="black", node_size=100, font_size=5)

    # Afficher le graphe
    plt.title("Affichage d'un graphe avec NetworkX")
    plt.show()

creation_graph(sommets_visites, arbre_couvrant, graphe)
afficher_graphe(graphe)
