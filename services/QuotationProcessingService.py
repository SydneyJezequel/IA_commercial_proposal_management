import json
import math
import re
import config
from BO.Llm import Llm
from BO.SqlDatabase import SqlDatabase
from services.QuotationDataExtractorService import QuotationDataExtractorService
import logging






class QuotationProcessingService:
    """ Classe chargée du traitement et de la comparaison des devis """



    def __init__(self, db_url=config.DB_URL):
        """ Constructeur """
        # Service qui récupère le texte des devis :
        self.get_quotations_data_service = QuotationDataExtractorService()
        # Initialisation de la BDD SQLite :
        self.sql_service = SqlDatabase()



    """ Configuration des logs. """
    logging.basicConfig(level=logging.INFO)



    def extract_relevant_info(self, text):
        """ Méthode qui extrait les infos clés de chaque devis en utilisant un LLM. """
        try:
            # Étape 1 : Prétraitement du texte :
            preprocessed_text = self.preprocess_text(text)
            # Étape 2 : Génération de la requête pour le LLM :
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
            # Étape 3 : Exécution de la requête au LLM pour extraire les informations :
            llm = Llm()
            response = llm.generate_answer(llm_prompt)
            logging.info(f"RESPONSE OBTENUE DU LLM : {response}")
            # Étape 4 : Récupération de la réponse (JSON valide) :
            response_dict = self.get_llm_response(response)
            logging.info(f"REPONSE RECUPEREE AVEC manual_parse_llm_response() : {response_dict}")
            # Étape 5 : Formatage et validation des données extraites :
            info = self.format_and_validate_llm_response(response_dict)
            logging.info(f"RESPONSE PARSÉE DU LLM : {info}")
            return info

        except ValueError as ve:
            raise ValueError(f"Une erreur de valeur s'est produite : {str(ve)}")
        except json.JSONDecodeError as jde:
            raise RuntimeError(f"Erreur de décodage JSON : {str(jde)}")
        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'extraction des informations : {str(e)}")



    def preprocess_text(self, text):
        """ Méthode pour prétraiter le texte avant l'extraction de chaque champ par le LLM. """
        try:
            # Vérification du type de l'entrée :
            if isinstance(text, tuple):
                text = text[1] if len(text) > 1 else text[0]
            # S'assurer que 'text' est une chaîne de caractères
            if not isinstance(text, str):
                raise ValueError("Le texte à prétraiter doit être une chaîne de caractères.")
            # Remplacement des caractères spéciaux :
            text = text.replace("€", " EUR")
            # Uniformisation des montants :
            text = re.sub(r'(\d+)[.,](\d{2})', r'\1.\2', text)
            # Suppression des espaces multiples pour éviter les erreurs de lecture :
            text = re.sub(r'\s+', ' ', text)
            return text

        except ValueError as ve:
            raise ValueError(f"Erreur de prétraitement du texte : {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Erreur lors du prétraitement du texte : {str(e)}") 



    def get_llm_response(self, response_text):
        """ Méthode pour extraire les données du JSON. """
        # Étape 1 : Extraction du JSON de la réponse :
        json_start = response_text.find("{")
        json_end = response_text.rfind("}")
        if json_start != -1 and json_end != -1:
            # Extraction de la chaîne JSON potentielle :
            json_potential = response_text[json_start:json_end + 1]
            # Étape 2 : Parser cette chaîne comme JSON :
            try:
                info = json.loads(json_potential)
                return info
            except json.JSONDecodeError:
                raise ValueError("Erreur : La partie extraite ne peut pas être parsée en JSON.")
        logging.error("Erreur : Impossible de trouver un JSON valide dans la réponse.")
        # Renvoi d'un dictionnaire vide ou d'un message d'erreur structuré :
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



    def format_and_validate_llm_response(self, response):
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
        logging.info(f"INFO RECUPEREE : {normalized_info}")
        # Validation et correction des données extraites
        normalized_info = self.validate_and_correct_info(normalized_info)
        return normalized_info

        

    def normalize_and_convert_amount(self, amount_str):
        """ Méthode qui supprime les séparateurs de milliers et remplace les virgules par des points. """
        try:
            # Suppression des séparateurs de milliers (point) avant la conversion
            amount_str = re.sub(r'\.(?=\d{3})', '', amount_str)
            # Remplacement des virgules par des points
            amount_str = amount_str.replace(',', '.')
            # Retrait des espaces et conversion du montant en float
            return float(amount_str.strip())  
        except ValueError as ve:
            logging.error(f"Erreur de conversion lors de la normalisation du montant : '{amount_str}' est invalide. Détails de l'erreur : {ve}")
            raise ValueError(f"Erreur de conversion lors de la normalisation du montant : '{amount_str}' est invalide.")  # Relève l'exception avec un message plus explicite



    def safe_convert_to_float(self, amount):
        """ Méthode sécurisée pour convertir un montant en float. """
        try:
            # Nettoyage de la string et exécution de la conversion :
            return self.normalize_and_convert_amount(amount.replace(' EUR', '').replace(' %', '')) 
        except ValueError as ve:
            raise ValueError(f"Impossible de convertir le montant '{amount}' en float. Vérifiez le format.")

 



    def validate_and_correct_info(self, info):
        """ Méthode pour valider et corriger les informations extraites. """

        # Validation du montant total, du taux de TVA et du montant TTC :
        if (info['montant_total'] != 0.0) and (info['taux_tva'] != 0.0) and (info['total_ttc'] != 0.0):

            try:
                montant_ht = info['montant_total']
                taux_tva = info['taux_tva'] / 100
                total_ttc_calculated = montant_ht * (1 + taux_tva)
                total_ttc_extracted = info['total_ttc']
                # Correction du montant TTC si nécessaire :
                if not math.isclose(total_ttc_calculated, total_ttc_extracted, rel_tol=1e-2):
                    info['total_ttc'] = f"{total_ttc_calculated:.2f} EUR"

            except ValueError as ve:
                raise ValueError("Erreur de conversion lors de la validation des montants.")
            
        return info
    


    def load_quotations(self):
        """ Méthode qui charge les devis en BDD. """

        try:
            # Récupération du contenu brut dans les devis :
            self.get_quotations_data_service.process_quotations()
            logging.info(f"Chargement des devis bruts : {self.get_quotations_data_service.extracted_texts}")
            # Traitement de chaque devis :
            logging.info("Récupération et intégration des données en BDD : ")
            for text in enumerate(self.get_quotations_data_service.extracted_texts):
                # Extraction des informations structurées :
                info = self.extract_relevant_info(text)
                # Enregistrement du devis en BDD :
                devis_instance = self.sql_service.save_devis(info)
                logging.info(f"devis intégré : {devis_instance}")
            logging.info(f"Liste des devis en BDD : {self.sql_service.get_all_devis()}")
            self.display_comparison_table()

        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement des devis : {e}")



    def display_comparison_table(self):
        """ Méthode qui renvoie une liste comparative de devis. """

        try:
            # Récupération des devis en BDD :
            all_devis = self.sql_service.get_all_devis()
            # Création de l'en-tête :
            headers = ["Devis", "Entreprise", "Montant", "Conditions", "Validité"]
            # Correspondance entre les headers et les attributs des objets devis :
            attribute_mapping = {
                "Devis": "devis",
                "Entreprise": "entreprise",
                "Montant": "montant_total",
                "Conditions": "conditions",
                "Validité": "date"
            }
            # Chargement de la liste :
            devis_list = []
            for devis in all_devis:
                devis_dict = {
                    header: getattr(devis, attribute_mapping[header], "Non spécifié")
                    for header in headers
                }
                devis_list.append(devis_dict)
            # Appel de la méthode pour afficher la liste des devis :
            self.print_devis_list(headers, devis_list)
            return devis_list

        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'affichage de la table de comparaison : {e}")



    def print_devis_list(self, headers, devis_list):
        """ Méthode pour logger la liste des devis avec les en-têtes. """

        try:
            if not headers or not devis_list:
                raise ValueError("Les en-têtes ou la liste des devis ne peuvent pas être vides.")
            logging.info(f"{' | '.join(headers)}")
            logging.info("-" * (len(headers) * 20))
            for devis in devis_list:
                if not isinstance(devis, dict):
                    raise TypeError(f"Élément inattendu dans la liste des devis : {devis}. Chaque élément doit être un dictionnaire.")
                logging.info(f"{' | '.join(map(str, devis.values()))}")
            logging.info(f"Liste renvoyée : {devis_list}")

        except ValueError as ve:
            logging.error(f"Erreur de valeur : {ve}")
        except TypeError as te:
            logging.error(f"Erreur de type : {te}")
        except Exception as e:
            logging.error(f"Une erreur est survenue lors de l'impression de la liste des devis : {e}")

