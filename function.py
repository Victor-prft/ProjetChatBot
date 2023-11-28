import os
import math


def prenom_president(nom: str) -> str:
    """Cette fonction renvoie le prénom d'un président en fonction du nom mis en argument
    Entrée: nom: str: nom du président pour lequelle on veut le prénom
    Sortie: un str contenant le prénom du président concerné"""
    # Chemin vers un fichier contenant le nom de tous les présidents associée à leur prénom
    fichier = "./Ressource/nom_president.txt"
    # ouverture du fichier en mode lecture
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
    Entrée: repertoire: str: chemin vers le dossier contenant les textes
    Sortie: tab: tableau de str: Tableau contenant le nom de tous les présidents ayant écris un discours présent dans le
                 dossier
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


def minuscule(fichier):
    """Fonction prenant en argument un fichier et va réecrire le contenu du fichier dans un autre en transformant toute
    les majuscules en minscules
    Entrée: fichier: str: Nom du fichier à transformer
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
    Entrée: f1: str: Nom du fichier à transformer
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
    # On réouvre le fichier pour réecrire la nouvelle version
    with open(fichier, 'w', encoding="utf-8") as fichier_1:
        for caractere in texte:
            fichier_1.write(caractere)


def liste_fichier(repertoire):
    """Fonction renvoyant à partir d'un répertoire donné un tableau contenant le nom de chacun des fichiers en .txt
    qu'il contient
    Entrée: repertoire: str: chemin du dossier dont on veut extraire les fichiers
    Sortie: tableau de str: tableau contenant le nom de tous les fichiers txt présent dans le repertoire"""
    tab_fichier = []
    # On parcourt les fichiers
    for fichier in os.listdir(repertoire):
        # On ne récupére que les fichiers en .txt
        if fichier.endswith(".txt"):
            tab_fichier.append(fichier)
    return tab_fichier


def transformation_fichier(repertoire):
    """Fonction permettant d'appeler les fonctions permettant d'effectuer le traitement de tout les fichiers dans un
    répertoire mis en argument
    Entrée: repertoire: str: Chaine de caractère contenant le nom du dossier à traiter
    Sortie: None"""
    # On vérifie si le fichier Cleaned est créé
    if not os.path.exists("Cleaned"):
        # Si c'est pas le cas on le crée
        os.makedirs("Cleaned")
    # On récupére la liste contenant le nom de tout les fichiers
    tab_fichier = liste_fichier(repertoire)
    # On les parcourt
    for fichier in tab_fichier:
        # On appele les fonctions nécessaire au traitement du texte
        minuscule(fichier)
        ponctuation(fichier)


def recuperation_texte(fichier):
    """Fonction qui a partir d'un texte va renvoyer une chaine de caractere contenant les mots du texte
    Entrée: fichier: str: Nom du fichier
    Sortie: texte: str: Chaine de caractere contenant le texte"""
    texte = ""
    # Chemin pour acceder au fichier
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
    """ Cette fonction nous donne tous les discours d'un président dans une liste
        Entrée : un repertoire et le nom du président
                repertoire : repertoire contenant dans fichier de type .txt
                president : str
        Sortie : la sortie est une liste des discours d'un même président
                liste_discours : list"""
    liste_discours = []
    # On parcours tous les discours
    for discours in liste_fichier(repertoire):
        # On regarde si le nom du président apparait dans le nom du fichier
        if president in discours:
            liste_discours.append(discours)
    return liste_discours


def maxi_dico(dico):
    """Cette fonction sert a donner la plus grande valeur et la clé d'un dictionnaire
        Entrée : dico est le dictionnaire où l'on veut savoir le maximum
                 dico : dict
        Sortie : une liste de deux valeurs :
                 cle_max est le cle du dictionnaire ayant la plus grande valeur du dictionnaire
                 maxi est la valeur la plus grande dans le dictionnaire
                 cle_max : str
                 maxi : float"""
    # Nécessité pour rentrer une première fois dans la boucle
    maxi = -float('inf')
    cle_max = ''
    # On parcours les clés du dictoinnaire
    for cle in dico.keys():
        # On regarde si la valeur dans le dictoinnaire est supérieur à l'ancienne
        if maxi <= dico[cle]:
            cle_max = cle
            maxi = dico[cle_max]
    return [cle_max, maxi]


def plus_petit_dico(liste):
    """ Cette fonction ressort le dictionnaire le plus petit en terme de nombre de clé dans un dico
        Entrée : une liste comportant des dictionnaires
                liste : list
        Sortie : le dictionnaire ayant le moins de clé
                 dico_mini : dict"""
    # Nécessité pour rentrer une première fois dans la boucle
    mini = float('inf')
    dico_mini = {}
    # On parcours la liste des dictoinnaires
    for dico in liste:
        # On compare le plus petit dictionnaire à l'actuel
        if len(dico) < mini:
            mini = len(dico)
            dico_mini = dico
    return dico_mini


def est_present(f, mot_rechercher):
    """Cette fonction nous indique si un mot est présent ou non dans un fichier.
    Entrée : f est le fichier où l'on veut recherche le mot,
             mot_rechercher est le mot qui est recherché dans le fichier.
             f : .txt , mot_rechercher : str
    Sortie : True si le mot_rechercher est dans le fichier f et False si le mot_rechercher n'est pas dans le fichier """
    fichier = f"./Cleaned/{f}"
    # Ouverture du fichier
    with open(fichier, "r", encoding="utf-8") as f1:
        for ligne in f1:
            # Création d'un tableau à partir de la séparation d'un texte où chaque valeur est un mot
            tab_mot = ligne.split(" ")
            # On parcours le tableau
            for mot in tab_mot:
                if mot[-1] == "\n":
                    mot = mot[:-1]
                if mot == mot_rechercher:
                    return True
        return False


def tf(texte):
    """ Fonction qui prend en argument le contenu d'un texte et associé un score tf à chacun des mot qu'il contient
    Entrée: texte: str: Chaine de caractère correspondant au contenu du texte
    Sortie: dico: dictionnaire: Dictionnaire associant à chaque mot du texte une valeur entiere correspondant à son
                  score tf
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


def idf(repertoire):
    """Cette fonction renvoie un dictoinnaire avec comme clé chaque mot du texte et en valeur sont idf
            Entrée : le repertoire qu'on veut analyser pour trouver les idf
                     repertoire : repertoire comtenant des fichiers de type .txt
            Sortie : la fonction ressort un dictoinnaire :
                     dictoinnaire.keys() : mot du texte sous type str
                     dictoinnaaire.values() : float """
    dictionnaire = {}
    # On crée une liste comptenant tous les fichiers
    tab_fichier = liste_fichier(repertoire)
    # On parcours tous les fichiers
    for i in range(len(tab_fichier)):
        # On ouvre les fichiers en lecture
        with open(repertoire + "./" + tab_fichier[i], "r", encoding="utf-8") as f1:
            for ligne in f1:
                # Création d'un tableau à partir de la séparation d'une ligne où chaque valeur est un mot
                tab_mot = ligne.split(" ")
                for mot in tab_mot:
                    if mot[-1] == "\n":
                        mot = mot[:-1]
                    # On regarde si le mot a déjà été traité
                    if mot not in dictionnaire.keys():
                        somme = 0
                        # On regarde si le mot est dans les autres textes
                        for f in range(i, len(tab_fichier)):
                            if est_present(tab_fichier[f], mot):
                                somme += 1
                        dictionnaire[mot] = math.log(len(tab_fichier)/somme)
    return dictionnaire


def creation_tf_idf(repertoire):
    """Fonction renvoyant la matrice tf-idf des documents contenu dans un répertoire mis en argument
    Entrée: repertoire: str: Nom du dossier où sont contenu les fichiers
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


def recuperation_tf_idf(mot, matrice, correspondance_ligne):
    ligne = indice_tab(correspondance_ligne, mot)
    return matrice[ligne]
    
  
def correspondance_mot(dico):
    """ Cette fonction sert à renvoyer toutes les clés d'un dictoinnaire sous forme de liste
        Entrée : un dictoinnaire
                dico : dict
        Sortie : une liste comportant toutes les clés du dictoinnaire
                cle : list"""
    # Création d'une liste
    cle = []
    # On parcours les clés du dictinnaire pour les ajouter à la liste
    for valeur in dico.keys():
        cle.append(valeur)
    return cle


def indice_tab(tab, element):
    """Fonction a partir d'un tableau et d'un élement renvoi son indice dans le tabelau ou -1 si il n'est pas présent
    Entrée: tab: tableau: tableau dans lequelle on cherche l'occurence de l'élément
           element: pas de type précis: element dont on cherche à otenir l'occurence
    Sortie: -1: int: Si l'élement n'est pas dans le tableau
            indice: int: indice de l'élément dans le tableau"""
    for indice in range(len(tab)):
        if tab[indice] == element:
            return indice
    return -1

  
def moins_important(dico_idf):
    """ Cette fonction sert a trouver le ou les mots moins importants des textes. C'est mot sont dient moins
        important si la valeur dans le dico est égal à 0
        Entrée : dico_idf qui est la sortie de la fonction idf
                 dico_idf : dict
        Sortie : Cette fonction ressort une liste des mots les moins importants de la matrice (idf = 0).
                liste_moins_important : list"""
    liste_moins_important = []
    for cle, valeur in dico_idf.items():
        if valeur == 0:
            liste_moins_important.append(cle)
    return liste_moins_important


def plus_eleve(matrice, correspondance_ligne):
    """ Cette fonction sert a trouver le ou les mots plus importants de la matrice. C'est mot sont dient plus
        important si la valeur dans le tableau est la plus haute de la matrice
        Entrée : Matrice qui est une liste de liste comportant la note tf-idf. Correspondance_ligne est la liste de mots
                matrice : list
                correspondance_ligne : list
        Sortie : Cette fonction ressort une liste des mots les plus importants de la matrice.
                 liste_plus_important : list"""
    liste_plus_important = []
    maximum = -float('inf')
    # On récupère les indices pour les utiliser pour parcourir les lignes du texte
    for indice_ligne in range(len(matrice)):
        # On parcours chaque ligne
        for score in range(len(matrice[indice_ligne])):
            # On regarde si le score tf-idf est égal au maximum de la matrice et on ajoute le mot dans la liste
            if matrice[indice_ligne][score] == maximum:
                liste_plus_important.append(correspondance_ligne[indice_ligne])
            # On regarde si le score tf-idf est supérieur à l'ancien maximum de la fonction
            elif matrice[indice_ligne][score] > maximum:
                # On remplace la liste par la nouvelle valeur max
                liste_plus_important = [correspondance_ligne[indice_ligne]]
                maximum = matrice[indice_ligne][score]
    return liste_plus_important


def repete_president(repertoire, president):
    """ Cette fonction sert  adonner le mot le plus dit par un président peut importe son discours
        Entrée : un repertoire et le nom du président
                 repertoire : repertoire contenant dans fichier de type .txt
                 president : str
        Sortie : la sortie est le mot le plus répété par un président
                maxi_dico(dico_occurence)[0] : str"""
    liste_discours = fichier_discours(repertoire, president)
    texte_total = ""
    # On parcours tous les discours d'un même président
    for fichier in liste_discours:
        texte = recuperation_texte(fichier)
        # Concaténation des textes d'un même président
        texte_total += texte
    dico_occurence = tf(texte_total)
    return maxi_dico(dico_occurence)[0]


def qui_a_ecrit(fichier):
    """Fonction qui a partir d'un fichier va renvoyer son auteur
    Entrée: fichier: str: Nom du fichier
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
    Entrée: repertoire: str: Nom du répertoire à analyser
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


def mot_evoque_par_tous(repertoire, liste_moins_importante):
    """ Cette focntion sert a donner la liste des mots les moins importants mais à la différence que les différents
        discours d'un même président sont comptés comme un seul discours
        Entrée : un repertoire et liste_moins_importante qui est la liste de mots les moins important
                repertoire : repertoire contenant dans fichier de type .txt
                liste_moins_importante : list
        Sortie : Cette fonction ressort une liste des mots les moins importants.
                mot_finaux : list"""
    liste_president = nom_president(repertoire)
    liste_dico = []
    mot_finaux = []
    cle_petit_dico = []
    # On parcours la liste des présidents
    for nom in liste_president:
        liste_discours = fichier_discours(repertoire, nom)
        texte_total = ""
        # On parcours les fichiers
        for fichier in liste_discours:
            texte = recuperation_texte(fichier)
            texte_total += texte
        dico_president = tf(texte_total)
        liste_dico.append(dico_president)
    petit_dico = plus_petit_dico(liste_dico)
    # On regarde si le mot appartient à la liste des mot moins importants
    for element in petit_dico.keys():
        if element not in liste_moins_importante and element != '':
            cle_petit_dico.append(element)
    for cle in cle_petit_dico:
        # On test si le nombre de présidents qui on parler est le bon
        if len(a_parler(repertoire, cle)[1]) == len(liste_president):
            mot_finaux.append(cle)
    return mot_finaux


def premiere_occurence(fichier, mot_recherche):
    """Fonction qui va ernvoyer l'indice de la premiere occurence d'un mot dans un texte
    Entrée: fichier: str: Nom du fichier
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
    Entrée: répertoire: str: Répertoire que l'on va étudier
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
    return premier, indice_premier


def demande_continuer():
    """Fonction qui demande a l'utilisateur si il veut continuer
    Entrée: None
    Sortie: """
    while True:
        reponse = input("Voulez vous continuer? oui/non\n")
        if reponse == "oui":
            return True
        elif reponse == "non":
            return False


def premier_dans_une_liste(tableau, repertoire):
    """Fonction qui a partir d'un tableau mis en argument va renvoyer l'auteur ayant utilisé en premier l'un de ces
    termes
    Entrée: tableau: tableau: tableau contenant tout les éléments recherché
            repertoire: str: repertoire dans lequelle on va cherher les fichiers
    Sortie: premiers_president: str: nom du président ayant utilisé l'un des termes en premier"""
    indice_premier = float('inf')
    premier_president = ''
    for element in tableau:
        president, indice = premier_a_parler(repertoire, element)
        if president != '':
            if indice < indice_premier:
                indice_premier = indice
                premier_president = president
    if premier_president == "":
        return "Aucun des mot n'a été cité dans le texte"
    else:
        return premier_president
