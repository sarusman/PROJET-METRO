import main

#listes
sommets = [] 
arretes = []
positions = []

#remplissage des listes
main.parse_metro(sommets, arretes)
main.parse_position(positions)

def prim_algo(sommets) :
    sommets_visites=[]
    arretes_utilisees=[]

    #principes :
    #partir d'un sommet
    #a partir de se sommet choisir l'arrete la plus petite et qui va sur un sommet jamais visiter
    #ajouter le sommet a la liste des sommet parcourue
    #en boucle :
    #   a partir de tous les sommets dans ma liste visiter choisir l'arrete la plus petite qui part vers un sommet jamais visiter
    #   ajouter le sommet a la liste visiter
    #   ajouter l'arretes a la liste visiter

prim_algo(sommets)