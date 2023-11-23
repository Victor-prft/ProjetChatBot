import os
import math


def prenom_president(nom):
    fichier = "./Ressource/nom_president.txt"
    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            tab = ligne.split("/")
            if tab[0] == nom:
                if tab[1][-1] == "\n":
                    return tab[1][:len(tab[1])-1]
                else:
                    return tab[1]


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
    tab_garder = ["é", "è", "ù", "à", "â", "ô", "ê"]
    texte = ""
    fichier = f"./Cleaned/{f1}"
    l_actuel = 0
    l_possible = ["a", "e"]
    with open(fichier, "r", encoding="utf-8") as fichier_1:
        for ligne in fichier_1:
            for element in ligne:
                if 'a' <= element <= 'z' or element in tab_garder:
                    texte += element
                else:
                    if element in tab_espace:
                        if element == "'":
                            if texte[-1] == 'l':
                                texte = texte + l_possible[l_actuel % 2]
                                l_actuel += 1
                            else:
                                texte = texte + "e"
                        if texte[-1] != " " and texte[-1] != '' and texte[-1] != '\n':
                            texte += " "
            texte += "\n"

    with open(fichier, 'w', encoding="utf-8") as fichier_1:
        for caractere in texte:
            fichier_1.write(caractere)


def tf(texte):
    dico = {}
    tab_mot = texte.split(" ")
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
                        dictionnaire[mot] = math.log(1/somme)
    return dictionnaire
              
              
def moins_important(repertoire):
    dico = idf(repertoire)
    liste_mot_moins_important = []
    for i in dico.keys():
        if dico[i] == 0:
            liste_mot_moins_important.append(i)
    return liste_mot_moins_important


def transformation_fichier(repertoire):
    if not os.path.exists("Cleaned"):
        os.makedirs("Cleaned")
    tab_fichier = liste_fichier(repertoire)
    for fichier in tab_fichier:
        if fichier.endswith(".txt"):
            minuscule(fichier)
            ponctuation(fichier)


def creation_tf_idf():
    tab_fichier = liste_fichier("./Cleaned")
    dico_idf = idf("./Cleaned")
    nb_ligne = len(dico_idf)
    nb_colonne = len(tab_fichier)
    matrice = [[0 for _ in range(nb_colonne)] for _ in range(nb_ligne)]
    cle = []
    for valeur in dico_idf.keys():
        cle.append(valeur)
    for colonne in range(nb_colonne):
        texte = recuperation_texte(tab_fichier[colonne])
        dico_tf = tf(texte)
        for element in dico_tf.keys():
            ligne = indice_tab(cle, element)
            if ligne != -1:
                matrice[ligne][colonne] = dico_tf[element] * dico_idf[element]
    return matrice


def indice_tab(tab, element):
    for indice in range(len(tab)):
        if tab[indice] == element:
            return indice
    return -1


def recuperation_texte(fichier):
    texte = ""
    path = f"./Cleaned/{fichier}"
    with  open(path, "r", encoding="utf-8") as f1:
        for ligne in f1:
            texte = texte + ligne
    return texte


