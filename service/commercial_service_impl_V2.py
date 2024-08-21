from BO import QuotationsComparatorV2, VectorDatabase
import config
import os






print(" ********** DEBUT DES TESTS ************ ")


# Création des chemins des images :
images_to_process = ["devis_2.png", "devis_3.png", "processed_image.png"]  
images_to_process_paths = []
for image in images_to_process:
    images_to_process_paths = [os.path.join(config.IMAGE_PATH, image) for image in images_to_process]


# Création de l'instance de la BDD Vectorielle :
vector_db_mock = VectorDatabase()


# Création de l'instance de QuotationsComparatorV2 :
comparator = QuotationsComparatorV2(images_to_process_paths, vector_db_mock)


# Simulation du texte extrait pour chaque image :
extracted_texts = comparator.extract_text(images_to_process_paths)


# Chargement du contenu des devis dans la variable processed_texts :
comparator.processed_texts = extracted_texts


# AAffichage du tableau comparatif et stockage des devis en BDD Vectorielle :
comparator.compare_quotations()


# Vérifier que l'affichage des données est correct.


print(" ********** FIN DES TESTS ************ ")

