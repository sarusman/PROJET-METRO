# Algorithme de Prim
def prim_algo(sommets, aretes) :
    arbre_couvrant=[]
    sommets_visites = []
    aretes_disponible = [] # les aretes disponlible
    sommets_visites.append(sommets[0]['numSommet']) # partir du premier sommet de la liste
    while (len(sommets) > len(sommets_visites)) :
        remplissage_aretes_dispo(sommets_visites[len(sommets_visites)-1], aretes_disponible, aretes, sommets_visites) # avoir les aretes disponible selon les nouveaux sommets decouvert
        arete_minimum = minimum(aretes_disponible) # prendre l'indice le l'arete la plus petite
        
        if(arete_minimum == -1) :
            print("aucune arete disponible")
            break

        arbre_couvrant.append(arete_minimum) # ajouter l'arete la plus petite à l'arbre couvrant
        if(arete_minimum['S1'] in sommets_visites) :
            sommets_visites.append(arete_minimum['S2'])
        elif(arete_minimum['S2'] in sommets_visites) :
            sommets_visites.append(arete_minimum['S1'])
        aretes_disponible.remove(arete_minimum)
        verif_aretes_dispo(sommets_visites, aretes_disponible, aretes) # verifie si les aretes disponible sont toujours disponible

    return arbre_couvrant
    print("nombre de sommets visites : ",len(sommets_visites)) # 376 sommmets en tout
    print("nombre d'aretes de l'ACPM : ",len(arbre_couvrant))
    print("nombre de doublons de sommets visites: ",len(sommets_visites) - len(set(sommets_visites)))

            
# donne l'arete avec le poinds le plus faible
def minimum(aretes_dispo) :
    # si il n'y a pas d'aretes return -1
    if len(aretes_dispo)==0 :
        print ("aretes vide")
        return -1

    a_min = aretes_dispo[0]['poids']
    indice = 0
    # on parcourt tous aretes disponibles
    for i in range (1,len(aretes_dispo)) :
        if(aretes_dispo[i]['poids'] < a_min) :
            a_min = aretes_dispo[i]['poids']
            indice = i
    return aretes_dispo[indice]


#fonction qui donne les aretes disponible selon les nouveaux sommets decouverts
def remplissage_aretes_dispo(nouveau_sommet_decouvert, aretes_disponible, aretes, sommets_visites) :
    for a in aretes :
        # si elle n'est pas deja dans arete
        if a not in aretes_disponible :
            # on verifie si le sommet n'est pas deja visite
            if ((a['S1'] == nouveau_sommet_decouvert) and (a['S2'] not in sommets_visites)) :
                aretes_disponible.append(a)
            if ((a['S2'] == nouveau_sommet_decouvert) and (a['S1'] not in sommets_visites)) :
                aretes_disponible.append(a)

# fonction qui permet de verifier si les 2 sommmets d'une arete disponible est deja visites
def verif_aretes_dispo(sommets_visites, aretes_dispo, aretes) :
    for a in aretes_dispo :
        if (a['S1'] in sommets_visites) and (a['S2'] in sommets_visites) :
            aretes_dispo.remove(a)
    for a in aretes :
        if (a['S1'] in sommets_visites) and (a['S2'] in sommets_visites) :
            aretes.remove(a)

