import parser, prim
from Bellman import Graph
import isConnexe

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MapWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Map Application')
        self.geometry('800x600')
        
        # Charger les données du graphe
        self.bellman=Graph()
        if self.bellman.charger_fichier("src/metro.txt"):
            print("Chargement des données de métro terminé.")

        # Charger le graphe
        parsed=parser.parse_metro()
        self.sommets=parsed[0]
        self.arretes=parsed[1]
        self.chem = tk.Label(self, text="")
        self.gares=parser.getListeGares(self.sommets)
        self.positions=parser.parse_position(self.sommets)

        # Layout principal
        self.layout_widgets()

    def layout_widgets(self):
        # Layout supérieur pour les sélecteurs et les boutons
        top_frame=tk.Frame(self)
        top_frame.pack(pady=10)

        # Selecteurs de gare (ComboBox)
        self.selector1=ttk.Combobox(top_frame, values=["Choisir la gare de départ"] + self.gares)
        self.selector2=ttk.Combobox(top_frame, values=["Choisir la gare d'arrivée"] + self.gares)
        self.selector1.set("Choisir la gare de départ")
        self.selector2.set("Choisir la gare d'arrivée")
        self.selector1.pack(side=tk.LEFT, padx=5)
        self.selector2.pack(side=tk.LEFT, padx=5)

        # Boutons
        self.go_button=tk.Button(top_frame, text='GO', command=self.go)
        self.go_button.pack(side=tk.LEFT, padx=5)
        self.prim_btn=tk.Button(top_frame, text='AFFICHER l\'ACPM SUR LA CARTE', command=self.affiche_prim)
        self.prim_btn.pack(side=tk.LEFT, padx=5)
        self.prim_btn=tk.Button(top_frame, text='AFFICHER PRIM', command=self.affiche_prim)
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
                x1_scaled=x1*self.scale_x
                y1_scaled=y1*self.scale_y
                x2_scaled=x2*self.scale_x
                y2_scaled=y2*self.scale_y
                self.canvas.create_line(x1_scaled, y1_scaled, x2_scaled, y2_scaled, fill="red", width=3, tags="prim")
            except :
                pass
        print(resultat)

    # Pour trouver et afficher le chemin bellman
    def go(self):
        # Effacer les anciennes lignes avant de tracer le nouveau chemin
        self.canvas.delete('chem')
        self.canvas.delete('prim')
        self.chem.destroy()
        depart=self.selector1.get()
        destination=self.selector2.get()
        resultat=self.bellman.itineraire_pcc(depart, destination)
        previous_numSommet=None
        for step in resultat:
            numSommet=step.get('numSommet')
            if numSommet is not None:
                x, y=self.positions[numSommet]["LAT"], self.positions[numSommet]["LONG"]
                # Ajuster les coordonnées en fonction du redimensionnement
                x_scaled=x*self.scale_x
                y_scaled=y*self.scale_y
                if previous_numSommet is not None:
                    x_prev, y_prev=self.positions[previous_numSommet]["LAT"], self.positions[previous_numSommet]["LONG"]
                    x_prev_scaled=x_prev*self.scale_x
                    y_prev_scaled=y_prev*self.scale_y
                    self.canvas.create_line(x_prev_scaled, y_prev_scaled, x_scaled, y_scaled, fill="blue", width=3, tags='chem')
                previous_numSommet=numSommet
        res=""
        for etape in resultat:
            action = etape.get('action', '')
            res+=action+" "
        self.chem = tk.Label(self, text=res)
        self.chem.place(relx=0.0, y=35, anchor='nw')
        print(res)
        print(depart, destination)

# Exécution de l'application
if __name__ == '__main__':
    app=MapWindow()
    app.mainloop()
