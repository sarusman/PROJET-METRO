import pandas as pd

data_metro="src/metro.txt"
data_position="src/pospoints.txt"

sommets=[]
arrete=[]

position={} #{"STATION": {"LAT": 14, "LONG": 43}}

def parse_metro():
	with open(data_metro, 'r') as f:
		for _ in range(13):
			next(f) # Pour sauter la consigne
		for l in f:
			if (l[0]=='V'):
				g=l.split(';')
				if (g[2].split(" ")[1]==""):
					ctc={"NS":int(g[0].split(" ")[1]), "nomSommet":" ".join(g[0].split(" ")[2:]), "numLigne":g[1], "IsTerminus":g[2].split(" ")[0], "dir":g[2].split(" ")[2][0]}
				else:
					ctc={"NS":int(g[0].split(" ")[1]), "nomSommet":" ".join(g[0].split(" ")[2:]), "numLigne":g[1], "IsTerminus":g[2].split(" ")[0], "dir":g[2].split(" ")[1][0]}
				sommets.append(ctc)
				#{"NS":entier, "nomSommet":str, "numLigne":str, "NbBranchement":entier, "dir":entier}
				#V 0017 Bastille ;5 ;False 

			elif (l[0]=='E'):
				g=l.split(' ')
				ctc={"S1": int(g[1]),"S2":int(g[2]), "poid":int(g[3][0:-1])}
				#E 232 348 46
				arrete.append(ctc)
				#ARRETE : {"S1":entier, "S2":entier, "poid":entier}
			print(ctc)

def parse_position():
	with open(data_position, 'r') as f:
		for l in f:
			g=l.split(";")
			position[g[2].replace("@", " ").replace("\n", "")]={"LAT":float(g[0]), "LONG":float(g[1])}

parse_metro()
parse_position()
print(position)
#print(sommets)
