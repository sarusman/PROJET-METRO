import main

#listes
sommets = [] 
arretes = []
sommets_visites = []
arbre_couvrant = []
#remplissage des listes
main.parse_metro(sommets, arretes)

# Algorithme de Prim
def prim_algo(sommets, arretes, arbre_couvrant, sommets_visites) :

    nouveaux_sommets_decouverts = [] # les nouveaux sommets decouverts a chaque iteration
    arretes_disponible = [] # les arretes disponlible

    nouveaux_sommets_decouverts.append(sommets[0]['numSommet']) # partir du premier sommet de la liste

    while (len(sommets_visites) != len(sommets)) :

        remplissage_arretes_dispo(nouveaux_sommets_decouverts, arretes_disponible, arretes, sommets_visites) # avoir les arretes disponible selon les nouveaux sommets decouvert
        verif_arretes_dispo(sommets_visites, arretes_disponible) # verifie si les arretes disponible qont toujours disponible
        arrete_minimum = minimum(arretes_disponible) # prendre l'indice le l'arrete la plus petite
        
        if(arrete_minimum == -1) :
            print("aucune arrete disponible")
            break

        arbre_couvrant.append(arrete_minimum) # ajouter l'arrete la plus petite à l'arbre couvrant
        if(arrete_minimum['S1'] in sommets_visites) :
            nouveaux_sommets_decouverts.append(arrete_minimum['S2'])
        else :
            nouveaux_sommets_decouverts.append(arrete_minimum['S1'])
        arretes_disponible.remove(arrete_minimum)
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

    for i in range (1,len(arretes_dispo) ) :
        if(arretes_dispo[i]['poid']<a_min) :
            a_min = arretes_dispo[i]['poid']
            indice = i
    return arretes_dispo[indice]


#fonction qui donne les arretes disponible selon les nouveaux sommets decouverts
def remplissage_arretes_dispo(nouveaux_sommets_decouverts, arretes_disponible, arretes, sommets_visites) :
    for s in nouveaux_sommets_decouverts :
        for a in arretes :
            if(a not in arretes_disponible) :
                if(a['S1'] == s and a['S2'] not in sommets_visites) or (a['S2'] == s and a['S1'] not in sommets_visites) :
                    arretes_disponible.append(a)
                    arretes.remove(a)
        sommets_visites.append(s)
        nouveaux_sommets_decouverts.remove(s)

# fonction qui permet de verifier si les 2 sommmets d'une arrete disponible est deja visites
def verif_arretes_dispo(sommets_visites, arretes_dispo) :
    for a in arretes_dispo :
        if (a['S1'] in sommets_visites and a['S2'] in sommets_visites) :
            arretes_dispo.remove(a)

