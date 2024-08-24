from BO.QuotationsComparatorV2 import QuotationsComparatorV2
from BO.VectorDatabase import VectorDataBase
import config
import os






print(" ********** DEBUT DES TESTS ************ ")


# Création des chemins des images :
images_to_process = ["Devis1.png", "Devis2.png", "Devis3.png", "Devis4.png", "Devis5.png"]  
images_to_process_paths = []
for image in images_to_process:
    images_to_process_paths = [os.path.join(config.IMAGE_PATH, image) for image in images_to_process]


# Création de l'instance de la BDD Vectorielle :
vector_db_mock = VectorDataBase()


# Création de l'instance de QuotationsComparatorV2 :
comparator = QuotationsComparatorV2(images_to_process_paths)
print("comparator.image_paths : ", comparator.image_paths)
# ==> OK


# Simulation du texte extrait pour chaque image :
extracted_texts = comparator.extract_text(images_to_process_paths)
print("Extract_texts : ", extracted_texts)
# ==> ???????


# Chargement du contenu des devis dans la variable processed_texts :
comparator.processed_texts = extracted_texts
print("comparator.processed_texts : ", comparator.processed_texts)


# AAffichage du tableau comparatif et stockage des devis en BDD Vectorielle :
comparator.compare_quotations()


# Vérifier que l'affichage des données est correct.


print(" ********** FIN DES TESTS ************ ")

