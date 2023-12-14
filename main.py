from function import *
running = True
repertoire_propre = "./Cleaned"
repertoire_non_traiter = "./Speeches"
demande_menu = """ Veuillez choisir une option :
-1: Accéder aux fonctionnalités de la partie I
-2: Accéder au mode Chatbot
-3: Sortir
"""
message_demande_mode = """Veuillez choisir une option :
-1: Accéder aux fonctionnalités de la partie I
-2: Accéder au mode Chatbot"""

demande = """ Veuillez choisir une option :
-1: Afficher les mots les moins important
-2: Afficher le mot avec le plus grand score tf-idf
-3: Afficher le/les mot(s) les plus utilisé par un président
-4: Afficher le/les président(s) qui a/ont le plus dit un mot
-5: Afficher tout les présidents qui ont dit un mot
-6: Afficher le premier président ayant parlé de certains termes
-7: Afficher tout les mots à la fois important et cité par tout les présidents
-8: Changer de mode
-9: Sortir
"""

transformation_fichier(repertoire_non_traiter)
matrice = creation_tf_idf(repertoire_propre)
dico_idf = idf(repertoire_propre)
correspondance_ligne = correspondance_mot(dico_idf)
correspondance_colonne = liste_fichier('./Cleaned')
mot_les_moins_important = moins_important(dico_idf)
choix_menu = None

#print(generation_reponse("Comment une nation peut-elle prendre soin du climat ?", dico_idf, matrice, correspondance_ligne, correspondance_colonne))


while running:
    if choix_menu is None:
        print()
        choix_menu = input(demande_menu)
    if choix_menu == "1":
        choix = input(demande)
        if choix == "1":
            print(mot_les_moins_important)
            print()
            running = demande_continuer()
        elif choix == "2":
            print(plus_eleve(matrice, correspondance_ligne))
            print()
            running = demande_continuer()
        elif choix == "3":
            president = input("Veuillez rentrer le nom d'un président\n")
            print(repete_president(repertoire_propre, president, mot_les_moins_important))
            print()
            running = demande_continuer()
        elif choix == "4" or choix == "5":
            mot_recherche = input("Veuillez choisir un mot\n")
            le_plus, liste_president = a_parler(repertoire_propre, mot_recherche)
            if choix == "4":
                print(le_plus)
                print()
            else:
                print(liste_president)
                print()
            running = demande_continuer()
        elif choix == "6":
            nombre_termes = int(input("Combien de termes voulez vous comparer\n"))
            while nombre_termes < 0:
                nombre_termes = int(input("Combien de termes voulez vous comparer\n"))
            terme = []
            for _ in range(nombre_termes):
                terme.append(input("Veuillez entrer un terme\n"))
            print(premier_dans_une_liste(terme, repertoire_propre))
            print()
            running = demande_continuer()
        elif choix == "7":
            print(mot_evoque_par_tous(repertoire_propre, moins_important(dico_idf)))
            print()
        elif choix == "8":
            choix_menu = None
        elif choix == "9":
            choix_menu = "3"
        else:
            print("Choix non valide veuillez recommencer")
    elif choix_menu == "2":
        question = input("Saisissez votre question : ")
        print(generation_reponse(question, dico_idf, matrice, correspondance_ligne, correspondance_colonne))
        print()
        continuer = demande_continuer()
        if continuer == True:
            choix_menu = demande_mode(message_demande_mode)
        elif continuer == False:
            running = False
    elif choix_menu == "3":
        print("Merci d'avoir utilisé notre programme")
        running = False

