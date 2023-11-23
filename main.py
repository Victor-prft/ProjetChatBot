from function import *
transformation_fichier("./Speeches")
matrice = creation_tf_idf("./Cleaned")
dico_idf = idf("./Cleaned")
liste_cle_dico = correspondance_mot(dico_idf)
print(plus_élevé(matrice,liste_cle_dico))
print(creation_tf_idf("./Cleaned"))
