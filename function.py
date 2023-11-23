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
            if not ('A' <= nom[indice] <= 'Z' or 'a' <= nom[indice] <= 'z' or nom[indice] == ' '):
                nom = nom[:indice] + nom[indice + 1:]
        if nom not in tab_nom:
            tab_nom.append(nom)
    return tab_nom


def liste_fichier(repertoire):
    tab_fichier = []
    for fichier in os.listdir(repertoire):
        if fichier.endswith(".txt"):
            tab_fichier.append(fichier)
    return tab_fichier

def minuscule(fichier):
    new_fichier = f"./Cleaned/{fichier}"
    old_fichier = f"./Speeches/{fichier}"
    with open(old_fichier, "r", encoding="utf-8") as old, open(new_fichier, "w", encoding="utf-8") as new:
        for ligne in old:
            for caractere in ligne:
                if 'A' <= caractere <= 'Z':
                    caractere = chr(ord(caractere) + 32)
                new.write(caractere)


def ponctuation(f1):
    tab_espace = [" ", "-", "'"]
    texte = ""
    fichier = f"./Cleaned/{f1}"
    with open(fichier, "r", encoding="utf-8") as fichier_1:
        for ligne in fichier_1:
            for element in ligne:
                if (0 <= ord(element) < ord('a')) or (ord('z') < ord(element) <= 127):

                    if element in tab_espace:

                        if texte[-1] != " " and texte[-1] != '' and texte[-1] != '\n':
                            texte += " "
                else:
                    texte += element
            texte += "\n"

    with open(fichier, 'w', encoding="utf-8") as fichier_1:
        for caractere in texte:
            fichier_1.write(caractere)


def tf(f):
    fichier = f"./Cleaned/{f}"
    dico = {}
    with open(fichier, "r", encoding="utf-8") as f1:
        for ligne in f1:
            tab_mot = ligne.split(" ")
            for mot in tab_mot:
                if mot[-1] == "\n":
                    mot = mot[:-1]
                if mot in dico.keys():
                    dico[mot] += 1
                else:
                    dico[mot] = 1
        return dico


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


def idf(repertoire):
    dictionnaire = {}
    tab_fichier = liste_fichier(repertoire)
    for i in range(len(tab_fichier)):
        with open(repertoire + "./" + tab_fichier[i], "r", encoding="utf-8") as f1:
            for ligne in f1:
                tab_mot = ligne.split(" ")
                for mot in tab_mot:
                    if mot[-1] == "\n":
                        mot = mot[:-1]
                    if mot not in dictionnaire.keys():
                        somme = 0
                        for f in range(i, len(tab_fichier)):
                            if est_present(tab_fichier[f], mot):
                                somme += 1
                        dictionnaire[mot] = math.log(somme)
    return dictionnaire



def transformation_fichier(repertoire):
    if not os.path.exists("Cleaned"):
        os.makedirs("Cleaned")
    tab_fichier = liste_fichier(repertoire)
    for fichier in tab_fichier:
        if fichier.endswith(".txt"):
            minuscule(fichier)
            ponctuation(fichier)


def creation_tf_idf(repertoire):
    tab_fichier = liste_fichier(repertoire)
    dico_idf = idf(repertoire)
    nb_ligne = len(dico_idf)
    nb_colonne = len(tab_fichier)
    matrice = [[0 for _ in range(nb_colonne)] for _ in range(nb_ligne)]
    cle = []
    for valeur in dico_idf.keys():
        cle.append(valeur)
    for colonne in range(nb_colonne):
        dico_tf = tf(tab_fichier[colonne])
        for element in dico_tf.keys():
            ligne = indice_tab(cle, element)
            if ligne != -1:
                matrice[ligne][colonne] = dico_tf[element] * dico_idf[element]
    return matrice

def correspondance_mot(dico):
    cle = []
    for valeur in dico.keys():
        cle.append(valeur)
    return cle


def indice_tab(tab, element):
    for indice in range(len(tab)):
        if tab[indice] == element:
            return indice
    return -1

def moins_important(matrice,correspondance_mot):
    liste_moins_important = []
    for indice_ligne in range(len(matrice)):
        i = 0
        ligne = matrice[indice_ligne]
        while ligne[i] == 0 and i<len(ligne)-1:
            i+=1
        if i == len(ligne)-1:
            liste_moins_important.append(correspondance_mot[indice_ligne])
    return liste_moins_important

def plus_élevé(matrice,correspondance_mot):
    liste_plus_important = []
    max = matrice[0][0]
    for indice_ligne in matrice:
        for score in indice_ligne:
        if i == len(ligne) - 1:
            liste_moins_important.append(correspondance_mot[indice_ligne])
    return liste_plus_important







