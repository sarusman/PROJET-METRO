import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import main
import affichage_prim

#remplissage des listes
sommets, aretes = main.parse_metro()
# Créer un graphe vide
graphe = nx.Graph()

def creation_graph() :
    for s in sommets :
        graphe.add_node(s['numSommet'], group=s['numLigne'])
    for a in aretes :
        graphe.add_edge(a['S1'], a['S2'])

    

def afficher_graphe() :
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
    pos = nx.kamada_kawai_layout(graphe)
    # Tracer le graphe
    fig = plt.figure(figsize=(16, 8))
    nx.draw(graphe, pos, with_labels=True,  node_color=colors, edge_color="black", node_size=100, font_size=7)
    
    # Fonction de callback pour le bouton
    def on_button_clicked(event):
        affichage_prim.afficher_graphe()

    # Créer le bouton
    button_ax = plt.axes([0.4, 0.05, 0.2, 0.075])  
    button = Button(button_ax, 'Afficher l\'ACPM')
    button.on_clicked(on_button_clicked)
    plt.show()


creation_graph()
afficher_graphe()