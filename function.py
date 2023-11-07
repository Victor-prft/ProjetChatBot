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
            if not (65 <= ord(nom[indice]) <= 90 or 97 <= ord(nom[indice]) <= 122 or ord(nom[indice]) == 32):
                nom = nom[:indice] + nom[indice + 1:]
        if nom not in tab_nom:
            tab_nom.append(nom)
    return tab_nom


def minuscule(fichier):
    new_fichier = f"./Cleaned/{fichier}"
    old_fichier = f"./Speeches/{fichier}"
    with open(old_fichier, "r") as old, open(new_fichier,"w") as new:
        for ligne in old:
            for caractere in ligne:
                if 65 <= ord(caractere) <= 90:
                    caractere = chr(ord(caractere) + 32)
                new.write(caractere)


def ponctuation(f1):
    tab_a_garder = [ord("é"), ord("à"), ord("è"), ord("ù"), ord("ê"), ord("ç")]
    print(tab_a_garder)
    texte = ""
    fichier = f"./Cleaned/{f1}"
    print(tab_a_garder)
    with open(fichier, "r") as fichier_1:
        for ligne in fichier_1:
            for indice in range(len(ligne)):
                if not(97 <= ord(ligne[indice]) <= 122):
                    if ligne[indice] == " " and len(ligne)-1 != indice:
                        if ligne[indice + 1] != " ":
                            texte += " "

                    elif ligne[indice] == "é":
                        print("passage")
                        texte += ligne[indice]
                else:
                    texte += ligne[indice]
            texte += "\n"
        print(texte)


