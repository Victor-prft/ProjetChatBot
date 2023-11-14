import os
import math

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
    with open(old_fichier, "r", encoding="utf-8") as old, open(new_fichier, "w", encoding="utf-8") as new:
        for ligne in old:
            for caractere in ligne:
                if 65 <= ord(caractere) <= 90:
                    caractere = chr(ord(caractere) + 32)
                new.write(caractere)


def ponctuation(f1):
    tab_a_garder = ["é", "à", "è", "ù", "ê", "ç"]
    tab_espace = [" ", "-", "'"]
    texte = u""
    fichier = f"./Cleaned/{f1}"
    with open(fichier, "r", encoding="utf-8") as fichier_1:
        for ligne in fichier_1:
            for element in ligne:
                if (0 <= ord(element) < 97) or (122 < ord(element) <= 127):
                    if element in tab_espace:
                        if texte[-1] != " " and texte[-1] != '' and texte[-1] != '\n':
                            texte += " "
                else:
                    texte += element
            texte += "\n"

    with open(fichier, 'w', encoding="utf-8") as fichier_1:
        for caractere in texte:
            fichier_1.write(caractere)



def est_present(f, mot_rechercher):
    fichier = f"./Cleaned/{f}"
    with open(fichier, "r", encoding="utf-8") as f1:
        for ligne in f1:
            tab_mot = ligne.split(" ")
            for mot in tab_mot:
                if mot[-1] == "\n":
                    mot = mot[:-1]
                if mot == mot_rechercher:
                    return True
        return False

def list_of_files(directory):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            files_names.append(filename)
    return

def idf(repertoire):
    dictionnaire = {}
    dictionnaire_final = {}
    liste_fichier = []
    for fichier in os.listdir(repertoire):
        if fichier.endswith(".txt"):
            liste_fichier.append(fichier)
    for i in range (len(liste_fichier)):
        with open(repertoire +"./" + liste_fichier[i], "r", encoding="utf-8") as f1:
            for ligne in f1:
                tab_mot = ligne.split(" ")
                for mot in tab_mot:
                    if mot[-1] == "\n":
                        mot = mot[:-1]
                    if mot not in dictionnaire.keys():
                        somme = 0
                        for f in range(i,len(liste_fichier)):
                            if est_present(liste_fichier[f], mot) == True:
                                somme+=1
                        dictionnaire[mot] = math.log(1/somme)
    return dictionnaire


def moins_important(repertoire):
    dico = idf(repertoire)
    liste_mot_moins_important = []
    for i in dico.keys():
        if dico[i] == 0:
            liste_mot_moins_important.append(i)
    return liste_mot_moins_important

print(moins_important("./Cleaned"))

