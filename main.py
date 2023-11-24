from function import *
transformation_fichier("./Speeches")
matrice = creation_tf_idf("./Cleaned")
dico_idf = idf("./Cleaned")
liste_cle_dico = correspondance_mot(dico_idf)
liste_moins_important = moins_important(matrice,liste_cle_dico)
print(mot_evoque_par_tous("./Cleaned",liste_moins_important))
