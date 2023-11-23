from function import *
transformation_fichier("./Speeches")
matrice = creation_tf_idf("./Cleaned")
dico_idf = idf("./Cleaned")
liste_cle_dico = correspondance_mot(dico_idf)
print(a_parler("./Cleaned", "nation"))
