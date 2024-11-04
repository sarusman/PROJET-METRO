import networkx as nx
import matplotlib.pyplot as plt
import main
import prim

#listes
sommets = [] 
arretes = []
arbre_couvrant = []
#remplissage des listes
main.parse_metro(sommets, arretes)
prim.prim_algo(sommets, arretes, arbre_couvrant)
# Créer un graphe vide
graphe = nx.Graph()


def creation_graph(arbre_couvrant, graphe) :
    for s in sommets :
        graphe.add_node(s['numSommet'], group=s['numLigne'])
    for a in arbre_couvrant :
        graphe.add_edge(a['S1'], a['S2'])

    

def afficher_graphe(graphe) :
    color_map = {
        '1': '#FFCE00',
        '2': '#0064B0',
        '3': '#9F9825',
        '3bis': '#98D4E2',
        '4' : '#C04191',
        '5' : '#F28E42',
        '6' : '#83C491',
        '7' : '#F3A4BA',
        '7bis' : '#83C491',
        '8' : '#CEADD2',
        '9' : '#D5C900',
        '10' : '#E3B32A',
        '11' : '#8D5E2A',
        '12' : '#00814F',
        '13' : '#98D4E2',
        '14' : '#662483'
    }
    colors = [color_map[graphe.nodes[node]['group']] for node in graphe.nodes]
    labels = {node: graphe.nodes[node]['group'] for node in graphe.nodes}
    pos = nx.kamada_kawai_layout(graphe)

    # Tracer le graphe
    plt.figure(figsize=(10, 10))
    nx.draw(graphe, pos, with_labels=True,  node_color=colors, edge_color="black", node_size=100, font_size=7)

    # Afficher le graphe
    plt.title("Affichage d'un graphe avec NetworkX")
    plt.show()

creation_graph(arbre_couvrant, graphe)
afficher_graphe(graphe)
