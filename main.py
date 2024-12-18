from Algorithmes.Bellman import Graph
from Algorithmes import isConnexe, parser, prim, affichage_prim, affichage_graphe
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MapWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Projet Metro')
        self.geometry('800x600')
        self.attributes('-fullscreen', True)

        # Charger les données du graphe pour appliquer l'algo de Bellmann
        self.bellman=Graph()
        if self.bellman.charger_fichier("src/metro.txt"):
            print("Chargement des données de métro terminé.")

        # Charger le graphe
        parsed=parser.parse_metro()
        self.sommets=parsed[0]
        self.arretes=parsed[1]
        self.chem=tk.Label(self, text="")
        self.gares=parser.getListeGares(self.sommets)
        self.positions=parser.parse_position(self.sommets)
        self.NomNumsommet=parser.NomNumsommet(self.sommets)
        self.NumNomsommet=parser.NumNomsommet(self.sommets)
        self.depArr=True
        # Layout principal
        self.layout_widgets()

    def layout_widgets(self):
        # Selecteur de bouton
        top_frame=tk.Frame(self)
        top_frame.pack(pady=10)


        self.style = ttk.Style()
        self.style.configure('TCombobox', foreground='black') # COULEUR TEXTE EN NOIR

        stations_uniques=list(set(self.gares))
        self.selector1=ttk.Combobox(top_frame, values=["Choisir la gare de départ"] + stations_uniques)
        self.selector2=ttk.Combobox(top_frame, values=["Choisir la gare d'arrivée"] + stations_uniques)
        self.selector1.set("Choisir la gare de départ")
        self.selector2.set("Choisir la gare d'arrivée")
        self.selector1.pack(side=tk.LEFT, padx=5)
        self.selector2.pack(side=tk.LEFT, padx=5)

        # Boutons
        self.go_button=tk.Button(top_frame, text='GO', command=self.go)
        self.go_button.pack(side=tk.LEFT, padx=5)
        self.prim_btn=tk.Button(top_frame, text='AFFICHER L\'ACPM SUR LA CARTE', command=self.affiche_prim)
        self.prim_btn.pack(side=tk.LEFT, padx=5)
        self.prim_btn=tk.Button(top_frame, text='AFFICHER L\'ACPM', command=affichage_prim.afficher_graphe)
        self.prim_btn.pack(side=tk.LEFT, padx=5)
        self.prim_btn=tk.Button(top_frame, text='AFFICHER LE GRAPHE', command=affichage_graphe.afficher_graphe)
        self.prim_btn.pack(side=tk.LEFT, padx=5)

        # Étiquette pour la onnexité
        self.conn=tk.Label(self, text=isConnexe.main())
        self.conn.pack(pady=10)

        # Affichage de la carte
        self.display_static_map()

    def display_static_map(self):
        # Charger l'image originale On doit faire une remise a l'échelle
        self.image=Image.open("src/metrof_r.png")
        width, height=self.image.size

        # Redimens l'image
        self.image=self.image.resize((987-100, 987-100-15), Image.LANCZOS)
        w, h=self.image.size

        # remise a l'échelle
        self.scale_x=w / width
        self.scale_y=h / height

        self.image_tk=ImageTk.PhotoImage(self.image)

        self.canvas=tk.Canvas(self, width=w, height=h)
        self.canvas.pack()
        self.canvas_image=self.canvas.create_image(0, 0, anchor='nw', image=self.image_tk)
        self.canvas.bind("<Button-1>", self.getstationProche)

    def getstationProche(self, event):
        x=event.x / self.scale_x
        y=event.y / self.scale_y
        res=None
        dist=float('inf')
        for sommet in self.positions:
            lat=self.positions[sommet]["LAT"]
            long=self.positions[sommet]["LONG"]
            current_dist=((lat - x)**2 + (long - y)**2)**0.5
            if current_dist < dist:
                dist=current_dist
                res=sommet
        if self.depArr:
            self.selector1.set(self.NumNomsommet[res])
        else:
            self.selector2.set(self.NumNomsommet[res])
        self.depArr=not self.depArr



    # Pour trouver et afficher les meilleurs chemin avec prim
    def affiche_prim(self):
        parsed=parser.parse_metro()
        self.sommets=parsed[0]
        self.arretes=parsed[1]
        resultat=prim.prim_algo(self.sommets, self.arretes)
        for arrete in resultat:
            try:
                x1, y1=self.positions[arrete["S1"]]["LAT"], self.positions[arrete["S1"]]["LONG"]
                x2, y2=self.positions[arrete["S2"]]["LAT"], self.positions[arrete["S2"]]["LONG"]
                # Ajuster les coordonnées en fonction du redimensionnement
                x1_old=x1*self.scale_x
                y1_old=y1*self.scale_y
                x2_old=x2*self.scale_x
                y2_old=y2*self.scale_y
                self.canvas.create_line(x1_old, y1_old, x2_old, y2_old, fill="red", width=3, tags="prim")
            except :
                pass

    # Pour trouver et afficher le chemin bellman
    def go(self):
        # Effacer les anciennes lignes avant de tracer le nouveau chemin
        self.canvas.delete('chem')
        self.canvas.delete('prim')
        self.chem.destroy()
        ##

        depart=self.selector1.get()
        destination=self.selector2.get()
        resultat=self.bellman.itineraire_pcc(depart, destination)
        previous_numSommet=None
        t=0
        for step in resultat:
            if (t>0): # Sinon on relie le départ et l'arrivé
                numSommet=step.get('numSommet')
                if numSommet is None:
                    station_=step.get('station')
                    if station_ and station_ in self.NomNumsommet:
                        numSommet=self.NomNumsommet[station_]

                if (numSommet is not None):
                        x, y=self.positions[numSommet]["LAT"], self.positions[numSommet]["LONG"]
                        # Ajuster les coordonnées en fonction du redimensionnement
                        x_old=x*self.scale_x
                        y_old=y*self.scale_y
                        if previous_numSommet is not None:
                            x_prev, y_prev=self.positions[previous_numSommet]["LAT"], self.positions[previous_numSommet]["LONG"]
                            x_prev_old=x_prev*self.scale_x
                            y_prev_old=y_prev*self.scale_y
                            self.canvas.create_line(x_prev_old, y_prev_old, x_old, y_old, fill="blue", width=3, tags='chem')
                        previous_numSommet=numSommet
            t+=1
        res=""
        for etape in resultat:
            action=etape.get('action', '')
            res+=action+" "
        self.chem=tk.Label(self, text=res)
        self.chem.place(relx=0.0, y=35, anchor='nw')
        print("MEILLEUR CHEMIN : ")
        print(res)


# Exécution de l'application
if __name__ == '__main__':
    app=MapWindow()
    app.mainloop()
