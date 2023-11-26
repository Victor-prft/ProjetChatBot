from function import *
transformation_fichier("./Speeches")
running = True
demande = """ Veuillez choisir une option:
-1: Afficher les mots les moins important
-2: Afficher les mots avec le plus grand score tf-idf
-3: Afficher le/les mot(s) les plus utilisé par un président
-4: Afficher le président qui a le plus dit un mot
-5: Afficher tout les présidents qui ont dit un mot
-6: Afficher le premier président ayant parlé de certains termes
-7: Afficher tout les mots à la fois important et cité par tout les 
-8: Sortir
"""
while running:
    choix = int(input(demande))
    if choix == 1:
        print(moins_important(matrice, correspondance_ligne))
