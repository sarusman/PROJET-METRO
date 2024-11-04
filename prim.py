# Algorithme de Prim
def prim_algo(sommets, arretes, arbre_couvrant) :
    sommets_visites = []
    arretes_disponible = [] # les arretes disponlible
    sommets_visites.append(sommets[0]['numSommet']) # partir du premier sommet de la liste
    a=0
    while (len(sommets) > len(sommets_visites)) :
        remplissage_arretes_dispo(sommets_visites[len(sommets_visites)-1], arretes_disponible, arretes, sommets_visites) # avoir les arretes disponible selon les nouveaux sommets decouvert
        arrete_minimum = minimum(arretes_disponible) # prendre l'indice le l'arrete la plus petite
        
        if(arrete_minimum == -1) :
            print("aucune arrete disponible")
            break

        arbre_couvrant.append(arrete_minimum) # ajouter l'arrete la plus petite à l'arbre couvrant
        if(arrete_minimum['S1'] in sommets_visites) :
            sommets_visites.append(arrete_minimum['S2'])
        elif(arrete_minimum['S2'] in sommets_visites) :
            sommets_visites.append(arrete_minimum['S1'])
        arretes_disponible.remove(arrete_minimum)
        verif_arretes_dispo(sommets_visites, arretes_disponible, arretes) # verifie si les arretes disponible sont toujours disponible
        a=a+1

    print("nombre de sommets visites : ",len(sommets_visites)) # 376 sommmets en tout
    print("nombre d'arretes de l'ACPM : ",len(arbre_couvrant))
    print("nombre de doublons de sommets visites: ",len(sommets_visites) - len(set(sommets_visites)))

            
# donne l'arrete avec le poinds le plus faible
def minimum(arretes_dispo) :
    if len(arretes_dispo)==0 :
        print ("arretes vide")
        return -1

    a_min = arretes_dispo[0]['poid']
    indice = 0

    for i in range (1,len(arretes_dispo)) :
        if(arretes_dispo[i]['poid'] < a_min) :
            a_min = arretes_dispo[i]['poid']
            indice = i
    return arretes_dispo[indice]


#fonction qui donne les arretes disponible selon les nouveaux sommets decouverts
def remplissage_arretes_dispo(nouveau_sommet_decouvert, arretes_disponible, arretes, sommets_visites) :
    for a in arretes :
        if a not in arretes_disponible :
            if ((a['S1'] == nouveau_sommet_decouvert) and (a['S2'] not in sommets_visites)) :
                arretes_disponible.append(a)
            if ((a['S2'] == nouveau_sommet_decouvert) and (a['S1'] not in sommets_visites)) :
                arretes_disponible.append(a)

# fonction qui permet de verifier si les 2 sommmets d'une arrete disponible est deja visites
def verif_arretes_dispo(sommets_visites, arretes_dispo, arretes) :
    for a in arretes_dispo :
        if (a['S1'] in sommets_visites) and (a['S2'] in sommets_visites) :
            arretes_dispo.remove(a)
    for a in arretes :
        if (a['S1'] in sommets_visites) and (a['S2'] in sommets_visites) :
            arretes.remove(a)

