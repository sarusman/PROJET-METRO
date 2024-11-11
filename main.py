"""
# Exercice 1
isConnexe.main()

# Exercice 2
depart = input("Entrez le nom de la station de départ : ")
destination = input("Entrez le nom de la station de destination : ")
#path = Graph.itineraire_pcc(depart, destination)
"""
# Exercice 3

import parser
from Bellman import Graph
import isConnexe

import sys
import folium
import io
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt


class MapWindow(QMainWindow):
    def __init__(self):
        self.gares=parser.getListeGares(parser.parse_metro()[0])

        super().__init__()
        self.setWindowTitle('Map Application')
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Top layout for buttons and selectors
        self.top_layout = QHBoxLayout()
        self.layout.addLayout(self.top_layout)

        # Selectors (ComboBoxes)
        self.selector1 = QComboBox()
        self.selector2 = QComboBox()
        # Folium map
        self.create_map()

        # Ajout gares
        print(self.gares)
        self.add_gares()

        # Boutons
        self.button1 = QPushButton('GO')
        self.top_layout.addWidget(self.button1)
        self.button2 = QPushButton('AFFICHER PRIM')
        self.top_layout.addWidget(self.button1)
        self.top_layout.addWidget(self.button2)
        self.button1.clicked.connect(self.go)
        self.button2.clicked.connect(self.affiche_prim)

        # est connexe
        self.label_text = QLabel(isConnexe.main())
        self.layout.addWidget(self.label_text)

        # Map display using QWebEngineView
        self.view = QWebEngineView()
        self.view.setHtml(self.data.getvalue().decode())
        self.layout.addWidget(self.view)


    def add_gares(self):
        self.gares.insert(0, "Choisir la gare de départ")
        self.selector1.addItems(self.gares)
        self.gares.pop(0)
        self.gares.insert(0, "Choisir la gare d'arrivé")
        self.selector2.addItems(self.gares)
        self.top_layout.addWidget(self.selector1)
        self.top_layout.addWidget(self.selector2)
        self.gares.pop(0)


    def create_map(self):
        # Create a Folium map
        m = folium.Map(location=[48.8566, 2.3522], zoom_start=13)

        # Save map data to a data object
        self.data = io.BytesIO()
        m.save(self.data, close_file=False)

    def affiche_prim(self):
        pass

    def go(self):
        pass

# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())
