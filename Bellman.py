import re
import heapq

class Station:
    def __init__(self, num_sommet, nom_sommet, numero_ligne, est_terminus, branchement):
        self.num_sommet = num_sommet
        self.nom_sommet = nom_sommet
        self.numero_ligne = numero_ligne
        self.est_terminus = est_terminus
        self.branchement = branchement
        self.connexions = []

    def __lt__(self, other):
        return self.num_sommet < other.num_sommet

    def __repr__(self):
        return f"{self.nom_sommet} (Ligne {self.numero_ligne})"

class Connexion:
    def __init__(self, station1, station2, temps):
        self.station1 = station1
        self.station2 = station2
        self.temps = temps

    def __repr__(self):
        return f"{self.station1} - {self.station2} ({self.temps} s)"

class Graph:
    def __init__(self):
        self.stations = {}

    def ajouter_station(self, ligne):
        match = re.match(r"V\s+(\d+)\s+(.+?)\s*;\s*(\d+)\s*;\s*(True|False)\s*(\d+)", ligne)
        if match:
            num_sommet = int(match.group(1))
            nom_sommet = match.group(2).strip()
            numero_ligne = int(match.group(3))
            est_terminus = match.group(4) == "True"
            branchement = int(match.group(5))
            station = Station(num_sommet, nom_sommet, numero_ligne, est_terminus, branchement)
            self.stations[num_sommet] = station
            self.stations[nom_sommet.lower()] = station

    def ajouter_connexion(self, ligne):
        match = re.match(r"E\s+(\d+)\s+(\d+)\s+(\d+)", ligne)
        if match:
            num_sommet1 = int(match.group(1))
            num_sommet2 = int(match.group(2))
            temps = int(match.group(3))
            station1 = self.stations.get(num_sommet1)
            station2 = self.stations.get(num_sommet2)
            if station1 and station2:
                station1.connexions.append((station2, temps))
                station2.connexions.append((station1, temps))

    def charger_fichier(self, fichier_chemin):
        try:
            with open(fichier_chemin, "r") as fichier:
                for ligne in fichier:
                    ligne = ligne.strip()
                    if ligne.startswith("V "):
                        self.ajouter_station(ligne)
                    elif ligne.startswith("E "):
                        self.ajouter_connexion(ligne)
            return True
        except FileNotFoundError:
            print(f"Erreur : Le fichier {fichier_chemin} est introuvable.")
            return False

    def trouver_station_par_nom(self, nom):
        """Retourne la station correspondant au nom donné."""
        return self.stations.get(nom.lower())

    def trouver_terminus(self, ligne_numero, station_depart, destination):
        """Trouve le bon terminus dans la direction de la destination en prenant en compte les branches."""
        terminus_stations = [
            station for station in self.stations.values()
            if station.numero_ligne == ligne_numero and station.est_terminus
        ]
        
        if ligne_numero == 7 and "villejuif" in destination.nom_sommet.lower():
            # Forcer le choix de Villejuif - Louis Aragon si la destination est sur la branche de Villejuif
            for terminus in terminus_stations:
                if "louis aragon" in terminus.nom_sommet.lower():
                    return terminus.nom_sommet

        if len(terminus_stations) == 2:
            # Sinon, calculez la distance de chaque terminus à la destination
            dist_terminus1_to_dest = self.calculer_distance(terminus_stations[0], destination)
            dist_terminus2_to_dest = self.calculer_distance(terminus_stations[1], destination)
            
            # Sélectionne le terminus le plus proche de la destination
            return terminus_stations[0].nom_sommet if dist_terminus1_to_dest < dist_terminus2_to_dest else terminus_stations[1].nom_sommet
        elif terminus_stations:
            return terminus_stations[0].nom_sommet
        return None

    def calculer_distance(self, station_a, station_b):
        """Calculer une estimation de la distance (nombre de sauts) entre deux stations."""
        visited = {station: False for station in self.stations.values()}
        queue = [(station_a, 0)]
        while queue:
            current_station, distance = queue.pop(0)
            if current_station == station_b:
                return distance
            for voisin, _ in current_station.connexions:
                if not visited[voisin]:
                    visited[voisin] = True
                    queue.append((voisin, distance + 1))
        return float('inf')


    def itineraire_pcc(self, nom_depart, nom_destination):
        depart = self.trouver_station_par_nom(nom_depart)
        destination = self.trouver_station_par_nom(nom_destination)

        if not depart or not destination:
            return "Station de départ ou de destination introuvable."

        distances = {station: float('inf') for station in self.stations.values()}
        distances[depart] = 0
        precedent = {station: None for station in self.stations.values()}
        queue = [(0, depart)]

        while queue:
            current_dist, current_station = heapq.heappop(queue)
            if current_station == destination:
                break
            for voisin, temps in current_station.connexions:
                alt = current_dist + temps
                if alt < distances[voisin]:
                    distances[voisin] = alt
                    precedent[voisin] = current_station
                    heapq.heappush(queue, (alt, voisin))

        if distances[destination] == float('inf'):
            return "Aucun itinéraire trouvé."

        # Construire l'itinéraire dans l'ordre chronologique
        itineraire = []
        current = destination
        duree_totale = distances[destination]

        # Ajouter la station de départ en premier
        itineraire.append({
            "station": depart.nom_sommet,
            "numSommet": current_station.num_sommet,
            "action": f"Vous êtes à {depart.nom_sommet}."
        })

        # Construire l'itinéraire dans l'ordre correct
        chemin = []
        while current:
            chemin.append(current)
            current = precedent[current]
        chemin.reverse()

        for i in range(len(chemin) - 1):
            current_station = chemin[i]
            next_station = chemin[i + 1]
            if current_station.numero_ligne != next_station.numero_ligne:
                # Changement de ligne avec format modifié
                terminus = self.trouver_terminus(next_station.numero_ligne, next_station, destination)
                itineraire.append({
                    "station": current_station.nom_sommet,
                    "action": f"- À {current_station.nom_sommet}, changez et prenez la ligne {next_station.numero_ligne} direction {terminus}."
                })
            else:
                # Première instruction sur la ligne initiale
                if i == 0:
                    terminus = self.trouver_terminus(current_station.numero_ligne, current_station, destination)
                    itineraire.append({
                        "station": current_station.nom_sommet,
                        "action": f"- Prenez la ligne {current_station.numero_ligne} direction {terminus}.",
                        "numSommet": current_station.num_sommet,
                    })

        # Ajouter la dernière étape (arrivée)
        itineraire.append({
            "station": destination.nom_sommet,
            "numSommet": current_station.num_sommet,
            "action": f"- Vous devriez arriver à {destination.nom_sommet} dans environ {duree_totale // 60} minutes."
        })

        return itineraire


def afficher_itineraire(itineraire):
    output = []
    for etape in itineraire:
        output.append(etape["action"])
    return "\n".join(output)

