import os
import math


def prenom_president(nom: str) -> str:
    """Cette fonction renvoie le prénom d'un président en fonction du nom mis en argument
    Entré: nom: str: nom du président pour lequelle on veut le prénom
    Sortie: un str contenant le prénom du président concerné"""
    #Chemin vers un fichier contenant le nom de tous les présidents associée à leur prénom
    fichier = "./Ressource/nom_president.txt"
    #ouverture du fichier en mode lecture
    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            # Les nom et prénom des présidents sont stocké sous la forme nom/prénom on crée donc un tableau grâce à la
            # fonction split en désignant / comme séparateur
            tab = ligne.split("/")
            # On vérifie si le nom correspond
            if tab[0] == nom:
                # On vérifie qu'il n'y ai pas de retour à la ligne après le prénom associé
                if tab[1][-1] == "\n":
                    return tab[1][:len(tab[1])-1]
                else:
                    return tab[1]


def nom_president(repertoire: str) -> list:
    """Fonction qui prend en argument un repertoire et qui va creer une liste contenant tous les noms des présidents
    en les récupérants à partir des noms des fichiers
    Entré: repertoire: str: chemin vers le dossier contenant les textes
    Sortie: tab: tableau de str: Tableau contenant le nom de tous les présidents ayant écris un discours présent dans le dossier
    """
    tab_nom = []
    # On récupére dans une liste le nom de tout les fichiers contenu dans le répertoire
    tab_fichier = os.listdir(repertoire)
    # On parcourt cette liste
    for element in tab_fichier:
        # On récupére le nom de la personne l'ayant écrit
        nom = qui_a_ecrit(element)
        # On vérifie si on a pas déjà sont nom dans la liste car on ne veut pas de doublon
        if nom not in tab_nom:
            tab_nom.append(nom)
    return tab_nom


def liste_fichier(repertoire):
    """Fonction renvoyant à partir d'un répertoire donné un tableau contenant le nom de chacun des fichiers en .txt
    qu'il contient
    Entré: repertoire: str: chemin du dossier dont on veut extraire les fichiers
    Sortie: tableau de str: tableau contenant le nom de tous les fichiers txt présent dans le repertoire"""
    tab_fichier = []
    # On parcourt les fichiers
    for fichier in os.listdir(repertoire):
        # On ne récupére que les fichiers en .txt
        if fichier.endswith(".txt"):
            tab_fichier.append(fichier)
    return tab_fichier


def minuscule(fichier):
    """Fonction prenant en argument un fichier et va réecrire le contenu du fichier dans un autre en transformant toute
    les majuscules en minscules
    Entré: fichier: str: Nom du fichier à transformer
    Sortie: None"""
    # Chemin des fichiers
    new_fichier = f"./Cleaned/{fichier}"
    old_fichier = f"./Speeches/{fichier}"
    # Ouverture des fichiers
    with open(old_fichier, "r", encoding="utf-8") as old, open(new_fichier, "w", encoding="utf-8") as new:
        for ligne in old:
            # On parcourt les caractères
            for caractere in ligne:
                # Cas où le caractère est une majuscule
                if 'A' <= caractere <= 'Z':
                    # On le transforme en minuscule
                    caractere = chr(ord(caractere) + 32)
                # On écrit le caractère dans le nouveau fichier
                new.write(caractere)


def ponctuation(f1):
    """Fonction prenant en argument un fichier et va réecrire le contenu du fichier et le réecrire sans la ponctuation
    et avec chaque mot séparé par des espaces
    Entré: f1: str: Nom du fichier à transformer
    Sortie: None"""
    # Tableau contenant les caractères à transformer par des espaces
    tab_espace = [" ", "-", "'"]
    # Tableau contenant les caractères or alphabétique à conserver
    tab_garder = ["é", "è", "ù", "à", "â", "ô", "ê", "ç"]
    texte = ""
    # Chemin vers le fichier
    fichier = f"./Cleaned/{f1}"
    # Cas du l' on va alterner entre écrire le et la
    l_actuel = 0
    l_possible = ["a", "e"]
    # Ouverture du fichier
    with open(fichier, "r", encoding="utf-8") as fichier_1:
        for ligne in fichier_1:
            # On parcourt les caractères
            for element in ligne:
                # Cas ou l'on doit conservé le caractères
                if 'a' <= element <= 'z' or element in tab_garder:
                    texte += element
                else:
                    # Cas ou l'on doit potentiellement transformé l'élément en 1 espace
                    if element in tab_espace:
                        # Cas des apostrophe que l'on remplace par des e ou des a
                        if element == "'":
                            if texte[-1] == 'l':
                                texte = texte + l_possible[l_actuel % 2]
                                l_actuel += 1
                            else:
                                texte = texte + "e"
                        # On écrit l'espace unqiuement si il n'est pas précéder par un saut de ligne, un espace ou un
                        # caractere vide
                        if texte[-1] != " " and texte[-1] != '' and texte[-1] != '\n':
                            texte += " "
            # On a fini la ligne on passe donc à la ligne suivante
            texte += "\n"
    #On réouvre le pour réecrire la nouvelle version
    with open(fichier, 'w', encoding="utf-8") as fichier_1:
        for caractere in texte:
            fichier_1.write(caractere)


def tf(texte):
    """ Fonction qui prend en argument le contenu d'un texte et associé un score tf à chacun des mot qu'il contient
    Entré: texte: str: Chaine de caractère correspondant au contenu du texte
    Sortie: dico: dictionnaire: Dictionnaire associant à chaque mot du texte une valeur entiere correspondant à son score tf
    """
    dico = {}
    # On va creer un tableau ou chaque élément est un mot. Cela est permis par le processus de prétraitement des textes
    tab_mot = texte.split(" ")
    # Parcourt les mots
    for mot in tab_mot:
        # Cas ou le mot a déjà été rencontré
        if mot in dico.keys():
            # On rajoute 1 à son score tf
            dico[mot] += 1
        # Cas où c'est la première rencontre
        else:
            # Le score tf du mot est mise à 1
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
    """Fonction permettant d'appeler les fonctions permettant d'effectuer le traitement de tout les fichiers dans un
    répertoire mis en argument
    Entré: repertoire: str: Chaine de caractère contenant le nom du dossier à traiter
    Sortie: None"""
    # On vérifie si le fichier Cleaned est créé
    if not os.path.exists("Cleaned"):
        # Si c'est pas le cas on le Crée
        os.makedirs("Cleaned")
    # On récupére la liste contenant le nom de tout les fichiers
    tab_fichier = liste_fichier(repertoire)
    # On les parcourt
    for fichier in tab_fichier:
        # On appele les fonctions nécessaire au traitement du texte
        minuscule(fichier)
        ponctuation(fichier)


def creation_tf_idf(repertoire):
    """Fonction renvoyant la matrice tf-idf des documents contenu dans un répertoire mis en argument
    Entré: repertoire: str: Nom du dossier où sont contenu les fichiers
    Sortie: matrice: Matrice: Matrice contenant les scores tf_idf des mots contenu dans les fichiers du répertoire."""
    # On récupére le nom des fichiers
    tab_fichier = liste_fichier(repertoire)
    # On récupére le dictionnaire contenant les scores idf des mots du repertoire
    dico_idf = idf(repertoire)
    # On récupere le nombre de ligne et de colonne nécessaire
    nb_ligne = len(dico_idf)
    nb_colonne = len(tab_fichier)
    # On initialise la matrice à la taille requise avec des 0.0
    matrice = [[0.0 for _ in range(nb_colonne)] for _ in range(nb_ligne)]
    # On récupére le tableau de correspondance
    cle = correspondance_mot(dico_idf)
    # On va remplir les colonnes 11 par une
    for colonne in range(nb_colonne):
        # Chaque colonne correpond à un fichier on va donc récupérer les scores tf associé à ce fichier
        texte = recuperation_texte(tab_fichier[colonne])
        dico_tf = tf(texte)
        # On parcourt les mots possédant un score tf
        for element in dico_tf.keys():
            # On récupére la ligne correspondant au mot que l'on est en train de traiter grâce au tableau de
            # correspondance
            ligne = indice_tab(cle, element)
            # Si le mot est bien dans le tableau de correspondance
            if ligne != -1:
                # On calcule son score tf-idf et on le place au bonne endroit
                matrice[ligne][colonne] = dico_tf[element] * dico_idf[element]
    return matrice

  
def correspondance_mot(dico):
    cle = []
    for valeur in dico.keys():
        cle.append(valeur)
    return cle


def indice_tab(tab, element):
    """Fonction a partir d'un tableau et d'un élement renvoi son indice dans le tabelau ou -1 si il n'est pas présent
    Entré: tab: tableau: tableau dans lequelle on cherche l'occurence de l'élément
           element: pas de type précis: element dont on cherche à otenir l'occurence
    Sortie: -1: int: Si l'élement n'est pas dans le tableau
            indice: int: indice de l'élément dans le tableau"""
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
    """Fonction qui a partir d'un texte va renvoyer une chaine de caractere contenant les mots du texte
    Entré: fichier: str: Nom du fichier
    Sortie: texte: str: Chaine de caractere contenant le texte"""
    texte = ""
    # Chemin pour acceder au ficheir
    path = f"./Cleaned/{fichier}"
    # Ouverture du fichier
    with open(path, "r", encoding="utf-8") as f1:
        for ligne in f1:
            # On souhaite enlever les retours à la ligne on les remplace donc par des espaces quand on les rencontres
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
    """Fonction qui a partir d'un fichier va renvoyer son auteur
    Entré: fichier: str: Nom du fichier
    Sortie: nom: str: Nom de l'auteur du fichier"""
    # On spéare le nom en 2 partie pour enlever le Nomination
    tab_temp = fichier.split("_")
    # On resépare en 2 partie ce qui reste pour enlever le .txt
    tab_temp = tab_temp[1].split(".")
    nom = tab_temp[0]
    # On parcourt ce qu'il reste pour enlever tout les caracteres numérqiues qui sont présent dans le cas où l'auteur à
    # écrit plusieurs texte
    for indice in range(len(nom))[::-1]:
        if not ('A' <= nom[indice] <= 'Z' or 'a' <= nom[indice] <= 'z' or nom[indice] == ' '):
            nom = nom[:indice] + nom[indice + 1:]
    return nom


def a_parler(repertoire, mot):
    """Fonction qui à partir d'un mot et d'un répertoire renvoyer l'auteur ayant le plus utilisé le mot et une liste
    contenant le nom de tout les auteurs l'ayant utilsé
    Entré: repertoire: str: Nom du répertoire à analyser
           mot: str: Mot à rechercher
    Sortie: a_le_plus_parler: str: Nom de la personne ayant le plus parler
            tab_parler: tableau de str: Tableau contenant le nom de tout les auteur ayant mentionner le mot """
    dico_parler = {}
    # On récupere un tableau avec le nom de tout les fichiers
    tab_fichier = liste_fichier(repertoire)
    tab_parler = []
    maximum = 0
    a_le_plus_parler = []
    # On parcourt les fichiers
    for fichier in tab_fichier:
        # On récupére son tf
        texte = recuperation_texte(fichier)
        dico_tf = tf(texte)
        # Si le mot est dans le texte
        if mot in dico_tf.keys():
            # On récupére l'auteur du texte
            auteur = qui_a_ecrit(fichier)
            # Si c'est la premiere fois que l'on rencontre cette auteur
            if auteur not in dico_parler.keys():
                # On met dans le dico la valeur du tf à la clé correspondant au nom de l'auteur
                dico_parler[auteur] = dico_tf[mot]
            # Si on l'a déjà rencontré on rajoute le score tf actuel à l'ancienne valeur
            else:
                dico_parler[auteur] += dico_tf[mot]
    # On parcourt le dictionnaire pour déterminer le maximum du dico
    for cle in dico_parler.keys():
        tab_parler.append(cle)
        if dico_parler[cle] > maximum:
            maximum = dico_parler[cle]
            a_le_plus_parler = [cle]
        elif dico_parler[cle] == maximum:
            a_le_plus_parler.append(cle)
    return a_le_plus_parler, tab_parler


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
    """Fonction qui va ernvoyer l'indice de la premiere occurence d'un mot dans un texte
    Entré: fichier: str: Nom du fichier
           mot_recherche: str: Mot dont on cherche l'indice
    Sortie: -1: int: mot non  trouvé dans le texte
            indice_mot: int: premiere indice du mot recherché
    """
    # On récupére le texte sous la forme d'un str
    texte = recuperation_texte(fichier)
    tab_texte = texte.split(" ")
    # On parcourt le texte
    for indice_mot in range(len(tab_texte)):
        # Si on le trouve le mot
        if tab_texte[indice_mot] == mot_recherche:
            return indice_mot
    return -1


def premier_a_parler(repertoire: str, mot: str) -> str and int:
    """Fonction qui va à partir d'un répertoire donné en argument renvoyer le premiere auteur à utiliser un mot ainsi
     que l'emplacement à lequelle il l'utise
    Entré: répertoire: str: Répertoire que l'on va étudier
           mot: str: mot que l'on recherche
    Sortie: premier: str: Nom du premier auteur à utiliser ce mot
            indice_premier: int: emplacement de la premiere occurence du mot recherché"""
    tab_fichier = liste_fichier(repertoire)
    premier = ''
    # + l'infini
    indice_premier = float("inf")
    # Parcourt des fichier
    for fichier in tab_fichier:
        # Si le mot est dans le fichier
        if est_present(fichier, mot):
            # On récupére l'emplacement de sa premiere occurence
            emplacement = premiere_occurence(fichier, mot)
            # Si c'est la plus petite on la considere comme étant celle qui a été dite en premier
            if emplacement < indice_premier:
                indice_premier = emplacement
                premier = qui_a_ecrit(fichier)
    # Si personne n'a utilisé le mot
    if premier == '':
        return "Ce mot n'est présent dans aucun texte"
    else:
        return premier, indice_premier
