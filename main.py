import pandas as pd

data="src/metro.txt"

sommets=[]
arrete=[]
def main():
	with open(data, 'r') as f:
		for _ in range(14):
			next(f) # Pour sauter la consigne
		for l in f:
			if (l[0]=='V'):
				g=l.split(';')
				ctc={"NS":int(g[0].split(" ")[1]), "nomSommet":g[0].split(" ")[1:], "numLigne":g[1], "IsTerminus":g[2].split(" ")[0], "dir":g[2].split(" ")[1]}
				print(ctc)
				sommets.append(ctc)
				#{"NS":entier, "nomSommet":str, "numLigne":str, "NbBranchement":entier, "dir":entier}

print(sommets)
#V 0017 Bastille ;5 ;False 0
			


main()
