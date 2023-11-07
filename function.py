import os

def prenom_president(nom):
    prenom = {"Sarkozy": "Nicolas", "Chirac": "Jacques", "Macron": "Emmanuel", "Giscard d'Estaing": "Valéry",
              "Mitterand": "François"}
    return prenom[nom]

def nom():
    tab_fichier = os.listdir("./Speeches")
    return tab_fichier



