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
        nom = qui_a_ecrit(element)
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
    tab_garder = ["é", "è", "ù", "à", "â", "ô", "ê", "ç"]
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
        if mot in dico.keys():
            dico[mot] += 1
        else:
            dico[mot] = 1
    return dico


def est_present(f, mot_rechercher):
    """Cette fonction nous indique si un mot est présent ou non dans un fichier.
    Entrée : f est le fichier où l'on veut recherche le mot,
             mot_rechercher est le mot qui est recherché dans le fichier.
             f : .txt , mot_rechercher : str
    Sortie : True si le mot_rechercher est dans le fichier f et False si le mot_rechercher n'est pas dans le fichier """
    fichier = f"./Cleaned/{f}"
    with open(fichier, "r", encoding="utf-8") as f1:
        for ligne in f1:
            # création d'un tableau à partir de la séparation d'un texte où chaque valeur est un mot
            tab_mot = ligne.split(" ")
            for mot in tab_mot:
                if mot[-1] == "\n":
                    mot = mot[:-1]
                if mot == mot_rechercher:
                    return True
        return False


def maxi_dico(dico):
    maxi = -float('inf')
    cle_max = ''
    for cle in dico.keys():
        if maxi <= dico[cle]:
            cle_max = cle
            maxi = dico[cle_max]
    return [cle_max, maxi]


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
                        dictionnaire[mot] = math.log(len(tab_fichier)/somme)
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
    matrice = [[0.0 for _ in range(nb_colonne)] for _ in range(nb_ligne)]
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

  
def moins_important(matrice, correspondance_ligne):
    liste_moins_important = []
    for indice_ligne in range(len(matrice)):
        i = 0
        ligne = matrice[indice_ligne]
        while ligne[i] == 0 and i < len(ligne)-1:
            i += 1
        if i == len(ligne)-1:
            liste_moins_important.append(correspondance_ligne[indice_ligne])
    return liste_moins_important


def plus_eleve(matrice, correspondance_ligne):
    liste_plus_important = []
    maximum = -float('inf')
    for indice_ligne in range(len(matrice)):
        for score in range(len(matrice[indice_ligne])):
            if matrice[indice_ligne][score] == maximum:
                liste_plus_important.append(correspondance_ligne[indice_ligne])
            elif matrice[indice_ligne][score] > maximum:
                liste_plus_important = [correspondance_ligne[indice_ligne]]
                maximum = matrice[indice_ligne][score]
    return liste_plus_important


def recuperation_texte(fichier):
    texte = ""
    path = f"./Cleaned/{fichier}"
    with open(path, "r", encoding="utf-8") as f1:
        for ligne in f1:
            if ligne[-1] == "\n":
                ligne = ligne[:len(ligne)-1] + " "
            texte = texte + ligne
    return texte


def fichier_discours(repertoire, president):
    liste_discours = []
    for discours in liste_fichier(repertoire):
        if president in discours:
            liste_discours.append(discours)
    return liste_discours


def repete_president(repertoire, president):
    liste_discours = fichier_discours(repertoire, president)
    texte_total = ""
    for fichier in liste_discours:
        texte = recuperation_texte(fichier)
        texte_total += texte
    dico_occurence = tf(texte_total)
    return maxi_dico(dico_occurence)[0]


def qui_a_ecrit(fichier):
    tab_temp = fichier.split("_")
    tab_temp = tab_temp[1].split(".")
    nom = tab_temp[0]
    for indice in range(len(nom))[::-1]:
        if not ('A' <= nom[indice] <= 'Z' or 'a' <= nom[indice] <= 'z' or nom[indice] == ' '):
            nom = nom[:indice] + nom[indice + 1:]
    return nom


def a_parler(repertoire, mot):
    dico_parler = {}
    tab_fichier = liste_fichier(repertoire)
    tab_parler = []
    maximum = 0
    a_le_plus_parler = []
    for fichier in tab_fichier:
        texte = recuperation_texte(fichier)
        dico_tf = tf(texte)
        if mot in dico_tf.keys():
            auteur = qui_a_ecrit(fichier)
            if auteur not in dico_parler.keys():
                dico_parler[auteur] = dico_tf[mot]
            else:
                dico_parler[auteur] += dico_tf[mot]
    for cle in dico_parler.keys():
        tab_parler.append(cle)
        if dico_parler[cle] > maximum:
            maximum = dico_parler[cle]
            a_le_plus_parler = [cle]
        elif dico_parler[cle] == maximum:
            a_le_plus_parler.append(cle)
    return [a_le_plus_parler, tab_parler]


def plus_petit_dico(liste):
    mini = float('inf')
    dico_mini = {}
    for dico in liste:
        if len(dico) < mini:
            mini = len(dico)
            dico_mini = dico
    return dico_mini


def mot_evoque_par_tous(repertoire, liste_moins_importante):
    liste_president = nom_president()
    liste_dico = []
    mot_finaux = []
    cle_petit_dico = []
    for nom in liste_president:
        liste_discours = fichier_discours(repertoire, nom)
        texte_total = ""
        for fichier in liste_discours:
            texte = recuperation_texte(fichier)
            texte_total += texte
        dico_president = tf(texte_total)
        liste_dico.append(dico_president)
    petit_dico = plus_petit_dico(liste_dico)
    for element in petit_dico.keys():
        if element not in liste_moins_importante and element != '':
            cle_petit_dico.append(element)
    for cle in cle_petit_dico:
        if len(a_parler(repertoire, cle)[1]) == len(liste_president):
            mot_finaux.append(cle)
    return mot_finaux


def premiere_occurence(fichier, mot_recherche):
    texte = recuperation_texte(fichier)
    tab_texte = texte.split(" ")
    for indice_mot in range(len(tab_texte)):
        if tab_texte[indice_mot] == mot_recherche:
            return indice_mot
    return -1


def premier_a_parler(repertoire, mot):
    tab_fichier = liste_fichier(repertoire)
    premier = ''
    indice_premier = float("inf")
    for fichier in tab_fichier:
        if est_present(fichier, mot):
            emplacement = premiere_occurence(fichier, mot)
            if emplacement < indice_premier:
                indice_premier = emplacement
                premier = qui_a_ecrit(fichier)
    if premier == '':
        return "Ce mot n'est présent dans aucun texte"
    else:
        return premier
