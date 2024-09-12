from datetime import datetime



# Emplacement des devis à traiter :
QUOTATIONS_FILES_PATH = "/Users/sjezequel/PycharmProjects/CommercialProposals/ressources/quotations_files/"
# Liste des fichiers à traier :
QUOTATIONS_FILES_LIST = ["Devis1.png", "Devis2.png", "Devis3.png", "Devis4.png", "Devis5.png"]
# Emplacement des devis traités pour être plus lisibles avant l'extraction des données :
PROCESSED_QUOTATIONS_FILES_PATH = "/Users/sjezequel/PycharmProjects/CommercialProposals/ressources/processed_quotations_files/"



# Données commerciales de notre compagnie :
COMPANY_COMMERCIAL_DATA = "/Users/sjezequel/PycharmProjects/CommercialProposals/ressources/commercial_advantages_list.jsonl"



# Url de la BDD SQL in memory :
DB_URL = 'sqlite:///devis.db'



# Modèle utilisé pour le traitement de texte dans une BDD Vectorielle :
VECTORIAL_BDD_MODEL = 'sentence-transformers/multi-qa-MiniLM-L6-cos-v1'



# Modèle utilisé pour récupérer les données des devis et générer une propposition commerciale :
MODEL_NAME = 'meta-llama/Meta-Llama-3-8B-Instruct'



# Accès à l'Api du modèle Llama-3 :
MONSTER_API_URL = "https://llm.monsterapi.ai/v1/"
MONSTER_API_KEY = "CREER UN COMPTE ET RECUPERER UNE CLE SUR LE SITE SUIVANT : https://monsterapi.ai/login/"



# Informations à renseigner sur le devis :
NUMERO_DEVIS = "001"
SOCIETE = "Plomberie Brestoise du 29"
ADRESSE_SOCIETE = "123 Rue de Verdun 29200 Brest"
DATE_DEVIS = datetime.today().strftime('%Y-%m-%d')
DEBUT_TRAVAUX = "2024-09-01"
RABAIS_APPLIQUE = "0.95"
DATE_DEBUT_TRAVAUX = "01/01/2025"

