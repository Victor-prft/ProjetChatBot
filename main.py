from function import *
running = True
repertoire_propre = "./Cleaned"
repertoire_non_traiter = "./Speeches"
demande = """ Veuillez choisir une option:
-1: Afficher les mots les moins important
-2: Afficher les mots avec le plus grand score tf-idf
-3: Afficher le/les mot(s) les plus utilisé par un président
-4: Afficher le/les président(s) qui a/ont le plus dit un mot
-5: Afficher tout les présidents qui ont dit un mot
-6: Afficher le premier président ayant parlé de certains termes
-7: Afficher tout les mots à la fois important et cité par tout les présidents
-8: Sortir
"""


transformation_fichier(repertoire_non_traiter)
matrice = creation_tf_idf(repertoire_propre)
dico_idf = idf(repertoire_propre)
correspondance_ligne = correspondance_mot(dico_idf)


while running:
    choix = input(demande)
    if choix == "1":
        print(moins_important(matrice, correspondance_ligne))
        running = demande_continuer()
    elif choix == "2":
        print(plus_eleve(matrice, correspondance_ligne))
        running = demande_continuer()
    elif choix == "3":
        president = input("Veuillez rentrer le nom d'un président\n")
        print(repete_president(repertoire_propre, president))
        running = demande_continuer()
    elif choix == "4" or choix == "5":
        mot_recherche = input("Veuillez choisir un mot\n")
        le_plus, liste_president = a_parler(repertoire_propre, mot_recherche)
        if choix == "4":
            print(le_plus)
        else:
            print(liste_president)
        running = demande_continuer()
    elif choix == "6":
        nombre_termes = int(input("Combien de termes voulez vous comparer\n"))
        while nombre_termes < 0:
            nombre_termes = int(input("Combien de termes voulez vous comparer\n"))
        terme = []
        for _ in range (nombre_termes):
            terme.append(input("Veuillez entrer un terme"))
        print(premier_dans_une_liste(terme, repertoire_propre))
        running = demande_continuer()
    elif choix == "7":
        print(mot_evoque_par_tous(repertoire_propre, moins_important(matrice, correspondance_ligne)))
        running = demande_continuer()
    elif choix == "8":
        print("Merci d'avoir utilisé notre programme")
        running = False
    else:
        print("Choix non valide veuillez recommencer")
