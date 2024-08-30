import json
import math
import re
from BO.VectorDatabase import VectorDataBase
import os
import config
from BO.Devis import Devis
from BO.Llm import Llm
from services.DevisDatabaseService import DevisDatabaseService
from services.GetQuotationsDataService import GetQuotationsDataService






class QuotationManagementService:
    """ Classe chargée du traitement et de la comparaison des devis """




    """ ***************** Constructeur ***************** """

    def __init__(self, db_url=config.DB_URL):
        """ Constructeur """
        # Service qui récupère le texte des devis :
        self.get_quotations_data_service = GetQuotationsDataService()
        # Liste des informations sur les devis :
        self.devis_data = [] 
        # Bdd Vectorielle :
        self.vector_db = VectorDataBase()
        # Initialisation de la BDD SQLlite :
        self.sql_service = DevisDatabaseService()





    """ ***************** Méthodes en charge de l'enregistrement des données des devis en BDD ***************** """

    def store_texts_in_vector_db(self, text, devis_number):
        """ Méthode qui stocke les données des devis sous forme non structurée dans la BDD Vectorielle """
        print("EXECUTION METHODE : store_texts_in_vector_db")
        print("TEXT : ", text)
        embedding = self.vector_db.generate_embedding(text)  # Utilise le modèle de VectorDataBase pour générer l'embedding
        metadata = {"Devis": f"Devis {devis_number}"}
        self.vector_db.insert(embedding, metadata=metadata)








    """ ***************** Méthodes en charge de la récupération et de l'affichage des données clés ***************** """

    def extract_relevant_info(self, text):
        """Méthode qui extrait les infos clés de chaque devis en utilisant un LLM avec prétraitement et validation."""
        # Étape 1 : Prétraitement du texte
        preprocessed_text = self.preprocess_text(text)
        
        # Étape 2 : Génération de la requête pour le LLM en demandant un JSON structuré
        llm_prompt = f"""
        Voici un texte de devis. Extrais les informations suivantes et renvoie les sous forme de JSON structuré :
        {{
            "Numéro de devis": "",
            "Société": "",
            "Adresse de la société": "",
            "Date du devis": "",
            "Nom du client": "",
            "Adresse du client": "",
            "Code Postal du client": "",
            "Description du travail": "",
            "Montant total HT": "",
            "Taux de TVA": "",
            "Montant total TTC": "",
            "Début des travaux": "",
            "Conditions de règlement": ""
        }}
        
        Texte :
        {preprocessed_text}
        """
        
        # Étape 3 : Interaction avec le LLM pour extraire les informations
        llm = Llm()
        response = llm.generate_answer(llm_prompt)
        print("RESPONSE OBTENUE DU LLM : ", response)
        
        # Étape 4 : Vérification si la réponse est un JSON valide
        response_dict = self.manual_parse_llm_response(response)
        print("REPONSE RECUPEREE AVEC manual_parse_llm_response() : ", response_dict)

        # Étape 5 : Parsing et validation des données extraites
        info = self.parse_and_validate_llm_response(response_dict)
        print("RESPONSE PARSÉE DU LLM : ", info)
        return info



    def manual_parse_llm_response(self, response_text):
        """Méthode pour extraire manuellement les données du texte brut en cas d'échec du parsing JSON."""
        # Étape 1 : Extraction de la partie JSON de la réponse
        json_start = response_text.find("{")
        json_end = response_text.rfind("}")
        if json_start != -1 and json_end != -1:
            # Extraire la chaîne JSON potentielle
            json_potential = response_text[json_start:json_end + 1]
            # Étape 2 : Tenter de parser cette chaîne comme JSON
            try:
                info = json.loads(json_potential)
                return info  # Si succès, retourner l'objet JSON parsé
            except json.JSONDecodeError:
                print("Erreur : La partie extraite ne peut pas être parsée en JSON.")
        # Si on arrive ici, cela signifie que le JSON n'a pas pu être extrait correctement
        print("Erreur : Impossible de trouver un JSON valide dans la réponse.")
        # Optionnel : Retourner un dictionnaire vide ou un message d'erreur structuré
        return {
            "Devis": "Non spécifié",
            "Entreprise": "Non spécifié",
            "Adresse Entreprise": "Non spécifié",
            "Date": "Non spécifié",
            "Client": "Non spécifié",
            "Adresse Client": "Non spécifié",
            "Code Postal Client": "Non spécifié",
            "Description": "Non spécifié",
            "Montant Total": "Non spécifié",
            "Taux TVA": "Non spécifié",
            "Total TTC": "Non spécifié",
            "Conditions": "Non spécifié",
            "Début Travaux": "Non spécifié"
        }



    def preprocess_text(self, text):
        """Méthode pour prétraiter le texte avant l'extraction."""
        # Remplacement des caractères spéciaux, uniformisation des montants, etc.
        text = text.replace("€", " EUR")  # Remplace le symbole € par EUR pour uniformiser
        text = re.sub(r'(\d+)[.,](\d{2})', r'\1.\2', text)  # Uniformise les montants 1.800,00 en 1800.00
        text = re.sub(r'\s+', ' ', text)  # Supprime les espaces multiples pour éviter les erreurs de lecture
        return text



    def parse_and_validate_llm_response(self, response):
        """ Méthode pour parser et valider la réponse du LLM. """
        # Parsing de la réponse et normalisation
        normalized_info = {
            'devis': response.get('Numéro de devis', 'Non spécifié'),
            'entreprise': response.get('Société', 'Non spécifié'),
            'adresse_entreprise': response.get('Adresse de la société', 'Non spécifié'),
            'date': response.get('Date du devis', 'Non spécifié'),
            'client': response.get('Nom du client', 'Non spécifié'),
            'adresse_client': response.get('Adresse du client', 'Non spécifié'),
            'code_postal_client': response.get('Code Postal du client', 'Non spécifié'),
            'description': response.get('Description du travail', 'Non spécifié'),
            'montant_total': float(self.normalize_and_convert_amount(response.get('Montant total HT', '0 EUR').replace(' EUR', ''))),
            'taux_tva': float(self.normalize_and_convert_amount(response.get('Taux de TVA', '0%').replace('%', ''))),
            'total_ttc': float(self.normalize_and_convert_amount(response.get('Montant total TTC', '0 EUR').replace(' EUR', ''))),
            'conditions': response.get('Conditions de règlement', 'Non spécifié'),
            'debut_travaux': response.get('Début des travaux', 'Non spécifié')
        }
        print("INFO RECUPEREE : ", normalized_info)
        # Validation et correction des données extraites
        normalized_info = self.validate_and_correct_info(normalized_info)
        return normalized_info



    def normalize_and_convert_amount(self, amount_str):
        """ Méthode qui supprime les séparateurs de milliers et remplace les virgules par des points. """
        try:
            # Suppression des espaces et changement des , par des points :
            normalized_amount = amount_str.replace(' ', '').replace(',', '.')
            return float(normalized_amount)
        except ValueError as e:
            print(f"Erreur de conversion : {e} avec la chaîne '{amount_str}'")
            return 0.0  # Return a default value or handle appropriately



    def validate_and_correct_info(self, info):
        """ Méthode pour valider et corriger les informations extraites. """
        # Validation du montant total, du taux de TVA et du montant TTC
        if (info['montant_total'] != 0.0) and (info['taux_tva'] != 0.0) and (info['total_ttc'] != 0.0):
            try:
                montant_ht = info['montant_total']  # Directement depuis normalized_info
                taux_tva = info['taux_tva'] / 100  # Normalisé
                total_ttc_calculated = montant_ht * (1 + taux_tva)
                total_ttc_extracted = info['total_ttc']  # Normalisé
                if not math.isclose(total_ttc_calculated, total_ttc_extracted, rel_tol=1e-2):
                    info['total_ttc'] = f"{total_ttc_calculated:.2f} EUR"  # Correction du montant TTC si nécessaire
            except ValueError:
                print("Erreur de conversion lors de la validation des montants.")
        return info



    def map_data_to_devis(self, data):
        """ Méthode qui mappe les données extraites à une instance de la classe Devis """
        print("DEVIS CHARGE DANS LA METHODE map_data_to_devis : ", data)
        devis_instance = Devis(
            devis=data.get('Devis', 'Non spécifié'),
            entreprise=data.get('Entreprise', 'Non spécifié'),
            adresse_entreprise=data.get('Adresse Entreprise', 'Non spécifié'),
            date=data.get('Date', 'Non spécifié'),
            client=data.get('Client', 'Non spécifié'),
            adresse_client=data.get('Adresse Client', 'Non spécifié'),
            code_postal_client=data.get('Code Postal Client', 'Non spécifié'),
            description=data.get('Description', ''),
            montant_total=data.get('Montant Total', 'Non spécifié'),
            taux_tva=data.get('Taux TVA', 'Non spécifié'),
            total_ttc=data.get('Total TTC', 'Non spécifié'),
            conditions=data.get('Conditions', 'Non spécifié'),
            debut_travaux=data.get('Début Travaux', 'Non spécifié')
        )
        print("VALEUR AFFECTEES AU DEVIS : ")
        print(f"Devis: {data.get('Devis', 'Non spécifié')}")
        print(f"Entreprise: {data.get('Entreprise', 'Non spécifié')}")
        print(f"Adresse Entreprise: {data.get('Adresse Entreprise', 'Non spécifié')}")
        print(f"Date: {data.get('Date', 'Non spécifié')}")
        print(f"Client: {data.get('Client', 'Non spécifié')}")
        print(f"Adresse Client: {data.get('Adresse Client', 'Non spécifié')}")
        print(f"Code Postal Client: {data.get('Code Postal Client', 'Non spécifié')}")
        print(f"Description: {data.get('Description', '')}")
        print(f"Montant Total: {data.get('Montant Total', 'Non spécifié')}")
        print(f"Taux TVA: {data.get('Taux TVA', 'Non spécifié')}")
        print(f"Total TTC: {data.get('Total TTC', 'Non spécifié')}")
        print(f"Conditions: {data.get('Conditions', 'Non spécifié')}")
        print(f"Début Travaux: {data.get('Début Travaux', 'Non spécifié')}")
        print("DEVIS INSTANCE GENEREE : ", devis_instance)
        return devis_instance



    def extract_value_using_pattern(self, text, pattern):
        """ Méthode qui extrait des valeurs basées sur un pattern regex """
        print("EXECUTION METHODE extract_value_using_pattern()")
        print("TEXT : ", text)
        print("PATTERN : ", pattern)
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
        return "Non spécifié"



    def compare_quotations(self):
        """ Méthode pour comparer les devis """
        print("EXECUTING METHOD compare_quotations()")
        self.get_quotations_data_service.process_quotations()
        print("TEXT RECUPERE DANS LES DEVIS : ", self.get_quotations_data_service.extracted_texts)

        # Traitement de chaque devis :
        for i, text in enumerate(self.get_quotations_data_service.extracted_texts):
            # Extraire les informations structurées
            info = self.extract_relevant_info(text)
            print("DEVIS RECUPERE : ", info)

            # Créer et enregistrer une instance de Devis en BDD
            devis_instance = self.sql_service.create_devis(info)
            print("DEVIS INTEGRE EN BDD : ", devis_instance)

            # Ajouter l'instance de Devis à self.devis_data
            self.devis_data.append(devis_instance)
            print("RETRIEVING KEY QUOTATION INFORMATION: ", self.devis_data)
        
        print("AFFICHAGE DE TOUS LES DEVIS EN BDD SQLITE : ", self.sql_service.get_all_devis())
        self.display_comparison_table()



    # ==> ANCIENNE VERSION :
    """
    def compare_quotations(self):
        # Method to compare quotations by converting them into instances of the Quotation class
        print("EXECUTING METHOD compare_quotations()")
        self.get_quotations_data_service.process_quotations()

        for i, text in enumerate(self.get_quotations_data_service.extracted_texts):
            # Extract structured information
            info = self.extract_relevant_info(text)
            print("DEVIS RECUPERE : ", info)
            # Transform into a Quotation instance before storing in the vector database
            quotation_instance = self.map_data_to_devis(info)
            print("DEVIS INTEGRE EN BDD : ", quotation_instance)

            self.store_texts_in_vector_db(str(quotation_instance), i)
            # print("STORAGE IN VECTOR DB COMPLETED")

            # Add the Quotation instance to self.devis_data
            self.devis_data.append(quotation_instance)
            print("RETRIEVING KEY QUOTATION INFORMATION: ", self.devis_data)
        
        self.display_comparison_table()
    """




    def display_comparison_table(self):
        """ Retrieve and return the quotations in a comparative list """
        print("EXECUTING METHOD display_comparison_table()")
        
        # Récupérer tous les devis depuis la base de données
        all_devis = self.sql_service.get_all_devis()

        headers = ["Devis", "Entreprise", "Montant", "Conditions", "Validité"]
        
        # Correspondance entre les headers et les attributs des objets devis
        attribute_mapping = {
            "Devis": "devis",
            "Entreprise": "entreprise",
            "Montant": "montant_total",
            "Conditions": "conditions",
            "Validité": "date"  # Remplacer par l'attribut approprié si besoin
        }
        
        devis_list = []
        for devis in all_devis:
            devis_dict = {
                header: getattr(devis, attribute_mapping[header], "Non spécifié")
                for header in headers
            }
            devis_list.append(devis_dict)
        
        print("DEVIS LIST RENVOYEE : ", devis_list)
        # Optionnel : affichage de la liste dans la console pour vérification
        print(f"{' | '.join(headers)}")
        print("-" * (len(headers) * 20))
        for devis in devis_list:
            print(f"{' | '.join(map(str, devis.values()))}")
        
        return devis_list




    # ==> ANCIENNE VERSION :
    """
    def display_comparison_table(self):
        # Display the quotations in a comparative table
        print("EXECUTING METHOD display_comparison_table()")
        headers = ["Devis", "Entreprise", "Montant", "Conditions", "Validité"]
        
        rows = []
        for data in self.devis_data:
            rows.append([
                getattr(data, header.lower(), "Non spécifié")  # Access attributes dynamically
                for header in headers
            ])
        
        # Print the table
        print(f"{' | '.join(headers)}")
        print("-" * (len(headers) * 20))
        for row in rows:
            print(f"{' | '.join(row)}")
    """



    def execute_full_comparison(self):
        """ Méthode encapsulant tout le processus de traitement et de comparaison des devis """
        print("Début de l'exécution complète")

        # Création des chemins des images
        images_to_process = config.QUOTATIONS_FILES_LIST
        images_to_process_paths = [os.path.join(config.QUOTATIONS_FILES_PATH, image) for image in images_to_process]
        print("Récupération des chemins : OK.")

        # Création de l'instance de la BDD Vectorielle
        vector_db_mock = VectorDataBase()
        print("Instanciation de la BDD : OK.")

        # Simulation du texte extrait pour chaque image
        extracted_texts = [self.get_quotations_data_service.extract_text(image_path) for image_path in images_to_process_paths]
        print("Extract_texts : ", extracted_texts)
        print("Extraction du texte dans chaque Image : OK.")

        # Affichage du tableau comparatif et stockage des devis en BDD Vectorielle
        self.compare_quotations()
        print("Stockage des données dans la BDD Vectorielle réalisé par cette méthode ==> OK")
        print("Récupération des infos clés des devis ==> OK.")

        print("********** FIN DES TESTS ************")




