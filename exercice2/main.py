from utils.graph import Graph



def main():

    # Chargement des données de métro

    graph = Graph()

    if graph.charger_fichier("data/metro.txt"):

        print("Chargement des données de métro terminé.")

    else:

        return



    print("Bienvenue dans le Calculateur de Route du Métro de Paris !")

    print("Instructions :")

    print("1. Entrez le nom exact de la station de départ.")

    print("2. Entrez le nom exact de la station de destination.")

    print("3. Le programme calculera l'itinéraire avec le temps de trajet le plus court.")

    print("------------------------------------------------------------")



    # Saisie des stations de départ et de destination par nom

    depart = input("Entrez le nom de la station de départ : ")

    destination = input("Entrez le nom de la station de destination : ")



    # Calcul du trajet le plus court

    path = graph.itineraire_pcc(depart, destination)

    if path:

        print(path)

    else:

        print("Itinéraire introuvable entre les deux stations spécifiées.")



if __name__ == "__main__":

    main()


