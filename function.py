import os


def prenom_president(nom):
    prenom = {"Sarkozy": "Nicolas", "Chirac": "Jacques", "Macron": "Emmanuel", "Giscard dEstaing": "Valéry",
              "Mitterand": "François"}
    return prenom[nom]


def nom_president():
    tab_nom = []
    tab_fichier = os.listdir("./Speeches")
    for element in tab_fichier:
        tab_temp = element.split("_")
        tab_temp = tab_temp[1].split(".")
        nom = tab_temp[0]
        for indice in range(len(nom))[::-1]:
            if not (65 <= ord(nom[indice]) <= 90 or 97 <= ord(nom[indice]) <= 122 or ord(nom[indice]) == 20):
                nom = nom[:indice] + nom[indice + 1:]
        tab_nom.append(nom)
    return tab_nom


def idf(repertoire):
    dictionnaire = {}
    for fichier in repertoire:
        for mot in fichier:
            if mot in dico.keys:

            else:
                dictionnaire[mot] = 1