from . import parser

# {'S1': 243, 'S2': 244, 'poid': 240}
# {'numSommet': 339, 'nomSommet': 'Stalingrad', 'numLigne': '2 ', 'isTerminus': 'False', 'direction': '0'}

# Il suffit de faire un parcours en profondeur

def getListeSommet(sommets):
	res=[]
	for i in sommets:
		res.append(i["numSommet"])
	return res

# Construisons d'abord la structure nécéssaire pour réaliser cela
def createGraph(listSommets, arretes):
	finalStruct={} # { S1 : [S2, S3...], S2 : [S3, S1...]...}
	##init de la structure
	for sommet in listSommets:
		finalStruct[sommet]=[]
	for sommet in (listSommets):
		for arrete in arretes:
			if (arrete["S2"] not in finalStruct[arrete["S1"]]):
				finalStruct[arrete["S1"]].append(arrete["S2"])
			if (arrete["S1"] not in finalStruct[arrete["S2"]]):
				finalStruct[arrete["S2"]].append(arrete["S1"])
	return finalStruct

# Algo de test de connxité : parcours en profondeur; Pour tester s'il est connexe, on lance le DFS depuis 
# le premier sommet et on doit s'attendre a obtenir tout les sommets dans le résultat


# retoune les sommets visités depuis un sommet
def parcoursProfondeur(graphe, depart):
	pile=[depart]
	visiter=[]
	while pile:
		s=pile.pop()
		for i in graphe[s]:
			if (i not in visiter):
				pile.append(i)
		if (s not in visiter):
			visiter.append(s)
	return visiter

# verifie si tout les sommets sont dans le résultat : si oui, alors il n'y qu'une seul composante connexe (donc graphe connexe)
# Si non, le graphe n'est pas connexe
def check(sommets, resultat):
	return sorted(sommets)==sorted(resultat)


def main():
	res=parser.parse_metro()
	sommets=getListeSommet(res[0])
	graphe=createGraph(sommets, res[1])
	res=parcoursProfondeur(graphe, 0)
	if (check(sommets, res)):
		return ("Le graphe est connexe")
	else:
		return ("Le graphe n'est pas connexe")

























