import pandas as pd

data_metro="src/metro.txt" #fichier avec les donnees des sommets et des arretes
data_position="src/pospoints.txt" #fichier avec les positions

#Structure utiliser pour les sommets : {"NS":entier, "nomSommet":str, "numLigne":str, "NbBranchement":entier, "dir":entier}
#Structure utiliser pour les arretes : {"S1":entier, "S2":entier, "poid":entier}
#Structure utiliser pour les positions : {"STATION": {"LAT": 14, "LONG": 43}}


def parse_metro(sommets, arretes):
	with open(data_metro, 'r') as f: # ouverture du fichier metro.txt
		for _ in range(13): #sauter les lignes avec les consignes
			next(f) 
		for l in f: # pour chaque ligne
			if (l[0]=='V'): # si la ligne commance par un V
				g=l.split(';') # separer la ligne par les ';'
				if (g[2].split(" ")[1]==""):
					ctc={"NS":int(g[0].split(" ")[1]), "nomSommet":"".join(g[0].split(" ")[2:]), "numLigne":g[1], "IsTerminus":g[2].split(" ")[0], "dir":g[2].split(" ")[2][0]}
				else:
					ctc={"NS":int(g[0].split(" ")[1]), "nomSommet":"".join(g[0].split(" ")[2:]), "numLigne":g[1], "IsTerminus":g[2].split(" ")[0], "dir":g[2].split(" ")[1][0]}
					sommets.append(ctc) # ajouter le sommet a la liste

			elif (l[0]=='E'):  # si la ligne commance par un E
				g=l.split(' ') # separer la ligne par les ' '
				ctc={"S1": int(g[1]),"S2":int(g[2]), "poid":int(g[3][0:-1])}
				arretes.append(ctc) # ajouter l'arrete a la liste
			print(ctc)

def parse_position(positions):
	with open(data_position, 'r') as f: #ouverture du fichier pospoints.txt
		for l in f: 
			g=l.split(";")
			station_name = g[2].replace("@", " ").replace("\n", "")
			positions[station_name] = {"LAT": float(g[0]), "LONG": float(g[1])}
			print(station_name + " : " + str({"LAT": float(g[0]), "LONG": float(g[1])}))


