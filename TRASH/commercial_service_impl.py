from BO.QuotationsComparator import QuotationsComparator
import config
import os






""" Exemple d'utilisation """

# Question posée :
question="Indique moi le montant total et l'entreprise émétrice pour chaque devis."

# Images à traiter :
images_to_process = ["devis_2.png", "devis_3.png", "processed_image.png"]  

# Création des chemins :
images_to_process_paths = []

# Création des chemins pour chaque image :
for image in images_to_process:
    images_to_process_paths = [os.path.join(config.IMAGE_PATH, image) for image in images_to_process]

comparer = QuotationsComparator(images_to_process_paths)
comparer.compare_quotations()

