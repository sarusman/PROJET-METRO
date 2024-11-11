data_metro="src/metro.txt" #fichier avec les donnees des sommets et des arretes
data_position="src/pospoints.txt" #fichier avec les positions

#Structure utiliser pour les sommets : {"NS":entier, "nomSommet":str, "numLigne":str, "NbBranchement":entier, "dir":entier}
#Structure utiliser pour les arretes : {"S1":entier, "S2":entier, "poid":entier}
#Structure utiliser pour les positions : {"STATION": {"LAT": 14, "LONG": 43}}


def parse_metro():
	sommets=[]
	arretes=[]
	with open(data_metro, 'r') as f:  # ouverture du fichier metro.txt
    # Ignorer les 13 premières lignes
		for _ in range(13):
			next(f)

		# Parcourir le fichier
		for l in f:
			l = l.strip()  # Enlever les espaces et retours a la ligne inutiles
			if l.startswith('V'):  # Si la ligne commence par 'V'
				g = l.split(';')
				dir_info = g[2].split(" ")[2][0] if len(g[2].split(" ")) > 2 else g[2].split(" ")[1][0]
				ctc = {
					"numSommet": int(g[0].split()[1]), 
					"nomSommet": " ".join(g[0].split()[2:]), 
					"numLigne": g[1].strip(), 
					"isTerminus": g[2].split()[0], 
					"direction": dir_info
				}
				sommets.append(ctc)  # Ajouter le sommet a la liste

			elif l.startswith('E'):  # Si la ligne commence par 'E'
				g = l.split()
				ctc = {
					"S1": int(g[1]), 
					"S2": int(g[2]), 
					"poids": int(g[3])
				}
				arretes.append(ctc)  # Ajouter l'arrete à la liste
	return [sommets, arretes]

def getListeGares(sommets):
	res=[]
	for i in sommets:
		res.append(i["nomSommet"])
	return res


def parse_position(positions):
	with open(data_position, 'r') as f: #ouverture du fichier pospoints.txt
		for l in f: 
			g=l.split(";")
			station_name = g[2].replace("@", " ").strip()
			ctc={"nomSommet" : "".join(station_name), "LAT" : int(g[0]), "LONG" : int(g[1]) }
			positions.append(ctc)
