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
            tab = fct_split(ligne, ["/"])
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


def minuscule(contenu, destination=None):
    """Fonction qui prend en argument une chaine de caractere et qui soit renvoie soit sa version minuscule si jamais
    aucune destination lui est fournie ou écris le contenu dans un dossier si jamais on lui donne un fichier de
    destinattion.
    Entrée: contenue: str: chaine de carectere qui doit être mis en minuscule
            destination: str: chemin vers le fichier dans lequel on veut écrire le texte
    Sortie: texte: str: Si aucun fichier de destination ne lui est fourni
    """
    texte = ''
    for caractere in contenu:
        # Cas où le caractère est une majuscule
        if 'A' <= caractere <= 'Z':
            # On le transforme en minuscule
            caractere = chr(ord(caractere) + 32)
            # On écrit le caractère dans le nouveau fichier
        texte = texte + caractere
    if destination is None:
        return texte
    else:
        with open(destination, "w", encoding="utf-8") as new:
            for caractere in texte:
                new.write(caractere)


def ponctuation_fichier(contenu, destination=None):
    """Fonction qui prend en argument une chaine de caractere et qui soit renvoie soit sa version sans ponctuation
    si aucune destination lui est fournie ou écris le contenu dans un dossier si jamais on lui donne un fichier de
    destinattion.
    Entrée: contenue: str: chaine de carectere qui doit être traiter
            destination: str: chemin vers le fichier dans lequel on veut écrire le texte
    Sortie: texte: str: Si aucun fichier de destination ne lui est fourni
    """
    # Tableau contenant les caractères à transformer par des espaces
    tab_espace = [" ", "-", "'", "."]
    # Tableau contenant les caractères or alphabétique à conserver
    tab_garder = ["é", "è", "ù", "à", "â", "ô", "ê", "ç", "\n"]
    texte = ""
    # Cas du l' on va alterner entre écrire le et la
    l_actuel = 0
    l_possible = ["a", "e"]
    # On parcourt les caractères
    for element in contenu:
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
                if len(texte) > 0:
                    if texte[-1] != " " and texte[-1] != '' and texte[-1] != '\n':
                        texte += " "
    if destination is None:
        return texte
    else:
        # On réouvre le fichier pour réecrire la nouvelle version
        with open(destination, 'w', encoding="utf-8") as fichier_1:
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
        path = f"./Speeches/{fichier}"
        texte = recuperation_texte_avec_mise_en_forme(path)
        path = f"./Cleaned/{fichier}"
        minuscule(texte, path)
        texte = recuperation_texte_avec_mise_en_forme(path)
        ponctuation_fichier(texte, path)


def recuperation_texte_avec_mise_en_forme(path):
    """Fonction qui prend en argument un chemin vers un fichier et va renvoyer un str contenant tous les caracteres y
    compris les retours à la ligne
    Entree: path: str: chemin vers un fichier
    Sortie: texte: contenu du texte sans les retours à la ligne"""
    texte = ''
    # on ouvre le fichier
    with open(path, "r", encoding="utf-8") as f1:
        for ligne in f1:
            texte = texte + ligne
    return texte


def recuperation_texte(path):
    """Fonction qui a partir d'un texte va renvoyer une chaine de caractere contenant les mots du texte
    Entrée: fichier: str: Nom du fichier
    Sortie: texte: str: Chaine de caractere contenant le texte"""
    texte = ""
    # Ouverture du fichier
    with open(path, "r", encoding="utf-8") as f1:
        for ligne in f1:
            if ligne != "":
                if ligne[-1] == "\n":
                    # On enleve le retour à la ligne
                    ligne = ligne[:len(ligne)-1]
                    ligne += " "
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


def maxi_dico(dico, exclusion=None):
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
            if exclusion is None:
                cle_max = cle
                maxi = dico[cle_max]
            else:
                if cle not in exclusion:
                    cle_max = cle
                    maxi = dico[cle_max]
    return [cle_max, maxi]


def fct_split(texte, separateur):
    liste = []
    mot = ''
    for element in texte:
        if element in separateur:
            if mot != ('' or ' '):
                liste.append(mot)
            mot = ''
        else:
            mot = mot + element
    if mot != '' and mot != " ":
        liste.append(mot)
    return liste


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


def est_present(fichier, mot_rechercher):
    """Cette fonction nous indique si un mot est présent ou non dans un fichier.
    Entrée : f est le fichier où l'on veut recherche le mot,
             mot_rechercher est le mot qui est recherché dans le fichier.
             f : .txt , mot_rechercher : str
    Sortie : True si le mot_rechercher est dans le fichier f et False si le mot_rechercher n'est pas dans le fichier """
    # Ouverture du fichier
    with open(fichier, "r", encoding="utf-8") as f1:
        for ligne in f1:
            # Création d'un tableau à partir de la séparation d'un texte où chaque valeur est un mot
            tab_mot = fct_split(ligne, [" "])
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
    tab_mot = fct_split(texte, [" "])
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
                tab_mot = fct_split(ligne, [" "])
                for mot in tab_mot:
                    if mot[-1] == "\n":
                        mot = mot[:-1]
                    # On regarde si le mot a déjà été traité
                    if mot not in dictionnaire.keys():
                        somme = 0
                        # On regarde si le mot est dans les autres textes
                        for f in range(i, len(tab_fichier)):
                            if est_present(f"./Cleaned/{tab_fichier[f]}", mot):
                                somme += 1
                        dictionnaire[mot] = math.log((len(tab_fichier)/somme), 10)
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
        path = f"./Cleaned/{tab_fichier[colonne]}"
        texte = recuperation_texte(path)
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
    """Fonction qui prend en argument une matrice, un mot et la liste de correspondance d'une matrice tf_idf pour
    obtenir les valeurs du tf_idf du mot dans les textes
    Entree: mot: str: mot dont on souhaite obtenir le score tf_idf"""
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


def repete_president(repertoire, president, mot_pas_important):
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
        path = f"./Cleaned/{fichier}"
        texte = recuperation_texte(path)
        # Concaténation des textes d'un même président
        texte_total += texte
    dico_occurence = tf(texte_total)
    return maxi_dico(dico_occurence, mot_pas_important)[0]


def qui_a_ecrit(fichier):
    """Fonction qui a partir d'un fichier va renvoyer son auteur
    Entrée: fichier: str: Nom du fichier
    Sortie: nom: str: Nom de l'auteur du fichier"""
    # On spéare le nom en 2 partie pour enlever le Nomination
    tab_temp = fct_split(fichier, ["_"])
    # On resépare en 2 partie ce qui reste pour enlever le .txt
    tab_temp = fct_split(tab_temp[1], ["."])
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
        path = f"./Cleaned/{fichier}"
        texte = recuperation_texte(path)
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
            path = f"./Cleaned/{fichier}"
            texte = recuperation_texte(path)
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


def premiere_occurence(path, mot_recherche):
    """Fonction qui va ernvoyer l'indice de la premiere occurence d'un mot dans un texte
    Entrée: fichier: str: Nom du fichier
           mot_recherche: str: Mot dont on cherche l'indice
    Sortie: -1: int: mot non  trouvé dans le texte
            indice_mot: int: premiere indice du mot recherché
    """
    # On récupére le texte sous la forme d'un str
    texte = recuperation_texte(path)
    tab_texte = fct_split(texte, [" "])
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
        path = f'./Cleaned/{fichier}'
        if est_present(fichier, mot):
            # On récupére l'emplacement de sa premiere occurence
            emplacement = premiere_occurence(path, mot)
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


def demande_mode(message):
    """Fonction qui demande a l'utilisateur le mode souhaité
    Entrée: None
    Sortie: """
    while True:
        reponse = input(message + "\n")
        if reponse == "1":
            return "1"
        elif reponse == "2":
            return "2"


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


def tf_phrase(tab_mot, sont_present):
    dico_tf_question = {}
    for mot in tab_mot:
        if mot in sont_present:
            if mot not in dico_tf_question.keys():
                dico_tf_question[mot] = 1
            else:
                dico_tf_question[mot] += 1
    return dico_tf_question


def tf_idf_phrase(dico_idf, dico_tf, mot_a_traiter):
    tab_tf_idf_phrase = []
    for mot in mot_a_traiter:
        tab_tf_idf_phrase.append(dico_tf[mot] * dico_idf[mot])
    return tab_tf_idf_phrase, mot_a_traiter


def token_question(texte_sale):
    txt = minuscule(texte_sale)
    texte_propre = ponctuation_fichier(txt)
    return fct_split(texte_propre, ' ')


def mots_present(tab_mot, dico_idf):
    sont_present = []
    for element in tab_mot:
        if element in dico_idf.keys() and element not in sont_present:
            sont_present.append(element)
    return sont_present


def produit_scalaire(liste_question_a, liste_doc_b, correspondance_question, correspondance_liste):
    res = 0
    for i in range(len(liste_question_a)):
        mot = correspondance_question[i]
        b = liste_doc_b[indice_tab(correspondance_liste, mot)]
        res = res + b * liste_question_a[i]
    return res


def norme_vecteur(liste):
    res = 0
    if isinstance(liste, list):
        for valeur in liste:
            res = res + (valeur ** 2)
        return math.sqrt(res)
    else:
        return None


def calcul_similarite(liste_tf_idf_question, liste_tf_idf_doc, correspondance_question, correspondance_liste):
    prt_scal = produit_scalaire(liste_tf_idf_question, liste_tf_idf_doc, correspondance_question, correspondance_liste)
    a = norme_vecteur(liste_tf_idf_question)
    b = norme_vecteur(liste_tf_idf_doc)
    if a == 0:
        return 0
    return prt_scal/(a*b)


def doc_pertinent(tab_tf_idf_question, matrice, correspondance_question, correspondance_liste, correspondance_colonne):
    maxi = -float('inf')
    indice_doc = 0
    for colonne in range(len(matrice[0])):
        new_ligne = []
        for indice_mot in range(len(matrice)):
            new_ligne.append(matrice[indice_mot][colonne])
        calcul_sim = calcul_similarite(tab_tf_idf_question, new_ligne, correspondance_question, correspondance_liste)
        if calcul_sim > maxi:
            maxi = calcul_sim
            indice_doc = colonne
    return f'./Cleaned/{correspondance_colonne[indice_doc]}'


def transformation_cleaned_speeches(nom_fichier):
    liste = fct_split(nom_fichier, ['/'])
    return f'./Speeches/{liste[-1]}'


def mot_question_max_tf_idf(question, dico_idf):
    liste_mot_question = token_question(question)
    liste_mot_question_texte = mots_present(liste_mot_question, dico_idf)
    dico_tf_phrase = tf_phrase(liste_mot_question, liste_mot_question_texte)
    tab_tf_idf_question, correspondance_mot_question = tf_idf_phrase(dico_idf, dico_tf_phrase, liste_mot_question_texte)
    return tab_tf_idf_question, correspondance_mot_question


def maximum_indice_tableau(tableau, document, correspondance):
    tab_max = []
    element_max = -float("inf")
    for indice in range(len(tableau)):
        if est_present(document, correspondance[indice]):
            if tableau[indice] > element_max:
                tab_max = [indice]
                element_max = tableau[indice]
            elif tableau[indice] == element_max:
                tab_max.append(indice)
    return tab_max


def generation_reponse(question, dico_idf, matrice, correspondance_mot_matrice, correspondance_matrice_colonne):
    tab_tf_idf_question, correspondance_mot_question = mot_question_max_tf_idf(question, dico_idf)
    if len(tab_tf_idf_question) == 0:
        return "Désolé nous ne pouvons pas vous fournir de réponse"
    document_pertinent = doc_pertinent(tab_tf_idf_question, matrice, correspondance_mot_question,
                                       correspondance_mot_matrice, correspondance_matrice_colonne)
    tab_max_indice = maximum_indice_tableau(tab_tf_idf_question, document_pertinent, correspondance_mot_question)
    tab_mot_max = [correspondance_mot_question[i] for i in tab_max_indice]
    reponse = reponse_question(document_pertinent, tab_mot_max)
    return affinage_reponse(question, reponse)


def reponse_question(document_path_cleaned, liste_mot):
    document_path_speeches = transformation_cleaned_speeches(document_path_cleaned)
    separateur = ["!", ".", "?", "..."]
    texte = recuperation_texte(document_path_speeches)
    texte_tab = fct_split(texte, separateur)
    indice_min = float('inf')
    mot_min = ''
    for mot in liste_mot:
        indice = premiere_occurence(document_path_cleaned, mot)
        if indice < indice_min and indice != -1:
            indice_min = indice
            mot_min = mot
    for phrase in texte_tab:
        phrase_cleaned = minuscule(phrase)
        phrase_cleaned = ponctuation_fichier(phrase_cleaned)
        tab_phrase_cleaned = fct_split(phrase_cleaned, [" "])
        if mot_min in tab_phrase_cleaned:
            return phrase
          
          
def affinage_reponse(question, reponse):
    question_starters = {"Comment": "Après analyse, ", "Pourquoi": "Car, ", "Peux-tu": "Oui, bien sûr!"}
    reponse_final = ''
    tab_question = fct_split(question, [" "])
    starter = tab_question[0]
    if starter in question_starters.keys():
        reponse_final = question_starters[starter]
        if starter != "Peux-tu":
            i = 0
            while reponse[i] == " ":
                i += 1
            reponse = chr(ord(reponse[i]) + 32) + reponse[i + 1:]
    reponse_final = reponse_final + reponse + '.'
    return reponse_final
