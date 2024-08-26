from BO.QuotationsComparatorV2 import QuotationsComparatorV2
from BO.VectorDatabase import VectorDataBase
import config
import os






print(" ********** DEBUT DES TESTS ************ ")


# Création des chemins des images :
images_to_process = ["Devis1.png", "Devis2.png", "Devis3.png", "Devis4.png", "Devis5.png", "processed_image.png"]  
images_to_process_paths = []
for image in images_to_process:
    images_to_process_paths = [os.path.join(config.QUOTATIONS_FILES_PATH, image) for image in images_to_process]
# ==> Récupération des chemins : OK.



# Création de l'instance de la BDD Vectorielle :
vector_db_mock = VectorDataBase()
# ==> Instanciation de la BDD : OK.




# Création de l'instance de QuotationsComparatorV2 :
comparator = QuotationsComparatorV2(images_to_process_paths)
print("comparator.image_paths : ", comparator.image_paths)
# Instanciation de la classe QuotationsComparator + Vérification des chemins ==> OK







# Simulation du texte extrait pour chaque image
extracted_texts = [comparator.extract_text(image_path) for image_path in images_to_process_paths]
print("Extract_texts : ", extracted_texts)
# ==> Extraction du texte dans chaque Image : OK.




# Affichage du tableau comparatif et stockage des devis en BDD Vectorielle :
comparator.compare_quotations()
# Stockage des données dans la BDD Vectorielle réalisé par cette méthode ==> OK 
# Récupération des infos clés des devis ==> OK.


# Récupération des données stockées sous forme de vecteur et comparaison ?
# => ?




# Vérifier que l'affichage des données est correct.



print(" ********** FIN DES TESTS ************ ")





["Société : a Plomberie Devis ne : 5290 adresse | rue Boulevard volontaire 29200 est Date 24/08/2024 téléphone : 02.02.02.02.02, émail : adPlomberie@gmall.com chien : Famille dupant adresse : 25 rue des Hortensias code Postale : 29 000 quitter Description : Pose dune nouvelle chaudière quantité Description Prix Unitaire Total de Chaudière à par 8500,00€| 8500,00€ 1 Main d'œuvre voie s000e total s000,00€ taux 20% _ 180€ totalité 10800,00€ Début des travaux : 01/01/2026 conditions de règlement Acompte de 20% à la commande Acompte de 30% au début des travaux Solde à la livraison paiement au comptant dès réception Merci de nous retourner un exemplaire de ce devis Signé avec votre nom et la mention bon pour accord et commande", "Société : sherry Les bons Tuyaux Devis ne : 15500 adresse : 2 rue de clam 29200 est Date 24/08/2024 Téléphone : 03.03.03.03.03, émail : LesbonsTuvaux@hotmalLcom chien : Famille dupant adresse : 25 rue des Hortensias code Postale : 29 000 quitter Description : installation dune nouvelle chaudière quantité Description PrixUnitaire | _ Total de Chaudière à par 8200,00€| 8200,00€ 1 Main d'œuvre z00c0€| _ code total 8500,00€ TAUXTVA 20% _ 170€ totalité 10200,00€ Début des travaux : 01/01/2027 conditions de règlement Acompte de 60% à la commande Solde à la livraison paiement au comptant dès réception Merci de nous retourner un exemplaire de ce devis Signé avec votre nom et la mention bon pour accord et commande", "Société : JeanPlomberte Devis ne : 500 adresse : 2 rue Jean après 29200 est Date 23/08/2024 Téléphone : 04,04,04.04.04, emballé Jeanplomberte@gmall.com client : Famille dupant adresse : 25 rue des Hortensias code Postale : 29 000 quitter Description : Installation dune chaudière à gaz quantité Description Prix Unitaire Total 1 Chaudière à gaz 8000,00€| 8000,00€ 1 mal d'œuvre 700,00€| 700,00€ total 8700,00€ TAUXTVA 20% 17406 totalité 10440,00 a Début des travaux ; 01/01/2028 conditions de règlement : Acompte de 50% à la commande Solde à la livraison paiement au comptant dès réception Merci de nous retourner un exemplaire de ce devis Signé avec votre nom la mention bon pour accord et commande", "société : EnglePlomberte Devis ne 65273 adresse : 2 rue comtesse modeler 25200 est base 25/08/2024 téléphone : 05.05.05.05.06. demain : EnelePlomberte@outiook.com calent : Famille dupant adresse : 25 rue des hortensias code Postale : 29 000 guimpes description : pose dune nouvelle chaudière quantité description Prix Unitaire Total de Chaudière à gaz sonoce|_ s000 a de Main d'œuvre 200,00€| _200,00€ total s20000€ TAUX va 20 a 18404 totalité 1104000€ Début des travaux 01/06/2028 Conditions de règlement : Acompte de 20% à la commande Acompte de 30% au début des travaux solide à la livraison paiement au comptant dès réception merci de nous retourner un exemplaire de ce devis Signé avec votre nom la mention bon pour accord et commande", "Société : SuperMarioPlomberie Devis ne : 1050 adresse : 2 rue de Gouesnou 29200 est Date 25/08/2024 Téléphone : 06.06.06.06.06. émail : SuperMarioPlomberie@outiook.com Client : Famille dupant adresse : 25 rue des Hortensias code Postale : 29 000 quitter Description : Pose dune chaudière à Gaz quantité Description Prix Unitaire Total 1 Chaudière à gaz 5000,00€| 5000,00€ 1 Main d'œuvre 64,00 a 64,00 a total 5064,00€ TAUXTVi 20% 1013€ totalité 6076,80€ Début des travaux : 01/12/2028 Conditions de règlement : Acompte de 50% à la commande Solde à la livraison paiement au comptant dès réception Merci de nous retourner un exemplaire de ce devis Signé avec votre nom et la mention bon pour accord et commande", "émetteur agressé à sari semaine Té:01 Fax émail Dgmait.com il ; vroree lactidends.fr Devis Réf. devise de 09-00034 a Date de devise 28 septembre 2021 Référence ou adresse de chantier : description Quantité [ Prix Unitaire prix chambre sinistre numéro 1 |Gratage, pression 2 passes enduit en plein sur plafond 2007 1880€ SBA0€ fourniture le application de 2 couches de peinture Mal sur plafond 12007> 2750€ 2330.00 a grattage pression de 2 passes d'endurt en plein sur bas de 2 murs 4.00 me 1880€ 7520€ fourniture le apphiçaton de 2 couches de peinture saline sur 2 murs 15.00 a 2750€ a12.50€ |Fournaure le application d' couche de permettre satanés sur 2 murs pour uniformisation 15.00 me 1900 a 2856.00 a protection du parquet de l'enirée à la chambre avec de la bâche plastique autocollante santé 17900 a 17900 a fourniture le pose dure prise de courant étanche 4 unité 5180€ s180€ total 1389.50 a Prestations annexes nettoyage . déplacement tenté 150 00 a 150.00 a total 150.00 a Conditions de règlement TotalH.T 153990€ * 40% à la signature du des de pas a 30% en cours des baveux Total T.T.C a 55550 a a 20% en fin des travaux Bon pour accord du"]